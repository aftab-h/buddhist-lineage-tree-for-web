#!/usr/bin/env python3
"""Precise check of specific rows"""

import csv

with open('data/dzogchen_lineage.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]

print("COLUMN INDICES:")
for i, col in enumerate(header):
    print(f"  {i}: {col}")

print("\n" + "=" * 80)
print("CHECKING 'Tulku Urgyen Rinpoche' row:")
print("=" * 80)

for row in rows[1:]:
    if row[0] == 'Tulku Urgyen Rinpoche':
        for i, value in enumerate(row):
            if i >= 12 and i <= 19:  # Show relationship columns
                print(f"  [{i:2d}] {header[i]:30s} = '{value}'")
        break

print("\n" + "=" * 80)
print("CHECKING 'Dawa Gyaltsen' row:")
print("=" * 80)

for row in rows[1:]:
    if row[0] == 'Dawa Gyaltsen':
        for i, value in enumerate(row):
            if i >= 12 and i <= 19:
                print(f"  [{i:2d}] {header[i]:30s} = '{value}'")
        break

print("\n" + "=" * 80)
print("ALL ROWS WITH 'TRUE' IN ANY RELATIONSHIP COLUMN:")
print("=" * 80)

for row in rows[1:]:
    for i in range(12, 18):  # Check all relationship columns
        if row[i].strip() == 'TRUE':
            print(f"\nRow: {row[0]}")
            print(f"  Column {i} ({header[i]}): 'TRUE' ❌")
            break
