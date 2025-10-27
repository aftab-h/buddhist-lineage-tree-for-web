#!/usr/bin/env python3
"""Inspect problematic rows in detail"""

import csv

with open('data/dzogchen_lineage.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
print("=" * 80)
print("DETAILED INSPECTION OF PROBLEM ROWS")
print("=" * 80)

# Check rows with TRUE in Reincarnated_As
print("\n1. Rows with 'TRUE' in Reincarnated_As (Column 15):")
print("-" * 80)

for i, row in enumerate(rows[1:], 2):
    if row[14].strip() == 'TRUE':  # Reincarnated_As column
        print(f"\nRow {i}: {row[0]}")
        print(f"  Col 13 (Taught): '{row[12]}'")
        print(f"  Col 14 (Taught_Familial_Related): '{row[13]}'")
        print(f"  Col 15 (Reincarnated_As): '{row[14]}' ❌")
        print(f"  Col 16 (Family_Relationship): '{row[15]}'")
        print(f"  Col 17 (Emanated as): '{row[16]}'")

# Check a few rows with non-name values in Emanated as
print("\n\n2. Sample rows with Links in Emanated as (Column 17):")
print("-" * 80)

count = 0
for i, row in enumerate(rows[1:], 2):
    if row[16].strip() in ['Treasury of Lives', 'BDRC', 'Rigpa Wiki'] and count < 5:
        count += 1
        print(f"\nRow {i}: {row[0]}")
        print(f"  Col 16 (Family_Relationship): '{row[15]}'")
        print(f"  Col 17 (Emanated as): '{row[16]}' ❌ (Should be in Links_Names)")
        print(f"  Col 18 (Links_Names): '{row[17]}'")
        print(f"  Col 19 (Links_URLs): '{row[18]}'")

print("\n" + "=" * 80)
print("DIAGNOSIS:")
print("=" * 80)
print("""
⚠️  CRITICAL ISSUES FOUND:

1. **Reincarnated_As column (15) has 'TRUE' values**
   - These appear to be leftover artifacts from Family_Relationship column
   - 6 rows affected
   - Fix: Replace 'TRUE' with empty string (or correct incarnation if known)

2. **Emanated as column (17) has link names instead of master names**
   - 69 rows have 'Treasury of Lives', 'BDRC', or 'Rigpa Wiki'
   - These look like they belong in Links_Names column (18)
   - This suggests columns were shifted during your edit
   - Fix: Need to check if Links_Names and Links_URLs shifted

POSSIBLE CAUSE:
When you renamed 'Incarnation_Of' to 'Reincarnated_As', the data in subsequent
columns may have been shifted. The 'Emanated as' column appears to have absorbed
data from Links_Names column.
""")

print("\n" + "=" * 80)
