#!/usr/bin/env python3
"""
Security scanning script for HA ESCPOS Thermal Printer integration.

This script runs comprehensive security scans including:
- Dependency vulnerability scanning with Safety
- Python security linting with Bandit
- Static analysis with Ruff (security rules)
- Dependency auditing with pip-audit

Usage:
    python scripts/security_scan.py [--fix] [--verbose]

Options:
    --fix       Attempt to auto-fix security issues where possible
    --verbose   Show detailed output
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional


class SecurityScanner:
    """Comprehensive security scanner for the project."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = Path(__file__).parent.parent

    def run_command(self, cmd: List[str], description: str) -> bool:
        """Run a command and return success status."""
        try:
            if self.verbose:
                print(f"\n🔍 Running {description}...")
                print(f"Command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=not self.verbose,
                text=True,
                check=False
            )

            if result.returncode == 0:
                print(f"✅ {description} passed")
                return True
            else:
                print(f"❌ {description} failed")
                if not self.verbose:
                    print(f"Error output: {result.stderr}")
                return False

        except FileNotFoundError:
            print(f"⚠️  {description} not found (tool may not be installed)")
            return False
        except Exception as e:
            print(f"❌ Error running {description}: {e}")
            return False

    def check_dependencies(self) -> bool:
        """Check if security tools are installed."""
        tools = ["safety", "bandit", "ruff", "pip-audit"]
        missing_tools = []

        for tool in tools:
            try:
                subprocess.run(
                    [tool, "--version"],
                    capture_output=True,
                    check=True
                )
            except (FileNotFoundError, subprocess.CalledProcessError):
                missing_tools.append(tool)

        if missing_tools:
            print(f"⚠️  Missing security tools: {', '.join(missing_tools)}")
            print("Install with: pip install safety bandit ruff pip-audit")
            return False

        print("✅ All security tools are available")
        return True

    def scan_dependencies(self) -> bool:
        """Scan dependencies for vulnerabilities using Safety."""
        return self.run_command(
            ["safety", "check", "--full-report"],
            "Dependency vulnerability scan (Safety)"
        )

    def scan_code_security(self) -> bool:
        """Scan Python code for security issues using Bandit."""
        return self.run_command(
            ["bandit", "-r", "custom_components/escpos_printer"],
            "Python security linting (Bandit)"
        )

    def scan_static_analysis(self) -> bool:
        """Run static analysis with security-focused rules."""
        return self.run_command(
            ["ruff", "check", "--select", "S", "custom_components/escpos_printer"],
            "Static analysis security rules (Ruff)"
        )

    def audit_dependencies(self) -> bool:
        """Audit dependencies for known vulnerabilities."""
        return self.run_command(
            ["pip-audit"],
            "Dependency vulnerability audit (pip-audit)"
        )

    def generate_report(self) -> None:
        """Generate a security scan report."""
        report_path = self.project_root / "security_report.md"
        print(f"\n📊 Generating security report: {report_path}")

        report_content = f"""# Security Scan Report
Generated: {Path(__file__).name}

## Project Information
- Project: HA ESCPOS Thermal Printer Integration
- Scan Date: {Path(__file__).stat().st_mtime}

## Security Tools Used
- Safety: Dependency vulnerability scanning
- Bandit: Python security linting
- Ruff: Static analysis with security rules
- pip-audit: Dependency vulnerability audit

## Recommendations
1. Review all security findings and address high-priority issues
2. Keep dependencies updated to latest secure versions
3. Run security scans regularly in CI/CD pipeline
4. Follow secure coding practices documented in SECURITY.md

## Security Best Practices
- Validate all user inputs
- Use parameterized queries for database operations
- Implement proper error handling
- Avoid storing sensitive data in logs
- Use HTTPS for network communications
- Regularly update dependencies
"""

        report_path.write_text(report_content)
        print("✅ Security report generated")

    def run_all_scans(self) -> bool:
        """Run all security scans."""
        print("🚀 Starting comprehensive security scan...")

        if not self.check_dependencies():
            return False

        scans = [
            self.scan_dependencies,
            self.scan_code_security,
            self.scan_static_analysis,
            self.audit_dependencies,
        ]

        results = []
        for scan in scans:
            results.append(scan())

        self.generate_report()

        passed = sum(results)
        total = len(results)

        print(f"\n📈 Security Scan Summary: {passed}/{total} scans passed")

        if passed == total:
            print("🎉 All security scans passed!")
            return True
        else:
            print("⚠️  Some security scans failed. Review the output above.")
            return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Security scanner for HA ESCPOS integration")
    parser.add_argument("--fix", action="store_true", help="Attempt to auto-fix issues")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    scanner = SecurityScanner(verbose=args.verbose)
    success = scanner.run_all_scans()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
