"""Pytest fixtures for ESCPOS integration testing."""

from __future__ import annotations

import asyncio
import pytest
import tempfile
import os
from typing import Dict, Any, Generator

from tests.integration_tests.emulator import VirtualPrinter, VirtualPrinterServer, set_active_server

# Lazy import HA environment to avoid dependency conflicts
def _get_ha_environment():
    """Get HA environment class on demand."""
    try:
        from tests.integration_tests.ha_environment import HATestEnvironment
        return HATestEnvironment
    except ImportError as e:
        pytest.skip(f"HA environment not available: {e}")
        return None


@pytest.fixture
async def virtual_printer() -> Generator[VirtualPrinterServer, None, None]:
    """Fixture that provides a virtual printer server."""
    async with VirtualPrinter(host='127.0.0.1', port=9100) as server:
        # Expose as active server for other helpers
        set_active_server(server)
        try:
            yield server
        finally:
            set_active_server(None)


@pytest.fixture
async def ha_test_environment(hass) -> Generator[Any, None, None]:
    """Fixture that provides a Home Assistant test environment."""
    HATestEnvironment = _get_ha_environment()
    if not HATestEnvironment:
        pytest.skip("HA environment not available")

    env = HATestEnvironment(hass)
    await env.setup()

    try:
        yield env
    finally:
        await env.teardown()


@pytest.fixture
async def printer_with_ha(hass, virtual_printer) -> Generator[Dict[str, Any], None, None]:
    """Fixture that provides both virtual printer and HA environment."""
    HATestEnvironment = _get_ha_environment()
    if not HATestEnvironment:
        pytest.skip("HA environment not available")

    env = HATestEnvironment(hass)
    await env.setup()

    # Initialize the integration with the virtual printer
    env.set_printer_server(virtual_printer)
    config = {
        'host': '127.0.0.1',
        'port': 9100,
        'timeout': 5.0,
        'codepage': 'cp437'
    }

    await env.initialize_integration(config)

    try:
        yield (virtual_printer, env, config)
    finally:
        await env.teardown()


@pytest.fixture
def temp_image_file() -> Generator[str, None, None]:
    """Fixture that creates a temporary image file for testing."""
    from PIL import Image

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tmp_file.name)

        try:
            yield tmp_file.name
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp_file.name):
                os.unlink(tmp_file.name)


@pytest.fixture
def test_config() -> Dict[str, Any]:
    """Fixture that provides default test configuration."""
    return {
        'host': '127.0.0.1',
        'port': 9100,
        'timeout': 5.0,
        'codepage': 'cp437',
        'default_align': 'left',
        'default_cut': 'full'
    }


@pytest.fixture
def automation_config() -> Dict[str, Any]:
    """Fixture that provides a sample automation configuration."""
    return {
        'id': 'test_print_automation',
        'alias': 'Test Print Automation',
        'trigger': {
            'platform': 'state',
            'entity_id': 'sensor.test_sensor',
            'to': 'on'
        },
        'condition': [],
        'action': {
            'service': 'escpos_printer.print_text',
            'data': {
                'text': 'Automation triggered!'
            }
        }
    }


@pytest.fixture
async def mock_printer_server() -> Generator[VirtualPrinterServer, None, None]:
    """Fixture that provides a mock printer server for testing."""
    server = VirtualPrinterServer(host='127.0.0.1', port=9101)

    # Start the server in a separate task
    server_task = asyncio.create_task(server.start())
    set_active_server(server)

    # Give the server time to start
    await asyncio.sleep(0.1)

    try:
        yield server
    finally:
        await server.stop()
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
        set_active_server(None)


@pytest.fixture
def sample_print_data() -> Dict[str, Any]:
    """Fixture that provides sample print data for testing."""
    return {
        'text': {
            'content': 'Hello, World!',
            'align': 'center',
            'bold': True,
            'underline': 'single'
        },
        'qr': {
            'data': 'https://example.com',
            'size': 6,
            'ec': 'M'
        },
        'barcode': {
            'code': '123456789',
            'bc': 'CODE128',
            'height': 64,
            'width': 3
        }
    }


@pytest.fixture
async def error_printer_server() -> Generator[VirtualPrinterServer, None, None]:
    """Fixture that provides a printer server configured for error testing."""
    from tests.integration_tests.emulator import create_offline_error

    server = VirtualPrinterServer(host='127.0.0.1', port=9102)

    # Add error conditions for testing
    await server.error_simulator.add_error_condition(
        create_offline_error(trigger_type='after_commands', trigger_value=3)
    )

    server_task = asyncio.create_task(server.start())
    set_active_server(server)
    await asyncio.sleep(0.1)

    try:
        yield server
    finally:
        await server.stop()
        server_task.cancel()
        try:
            await server_task
        except asyncio.CancelledError:
            pass
        set_active_server(None)
