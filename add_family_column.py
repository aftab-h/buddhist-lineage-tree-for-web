#!/usr/bin/env python3
"""
Add Taught_Familial_Related column to dzogchen_lineage.csv
This column will be inserted after the Taught column (position 14)
"""

import csv

input_file = 'data/old/dzogchen_lineage_backup_before_family_column.csv'
output_file = 'data/dzogchen_lineage.csv'

# Read the CSV with proper quoting
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_ALL)
    rows = list(reader)

# Process header
header = rows[0]
# Find the index of 'Taught' column
taught_index = header.index('Taught')
# Insert new column after Taught
new_header = header[:taught_index + 1] + ['Taught_Familial_Related'] + header[taught_index + 1:]

# Process data rows - add empty value for new column
new_rows = [new_header]
for row in rows[1:]:
    # Insert empty string at the position after Taught column
    new_row = row[:taught_index + 1] + [''] + row[taught_index + 1:]
    new_rows.append(new_row)

# Write the updated CSV with proper quoting
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(new_rows)

print(f"✓ Added Taught_Familial_Related column at position {taught_index + 2}")
print(f"✓ Total columns: {len(new_header)} (was {len(header)})")
print(f"✓ Updated {len(new_rows) - 1} data rows")
print(f"✓ CSV updated successfully with proper quoting")
