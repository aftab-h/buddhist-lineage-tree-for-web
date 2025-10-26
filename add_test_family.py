#!/usr/bin/env python3
"""
Add test familial relationship:
Move "Rigdzin Pema Trinlé" from Dawa Gyaltsen's Taught column to Taught_Familial_Related
"""

import csv

csv_file = 'data/dzogchen_lineage.csv'

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Find column indices
header = rows[0]
name_idx = header.index('Name_English')
taught_idx = header.index('Taught')
family_idx = header.index('Taught_Familial_Related')

# Find Dawa Gyaltsen row
for i, row in enumerate(rows[1:], 1):
    if row[name_idx] == 'Dawa Gyaltsen':
        print(f"Found Dawa Gyaltsen at row {i + 1}")
        print(f"  Current Taught: {row[taught_idx]}")
        print(f"  Current Taught_Familial_Related: {row[family_idx]}")

        # Move "Rigdzin Pema Trinlé" from Taught to Taught_Familial_Related
        row[family_idx] = 'Rigdzin Pema Trinlé'
        # Remove from Taught (empty it since this was the only student)
        row[taught_idx] = ''

        print(f"  Updated Taught: {row[taught_idx]}")
        print(f"  Updated Taught_Familial_Related: {row[family_idx]}")
        break

# Write back
with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)

print("\n✓ Test familial relationship added successfully!")
print("  Dawa Gyaltsen → Rigdzin Pema Trinlé (family link)")
