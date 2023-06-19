#!/usr/bin/env python
import datetime
import difflib
import sys
import re

def lines(fn):
    """Read lines from a file and return them as a list."""
    return open(fn).readlines()

def want(line):
    """Check if a line should be considered for comparison."""
    if re.search("^[+-][^+-]{2}", line):
        return True

def change(line):
    """Extract the operation (added or removed) and the content of a line."""
    rest = line[1:].rstrip()

    if line[0] == '+':
        return "added", rest

    if line[0] == '-':
        return "removed", rest

def show_diff(a, b):
    """Compare two files and display the added and removed lines."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate the differences between the lines of the two files
    diff = difflib.unified_diff(lines(a), lines(b))

    # Filter the differences and print the changes
    for line in filter(want, diff):
        op, what = change(line)
        print(f"{now} {op} {what}")

if __name__ == "__main__":
    # Check if the script is called with two file names as command-line arguments
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s file1 file2\n" % sys.argv[0])
        sys.exit(1)

    # Assign the file names to variables
    a = sys.argv[1]
    b = sys.argv[2]

    # Compare the files and display the differences
    show_diff(a, b)
