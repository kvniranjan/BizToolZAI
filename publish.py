import re
import datetime

# Read markdown
with open('content/Pictory_2026-04-17.md', 'r') as f:
    md = f.read()

# Extract Title and Meta Description
title_match = re.search(r'\*\*Title:\*\* (.*)', md)
meta_match = re.search(r'\*\*Meta Description:\*\* (.*)', md)

title = title_match.group(1) if title_match else "Pictory Review 2026"
meta = meta_match.group(1) if meta_match else ""

# Replace markdown with HTML
body = md.split('## Review Body')[1].split('## Social Content Drafts')[0]
# basic markdown to HTML for body
body_html = body.replace('\n\n', '</p>\n<p>').replace('**', '<strong>').replace('- **', '<li><strong>').replace('**:', '</strong>:')

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>{title}</title>
    <meta name="description" content="{meta}">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{ background-color: #F8FAFC; color: #020617; font-family: 'Plus Jakarta Sans', sans-serif; }}
    </style>
</head>
<body class="bg-gray-50 text-gray-900 font-sans p-8">
    <nav class="max-w-3xl mx-auto mb-8 flex items-center gap-4">
        <a href="/" class="text-blue-600 font-bold">← Back to Home</a>
        <a href="/blog/" class="text-blue-600 font-bold">← Back to Blog</a>
    </nav>
    <div class="max-w-3xl mx-auto bg-white p-8 rounded-2xl shadow">
        <div class="flex items-center gap-4 mb-6">
            <img src="https://logo.clearbit.com/pictory.ai?size=64" onerror="this.style.display='none'" class="w-16 h-16 rounded-md shadow-sm border border-gray-200 object-cover" alt="Pictory Logo">
            <h1 class="text-4xl font-bold">{title}</h1>
        </div>
        <div class="prose lg:prose-xl">
            <p>{body_html}</p>
        </div>
    </div>
</body>
</html>"""

with open('blog/pictory.html', 'w') as f:
    f.write(html)

