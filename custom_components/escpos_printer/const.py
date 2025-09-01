DOMAIN = "escpos_printer"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_TIMEOUT = "timeout"
CONF_CODEPAGE = "codepage"
CONF_DEFAULT_ALIGN = "default_align"
CONF_DEFAULT_CUT = "default_cut"
CONF_KEEPALIVE = "keepalive"
CONF_STATUS_INTERVAL = "status_interval"
CONF_PROFILE = "profile"
CONF_LINE_WIDTH = "line_width"

DEFAULT_PORT = 9100
DEFAULT_TIMEOUT = 4.0
DEFAULT_ALIGN = "left"
DEFAULT_CUT = "none"
DEFAULT_LINE_WIDTH = 48

# Common supported codepages (not exhaustive)
CODEPAGE_CHOICES: list[str] = [
    "CP437",
    "CP932",
    "CP851",
    "CP850",
    "CP852",
    "CP858",
    "CP1252",
    "ISO_8859-1",
    "ISO_8859-7",
    "ISO_8859-15",
]

LINE_WIDTH_CHOICES: list[int] = [32, 42, 48, 64]

SERVICE_PRINT_TEXT = "print_text"
SERVICE_PRINT_QR = "print_qr"
SERVICE_PRINT_IMAGE = "print_image"
SERVICE_FEED = "feed"
SERVICE_CUT = "cut"
SERVICE_PRINT_BARCODE = "print_barcode"
SERVICE_BEEP = "beep"

ATTR_TEXT = "text"
ATTR_ALIGN = "align"
ATTR_BOLD = "bold"
ATTR_UNDERLINE = "underline"
ATTR_WIDTH = "width"
ATTR_HEIGHT = "height"
ATTR_ENCODING = "encoding"
ATTR_CUT = "cut"
ATTR_FEED = "feed"
ATTR_DATA = "data"
ATTR_SIZE = "size"
ATTR_EC = "ec"
ATTR_IMAGE = "image"
ATTR_HIGH_DENSITY = "high_density"
ATTR_LINES = "lines"
ATTR_MODE = "mode"

# Barcode-related
ATTR_CODE = "code"
ATTR_BC = "bc"
ATTR_BARCODE_HEIGHT = "height"
ATTR_BARCODE_WIDTH = "width"
ATTR_POS = "pos"
ATTR_FONT = "font"
ATTR_ALIGN_CT = "align_ct"
ATTR_CHECK = "check"
ATTR_FORCE_SOFTWARE = "force_software"

# Beep-related
ATTR_TIMES = "times"
ATTR_DURATION = "duration"
