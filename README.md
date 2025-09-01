# ESC/POS Thermal Printer for Home Assistant

![Validate](https://github.com/cognitivegears/ha-escpos-thermal-printer/actions/workflows/validate.yml/badge.svg)
![Hassfest](https://github.com/cognitivegears/ha-escpos-thermal-printer/actions/workflows/hassfest.yml/badge.svg)
![HACS Validation](https://github.com/cognitivegears/ha-escpos-thermal-printer/actions/workflows/hacs.yml/badge.svg)

A comprehensive Home Assistant integration for ESC/POS thermal printers that enables printing text, QR codes, barcodes, images, and more through intuitive services and automation.

![Printed Receipt Example](docs/assets/receipt.png)

The above is an example receipt printed using this integration.

*NOTE:* This project has been developed as a side project for me to integrate my own thermal printer into Home Assistant. As such, this has not had extensive testing with mulitple printers, or with features my printer doesn't support (particularly image support is implemented but hasn't been tested) - do not expect this to work in your own environment, though it does in mine. If this is useful to you, please consider contributing or adapting it for your needs.

## Features

- **UI Configuration Flow** - No YAML required, easy setup through Home Assistant UI
- **Multiple Print Services** - Text, QR codes, barcodes, images, paper feed, cutting, and buzzer control
- **Notify Integration** - Send messages as printed receipts through Home Assistant notifications
- **Robust Error Handling** - Non-blocking I/O with configurable timeouts and connection management
- **Network Printer Support** - Works with any ESC/POS compatible thermal printer on your network
- **Flexible Formatting** - Support for text alignment, bold, underline, font sizes, and custom encoding

## Requirements

### System Requirements

- **Home Assistant**: 2024.8 or later
- **Network Printer**: ESC/POS compatible thermal printer reachable on TCP port 9100 (default)
- **Network Connectivity**: Printer must be accessible from your Home Assistant instance

### Dependencies

This integration automatically installs required Python packages, including:

- python-escpos — Core ESC/POS printing library
- Pillow — Image processing for printing images
- qrcode — QR code generation
- python-barcode — Barcode generation

## Installation

### Method 1: HACS (Recommended)

1. **Install HACS** (if not already installed):
   - Open Home Assistant and go to **Settings** → **Add-ons, Backups & Supervisor** → **Add-on Store**
   - Search for "HACS" and install it following the official [HACS installation guide](https://hacs.xyz/docs/setup/download)

2. **Add Custom Repository**:
   - In HACS, go to **Settings** → **Custom repositories**
   - Add this repository: `https://github.com/cognitivegears/ha-escpos-thermal-printer`
   - Select **Integration** as the category

3. **Install the Integration**:
   - Go to **HACS** → **Integrations**
   - Search for "ESC/POS Thermal Printer"
   - Click **Download** and restart Home Assistant when prompted

4. **Configure the Integration**:
   - Go to **Settings** → **Devices & services** → **Add Integration**
   - Search for "ESC/POS Thermal Printer" and select it
   - Follow the configuration steps below

### Method 2: Manual Installation

1. **Download the Integration**:
   - Clone or download this repository to any temporary folder on your machine, then copy only the component folder into Home Assistant:

   ```bash
   # On your workstation or HA host shell
   git clone https://github.com/cognitivegears/ha-escpos-thermal-printer.git
   cp -R ha-escpos-thermal-printer/custom_components/escpos_printer /config/custom_components/
   ```

2. **Restart Home Assistant**:
   - Go to **Settings** → **System** → **Restart** to load the new integration

3. **Configure the Integration**:
   - Follow the configuration steps in the next section

## Configuration

### Initial Setup

1. **Add the Integration**:
   - Go to **Settings** → **Devices & services** → **Add Integration**
   - Search for "ESC/POS Thermal Printer" and click it

2. **Configure Printer Connection**:
   - **Host**: IP address or hostname of your thermal printer (e.g., `192.168.1.100`)
   - **Port**: TCP port for the printer (default: `9100`)
   - **Timeout**: Connection timeout in seconds (default: `4.0`)
   - **Codepage**: Character encoding for your printer (optional, e.g., `cp437`, `cp1252`)
   - **Default Alignment**: Default text alignment (`left`, `center`, or `right`)
   - **Default Cut Mode**: Default paper cutting behavior (`none`, `partial`, or `full`)

3. **Test the Connection**:
   - The integration will automatically test the connection during setup
   - If successful, you'll see a new device and services in your integration list

### Advanced Configuration Options

After initial setup, you can modify additional settings:

1. **Access Options**:
   - Go to **Settings** → **Devices & services**
   - Find your ESC/POS printer and click **Configure**

2. **Available Options**:
   - **Timeout**: Adjust connection timeout (useful for slower networks)
   - **Codepage**: Set character encoding for international characters
   - **Default Alignment**: Set default text alignment for all print jobs
   - **Default Cut Mode**: Configure automatic paper cutting behavior
   - **Keep Alive**: Maintain persistent connection to printer (experimental)
   - **Status Interval**: Enable periodic printer status checks (seconds, 0 = disabled)

## Printer Setup

### Network Configuration

Most ESC/POS thermal printers support network connectivity. Here's how to configure common models:

#### Epson TM Series Printers

1. **Connect to Network**:
   - Connect the printer to your network using Ethernet cable
   - Power on the printer and wait for initialization

2. **Find Printer IP Address**:
   - Print a network configuration receipt (usually by holding the feed button during power-on)
   - Look for the IP address on the printed receipt

3. **Test Connectivity**:

   ```bash
   # From your Home Assistant host, test connection
   telnet <PRINTER_IP> 9100
   ```

#### Other ESC/POS Compatible Printers

- **Star Micronics**: Follow similar Ethernet setup procedures
- **Citizen Printers**: Use the printer's web interface or configuration utility
- **Generic ESC/POS**: Ensure the printer supports raw TCP printing on port 9100

### Supported Printers

This integration works with any printer supported by the [python-escpos library](https://python-escpos.readthedocs.io/en/latest/). Popular supported models include:

- **Epson**: TM-20, TM-88, TM-T20, TM-T70, TM-T88, TM-U220, TM-U295
- **Star Micronics**: TSP100, TSP650, TSP700, TSP800, SP500, SP700
- **Citizen**: CT-S2000, CT-S4000, CT-S601, CT-S651, CT-S801, CT-S851
- **And many more...**

For a complete list, see the [python-escpos documentation](https://python-escpos.readthedocs.io/en/latest/user/printers.html).

## Usage

### Basic Usage

#### Print Text

```yaml
service: escpos_printer.print_text
data:
  text: "Hello, World!"
  align: center
  bold: true
  cut: partial
  feed: 2
```

#### Print QR Code

```yaml
service: escpos_printer.print_qr
data:
  data: "https://www.home-assistant.io"
  size: 8
  ec: M
  align: center
  cut: partial
```

#### Print Image

```yaml
service: escpos_printer.print_image
data:
  image: "/config/www/logo.png"
  align: center
  cut: partial
  feed: 1
```

### Advanced Usage Examples

#### Receipt Printing

```yaml
service: escpos_printer.print_text
data:
  text: |
    ====================================
               STORE RECEIPT
    ====================================

    Item 1.......................$10.00
    Item 2.......................$15.50
    ------------------------------------
    Total........................$25.50

    Thank you for your business!
  align: left
  cut: full
  feed: 3
```

#### Multi-format Receipt with QR Code

```yaml
# Print header
service: escpos_printer.print_text
data:
  text: "=== SMART HOME RECEIPT ==="
  align: center
  bold: true
  width: double
  height: double

# Print details
service: escpos_printer.print_text
data:
  text: |
    Date: {{ now().strftime('%Y-%m-%d %H:%M') }}
    Temperature: {{ states('sensor.temperature') }}°F
    Humidity: {{ states('sensor.humidity') }}%
  align: left

# Print QR code for feedback
service: escpos_printer.print_qr
data:
  data: "https://forms.example.com/feedback"
  size: 6
  align: center

# Print footer and cut
service: escpos_printer.print_text
data:
  text: "Scan QR code for feedback!"
  align: center
  cut: partial
  feed: 2
```

#### Print Barcode

```yaml
service: escpos_printer.print_barcode
data:
  code: "4006381333931"
  bc: "EAN13"
  height: 100
  width: 3
  align: center
  cut: partial
```

### Service Reference

#### `escpos_printer.print_text`

Print formatted text to the printer.

**Parameters:**

- `text` (required): Text to print (supports multiline with `|` in YAML)
- `align`: Text alignment (`left`, `center`, `right`)
- `bold`: Enable bold text (`true`/`false`)
- `underline`: Underline style (`none`, `single`, `double`)
- `width`: Font width (`normal`, `double`, `triple`)
- `height`: Font height (`normal`, `double`, `triple`)
- `encoding`: Character encoding override
- `cut`: Paper cutting (`none`, `partial`, `full`)
- `feed`: Lines to feed after printing (0-10)

#### `escpos_printer.print_qr`

Print a QR code.

**Parameters:**

- `data` (required): Data to encode in QR code
- `size`: QR code size (1-16, default: 3)
- `ec`: Error correction level (`L`, `M`, `Q`, `H`)
- `align`: QR code alignment (`left`, `center`, `right`)
- `cut`: Paper cutting (`none`, `partial`, `full`)
- `feed`: Lines to feed after printing (0-10)

#### `escpos_printer.print_image`

Print an image from URL or local path.

**Parameters:**

- `image` (required): Image URL or local path (e.g., `/config/www/image.png`)
- `high_density`: Use high-density printing (`true`/`false`)
- `align`: Image alignment (`left`, `center`, `right`)
- `cut`: Paper cutting (`none`, `partial`, `full`)
- `feed`: Lines to feed after printing (0-10)

#### `escpos_printer.feed`

Feed paper without printing.

**Parameters:**

- `lines` (required): Number of lines to feed (1-10)

#### `escpos_printer.cut`

Cut the paper.

**Parameters:**

- `mode` (required): Cut type (`full` or `partial`)

#### `escpos_printer.print_barcode`

Print a barcode.

**Parameters:**

- `code` (required): Barcode data
- `bc` (required): Barcode type (e.g., `EAN13`, `CODE128`, `UPCA`)
- `height`: Barcode height in dots (1-255)
- `width`: Barcode width (2-6)
- `pos`: Human-readable text position (`ABOVE`, `BELOW`, `BOTH`, `OFF`)
- `font`: Font for human-readable text (`A` or `B`)
- `align_ct`: Center alignment (`true`/`false`)
- `check`: Enable checksum (`true`/`false`)
- `force_software`: Rendering method
- `align`: Barcode alignment (`left`, `center`, `right`)
- `cut`: Paper cutting (`none`, `partial`, `full`)
- `feed`: Lines to feed after printing (0-10)

#### `escpos_printer.beep`

Sound the printer buzzer (if supported).

**Parameters:**

- `times`: Number of beeps (1-10)
- `duration`: Beep duration (1-10)

## Home Assistant Automations

### Door Access Logging

```yaml
automation:
  - alias: "Log Door Access"
    trigger:
      platform: state
      entity_id: binary_sensor.front_door
      to: "on"
    action:
      - service: escpos_printer.print_text
        data:
          text: |
            === DOOR ACCESS ===
            Time: {{ now().strftime('%H:%M:%S') }}
            Date: {{ now().strftime('%Y-%m-%d') }}
            Access: FRONT DOOR
            Status: OPENED
          align: center
          cut: partial
          feed: 1
```

### Temperature Alert Receipts

```yaml
automation:
  - alias: "Temperature Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.temperature
      above: 80
    action:
      - service: escpos_printer.print_text
        data:
          text: |
            ⚠️  TEMPERATURE ALERT  ⚠️
            Current: {{ states('sensor.temperature') }}°F
            Time: {{ now().strftime('%H:%M') }}
            Location: Living Room
          align: center
          bold: true
          cut: partial
          feed: 2
```

### Daily Summary Report

```yaml
automation:
  - alias: "Daily Summary Report"
    trigger:
      platform: time
      at: "08:00:00"
    action:
      - service: escpos_printer.print_text
        data:
          text: |
            === DAILY SUMMARY ===
            Date: {{ now().strftime('%Y-%m-%d') }}

            Temperature Range:
            Min: {{ state_attr('sensor.temperature_daily', 'min_value') }}°F
            Max: {{ state_attr('sensor.temperature_daily', 'max_value') }}°F
            Avg: {{ state_attr('sensor.temperature_daily', 'average') }}°F

            System Status: {{ states('binary_sensor.system_healthy') }}
          align: left
          cut: full
          feed: 3
```

### Notification Integration

```yaml
automation:
  - alias: "Print Notifications"
    trigger:
      platform: event
      event_type: call_service
      event_data:
        domain: notify
        service: send_message
    condition:
      condition: template
      value_template: "{{ trigger.event.data.service_data.entity_id == 'notify.esc_pos_printer_192_168_1_100_9100' }}"
    action:
      - service: escpos_printer.print_text
        data:
          text: |
            📢 NOTIFICATION 📢
            {{ trigger.event.data.service_data.message }}
            ---
            {{ now().strftime('%H:%M %m/%d/%Y') }}
          align: center
          cut: partial
          feed: 1
```

## Notification Usage

The integration creates a notification entity that allows you to send messages as printed receipts:

1. **Find the Notify Entity**:
   - Go to **Developer Tools** → **Actions**
   - Look for entities starting with `notify.esc_pos_printer_`

2. **Send a Notification**:

   ```yaml
   service: notify.send_message
   data:
     entity_id: notify.esc_pos_printer_192_168_1_100_9100
     message: "Hello from Home Assistant!"
   ```

3. **Advanced Notification**:

   ```yaml
   service: notify.send_message
   data:
     entity_id: notify.esc_pos_printer_192_168_1_100_9100
     message: |
       🚨 System Alert 🚨
       {{ states('sensor.temperature') }}°F
       {{ now().strftime('%H:%M') }}
     title: "Temperature Alert"
   ```

## Troubleshooting

### Common Issues and Solutions

#### Connection Problems

**Issue**: "Cannot connect to printer"
**Solutions**:

- Verify the printer IP address and port (9100 is default)
- Check network connectivity between Home Assistant and printer
- Ensure the printer is powered on and connected to the network
- Try increasing the timeout value in integration options
- Test connectivity with: `telnet <PRINTER_IP> 9100`

#### Print Quality Issues

**Issue**: "Text appears garbled or incorrect characters"
**Solutions**:

- Set the correct codepage in integration options (e.g., `cp437` for English, `cp1252` for Western European)
- Ensure the printer supports the selected codepage
- Try different encoding options in service calls

#### Image Printing Problems

**Issue**: "Images are too wide or distorted"
**Solutions**:

- Resize images to maximum 512 pixels width
- Use PNG or JPEG formats (avoid BMP if possible)
- Enable/disable `high_density` option based on your printer model
- Check printer DPI settings

#### Paper Cutting Issues

**Issue**: "Paper doesn't cut properly"
**Solutions**:

- Verify your printer supports automatic cutting
- Try `partial` cut instead of `full` cut
- Check paper type and ensure it's loaded correctly
- Some printers require manual cutting

#### Service Not Found

**Issue**: "Service 'escpos_printer.*' not found"
**Solutions**:

- Restart Home Assistant after installation
- Verify the integration is properly loaded in **Settings** → **Devices & services**
- Check Home Assistant logs for integration errors

### Debug Logging

Enable debug logging to troubleshoot issues:

1. **Add to configuration.yaml**:

   ```yaml
   logger:
     logs:
       escpos: debug
       custom_components.escpos_printer: debug
   ```

2. **Restart Home Assistant** and check logs in **Settings** → **System** → **Logs**

### Printer-Specific Issues

#### Epson TM Series

- Ensure printer is in ESC/POS mode (not Epson proprietary mode)
- Check DIP switch settings for network configuration
- Update printer firmware to latest version

#### Star Micronics

- Verify correct emulation mode (ESC/POS)
- Check interface settings in printer configuration
- Ensure proper driver installation on network interface

#### Generic ESC/POS

- Test with minimal ESC/POS commands first
- Verify printer supports raw TCP printing
- Check manufacturer documentation for ESC/POS compatibility

### Getting Help

If you continue to have issues:

1. **Check Existing Issues**: Search [GitHub Issues](https://github.com/cognitivegears/ha-escpos-thermal-printer/issues) for similar problems
2. **Create a New Issue**: Include:
   - Your printer model and firmware version
   - Home Assistant version and installation method
   - Complete error logs with debug logging enabled
   - Steps to reproduce the issue
   - Your configuration (without sensitive information)

## Development

### Contributing

Contributions are welcome! See CONTRIBUTING.md for setup, coding standards, dependency policy (exact pins with uv + Renovate), and how to run local checks.

### Testing

Run the test suite:

```bash
python -m pytest tests/
```

### Developer Utilities

- Framework smoke test (no Home Assistant required):

  ```bash
  python scripts/framework_smoke_test.py
  ```

### Building

This integration follows Home Assistant's integration structure. See the [Home Assistant Developer Documentation](https://developers.home-assistant.io/docs/creating_integration_file_structure) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## References

- [Python-ESC/POS Library](https://github.com/python-escpos/python-escpos) - Core printing functionality
- [Python-ESC/POS Documentation](https://python-escpos.readthedocs.io/) - Detailed API documentation
- [Home Assistant Integration Development](https://developers.home-assistant.io/docs/creating_integration_file_structure) - Integration guidelines
- [HACS Documentation](https://hacs.xyz/) - Custom repository installation
- [Aaron Godfrey's HA Custom Component Series](https://www.youtube.com/playlist?list=PL9luKH1ZjSZtTlMNbSbhX0CCJsHQp7ZW) - Development tutorials

## Support

- **Issues**: [GitHub Issues](https://github.com/cognitivegears/ha-escpos-thermal-printer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/cognitivegears/ha-escpos-thermal-printer/discussions)
- **Documentation**: [GitHub Wiki](https://github.com/cognitivegears/ha-escpos-thermal-printer/wiki)

---

**Note**: This integration is not officially affiliated with Home Assistant or any printer manufacturers. Use at your own risk.
