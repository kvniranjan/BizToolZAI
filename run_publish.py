import os
import csv
import re
from datetime import datetime

# 1. Read content_approval.csv
target_row = None
with open("content_approval.csv", "r") as f:
    lines = f.readlines()
    last_line = lines[-1].strip()
    parts = last_line.split(",")
    date = parts[0]
    tool_name = parts[1]
    draft_path = parts[2]
    status = parts[3]

if status in ["Reject", "Stop"]:
    print(f"Status is {status}, exiting.")
    exit(0)

# Read draft markdown
with open(draft_path, "r") as f:
    md_content = f.read()

# Extract Title and Meta Description
title_match = re.search(r'\*\*Title\*\*:\s*(.*)', md_content)
title = title_match.group(1).strip() if title_match else f"{tool_name} Review"

meta_match = re.search(r'\*\*Meta Description\*\*:\s*(.*)', md_content)
meta = meta_match.group(1).strip() if meta_match else "Review."

review_match = re.search(r'## Review Body\n(.*?)(?=\n##|$)', md_content, re.DOTALL)
review_body = review_match.group(1).strip() if review_match else ""

slug = "customers-ai"

# 3 & 4. Write new HTML to blog/customers-ai.html
html_content = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta}">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #F8FAFC; color: #020617; }}
        .glass-nav {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid #E2E8F0; }}
    </style>
</head>
<body class="antialiased font-sans">
    <nav class="glass-nav fixed w-full top-0 z-50 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex-shrink-0 flex items-center gap-2">
                    <span class="text-2xl">⚡</span>
                    <a href="/" class="font-bold text-xl tracking-tight text-foreground hover:text-primary transition-colors">BizToolz AI</a>
                </div>
                <div class="hidden md:flex space-x-8 items-center">
                    <a href="/#tools" class="text-muted-foreground hover:text-primary font-medium transition-colors">Top Tools</a>
                    <a href="/use-cases/" class="text-muted-foreground hover:text-primary font-medium transition-colors">Use Cases</a>
                    <a href="/blog/" class="text-primary font-medium transition-colors">Reviews</a>
                    <a href="#newsletter" class="bg-primary hover:bg-primary-hover text-white px-5 py-2 rounded-full font-medium transition-colors shadow-sm">Get Updates</a>
                </div>
            </div>
        </div>
    </nav>
    <main class="py-32 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 class="text-4xl font-bold mb-4">{title}</h1>
        <img src="https://logo.clearbit.com/customers.ai?size=128" alt="{tool_name} Logo" class="mb-8 rounded-xl shadow-sm">
        <div class="prose prose-lg max-w-none">
            <p>{review_body}</p>
        </div>
    </main>
</body>
</html>
"""

with open(f"blog/{slug}.html", "w") as f:
    f.write(html_content)

# 5. Update blog/index.html
with open("blog/index.html", "r") as f:
    blog_index = f.read()

card_html = f"""            <a href="{slug}.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Social Media</span>
                    <img src="https://logo.clearbit.com/customers.ai?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="{tool_name} Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">{title}</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">{meta.split('.')[0]}.</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 3 min read</span>
                    <span>🚀 New</span>
                </div>
            </a>\n"""

target = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">'
if target in blog_index:
    blog_index = blog_index.replace(target, target + "\n" + card_html)
    with open("blog/index.html", "w") as f:
        f.write(blog_index)

# 6. HUB & SPOKE ROUTING
with open("use-cases/ai-for-social-media.html", "r") as f:
    uc_html = f.read()

uc_card = f"""            <!-- CUSTOMERS.AI CARD -->
            <a href="/blog/{slug}.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Social Media AI</span>
                    <img src="https://logo.clearbit.com/customers.ai?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="{tool_name} Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">{tool_name}</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">{meta.split('.')[0]}.</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>Read Review &rarr;</span>
                </div>
            </a>\n"""

uc_target = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">'
if uc_target in uc_html:
    uc_html = uc_html.replace(uc_target, uc_target + "\n" + uc_card)
    with open("use-cases/ai-for-social-media.html", "w") as f:
        f.write(uc_html)

# Update CSV status to Published
lines[-1] = lines[-1].replace("Auto-Queue", "Published")
with open("content_approval.csv", "w") as f:
    f.writelines(lines)
print("done")
