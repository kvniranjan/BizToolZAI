import os
import re
import csv
import datetime

# 1. Read CSV and find today's entry
with open('content_approval.csv', 'r') as f:
    rows = list(csv.reader(f))

last_row = rows[-1]
date, tool, filename, status = last_row

if status in ["Reject", "Stop"]:
    print(f"Status is {status}. Exiting.")
    exit(0)

# 2. Read markdown
with open(filename, 'r') as f:
    md_content = f.read()

# 3. Extract title and meta description
title_match = re.search(r'# (.*)', md_content)
title = title_match.group(1) if title_match else f"{tool} Review"

meta_match = re.search(r'\*\*Meta Description:\*\* (.*)', md_content)
meta = meta_match.group(1) if meta_match else f"Review of {tool}"

# Remove title and meta from md_content for the body
body_md = re.sub(r'# .*\n', '', md_content, 1)
body_md = re.sub(r'\*\*Meta Description:\*\* .*\n', '', body_md, 1)

# Super simple MD to HTML for the specific format
html_body = body_md
html_body = re.sub(r'## (.*)', r'<h2 class="text-2xl font-bold mt-8 mb-4">\1</h2>', html_body)
html_body = re.sub(r'### (.*)', r'<h3 class="text-xl font-bold mt-6 mb-3">\1</h3>', html_body)
html_body = re.sub(r'- \*\*(.*?)\*\*(.*)', r'<li class="mb-2"><strong>\1</strong>\2</li>', html_body)
html_body = re.sub(r'(?m)^- (.*)', r'<li class="mb-2">\1</li>', html_body)
html_body = re.sub(r'(?s)(<li.*</li>)', r'<ul class="list-disc pl-6 mb-4">\n\1\n</ul>', html_body)
html_body = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_body)
html_body = html_body.replace('---', '<hr class="my-8 border-gray-200">')

paragraphs = html_body.split('\n\n')
final_html_body = []
for p in paragraphs:
    p = p.strip()
    if not p or p.startswith('<h') or p.startswith('<ul') or p.startswith('<hr'):
        final_html_body.append(p)
    else:
        final_html_body.append(f'<p class="mb-4">{p}</p>')
html_body = '\n'.join(final_html_body)

slug = f"{tool.lower().replace(' ', '-')}-2026-05-06"
html_filename = f"blog/{slug}.html"

# 4. Generate HTML
html_template = f"""<!DOCTYPE html>
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
                <img src="https://logo.clearbit.com/{tool.lower().replace(' ', '')}.ai?size=128" onerror="this.src='https://logo.clearbit.com/{tool.lower().replace(' ', '')}.com?size=128'" class="w-16 h-16 rounded-xl border border-gray-100 shadow-sm" alt="{tool} Logo">
                <div>
                    <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">{title}</h1>
                    <p class="text-gray-500 mt-2 text-sm font-medium">Published on May 6, 2026</p>
                </div>
            </div>
            
            <article class="prose prose-lg prose-blue max-w-none text-gray-700">
                {html_body}
            </article>
        </div>
    </div>
</body>
</html>"""

with open(html_filename, 'w') as f:
    f.write(html_template)

# 5. Update blog/index.html
with open('blog/index.html', 'r') as f:
    index_html = f.read()

card_html = f"""
            <a href="/{html_filename}" class="group block bg-white rounded-2xl p-6 shadow-sm border border-gray-200 hover:border-blue-500 hover:shadow-md transition-all">
                <div class="flex items-center gap-4 mb-4">
                    <img src="https://logo.clearbit.com/{tool.lower().replace(' ', '')}.ai?size=64" onerror="this.src='https://logo.clearbit.com/{tool.lower().replace(' ', '')}.com?size=64'" class="w-12 h-12 rounded-lg border border-gray-100" alt="{tool} Logo">
                    <h3 class="text-xl font-bold text-gray-900 group-hover:text-blue-600">{title}</h3>
                </div>
                <p class="text-gray-600 text-sm">{meta}</p>
            </a>
            <!-- NEW_BLOG_CARD -->"""

index_html = index_html.replace('<!-- NEW_BLOG_CARD -->', card_html)

with open('blog/index.html', 'w') as f:
    f.write(index_html)

# 6. Update Use Cases Hub (ai-for-content-creators.html)
use_case_file = 'use-cases/ai-for-content-creators.html'
with open(use_case_file, 'r') as f:
    use_case_html = f.read()

uc_card_html = f"""
            <a href="/{html_filename}" class="block bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md hover:border-blue-300 transition-all">
                <div class="flex items-center gap-3 mb-3">
                    <img src="https://logo.clearbit.com/{tool.lower().replace(' ', '')}.ai?size=64" onerror="this.src='https://logo.clearbit.com/{tool.lower().replace(' ', '')}.com?size=64'" class="w-10 h-10 rounded-lg" alt="{tool} Logo">
                    <h3 class="text-lg font-bold text-gray-900">{tool}</h3>
                </div>
                <p class="text-sm text-gray-600 mb-4">{meta}</p>
                <span class="text-blue-600 font-semibold text-sm">Read Review &rarr;</span>
            </a>
            <!-- NEW_USE_CASE_CARD -->"""

if '<!-- NEW_USE_CASE_CARD -->' in use_case_html:
    use_case_html = use_case_html.replace('<!-- NEW_USE_CASE_CARD -->', uc_card_html)
else:
    # Just append before the last closing div/main if possible, or append at the end
    print("Warning: <!-- NEW_USE_CASE_CARD --> not found in use cases hub.")

with open(use_case_file, 'w') as f:
    f.write(use_case_html)

# 7. Update CSV
rows[-1][3] = "Published"
with open('content_approval.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Successfully processed {tool}.")
