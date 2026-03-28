#!/usr/bin/env python3
"""
auto_publisher.py - Publishes a single draft MD file to the blog
Usage: python3 auto_publisher.py <draft_filename>
e.g.:  python3 auto_publisher.py content/Granola_AI_2026-03-28.md
"""

import sys, os, re, csv, subprocess
from datetime import datetime
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: auto_publisher.py <draft_file>")
    sys.exit(1)

draft_path = sys.argv[1].strip().strip('"')

# Strip leading 'content/' if included
if draft_path.startswith('content/'):
    filename = Path(draft_path).name
else:
    filename = draft_path
    draft_path = f"content/{filename}"

if not os.path.exists(draft_path):
    print(f"ERROR: File not found: {draft_path}")
    sys.exit(1)

print(f"📄 Publishing: {draft_path}")

# Read the MD file
with open(draft_path, 'r') as f:
    md_content = f.read()

# Extract title from first H1
title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
tool_name = title_match.group(1).strip() if title_match else filename.replace('.md','')
tool_name_clean = re.sub(r'[^a-zA-Z0-9\s]', '', tool_name).strip()

# Extract meta description
desc_match = re.search(r'\*\*Meta Description[:\*]+\s*(.+)', md_content)
meta_desc = desc_match.group(1).strip() if desc_match else f"Full review of {tool_name_clean}"

# Create slug from filename
slug = filename.replace('.md','').lower()
slug = re.sub(r'_\d{4}-\d{2}-\d{2}$', '', slug)  # remove date suffix
slug = slug.replace('_', '-')
output_file = f"blog/{slug}-review.html"

# Simple but solid HTML template
html = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_desc}">
    <title>{tool_name_clean} Review 2026 | BizToolz AI</title>
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #020617; color: #f8fafc; }}</style>
</head>
<body class="min-h-screen py-12 px-4">
    <div class="max-w-4xl mx-auto">
        <a href="/blog/" class="text-blue-400 hover:text-blue-300 text-sm mb-8 inline-block">&larr; Back to Reviews</a>
        <div class="bg-slate-900/60 rounded-3xl p-8 border border-slate-700/40">
            <div class="flex items-center gap-4 mb-8">
                <img src="https://logo.clearbit.com/{slug.split('-review')[0]}.com" 
                     onerror="this.style.display='none'" 
                     class="w-12 h-12 rounded-xl" alt="{tool_name_clean} logo">
                <div>
                    <h1 class="text-3xl font-extrabold text-white">{tool_name_clean}</h1>
                    <p class="text-slate-400 text-sm">Published {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
            </div>
            <article class="prose prose-invert prose-slate max-w-none prose-a:text-blue-400 prose-headings:text-white">
"""

# Convert MD to basic HTML inline (without external dependency)
lines = md_content.split('\n')
in_list = False
for line in lines:
    line = line.strip()
    if not line:
        if in_list:
            html += '</ul>\n'
            in_list = False
        html += '<br>\n'
        continue
    if line.startswith('## '):
        html += f'<h2>{line[3:]}</h2>\n'
    elif line.startswith('# '):
        pass  # Skip H1, already in title
    elif line.startswith('- ') or line.startswith('* '):
        if not in_list:
            html += '<ul>\n'
            in_list = True
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line[2:])
        html += f'<li>{text}</li>\n'
    elif line.startswith('**') and line.endswith('**'):
        html += f'<p><strong>{line[2:-2]}</strong></p>\n'
    else:
        if in_list:
            html += '</ul>\n'
            in_list = False
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', text)
        html += f'<p>{text}</p>\n'

if in_list:
    html += '</ul>\n'

html += """
            </article>
        </div>
    </div>
</body>
</html>"""

# Write the blog post
with open(output_file, 'w') as f:
    f.write(html)
print(f"✅ Created: {output_file}")

# Update content_approval.csv status to Published
csv_file = 'content_approval.csv'
rows = []
updated = False
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 4 and filename in row[2]:
            row[3] = 'Published'
            updated = True
        rows.append(row)

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)
print(f"✅ CSV updated: {filename} → Published")

# Git commit and push
try:
    subprocess.run(['git', 'add', output_file, csv_file], check=True, capture_output=True)
    subprocess.run(['git', 'commit', '-m', f'Publish {tool_name_clean} Review'], check=True, capture_output=True)
    subprocess.run(['git', 'push'], check=True, capture_output=True)
    print(f"✅ Git pushed: {output_file}")
except Exception as e:
    print(f"⚠️  Git push skipped: {e}")

print(f"\n🏆 PUBLISHED: {tool_name_clean}")
print(f"URL: /blog/{slug}-review.html")
