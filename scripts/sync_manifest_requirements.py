#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Dict, List

try:
    import tomllib  # Python 3.11+
except Exception:  # pragma: no cover
    raise SystemExit("Python 3.11+ required for tomllib")

from packaging.requirements import Requirement

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "custom_components" / "escpos_printer" / "manifest.json"
PYPROJECT = ROOT / "pyproject.toml"
UVLOCK = ROOT / "uv.lock"


def parse_pyproject_dependencies() -> List[Requirement]:
    data = tomllib.loads(PYPROJECT.read_text())
    deps = data.get("project", {}).get("dependencies", [])
    return [Requirement(d) for d in deps]


def parse_uv_lock_versions() -> Dict[str, str]:
    if not UVLOCK.exists():
        return {}
    text = UVLOCK.read_text()
    # Naive parser for [[package]] sections to extract top-level pinned versions
    versions: Dict[str, str] = {}
    current: Dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if line == "[[package]]":
            current = {}
            continue
        if line.startswith("name = "):
            current["name"] = line.split("=", 1)[1].strip().strip('"')
            continue
        if line.startswith("version = "):
            current["version"] = line.split("=", 1)[1].strip().strip('"')
            # When we see version, we can store if name present
            if "name" in current:
                versions[current["name"].lower()] = current["version"]
            continue
    return versions


def build_manifest_requirements() -> List[str]:
    reqs = parse_pyproject_dependencies()
    locked = parse_uv_lock_versions()
    out: List[str] = []
    for r in reqs:
        name = r.name
        # Prefer exact version from pyproject if present
        version = None
        if r.specifier and "==" in str(r.specifier):
            # Find exact equality
            for spec in str(r.specifier).split(","):
                spec = spec.strip()
                if spec.startswith("=="):
                    version = spec[2:]
                    break
        # Fallback to uv.lock resolved version
        if not version:
            version = locked.get(name.lower())
        if not version:
            raise SystemExit(f"Cannot determine exact version for {name}. Pin it in pyproject or lock with uv.")
        out.append(f"{name}=={version}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync manifest requirements with pinned versions")
    parser.add_argument("--check", action="store_true", help="Only check for drift; non-zero exit on mismatch")
    args = parser.parse_args()

    desired = build_manifest_requirements()
    manifest = json.loads(MANIFEST.read_text())
    current = manifest.get("requirements", [])

    if current != desired:
        if args.check:
            print("❌ manifest.json requirements do not match pyproject/uv.lock:")
            print("Current:")
            for r in current:
                print(f"  - {r}")
            print("Desired:")
            for r in desired:
                print(f"  - {r}")
            return 1
        # Write updated manifest
        manifest["requirements"] = desired
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
        print("✅ Updated manifest.json requirements")
    else:
        print("✅ manifest.json requirements are up-to-date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

