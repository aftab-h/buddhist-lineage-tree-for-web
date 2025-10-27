#!/usr/bin/env python3
"""Check for name mismatches in all relationship columns"""

import csv

with open('data/dzogchen_lineage.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
name_idx = header.index('Name_English')

# Get all valid names
all_names = set(row[name_idx].strip() for row in rows[1:] if row[name_idx].strip())

print("=" * 80)
print("NAME REFERENCE VALIDATION")
print("=" * 80)
print(f"\nTotal masters in database: {len(all_names)}\n")

# Check each relationship column
relationship_cols = [
    ('Taught', 13),
    ('Taught_Familial_Related', 14),
    ('Reincarnated_As', 15),
    ('Emanated as', 17)
]

mismatches_found = False

for col_name, col_idx in relationship_cols:
    print(f"\n{col_name} (Column {col_idx}):")
    print("-" * 80)

    mismatches = []
    for row in rows[1:]:
        if col_idx < len(row) and row[col_idx].strip():
            source_name = row[name_idx]
            references = [v.strip() for v in row[col_idx].split(';') if v.strip()]

            for ref in references:
                if ref not in all_names:
                    mismatches.append((source_name, ref))

    if mismatches:
        mismatches_found = True
        print(f"  ⚠️  Found {len(mismatches)} name mismatch(es):")
        for source, target in mismatches:
            print(f"     '{source}' → '{target}' ❌ (NOT FOUND)")
    else:
        print(f"  ✓ All name references are valid")

if not mismatches_found:
    print("\n" + "=" * 80)
    print("✓✓✓ ALL NAME REFERENCES ARE VALID! ✓✓✓")
    print("=" * 80)
else:
    print("\n" + "=" * 80)
    print("⚠️  NAME MISMATCHES DETECTED - THESE MUST BE FIXED!")
    print("=" * 80)

# Check for circular references
print("\n" + "=" * 80)
print("CIRCULAR REFERENCE CHECK")
print("=" * 80)

# Check reincarnation chains
reincarnation_map = {}
for row in rows[1:]:
    name = row[name_idx]
    if row[15].strip():  # Reincarnated_As column
        next_incarnations = [v.strip() for v in row[15].split(';') if v.strip()]
        reincarnation_map[name] = next_incarnations

# Find chains
chains = []
for start_name in reincarnation_map:
    chain = [start_name]
    current = start_name
    visited = {start_name}

    while current in reincarnation_map:
        next_list = reincarnation_map[current]
        if len(next_list) > 0:
            next_name = next_list[0]  # Take first if multiple
            if next_name in visited:
                print(f"  ⚠️  Circular reference detected: {' → '.join(chain)} → {next_name}")
                break
            chain.append(next_name)
            visited.add(next_name)
            current = next_name
        else:
            break

    if len(chain) > 2:
        chains.append(chain)

if chains:
    print(f"\n  Found {len(chains)} reincarnation chains:")
    for chain in chains[:10]:  # Show first 10
        print(f"    {' → '.join(chain)}")
else:
    print("  ✓ No long reincarnation chains found")

print("\n" + "=" * 80)
