#!/usr/bin/env python3
"""
Hex Decoder - Converts $HEX[...] encoded strings within Hashcat potfiles to UTF-8 text
"""

import argparse
import sys
import re

# ==============================
# Function to convert HEX to UTF8 string
# ==============================
def convert_hex_to_utf8(hex_string):
    """Converts a hexadecimal string to UTF-8 decoded text."""
    # Remove any whitespace from the hex string
    hex_string = re.sub(r'\s', '', hex_string)
    
    try:
        # Convert hex string to bytes, then decode as UTF-8
        bytes_data = bytes.fromhex(hex_string)
        return bytes_data.decode('utf-8')
    except (ValueError, UnicodeDecodeError) as e:
        # Return None if conversion fails
        return None

# ==============================
# Process input file
# ==============================
def process_file(input_file, output_file):
    """Reads input file, decodes $HEX[...] lines, and writes to output file."""
    decoded_lines = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n\r')
                
                # Check if line matches $HEX[hexadecimal] pattern
                match = re.match(r'^\$HEX\[([0-9A-Fa-f]+)\]$', line)
                
                if match:
                    hex_value = match.group(1)
                    decoded = convert_hex_to_utf8(hex_value)
                    
                    # Use decoded value if successful, otherwise keep original line
                    decoded_lines.append(decoded if decoded is not None else line)
                else:
                    # Non-HEX lines remain unchanged
                    decoded_lines.append(line)
        
        # Write all decoded lines to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(decoded_lines) + '\n')
        
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
        epilog='Example: python convert_hex_to_UTF8.py --input hex_input.txt --output hex_decoded.txt'
    )
    
    # Define command-line arguments
    parser.add_argument('--input', '-i', 
                        required=True,
                        help='Input file path containing hex-encoded text')
    parser.add_argument('--output', '-o',
                        required=True,
                        help='Output file path for decoded text')
    
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    # Process the input file and create output
    process_file(args.input, args.output)

if __name__ == '__main__':
    main()
