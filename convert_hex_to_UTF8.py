#!/usr/bin/env python3
"""
Hex Decoder - Converts $HEX[...] encoded strings within Hashcat potfiles to UTF-8 text
"""

import argparse
import sys
import re
import os

# ==============================
# Function to convert HEX to UTF8 string
# ==============================
def convert_hex_to_utf8(hex_string):
    """Converts a hexadecimal string to UTF-8 decoded text."""
    # Remove any whitespace from the hex string
    hex_string = re.sub(r'\s', '', hex_string)

    try:
        # Convert hex string to bytes
        bytes_data = bytes.fromhex(hex_string)
    except ValueError as e:
        # Invalid hex format
        return None, f"Invalid hex format: {e}"

    try:
        # Try to decode as UTF-8
        return bytes_data.decode('utf-8')
    except UnicodeDecodeError as e:
        # Invalid UTF-8 sequence - try latin-1 as fallback
        try:
            decoded = bytes_data.decode('latin-1')
            return decoded, "Warning: Decoded using latin-1 (not valid UTF-8)"
        except Exception:
            return None, f"UTF-8 decode error: {e}"

# ==============================
# Process hex string directly
# ==============================
def process_hex_string(hex_input, output_file=None):
    """Decodes a hex string directly and outputs to file or stdout."""
    # Check if input matches $HEX[hexadecimal] pattern
    match = re.match(r'^\$HEX\[([0-9A-Fa-f]+)\]$', hex_input)

    warning_msg = None
    if match:
        hex_value = match.group(1)
        result = convert_hex_to_utf8(hex_value)

        if isinstance(result, tuple):
            decoded, msg = result
            if decoded is None:
                print(f"Error: {msg}", file=sys.stderr)
                if "non-hexadecimal number found in fromhex() arg at position 0" in msg:
                    print("\nTip: Did you use single quotes? On Windows, use single quotes '$HEX[...]' to prevent shell interpretation of the $ character.", file=sys.stderr)
                sys.exit(1)
            else:
                result = decoded
                warning_msg = msg
        else:
            # Successful UTF-8 decode (no tuple returned)
            pass
    else:
        # Assume it's raw hex without $HEX[] wrapper
        result = convert_hex_to_utf8(hex_input)
        if isinstance(result, tuple):
            decoded, msg = result
            if decoded is None:
                print(f"Error: {msg}", file=sys.stderr)
                if "non-hexadecimal number found in fromhex() arg at position 0" in msg:
                    print("\nTip: Did you use single quotes? On Windows, use single quotes '$HEX[...]' to prevent shell interpretation of the $ character.", file=sys.stderr)
                sys.exit(1)
            else:
                result = decoded
                warning_msg = msg

    # Output to file or stdout
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result + '\n')
            if warning_msg:
                print(f"\n{warning_msg}")
            print(f"Decoded output written to '{output_file}'")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if warning_msg:
            print(f"\n{warning_msg}")
        print(f"Decoded: {result}")

# ==============================
# Process input file
# ==============================
def process_file(input_file, output_file):
    """Reads input file, decodes $HEX[...] lines, and writes to output file."""
    decoded_lines = []
    warnings = []

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.rstrip('\n\r')

                # Check if line matches $HEX[hexadecimal] pattern
                match = re.match(r'^\$HEX\[([0-9A-Fa-f]+)\]$', line)

                if match:
                    hex_value = match.group(1)
                    result = convert_hex_to_utf8(hex_value)

                    if isinstance(result, tuple):
                        decoded, msg = result
                        if decoded is not None:
                            decoded_lines.append(decoded)
                            warnings.append(f"Line {line_num}: {msg}")
                        else:
                            decoded_lines.append(line)
                            warnings.append(f"Line {line_num}: Failed - {msg}")
                    else:
                        # Successful UTF-8 decode
                        decoded_lines.append(result)
                else:
                    # Non-HEX lines remain unchanged
                    decoded_lines.append(line)

        # Write all decoded lines to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(decoded_lines) + '\n')

        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(f"  {warning}")

        print(f"\nDecoded output written to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"Error: Permission denied - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

# ==============================
# Main entry point
# ==============================
def main():
    """Parses command-line arguments and runs the hex decoder."""
    parser = argparse.ArgumentParser(
        description='Hashcat Hex Decoder - Converts lines with $HEX[...] encoding to UTF-8 text',
        epilog='''Examples:
  File mode:    python convert_hex_to_UTF8.py --input hex_input.txt --output hex_decoded.txt
  Direct mode:  python convert_hex_to_UTF8.py --input "$HEX[48656c6c6f]"
  Direct mode:  python convert_hex_to_UTF8.py --input "48656c6c6f" --output decoded.txt''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Define command-line arguments
    parser.add_argument('--input', '-i',
                        required=True,
                        help='Input file path OR hex string (with or without $HEX[] wrapper)')
    parser.add_argument('--output', '-o',
                        required=False,
                        help='Output file path for decoded text (optional for direct hex input)')

    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Determine if input is a file or a hex string
    if os.path.isfile(args.input):
        # Input is a file - require output file
        if not args.output:
            print("Error: --output is required when processing a file.", file=sys.stderr)
            sys.exit(1)
        process_file(args.input, args.output)
    else:
        # Input is treated as a hex string
        process_hex_string(args.input, args.output)

if __name__ == '__main__':
    main()
