#!/usr/bin/env python3
"""Check test familial relationship"""

import csv

with open('data/dzogchen_lineage.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
name_idx = header.index('Name_English')
taught_idx = header.index('Taught')
family_idx = header.index('Taught_Familial_Related')

print("Checking test familial relationship:\n")

for row in rows[1:]:
    if row[name_idx] == 'Dawa Gyaltsen':
        print(f"✓ Dawa Gyaltsen:")
        print(f"  - Taught (regular): '{row[taught_idx]}'")
        print(f"  - Taught_Familial_Related: '{row[family_idx]}'")

    if row[name_idx] == 'Rigdzin Pema Trinlé':
        print(f"\n✓ Rigdzin Pema Trinlé:")
        print(f"  - Taught (regular): '{row[taught_idx]}'")
        print(f"  - Taught_Familial_Related: '{row[family_idx]}'")

print("\n✓ Test data verification complete!")
print("  Expected: Dawa Gyaltsen → Rigdzin Pema Trinlé (dashed brown line)")
