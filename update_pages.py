import os
import re

TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    
    <!-- Tailwind + Typography -->
    <script src="https://cdn.tailwindcss.com?plugins=typography"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    fontFamily: {{ sans: ['"Plus Jakarta Sans"', 'sans-serif'] }},
                    colors: {{
                        background: '#F8FAFC', foreground: '#020617',
                        primary: '#0369A1', 'primary-hover': '#0284c7',
                        secondary: '#334155', card: '#FFFFFF',
                        border: '#E2E8F0', success: '#059669', warning: '#F59E0B'
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ background-color: #F8FAFC; color: #020617; }}
        .glass-nav {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border-bottom: 1px solid #E2E8F0; }}
    </style>
</head>
<body class="antialiased font-sans bg-background">

    <!-- Navigation -->
    <nav class="glass-nav fixed w-full top-0 z-50 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex-shrink-0 flex items-center gap-2">
                    <span class="text-2xl">⚡</span>
                    <a href="/" class="font-bold text-xl tracking-tight text-foreground hover:text-primary transition-colors">BizToolz AI</a>
                </div>
                <div class="hidden md:flex space-x-8 items-center">
                    <a href="/#tools" class="text-muted-foreground hover:text-primary font-medium transition-colors">Top Tools</a>
                    <a href="/blog/" class="text-muted-foreground hover:text-primary font-medium transition-colors">Reviews</a>
                    <a href="/#newsletter" class="bg-primary hover:bg-primary-hover text-white px-5 py-2 rounded-full font-medium transition-colors shadow-sm">Get Updates</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Page Content -->
    <main class="pt-32 pb-16 max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-10 text-center">
            <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-foreground mb-6 leading-tight">{h1}</h1>
        </div>

        <article class="prose prose-slate prose-lg max-w-none prose-headings:font-bold prose-a:text-primary hover:prose-a:text-primary-hover bg-white p-8 sm:p-12 rounded-2xl shadow-sm border border-border">
            {content}
        </article>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-border py-12 mt-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="flex items-center gap-2">
                <span class="text-xl">⚡</span>
                <span class="font-bold tracking-tight text-foreground">BizToolz AI</span>
            </div>
            <p class="text-muted-foreground text-sm">© 2026 BizToolz AI. All rights reserved.</p>
            <div class="flex gap-6 text-sm font-medium">
                <a href="/privacy-policy.html" class="text-muted-foreground hover:text-foreground transition-colors">Privacy</a>
                <a href="/affiliate-disclosure.html" class="text-muted-foreground hover:text-foreground transition-colors">Affiliate Disclosure</a>
            </div>
        </div>
    </footer>

</body>
</html>
"""

pages = ['privacy-policy.html', 'affiliate-disclosure.html', 'contact.html', 'about.html', 'submit-tool.html']

for f in pages:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            html = file.read()
            
        title_m = re.search(r'<title>(.*?)</title>', html)
        title = title_m.group(1) if title_m else "BizToolz AI"
        
        h1_m = re.search(r'<h1>(.*?)</h1>', html)
        h1 = h1_m.group(1) if h1_m else title.split('—')[0].strip()
        
        # Try to extract content
        content_match = re.search(r'<div class="page-content">(.*?)</div>\s*</div>\s*</section>', html, re.DOTALL)
        if not content_match:
            # Fallbacks for different old templates
            content_match = re.search(r'<div class="legal-content">(.*?)</main>', html, re.DOTALL)
        if not content_match:
            content_match = re.search(r'<main.*?>(.*?)</main>', html, re.DOTALL)
            
        content = content_match.group(1) if content_match else ""
        
        # Clean up nested headers inside main if they match the h1
        content = re.sub(r'<h1.*?>.*?</h1>', '', content, count=1, flags=re.DOTALL)
        content = re.sub(r'<header.*?>.*?</header>', '', content, flags=re.DOTALL)
        
        if content.strip():
            new_html = TEMPLATE.format(
                title=title, h1=h1, content=content
            )
            
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_html)
            print(f"Updated {f}")

