#!/usr/bin/env python3
"""Check current incarnation relationships in CSV"""

import csv

with open('data/dzogchen_lineage.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
name_idx = header.index('Name_English')
incarnation_idx = header.index('Incarnation_Of')

print("Current Incarnation_Of relationships:\n")

incarnation_count = 0
for row in rows[1:]:
    if row[incarnation_idx].strip():
        incarnation_count += 1
        print(f"  {row[name_idx]} ← incarnation of ← {row[incarnation_idx]}")

print(f"\n✓ Found {incarnation_count} incarnation relationships")
print(f"  (These will need to be reversed when converting to Reincarnated_As)")
