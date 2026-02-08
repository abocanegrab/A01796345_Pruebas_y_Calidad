"""
Program to calculate descriptive statistics from numeric data files.

This program reads numbers from files and calculates:
- Mean (average)
- Median (middle value)
- Mode (most frequent value)
- Standard Deviation
- Variance

Usage: python computeStatistics.py <filename1> [filename2] [filename3] ...
"""
# pylint: disable=invalid-name
# Module name required by assignment specification

import sys
import time
import math
import os


def read_numbers_from_file(filename):
    """
    Read numbers from a file, skipping invalid entries.

    Args:
        filename: Path to the input file

    Returns:
        A tuple of (list of valid numbers, list of error messages)
    """
    numbers = []
    errors = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    number = float(line)
                    numbers.append(number)
                except ValueError:
                    error_msg = (f"Line {line_number}: "
                                 f"Invalid data '{line}'")
                    errors.append(error_msg)

        return numbers, errors

    except FileNotFoundError:
        return None, [f"File not found: {filename}"]
    except IOError as e:
        return None, [f"Error reading file: {e}"]


def calculate_mean(numbers):
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
        numbers: List of numeric values

    Returns:
        The mean value
    """
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    """
    Calculate the median of a list of numbers.

    Args:
        numbers: List of numeric values

    Returns:
        The median value
    """
    if not numbers:
        return 0

    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)

    if n % 2 == 0:
        # Even number of elements: average of two middle values
        return (sorted_numbers[n // 2 - 1] + sorted_numbers[n // 2]) / 2

    # Odd number of elements: middle value
    return sorted_numbers[n // 2]


def calculate_mode(numbers):
    """
    Calculate the mode of a list of numbers.

    If all values are unique or multiple values tie for highest frequency,
    returns "N/A".

    Args:
        numbers: List of numeric values

    Returns:
        The mode value or "N/A"
    """
    if not numbers:
        return "N/A"

    # Count frequency of each number
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1

    # Find maximum frequency
    max_freq = max(frequency.values())

    # Check if all values are unique
    if max_freq == 1:
        return "N/A"

    # Find all numbers with maximum frequency
    modes = [num for num, freq in frequency.items() if freq == max_freq]

    # If multiple modes, return first one with indicator
    if len(modes) > 1:
        return f"{modes[0]}*"

    return modes[0]


def calculate_variance(numbers, mean):
    """
    Calculate the variance of a list of numbers.

    Args:
        numbers: List of numeric values
        mean: The mean of the numbers

    Returns:
        The variance value
    """
    if not numbers:
        return 0

    squared_diffs = [(x - mean) ** 2 for x in numbers]
    return sum(squared_diffs) / len(numbers)


def calculate_std_deviation(variance):
    """
    Calculate the standard deviation from variance.

    Args:
        variance: The variance value

    Returns:
        The standard deviation
    """
    return math.sqrt(variance)


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


def format_cross_table(all_stats, filenames):
    """
    Format statistics as a cross table.

    Args:
        all_stats: List of statistics dictionaries
        filenames: List of filenames

    Returns:
        Formatted string with cross table
    """
    # Get short names for files
    short_names = [get_file_short_name(f) for f in filenames]

    # Calculate column widths
    name_col_width = max(20, max(len(name) for name in short_names) + 2)

    output = []
    output.append("=" * (25 + name_col_width * len(filenames)))
    output.append("DESCRIPTIVE STATISTICS - CROSS TABLE")
    output.append("=" * (25 + name_col_width * len(filenames)))

    # Header row
    header = f"{'Statistic':<25}"
    for name in short_names:
        header += f"{name:>{name_col_width}}"
    output.append(header)
    output.append("-" * (25 + name_col_width * len(filenames)))

    # Data rows
    metrics = [
        ('Count', 'count', ''),
        ('Mean', 'mean', '.2f'),
        ('Median', 'median', '.2f'),
        ('Mode', 'mode', ''),
        ('Variance', 'variance', '.2f'),
        ('Standard Deviation', 'std_dev', '.2f')
    ]

    for label, key, fmt in metrics:
        row = f"{label:<25}"
        for stats in all_stats:
            if stats is None:
                row += f"{'ERROR':>{name_col_width}}"
            else:
                value = stats[key]
                if isinstance(value, (int, float)) and fmt:
                    row += f"{value:>{name_col_width}{fmt}}"
                else:
                    row += f"{str(value):>{name_col_width}}"
        output.append(row)

    output.append("=" * (25 + name_col_width * len(filenames)))
    output.append("\n* Multiple modes detected (showing first one)")

    return "\n".join(output)


def process_file(filename):
    """
    Process a single file and return statistics.

    Args:
        filename: Path to file

    Returns:
        Dictionary with statistics or None if error
    """
    numbers, errors = read_numbers_from_file(filename)

    if numbers is None:
        return None, errors

    if not numbers:
        return None, ["No valid numeric data found"]

    # Calculate statistics
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = calculate_mode(numbers)
    pop_variance = calculate_variance(numbers, mean)
    std_dev = calculate_std_deviation(pop_variance)
    n = len(numbers)
    variance = pop_variance * n / (n - 1) if n > 1 else 0

    stats = {
        'count': len(numbers),
        'mean': mean,
        'median': median,
        'mode': mode,
        'variance': variance,
        'std_dev': std_dev
    }

    return stats, errors


def main():
    # pylint: disable=too-many-locals,too-many-branches
    """Main program function."""
    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python computeStatistics.py <filename1> "
              "[filename2] [filename3] ...")
        sys.exit(1)

    filenames = sys.argv[1:]

    # Start timing
    start_time = time.time()

    print(f"\nProcessing {len(filenames)} file(s)...")
    print("=" * 70)

    # Process each file
    all_stats = []
    all_errors = {}

    for filename in filenames:
        short_name = get_file_short_name(filename)
        print(f"Processing: {short_name}...", end=" ")

        stats, errors = process_file(filename)

        if stats is None:
            print("ERROR")
            all_errors[filename] = errors
        else:
            print(f"OK ({stats['count']} numbers)")
            if errors:
                all_errors[filename] = errors

        all_stats.append(stats)

    print()

    # Display errors if any
    if all_errors:
        print("=" * 70)
        print("ERRORS ENCOUNTERED:")
        print("=" * 70)
        for filename, errors in all_errors.items():
            short_name = get_file_short_name(filename)
            print(f"\n{short_name}:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(errors) > 5:
                print(f"  ... and {len(errors) - 5} more errors")
        print()

    # Format cross table
    output = format_cross_table(all_stats, filenames)

    # Display results
    print(output)

    # Write results to file
    try:
        with open("results/StatisticsResults.txt", 'w', encoding='utf-8') as f:
            f.write(f"Processed {len(filenames)} file(s)\n\n")

            if all_errors:
                f.write("ERRORS ENCOUNTERED:\n")
                f.write("=" * 70 + "\n")
                for filename, errors in all_errors.items():
                    f.write(f"\n{filename}:\n")
                    for error in errors:
                        f.write(f"  - {error}\n")
                f.write("\n")

            f.write(output)
    except IOError as e:
        print(f"\nWarning: Could not write results to file: {e}")

    # Display execution time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nExecution time: {elapsed_time:.4f} seconds")

    print("\nResults saved to: results/StatisticsResults.txt")


if __name__ == "__main__":
    main()
