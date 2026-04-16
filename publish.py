import os
import csv
import subprocess
import re

csv_path = 'content_approval.csv'
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

last_row = rows[-1]
date, tool_name, md_path, status = last_row[0], last_row[1], last_row[2], last_row[3]

if status in ["Auto-Queue", "Approve"]:
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    slug = tool_name.lower().replace(" ", "-")

    title_match = re.search(r'## SEO Title\n(.*?)\n', md_content)
    title = title_match.group(1).strip() if title_match else f"{tool_name} Review"

    meta_match = re.search(r'## Meta Description\n(.*?)\n', md_content)
    meta_desc = meta_match.group(1).strip() if meta_match else ""

    body_match = re.search(r'## Review Body\n(.*?)(?:\n---|\n##)', md_content, re.DOTALL)
    body_md = body_match.group(1).strip() if body_match else ""

    body_html = body_md.replace("\n\n", "</p>\n<p>")
    body_html = f"<p>{body_html}</p>"
    body_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', body_html)
    body_html = re.sub(r'- (.*?)(?=\n|$)', r'<li>\1</li>', body_html)
    body_html = re.sub(r'(<li>.*?</li>\n?)+', lambda m: f"<ul>\n{m.group(0)}</ul>\n", body_html)

    logo_url = f"https://logo.clearbit.com/{slug}.com?size=128"

    html_template = f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{meta_desc}">
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
        <img src="{logo_url}" alt="{tool_name} Logo" class="mb-8 rounded-xl shadow-sm">
        <div class="prose prose-lg max-w-none">
            {body_html}
        </div>
    </main>
</body>
</html>"""

    with open(f"blog/{slug}.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    # blog/index.html
    with open("blog/index.html", "r", encoding="utf-8") as f:
        blog_idx = f.read()
    new_link = f'<li class="mb-2"><a href="/blog/{slug}.html" class="text-blue-600 hover:underline">{tool_name} Review</a></li>'
    if '<ul' in blog_idx:
        blog_idx = re.sub(r'(<ul[^>]*>)', r'\1\n        ' + new_link, blog_idx, count=1)
    with open("blog/index.html", "w", encoding="utf-8") as f:
        f.write(blog_idx)

    # use-cases/ai-for-video-creators.html
    use_case_path = "use-cases/ai-for-video-creators.html"
    with open(use_case_path, "r", encoding="utf-8") as f:
        uc_html = f.read()
    card_html = f"""
    <div class="bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow">
        <img src="{logo_url}" alt="{tool_name}" class="w-12 h-12 rounded-lg mb-4">
        <h3 class="text-xl font-bold mb-2">{tool_name}</h3>
        <p class="text-slate-600 mb-4 text-sm">{meta_desc}</p>
        <a href="/blog/{slug}.html" class="text-primary font-medium hover:underline">Read Review →</a>
    </div>"""
    if '<div class="grid' in uc_html:
        uc_html = re.sub(r'(<div class="grid[^>]*>)', r'\1\n' + card_html, uc_html, count=1)
    with open(use_case_path, "w", encoding="utf-8") as f:
        f.write(uc_html)

    # Git
    subprocess.run(["git", "add", "blog/", "use-cases/", "content_approval.csv"])
    subprocess.run(["git", "commit", "-m", f"Publish {tool_name} + Update Hubs"])
    subprocess.run(["git", "push", "origin", "main"])

    # Update CSV
    rows[-1][3] = "Published"
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"🚀 Published: {tool_name} to biztoolzai.com and routed to Use-Case Hubs.")
