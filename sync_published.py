#!/usr/bin/env python3
"""
Syncs content_approval.csv with actual blog HTML files on disk.
Any tool with a matching HTML file gets marked Published.
"""
import os, csv, re, glob

# Get all published blog HTML files
html_files = glob.glob('blog/*.html')
published_slugs = set()
for f in html_files:
    basename = os.path.basename(f).replace('.html', '').replace('-review', '').replace('-', ' ').strip()
    published_slugs.add(basename)

print(f"Found {len(html_files)} HTML files in blog/")

# Read CSV
rows = []
header = None
updated = 0
already_published = 0

with open('content_approval.csv', 'r') as f:
    reader = csv.reader(f)
    for i, row in enumerate(reader):
        if i == 0:
            header = row
            rows.append(row)
            continue
        if len(row) < 4:
            rows.append(row)
            continue

        tool_name = row[1].strip().lower()
        draft_file = row[2].strip()
        status = row[3].strip()

        if status == 'Published':
            already_published += 1
            rows.append(row)
            continue

        # Check if a matching HTML file exists
        tool_clean = tool_name.replace(' ai','').replace(' io','').replace(' ', '-').strip()
        tool_full = tool_name.replace(' ', '-')

        matched = False
        for f_path in html_files:
            fname = os.path.basename(f_path).lower()
            if tool_clean in fname or tool_full in fname or tool_name.replace(' ','-') in fname:
                row[3] = 'Published'
                updated += 1
                matched = True
                print(f"  ✅ Marked Published: {row[1]} -> {os.path.basename(f_path)}")
                break

        rows.append(row)

# Write back
with open('content_approval.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"\n📊 Summary:")
print(f"  Already published: {already_published}")
print(f"  Newly marked published: {updated}")
print(f"  Total rows: {len(rows)-1}")
