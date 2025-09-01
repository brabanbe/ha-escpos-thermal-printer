import sys
import types

import pytest
import threading


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    yield


@pytest.fixture(autouse=True)
def fake_escpos_module(request):
    # Do not stub escpos for integration tests; use real network path
    if request.node.get_closest_marker("integration"):
        yield
        return
    escpos = types.ModuleType("escpos")
    printer = types.ModuleType("escpos.printer")

    class _FakeNetwork:
        def __init__(self, *_, **__):
            pass

        def set(self, *_, **__):
            pass

        def text(self, *_, **__):
            pass

        def qr(self, *_, **__):
            pass

        def image(self, *_, **__):
            pass

        def control(self, *_, **__):
            pass

        def cut(self, *_, **__):
            pass

        def close(self):
            pass

        def _set_codepage(self, *_, **__):
            pass

        def _raw(self, *_, **__):
            pass

    printer.Network = _FakeNetwork
    escpos.printer = printer

    sys.modules.setdefault("escpos", escpos)
    sys.modules.setdefault("escpos.printer", printer)
    yield


@pytest.fixture(autouse=True)
def disable_platform_forwarding_for_unit_tests(monkeypatch, request):
    """Avoid starting HA http/notify stack in unit tests.

    For tests not marked as 'integration', prevent platform forwarding by
    setting PLATFORMS to an empty list. Service registration remains intact.
    """
    if request.node.get_closest_marker("integration"):
        return
    try:
        import custom_components.escpos_printer.__init__ as cc_init

        # Allow notify platform during unit tests; disable others via env flag
        monkeypatch.setattr(cc_init, "PLATFORMS", ["notify"], raising=False)
        monkeypatch.setenv("ESC_POS_DISABLE_PLATFORMS", "0")
    except Exception:
        pass


@pytest.fixture(autouse=True)
def stub_http_component_for_unit_tests(monkeypatch, request):
    """Provide a minimal stub for the Home Assistant http component in unit tests.

    The real http component can spawn background threads; stubbing avoids lingering
    thread assertions in unit tests. Integration tests use the real component.
    """
    if request.node.get_closest_marker("integration"):
        return
    mod = types.ModuleType("homeassistant.components.http")
    async def _ok(*args, **kwargs):
        return True
    # Provide the setup entrypoints expected by HA
    mod.async_setup = _ok
    mod.async_setup_entry = _ok
    mod.async_unload_entry = _ok
    sys.modules.setdefault("homeassistant.components.http", mod)


@pytest.fixture(autouse=True)
def avoid_safe_shutdown_thread(monkeypatch, request):
    """Prevent Home Assistant's safe-shutdown background thread in unit tests.

    Intercepts thread starts whose target function is named '_run_safe_shutdown_loop'
    and short-circuits them. This avoids lingering thread assertions from the
    test harness. Integration tests keep the real behavior.
    """
    if request.node.get_closest_marker("integration"):
        return

    _orig_start = threading.Thread.start

    def _patched_start(self, *args, **kwargs):  # type: ignore[override]
        target_name = getattr(getattr(self, "_target", None), "__name__", None)
        if target_name == "_run_safe_shutdown_loop":
            # Do not start this thread in unit tests
            return None
        return _orig_start(self, *args, **kwargs)

    monkeypatch.setattr(threading.Thread, "start", _patched_start, raising=True)
