#!/usr/bin/env python3
"""
Reddit lead generator - includes live review URLs automatically
"""
import os, csv, re

# Build a map of tool name -> published URL from content_approval.csv
tool_url_map = {}
with open('content_approval.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        if len(row) < 4: continue
        tool_name = row[1].strip().lower() if row[1] else ''
        draft_file = row[2].strip() if row[2] else ''
        status = row[3].strip() if row[3] else ''
        
        if status == 'Published' and draft_file:
            # Derive slug from filename (e.g. Granola_AI_2026-03-28.md -> granola-ai-review)
            slug = os.path.basename(draft_file).replace('.md','').lower()
            slug = re.sub(r'_\d{4}-\d{2}-\d{2}$', '', slug)
            slug = slug.replace('_', '-')
            url = f"https://biztoolzai.com/blog/{slug}-review"
            tool_url_map[tool_name] = url

print("Published tool URL map:")
for k, v in tool_url_map.items():
    print(f"  {k}: {v}")
