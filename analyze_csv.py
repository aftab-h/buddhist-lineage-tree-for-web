#!/usr/bin/env python3
"""Comprehensive CSV analysis for issues and redundancies"""

import csv
from collections import defaultdict

with open('data/dzogchen_lineage.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
print("=" * 80)
print("CSV STRUCTURE ANALYSIS")
print("=" * 80)

# Check header
print(f"\n1. HEADER CHECK:")
print(f"   Total columns: {len(header)}")
for i, col in enumerate(header, 1):
    print(f"   {i:2d}. {col}")

# Get column indices
name_idx = header.index('Name_English')
taught_idx = header.index('Taught') if 'Taught' in header else -1
family_idx = header.index('Taught_Familial_Related') if 'Taught_Familial_Related' in header else -1
incarnation_idx = -1
reincarnated_idx = -1

# Check for incarnation column name
if 'Incarnation_Of' in header:
    incarnation_idx = header.index('Incarnation_Of')
    print(f"\n   ⚠️  WARNING: Found 'Incarnation_Of' at column {incarnation_idx + 1}")
if 'Reincarnated_As' in header:
    reincarnated_idx = header.index('Reincarnated_As')
    print(f"   ✓ Found 'Reincarnated_As' at column {reincarnated_idx + 1}")

emanation_idx = header.index('Emanated as') if 'Emanated as' in header else -1

print("\n" + "=" * 80)
print("2. RELATIONSHIP DATA ANALYSIS")
print("=" * 80)

# Analyze relationship columns
relationships = {
    'Taught': (taught_idx, []),
    'Taught_Familial_Related': (family_idx, []),
    'Incarnation_Of': (incarnation_idx, []),
    'Reincarnated_As': (reincarnated_idx, []),
    'Emanated as': (emanation_idx, [])
}

for row in rows[1:]:
    name = row[name_idx]
    for rel_name, (idx, data_list) in relationships.items():
        if idx >= 0 and idx < len(row) and row[idx].strip():
            values = [v.strip() for v in row[idx].split(';') if v.strip()]
            data_list.append((name, values))

# Print relationship summaries
for rel_name, (idx, data_list) in relationships.items():
    if idx >= 0:
        print(f"\n{rel_name} (Column {idx + 1}):")
        print(f"  - {len(data_list)} rows have data")
        if len(data_list) > 0:
            print(f"  - Examples:")
            for name, values in data_list[:5]:
                print(f"      {name} → {', '.join(values)}")
    else:
        print(f"\n{rel_name}: Column not found")

print("\n" + "=" * 80)
print("3. POTENTIAL ISSUES")
print("=" * 80)

issues = []

# Issue 1: Check if both Incarnation_Of and Reincarnated_As exist
if incarnation_idx >= 0 and reincarnated_idx >= 0:
    issues.append("⚠️  CRITICAL: Both 'Incarnation_Of' AND 'Reincarnated_As' columns exist!")
    issues.append("   → This will cause duplicate incarnation links")
    issues.append("   → Solution: Remove 'Incarnation_Of' column entirely")

# Issue 2: Check for name mismatches
all_names = set(row[name_idx] for row in rows[1:])
for rel_name, (idx, data_list) in relationships.items():
    if idx >= 0:
        for name, values in data_list:
            for value in values:
                if value not in all_names:
                    issues.append(f"⚠️  Name mismatch in {rel_name}: '{name}' references '{value}' (not found in Name_English)")

# Issue 3: Check for both Taught and Taught_Familial_Related having same person
if taught_idx >= 0 and family_idx >= 0:
    overlaps = []
    for row in rows[1:]:
        name = row[name_idx]
        taught_values = set(v.strip() for v in row[taught_idx].split(';') if v.strip())
        family_values = set(v.strip() for v in row[family_idx].split(';') if v.strip())
        overlap = taught_values & family_values
        if overlap:
            overlaps.append((name, overlap))

    if overlaps:
        issues.append(f"⚠️  {len(overlaps)} rows have same person in BOTH Taught and Taught_Familial_Related:")
        for name, overlap in overlaps[:5]:
            issues.append(f"   → {name}: {', '.join(overlap)}")

# Issue 4: Check column count consistency
col_counts = defaultdict(int)
for i, row in enumerate(rows, 1):
    col_counts[len(row)] += 1

if len(col_counts) > 1:
    issues.append(f"⚠️  Inconsistent column counts across rows:")
    for count, num_rows in sorted(col_counts.items()):
        issues.append(f"   → {count} columns: {num_rows} rows")

if issues:
    for issue in issues:
        print(issue)
else:
    print("✓ No critical issues found!")

print("\n" + "=" * 80)
print("4. RECOMMENDATIONS")
print("=" * 80)

recommendations = []

# Check if we need to update the app code
if reincarnated_idx >= 0:
    recommendations.append("✓ Update index.html to use 'Reincarnated_As' instead of 'Incarnation_Of'")
    recommendations.append("✓ Update link direction: source = current, target = future incarnation")

if incarnation_idx >= 0 and reincarnated_idx >= 0:
    recommendations.append("❗ REMOVE 'Incarnation_Of' column (it's been replaced by 'Reincarnated_As')")

recommendations.append("✓ Verify all name references match Name_English column exactly")

if recommendations:
    for rec in recommendations:
        print(rec)

print("\n" + "=" * 80)
