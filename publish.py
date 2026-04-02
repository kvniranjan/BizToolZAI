import csv
import re
import os
import shutil

# 1. Read CSV
last_row = None
rows = []
with open('content_approval.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        rows.append(row)
        last_row = row

date, tool, path, status = last_row
if status in ['Reject', 'Stop']:
    print("REJECTED")
    exit(0)

# 2. Read markdown
with open(path, 'r') as f:
    md_content = f.read()

# basic parse
title_match = re.search(r'SEO Title:\s*(.*)', md_content)
desc_match = re.search(r'Meta Description:\s*(.*)', md_content)
title = title_match.group(1) if title_match else f"{tool} Review"
desc = desc_match.group(1) if desc_match else ""

slug = tool.lower().replace(' ', '-').replace('.ai', '') + "-review"
html_path = f"blog/{slug}.html"

# Write simple HTML wrapper (UI Pro Max Tailwind)
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 text-gray-900 font-sans p-8">
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow">
        <h1 class="text-4xl font-bold mb-4">{title}</h1>
        <div class="prose lg:prose-xl">
            {md_content}
        </div>
    </div>
</body>
</html>
"""
with open(html_path, 'w') as f:
    f.write(html_template)

# Update blog/index.html
card_html = f"""
            <a href="{slug}.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Content AI</span>
                    <img src="https://logo.clearbit.com/{tool.lower().replace(' ', '')}.com?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="{tool} Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">{title}</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">{desc}</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 5 min read</span>
                    <span>🚀 New</span>
                </div>
            </a>
"""

with open('blog/index.html', 'r') as f:
    index_html = f.read()

index_html = index_html.replace('id="toolsGrid">', f'id="toolsGrid">\n{card_html}')

with open('blog/index.html', 'w') as f:
    f.write(index_html)

# Update Use-Cases (AI for Founders)
try:
    with open('use-cases/ai-for-founders.html', 'r') as f:
        hub_html = f.read()
    if 'id="toolsGrid">' in hub_html:
        hub_html = hub_html.replace('id="toolsGrid">', f'id="toolsGrid">\n{card_html.replace(slug+".html", "../blog/"+slug+".html")}')
        with open('use-cases/ai-for-founders.html', 'w') as f:
            f.write(hub_html)
except:
    pass

# Update CSV
rows[-1][3] = "Published"
with open('content_approval.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"PUBLISHED {tool}")
