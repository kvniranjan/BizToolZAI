import sys, os, re, csv

# 1. Read the draft
draft_path = "content/CustomGPT.ai_2026-05-03.md"
with open(draft_path, "r") as f:
    md_content = f.read()

# Parse MD
title_match = re.search(r'\*\*Title:\*\*\s*(.+)$', md_content, re.MULTILINE)
title = title_match.group(1).strip() if title_match else "CustomGPT.ai Review 2026"

meta_match = re.search(r'\*\*Meta Description:\*\*\s*(.+)$', md_content, re.MULTILINE)
meta = meta_match.group(1).strip() if meta_match else ""

body_match = re.search(r'## Review Body(.*?)## Social Content', md_content, re.DOTALL)
body_md = body_match.group(1).strip() if body_match else md_content

# Convert body MD to HTML
html_body = ""
lines = body_md.split('\n')
in_list = False
for line in lines:
    line = line.strip()
    if not line:
        continue
    if line.startswith('### '):
        if in_list: html_body += "</ul>\n"; in_list = False
        html_body += f'<h3 class="text-2xl font-bold mt-8 mb-4">{line[4:]}</h3>\n'
    elif line.startswith('- '):
        if not in_list: html_body += '<ul class="list-disc pl-6 mb-4">\n'; in_list = True
        html_body += f'<li class="mb-2">{line[2:]}</li>\n'
    else:
        if in_list: html_body += "</ul>\n"; in_list = False
        html_body += f'<p class="mb-4">{line}</p>\n'
if in_list: html_body += "</ul>\n"

html_body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_body)
html_body = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_body)

slug = "customgpt-ai-2026-05-03"
html_file = f"blog/{slug}.html"
logo_domain = "customgpt.ai"

# Tailwind template
html_page = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta}">
    <title>{title} | BizToolz AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #F8FAFC; color: #020617; }}
    </style>
</head>
<body class="antialiased min-h-screen">
    <div class="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <a href="/blog/" class="text-blue-600 hover:text-blue-800 text-sm mb-8 inline-block font-semibold">&larr; Back to Blog</a>
        
        <div class="bg-white rounded-3xl p-8 sm:p-12 shadow-sm border border-gray-200">
            <div class="flex items-center gap-4 mb-8">
                <img src="https://logo.clearbit.com/{logo_domain}?size=128" class="w-16 h-16 rounded-xl border border-gray-100 shadow-sm" alt="CustomGPT.ai Logo">
                <div>
                    <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">{title}</h1>
                    <p class="text-gray-500 mt-2 text-sm font-medium">Published on May 3, 2026</p>
                </div>
            </div>
            
            <article class="prose prose-lg prose-blue max-w-none text-gray-700">
                {html_body}
            </article>
        </div>
    </div>
</body>
</html>"""

with open(html_file, "w") as f:
    f.write(html_page)

# Update blog/index.html
with open("blog/index.html", "r") as f:
    blog_idx = f.read()

card_html = f"""
            <a href="{slug}.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Founders</span>
                    <img src="https://logo.clearbit.com/{logo_domain}?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="CustomGPT.ai Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">{title}</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">{meta}</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 4 min read</span>
                    <span>🚀 New</span>
                </div>
            </a>
"""

if '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">' in blog_idx:
    blog_idx = blog_idx.replace('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">', '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">\n' + card_html)
    with open("blog/index.html", "w") as f:
        f.write(blog_idx)

# Hub & Spoke: Update /use-cases/ai-for-founders.html
hub_path = "use-cases/ai-for-founders.html"
with open(hub_path, "r") as f:
    hub_idx = f.read()

hub_card_html = f"""
            <a href="/blog/{slug}.html" class="bg-white border border-gray-200 p-6 rounded-2xl shadow-sm hover:shadow-md transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-blue-600 uppercase tracking-wider">Custom AI Bots</span>
                    <img src="https://logo.clearbit.com/{logo_domain}?size=64" class="w-10 h-10 rounded-md border border-gray-100" alt="CustomGPT.ai Logo">
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">{title}</h3>
                <p class="text-gray-600 text-sm mb-6 flex-grow">{meta}</p>
            </a>
"""

if '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">' in hub_idx:
    hub_idx = hub_idx.replace('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">', '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">\n' + hub_card_html)
    with open(hub_path, "w") as f:
        f.write(hub_idx)

# Update CSV
csv_file = 'content_approval.csv'
rows = []
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) >= 4 and 'CustomGPT.ai' in row[1]:
            row[3] = 'Published'
        rows.append(row)

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Publishing script completed.")