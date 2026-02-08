"""
Program to convert decimal numbers to binary and hexadecimal.

This program reads decimal numbers from files and converts each to:
- Binary representation
- Hexadecimal representation

Usage: python convertNumbers.py <filename1> [filename2] [filename3] ...
"""
# pylint: disable=invalid-name
# Module name required by assignment specification

import sys
import time
import os


def decimal_to_binary(num):
    """
    Convert a decimal number to binary using basic algorithm.

    Args:
        num: Decimal number (int or float)

    Returns:
        Binary representation as a string
    """
    if num == 0:
        return "0"

    # Handle negative numbers
    negative = num < 0
    num = abs(int(num))

    binary = ""
    while num > 0:
        remainder = num % 2
        binary = str(remainder) + binary
        num = num // 2

    if negative:
        binary = "-" + binary

    return binary


def decimal_to_hexadecimal(num):
    """
    Convert a decimal number to hexadecimal using basic algorithm.

    Args:
        num: Decimal number (int or float)

    Returns:
        Hexadecimal representation as a string
    """
    if num == 0:
        return "0"

    # Handle negative numbers
    negative = num < 0
    num = abs(int(num))

    hex_chars = "0123456789ABCDEF"
    hexadecimal = ""

    while num > 0:
        remainder = num % 16
        hexadecimal = hex_chars[remainder] + hexadecimal
        num = num // 16

    if negative:
        hexadecimal = "-" + hexadecimal

    return hexadecimal


def read_and_convert_numbers(filename):
    """
    Read numbers from file and convert them.

    Args:
        filename: Path to the input file

    Returns:
        A tuple of (list of conversion results, list of errors)
    """
    conversions = []
    errors = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    number = float(line)
                    binary = decimal_to_binary(number)
                    hexadecimal = decimal_to_hexadecimal(number)

                    conversions.append({
                        'decimal': int(number),
                        'binary': binary,
                        'hex': hexadecimal
                    })

                except ValueError:
                    error_msg = (f"Line {line_number}: "
                                 f"Invalid data '{line}'")
                    errors.append(error_msg)

        return conversions, errors

    except FileNotFoundError:
        return None, [f"File not found: {filename}"]
    except IOError as e:
        return None, [f"Error reading file: {e}"]


def get_file_short_name(filepath):
    """
    Get a short name for a file (filename without path and extension).

    Args:
        filepath: Full path to file

    Returns:
        Short filename
    """
    basename = os.path.basename(filepath)
    name_without_ext = os.path.splitext(basename)[0]
    return name_without_ext


def format_file_results(filename, conversions, errors):
    """
    Format conversion results for a single file.

    Args:
        filename: Name of the file
        conversions: List of conversion dictionaries
        errors: List of error messages

    Returns:
        Formatted string with conversions
    """
    output = []
    short_name = get_file_short_name(filename)

    output.append("=" * 80)
    output.append(f"FILE: {short_name}")
    output.append("=" * 80)

    if conversions is None:
        output.append("ERROR: Could not process file")
        if errors:
            for error in errors:
                output.append(f"  - {error}")
        return "\n".join(output)

    if errors:
        output.append(f"Errors found: {len(errors)}")
        for error in errors[:3]:
            output.append(f"  - {error}")
        if len(errors) > 3:
            output.append(f"  ... and {len(errors) - 3} more errors")
        output.append("")

    output.append(f"{'Decimal':<15} {'Binary':<35} {'Hexadecimal':<15}")
    output.append("-" * 80)

    # Show first 10 conversions
    for conv in conversions[:10]:
        output.append(
            f"{conv['decimal']:<15} {conv['binary']:<35} {conv['hex']:<15}"
        )

    if len(conversions) > 10:
        output.append(f"... and {len(conversions) - 10} more conversions")

    output.append("-" * 80)
    output.append(f"Total conversions: {len(conversions)}")

    return "\n".join(output)


def format_summary_table(all_results, filenames):
    """
    Format a summary table of all files processed.

    Args:
        all_results: List of tuples (conversions, errors)
        filenames: List of filenames

    Returns:
        Formatted summary string
    """
    output = []
    output.append("\n" + "=" * 80)
    output.append("CONVERSION SUMMARY - ALL FILES")
    output.append("=" * 80)
    output.append(f"{'File':<30} {'Conversions':<15} {'Errors':<15} {'Status':<20}")
    output.append("-" * 80)

    for filename, (conversions, errors) in zip(filenames, all_results):
        short_name = get_file_short_name(filename)

        if conversions is None:
            status = "FAILED"
            conv_count = 0
            error_count = len(errors) if errors else 0
        else:
            status = "OK" if not errors else "OK (with errors)"
            conv_count = len(conversions)
            error_count = len(errors) if errors else 0

        output.append(
            f"{short_name:<30} {conv_count:<15} {error_count:<15} {status:<20}"
        )

    output.append("=" * 80)

    total_conversions = sum(
        len(conv) for conv, _ in all_results if conv is not None
    )
    total_errors = sum(
        len(err) for _, err in all_results if err is not None
    )

    output.append(f"Total conversions across all files: {total_conversions}")
    output.append(f"Total errors across all files: {total_errors}")

    return "\n".join(output)


def main():
    # pylint: disable=too-many-locals
    """Main program function."""
    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python convertNumbers.py <filename1> "
              "[filename2] [filename3] ...")
        sys.exit(1)

    filenames = sys.argv[1:]

    # Start timing
    start_time = time.time()

    print(f"\nProcessing {len(filenames)} file(s)...")
    print("=" * 80)

    # Process each file
    all_results = []

    for filename in filenames:
        short_name = get_file_short_name(filename)
        print(f"Processing: {short_name}...", end=" ")

        conversions, errors = read_and_convert_numbers(filename)

        if conversions is None:
            print("ERROR")
        else:
            status = "OK" if not errors else f"OK ({len(errors)} errors)"
            print(f"{status} - {len(conversions)} conversions")

        all_results.append((conversions, errors))

    print()

    # Format output for each file
    output_lines = []

    for filename, (conversions, errors) in zip(filenames, all_results):
        file_output = format_file_results(filename, conversions, errors)
        print(file_output)
        print()
        output_lines.append(file_output)

    # Format summary table
    summary = format_summary_table(all_results, filenames)
    print(summary)
    output_lines.append(summary)

    # Write results to file
    try:
        with open("results/ConversionResults.txt", 'w', encoding='utf-8') as f:
            f.write(f"Processed {len(filenames)} file(s)\n\n")
            f.write("\n\n".join(output_lines))
    except IOError as e:
        print(f"\nWarning: Could not write results to file: {e}")

    # Display execution time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nExecution time: {elapsed_time:.4f} seconds")

    print("\nResults saved to: results/ConversionResults.txt")


if __name__ == "__main__":
    main()
