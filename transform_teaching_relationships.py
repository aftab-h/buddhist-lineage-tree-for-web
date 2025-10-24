#!/usr/bin/env python3
"""
Transform teaching relationships from upstream (Received_Teachings_From)
to downstream (Taught) format while preserving all data.
"""

import csv
import shutil
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Paths
CSV_PATH = Path("data/dzogchen_lineage.csv")
BACKUP_DIR = Path("data/old")
REPORT_PATH = Path("transformation_report.txt")

def create_backup():
    """Create timestamped backup of original CSV"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"dzogchen_lineage_backup_{timestamp}.csv"
    BACKUP_DIR.mkdir(exist_ok=True)
    shutil.copy2(CSV_PATH, backup_path)
    print(f"✓ Backup created: {backup_path}")
    return backup_path

def load_csv():
    """Load CSV into memory"""
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"✓ Loaded {len(rows)} rows from CSV")
    return rows

def find_column_index(fieldnames, column_name):
    """Find the index of a column in the fieldnames list"""
    try:
        return fieldnames.index(column_name)
    except ValueError:
        return -1

def transform_relationships(rows):
    """
    Transform teaching relationships from upstream to downstream format.
    Returns: (updated_rows, report_data, missing_names)
    """
    # Create name lookup for fast searching
    name_to_row = {row['Name_English']: row for row in rows}
    all_names = set(name_to_row.keys())

    # Initialize Taught column for all rows
    for row in rows:
        row['Taught'] = ''

    # Track statistics
    total_received_relationships = 0
    total_taught_relationships = 0
    missing_names = []
    transformations = []

    # Process each person
    for row in rows:
        person_name = row['Name_English']
        received_from = row.get('Received_Teachings_From', '').strip()

        if not received_from:
            continue

        # Split teachers (semicolon-separated)
        teachers = [t.strip() for t in received_from.split(';') if t.strip()]
        total_received_relationships += len(teachers)

        # For each teacher, add this person to their "Taught" list
        for teacher_name in teachers:
            # Check if teacher exists
            if teacher_name not in all_names:
                missing_names.append({
                    'student': person_name,
                    'missing_teacher': teacher_name
                })
                continue

            # Add person to teacher's Taught column
            teacher_row = name_to_row[teacher_name]
            current_taught = teacher_row['Taught'].strip()

            if current_taught:
                # Append with semicolon
                if person_name not in current_taught.split(';'):
                    teacher_row['Taught'] = f"{current_taught};{person_name}"
            else:
                # First student
                teacher_row['Taught'] = person_name

            # Track for report
            transformations.append({
                'teacher': teacher_name,
                'student': person_name
            })

    # Count total taught relationships
    for row in rows:
        taught = row['Taught'].strip()
        if taught:
            students = [s.strip() for s in taught.split(';') if s.strip()]
            total_taught_relationships += len(students)

    report_data = {
        'total_received': total_received_relationships,
        'total_taught': total_taught_relationships,
        'transformations': transformations,
        'sample_size': min(10, len([r for r in rows if r['Taught']]))
    }

    return rows, report_data, missing_names

def write_csv(rows, fieldnames):
    """Write updated CSV with new Taught column"""
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"✓ Updated CSV written to {CSV_PATH}")

def generate_report(report_data, missing_names, rows):
    """Generate detailed verification report"""
    report = []
    report.append("=" * 80)
    report.append("TEACHING RELATIONSHIPS TRANSFORMATION REPORT")
    report.append("=" * 80)
    report.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # Summary
    report.append("SUMMARY")
    report.append("-" * 80)
    report.append(f"Total relationships in 'Received_Teachings_From': {report_data['total_received']}")
    report.append(f"Total relationships in 'Taught':                 {report_data['total_taught']}")

    if report_data['total_received'] == report_data['total_taught']:
        report.append("✓ MATCH: Relationship counts are identical!")
    else:
        report.append("✗ MISMATCH: Relationship counts differ!")
        report.append(f"  Difference: {abs(report_data['total_received'] - report_data['total_taught'])}")

    report.append("")

    # Missing names
    if missing_names:
        report.append("MISSING NAMES (teachers not found in Name_English)")
        report.append("-" * 80)
        for item in missing_names:
            report.append(f"  Student: {item['student']}")
            report.append(f"  Missing Teacher: {item['missing_teacher']}")
            report.append("")
    else:
        report.append("✓ No missing names - all teachers found successfully")
        report.append("")

    # Sample transformations
    report.append(f"SAMPLE TRANSFORMATIONS (showing first {report_data['sample_size']})")
    report.append("-" * 80)

    # Get rows that have students
    rows_with_students = [r for r in rows if r['Taught'].strip()][:report_data['sample_size']]

    for row in rows_with_students:
        teacher = row['Name_English']
        students = row['Taught'].split(';')
        report.append(f"Teacher: {teacher}")
        report.append(f"  Taught → {', '.join(students)}")

        # Show reverse relationship
        received = row.get('Received_Teachings_From', '').strip()
        if received:
            report.append(f"  Received from ← {received}")
        report.append("")

    # Full transformation list
    report.append("")
    report.append(f"FULL TRANSFORMATION LIST ({len(report_data['transformations'])} relationships)")
    report.append("-" * 80)

    # Group by teacher
    by_teacher = defaultdict(list)
    for t in report_data['transformations']:
        by_teacher[t['teacher']].append(t['student'])

    for teacher in sorted(by_teacher.keys()):
        students = by_teacher[teacher]
        report.append(f"{teacher} → [{len(students)} students]")
        for student in sorted(students):
            report.append(f"    • {student}")

    report.append("")
    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    report_text = '\n'.join(report)

    # Write to file
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print(f"✓ Detailed report written to {REPORT_PATH}")

    return report_text

def main():
    print("\n" + "=" * 80)
    print("TEACHING RELATIONSHIPS TRANSFORMATION")
    print("=" * 80 + "\n")

    # Step 1: Backup
    print("Step 1: Creating backup...")
    backup_path = create_backup()

    # Step 2: Load CSV
    print("\nStep 2: Loading CSV...")
    rows = load_csv()

    # Get fieldnames and add Taught column
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)

    # Insert Taught column after Received_Teachings_From
    received_idx = find_column_index(fieldnames, 'Received_Teachings_From')
    if received_idx != -1:
        fieldnames.insert(received_idx + 1, 'Taught')
    else:
        # Fallback: add at end
        fieldnames.append('Taught')

    print(f"✓ Added 'Taught' column at position {fieldnames.index('Taught') + 1}")

    # Step 3: Transform relationships
    print("\nStep 3: Transforming relationships...")
    rows, report_data, missing_names = transform_relationships(rows)

    # Step 4: Check for missing names
    if missing_names:
        print(f"\n⚠ WARNING: Found {len(missing_names)} missing teacher names!")
        print("\nMissing names:")
        for item in missing_names[:5]:  # Show first 5
            print(f"  - '{item['missing_teacher']}' (listed as teacher of {item['student']})")
        if len(missing_names) > 5:
            print(f"  ... and {len(missing_names) - 5} more")

        print("\n⛔ STOPPING: Please review missing names before proceeding.")
        print(f"Full list will be in: {REPORT_PATH}")

        # Generate report even on error
        generate_report(report_data, missing_names, rows)
        return False

    print("✓ All teacher names found successfully")

    # Step 5: Write updated CSV
    print("\nStep 4: Writing updated CSV...")
    write_csv(rows, fieldnames)

    # Step 6: Generate report
    print("\nStep 5: Generating verification report...")
    report_text = generate_report(report_data, missing_names, rows)

    # Print summary
    print("\n" + "=" * 80)
    print("TRANSFORMATION COMPLETE!")
    print("=" * 80)
    print(f"Backup saved to: {backup_path}")
    print(f"Report saved to: {REPORT_PATH}")
    print(f"\nRelationships transformed: {report_data['total_taught']}")
    print(f"Verification: {'✓ PASS' if report_data['total_received'] == report_data['total_taught'] else '✗ FAIL'}")
    print("\n")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
