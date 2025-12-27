# Hashcat Hex Decoder

Convert $HEX[...] output in the potfile that Hashcat produces due to the password containing non-printable characters, special characters (like a colon :), or characters outside the standard ASCII range (0x20-0x7f).

## Features

- **Input Methods**
  - **File Input**: Process entire Hashcat potfiles with multiple $HEX[...] encoded lines
  - **Command Line**: Decode single hex strings directly from the command line

- **Flexible Input Support**
  - Accepts $HEX[...] formatted strings (Use single quotes if running on Windows).
  - Accepts raw hexadecimal strings without the wrapper

- **Smart Encoding Detection**
  - Primary UTF-8 decoding with automatic fallback to latin-1 for non-UTF-8 sequences. Did I miss anything?
  - Detailed error messages with troubleshooting tips

## Usage

### Basic Syntax

```bash
python hashcat_hex_decoder.py --input <INPUT> [--output <OUTPUT>]
```

Or using the alternative script name:

```bash
python hashcat_hex_decoder.py --input <INPUT> [--output <OUTPUT>]
```

### Command-Line Arguments

- `--input` or `-i`: (Required) Input file path OR hex string to decode
- `--output` or `-o`: (Optional for direct mode, Required for file mode) Output file path for decoded text

### File Input

Process an entire potfile with multiple hex-encoded lines:

```bash
python hashcat_hex_decoder.py --input potfile.txt --output decoded.txt
```

**Example Input File** (`potfile.txt`):
```
$HEX[48656c6c6f20576f726c64]
normalpassword123
$HEX[5061737377c3b67264]
```

**Output** (`decoded.txt`):
```
Hello World
normalpassword123
Passwörd
```

### Command Line

Decode a single hex string and display the result in the console:

```bash
python hashcat_hex_decoder.py --input '$HEX[48656c6c6f]'
```

**Output**:
```
Decoded: Hello
```

Decode raw hex without the $HEX[] wrapper:

```bash
python hashcat_hex_decoder.py --input "48656c6c6f"
```

Save direct decode output to a file:

```bash
python hashcat_hex_decoder.py --input '$HEX[48656c6c6f]' --output result.txt
```

### Platform-Specific Notes

**Windows Users**: Use single quotes around $HEX[...] strings to prevent PowerShell/CMD from interpreting the `$` character:

```bash
python hashcat_hex_decoder.py --input '$HEX[48656c6c6f]'
```

**Linux/Mac Users**: Either single or double quotes work:

```bash
python hashcat_hex_decoder.py --input "$HEX[48656c6c6f]"
```

### Examples

**Quick hex decode**:
```bash
python hashcat_hex_decoder.py -i '$HEX[48656c6c6f20576f726c64]'
# Output: Decoded: Hello World
```

**Process Hashcat potfile**:
```bash
python hashcat_hex_decoder.py -i hashcat.potfile -o decoded_passwords.txt
```

**Decode raw hex to file**:
```bash
python hashcat_hex_decoder.py -i "5061737377c3b67264" -o password.txt
```

## Error Handling

The tool provides clear, color-coded error messages for common issues:

- **Invalid hex format**: Non-hexadecimal characters in the input
- **File not found**: Input file doesn't exist
- **UTF-8 decode errors**: Invalid UTF-8 sequences (automatically falls back to latin-1)

## Requirements

- Python 3.x
- No external dependencies (uses only standard library modules)
