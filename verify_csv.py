#!/usr/bin/env python3
"""Verify CSV structure"""

import csv

csv_file = 'data/dzogchen_lineage.csv'

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Total rows: {len(rows)}")
print(f"Header columns: {len(rows[0])}")

# Check column consistency
column_counts = {}
for i, row in enumerate(rows):
    col_count = len(row)
    if col_count not in column_counts:
        column_counts[col_count] = []
    column_counts[col_count].append(i + 1)

print(f"\nColumn count distribution:")
for count, row_nums in sorted(column_counts.items()):
    if len(row_nums) <= 5:
        print(f"  {count} columns: rows {row_nums}")
    else:
        print(f"  {count} columns: {len(row_nums)} rows (e.g., rows {row_nums[:5]}...)")

if len(column_counts) == 1:
    print("\n✓ All rows have consistent column count!")
else:
    print("\n✗ Warning: Inconsistent column counts found!")

# Show header
print(f"\nHeader columns:")
for i, col in enumerate(rows[0], 1):
    print(f"  {i}. {col}")
