"""
Program to count frequency of distinct words in text files.

This program reads words from text files and counts the frequency
of each distinct word, outputting results in alphabetical order.

Usage: python wordCount.py <filename1> [filename2] [filename3] ...
"""
# pylint: disable=invalid-name
# Module name required by assignment specification

import sys
import time
import os


def read_and_count_words(filename):
    """
    Read words from file and count their frequencies.

    Args:
        filename: Path to the input file

    Returns:
        Tuple of (word_count dictionary, error message or None)
    """
    word_count = {}

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                # Split line into words (handles multiple spaces)
                words = line.split()

                for word in words:
                    # Convert to lowercase for case-insensitive counting
                    word_lower = word.lower()
                    word_count[word_lower] = word_count.get(word_lower, 0) + 1

        return word_count, None

    except FileNotFoundError:
        return None, f"File not found: {filename}"
    except IOError as e:
        return None, f"Error reading file: {e}"


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


def format_file_results(filename, word_count):
    """
    Format word count results for a single file.

    Args:
        filename: Name of the file
        word_count: Dictionary of word frequencies

    Returns:
        Formatted string with word counts
    """
    output = []
    short_name = get_file_short_name(filename)

    output.append("=" * 70)
    output.append(f"FILE: {short_name}")
    output.append("=" * 70)

    if word_count is None:
        output.append("ERROR: Could not process file")
        return "\n".join(output)

    if not word_count:
        output.append("Warning: No words found in file")
        return "\n".join(output)

    output.append(f"{'Word':<30} {'Frequency':<10}")
    output.append("-" * 70)

    # Sort words alphabetically and show first 20
    sorted_words = sorted(word_count.keys())

    for word in sorted_words[:20]:
        output.append(f"{word:<30} {word_count[word]:<10}")

    if len(sorted_words) > 20:
        output.append(f"... and {len(sorted_words) - 20} more words")

    output.append("-" * 70)
    output.append(f"Total distinct words: {len(word_count)}")
    total_words = sum(word_count.values())
    output.append(f"Total word count: {total_words}")

    return "\n".join(output)


def format_summary_table(all_word_counts, filenames):
    """
    Format a summary table of all files processed.

    Args:
        all_word_counts: List of word count dictionaries
        filenames: List of filenames

    Returns:
        Formatted summary string
    """
    output = []
    output.append("\n" + "=" * 80)
    output.append("WORD COUNT SUMMARY - ALL FILES")
    output.append("=" * 80)
    output.append(f"{'File':<30} {'Distinct Words':<20} "
                  f"{'Total Words':<15} {'Status':<15}")
    output.append("-" * 80)

    for filename, word_count in zip(filenames, all_word_counts):
        short_name = get_file_short_name(filename)

        if word_count is None:
            status = "FAILED"
            distinct = 0
            total = 0
        else:
            status = "OK"
            distinct = len(word_count)
            total = sum(word_count.values())

        output.append(
            f"{short_name:<30} {distinct:<20} {total:<15} {status:<15}"
        )

    output.append("=" * 80)

    total_distinct_all = len(set().union(
        *[set(wc.keys()) for wc in all_word_counts if wc is not None]
    )) if any(wc is not None for wc in all_word_counts) else 0

    total_words_all = sum(
        sum(wc.values()) for wc in all_word_counts if wc is not None
    )

    output.append(f"Total distinct words across all files: "
                  f"{total_distinct_all}")
    output.append(f"Total words across all files: {total_words_all}")

    return "\n".join(output)


def format_consolidated_frequencies(all_word_counts):
    """
    Format consolidated word frequencies across all files.

    Args:
        all_word_counts: List of word count dictionaries

    Returns:
        Formatted string with consolidated frequencies
    """
    # Combine all word counts
    combined = {}
    for word_count in all_word_counts:
        if word_count is not None:
            for word, count in word_count.items():
                combined[word] = combined.get(word, 0) + count

    if not combined:
        return ""

    output = []
    output.append("\n" + "=" * 80)
    output.append("CONSOLIDATED WORD FREQUENCIES (Top 30 words)")
    output.append("=" * 80)
    output.append(f"{'Word':<30} {'Total Frequency':<20} {'Avg per File':<20}")
    output.append("-" * 80)

    # Sort by frequency (descending) and show top 30
    sorted_words = sorted(combined.items(), key=lambda x: x[1], reverse=True)

    num_files = sum(1 for wc in all_word_counts if wc is not None)

    for word, freq in sorted_words[:30]:
        avg_freq = freq / num_files if num_files > 0 else 0
        output.append(f"{word:<30} {freq:<20} {avg_freq:<20.2f}")

    if len(sorted_words) > 30:
        output.append(f"\n... and {len(sorted_words) - 30} more words")

    output.append("=" * 80)

    return "\n".join(output)


def main():
    # pylint: disable=too-many-locals,too-many-statements
    """Main program function."""
    # Check command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python wordCount.py <filename1> "
              "[filename2] [filename3] ...")
        sys.exit(1)

    filenames = sys.argv[1:]

    # Start timing
    start_time = time.time()

    print(f"\nProcessing {len(filenames)} file(s)...")
    print("=" * 80)

    # Process each file
    all_word_counts = []
    errors = {}

    for filename in filenames:
        short_name = get_file_short_name(filename)
        print(f"Processing: {short_name}...", end=" ")

        word_count, error = read_and_count_words(filename)

        if word_count is None:
            print("ERROR")
            errors[filename] = error
        else:
            distinct = len(word_count)
            total = sum(word_count.values())
            print(f"OK - {distinct} distinct words, {total} total words")

        all_word_counts.append(word_count)

    print()

    # Display errors if any
    if errors:
        print("=" * 80)
        print("ERRORS ENCOUNTERED:")
        print("=" * 80)
        for filename, error in errors.items():
            short_name = get_file_short_name(filename)
            print(f"{short_name}: {error}")
        print()

    # Format output for each file
    output_lines = []

    for filename, word_count in zip(filenames, all_word_counts):
        file_output = format_file_results(filename, word_count)
        print(file_output)
        print()
        output_lines.append(file_output)

    # Format summary table
    summary = format_summary_table(all_word_counts, filenames)
    print(summary)
    output_lines.append(summary)

    # Format consolidated frequencies
    consolidated = format_consolidated_frequencies(all_word_counts)
    if consolidated:
        print(consolidated)
        output_lines.append(consolidated)

    # Write results to file
    try:
        with open("results/WordCountResults.txt", 'w', encoding='utf-8') as f:
            f.write(f"Processed {len(filenames)} file(s)\n\n")

            if errors:
                f.write("ERRORS ENCOUNTERED:\n")
                f.write("=" * 80 + "\n")
                for filename, error in errors.items():
                    f.write(f"{filename}: {error}\n")
                f.write("\n")

            f.write("\n\n".join(output_lines))
    except IOError as e:
        print(f"\nWarning: Could not write results to file: {e}")

    # Display execution time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nExecution time: {elapsed_time:.4f} seconds")

    print("\nResults saved to: results/WordCountResults.txt")


if __name__ == "__main__":
    main()
