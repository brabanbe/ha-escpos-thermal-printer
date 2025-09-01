"""Virtual printer emulator package for ESCPOS integration testing."""

from .command_parser import EscposCommandParser
from .printer_state import PrinterState, PrintJob, Command
from .virtual_printer import VirtualPrinterServer, VirtualPrinter
from .error_simulator import (
    ErrorSimulator,
    ErrorCondition,
    create_offline_error,
    create_paper_out_error,
    create_timeout_error,
    create_connection_error,
    create_intermittent_error
)

__all__ = [
    'EscposCommandParser',
    'PrinterState',
    'PrintJob',
    'Command',
    'VirtualPrinterServer',
    'VirtualPrinter',
    'ErrorSimulator',
    'ErrorCondition',
    'create_offline_error',
    'create_paper_out_error',
    'create_timeout_error',
    'create_connection_error',
    'create_intermittent_error'
]

# Global hook to expose the most recently started virtual printer server
# so other test utilities can discover it when fixtures are used separately.
ACTIVE_PRINTER_SERVER: VirtualPrinterServer | None = None

def set_active_server(server: VirtualPrinterServer | None) -> None:
    global ACTIVE_PRINTER_SERVER
    ACTIVE_PRINTER_SERVER = server

def get_active_server() -> VirtualPrinterServer | None:
    return ACTIVE_PRINTER_SERVER
