import re

# Read Draft
with open('content/DeepbrainAI_2026-04-11.md', 'r') as f:
    draft = f.read()

# Parse draft
title_match = re.search(r'\*\*Title:\*\*\s*(.*)', draft)
meta_match = re.search(r'\*\*Meta Description:\*\*\s*(.*)', draft)
body_match = re.search(r'\*\*Review Body:\*\*\n(.*?)(\n\n##|\Z)', draft, re.DOTALL)

title = title_match.group(1).strip() if title_match else "Deepbrain AI Review"
meta = meta_match.group(1).strip() if meta_match else ""
body = body_match.group(1).strip() if body_match else ""

# Replace single newlines with spaces and double newlines with </p><p>
paragraphs = body.split('\n\n')
body_html = '<p>' + '</p>\n            <p>'.join(p.replace('\n', ' ').strip() for p in paragraphs) + '</p>'

html_template = f"""<!DOCTYPE html>
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
        <img src="https://logo.clearbit.com/deepbrain.io?size=128" alt="Deepbrain AI Logo" class="mb-8 rounded-xl shadow-sm">
        <div class="prose prose-lg max-w-none">
            {body_html}
        </div>
    </main>
</body>
</html>"""

with open('blog/deepbrain-ai.html', 'w') as f:
    f.write(html_template)

print("Created blog/deepbrain-ai.html")
