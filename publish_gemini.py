import os
import re
import markdown

with open('content/BigTech_Update_20260324.md', 'r') as f:
    md_content = f.read()

# Convert markdown to html
html_content = markdown.markdown(md_content)

# Clean up h1 from markdown to use in template
html_content = re.sub(r'<h1>(.*?)</h1>', '', html_content)

TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
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
        .article-content img {{ border-radius: 0.75rem; border: 1px solid #E2E8F0; }}
        .article-content h2 {{ margin-top: 2rem; color: #020617; font-weight: 700; }}
        .article-content h3 {{ margin-top: 1.5rem; color: #334155; font-weight: 600; }}
    </style>
    
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-2YNJ0HMCDY"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-2YNJ0HMCDY');
    </script>
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
                    <a href="/use-cases/" class="text-muted-foreground hover:text-primary font-medium transition-colors">Use Cases</a>
                    <a href="/blog/" class="text-muted-foreground hover:text-primary font-medium transition-colors">Reviews</a>
                    <a href="/#newsletter" class="bg-primary hover:bg-primary-hover text-white px-5 py-2 rounded-full font-medium transition-colors shadow-sm">Get Updates</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Article Header -->
    <main class="pt-32 pb-16 max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="mb-10 text-center">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-primary border border-blue-100 text-xs font-bold uppercase tracking-wider mb-4">
                {cat} • {date}
            </div>
            <img src="https://logo.clearbit.com/google.com?size=128" onerror="this.style.display='none'" class="w-16 h-16 mx-auto mb-6 rounded-2xl shadow-sm border border-border object-cover" alt="Logo">
            <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-foreground mb-6 leading-tight">{h1}</h1>
            <p class="text-xl text-muted-foreground">{sub}</p>
        </div>

        <!-- Article Content -->
        <article class="prose prose-slate prose-lg max-w-none prose-headings:font-bold prose-a:text-primary hover:prose-a:text-primary-hover bg-white p-8 sm:p-12 rounded-2xl shadow-sm border border-border">
            {content}
        </article>
    </main>

    <!-- Newsletter -->
    <section id="newsletter" class="py-20 bg-background border-t border-border">
        <div class="max-w-3xl mx-auto px-4 text-center">
            <h2 class="text-2xl font-bold mb-4 tracking-tight">Stay Ahead of the Curve.</h2>
            <p class="text-muted-foreground mb-8">Join 1,000+ professionals getting the absolute best AI tools delivered every week.</p>
            <form class="newsletter-form flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
                <input type="email" name="email" placeholder="Enter your work email" required class="flex-grow px-4 py-3 rounded-xl border border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent">
                <button type="submit" class="bg-primary hover:bg-primary-hover text-white font-semibold py-3 px-6 rounded-xl transition-colors whitespace-nowrap">Subscribe</button>
            </form>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white py-12 border-t border-border">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="flex items-center gap-2">
                <span class="text-xl">⚡</span>
                <span class="font-bold tracking-tight text-foreground">BizToolz AI</span>
            </div>
            <p class="text-muted-foreground text-sm">© 2026 BizToolz AI. All rights reserved.</p>
            <div class="flex gap-6 text-sm font-medium">
                <a href="../privacy-policy.html" class="text-muted-foreground hover:text-foreground transition-colors">Privacy</a>
                <a href="../affiliate-disclosure.html" class="text-muted-foreground hover:text-foreground transition-colors">Affiliate Disclosure</a>
            </div>
        </div>
    </footer>

    <script type="module" src="../js/main.js"></script>
</body>
</html>
"""

final_html = TEMPLATE.format(
    title="Google Gemini 3.1 Pro Review: The Agentic Shift — BizToolz AI",
    desc="Google just dropped Gemini 3.1 Pro and Flash-Lite. Here is why Business Analysts and Founders need to pay attention to agentic workflows.",
    cat="Big Tech AI",
    date="March 2026",
    h1="Google's New Gemini 3.1 Pro Is Here to Do Your Job",
    sub="Google just dropped Gemini 3.1 Pro and Flash-Lite. Here is why Business Analysts and Founders need to pay attention to \"agentic workflows\".",
    content=html_content
)

with open('blog/gemini-3-1-update.html', 'w') as f:
    f.write(final_html)

# Update blog index
with open('blog/index.html', 'r') as f:
    index_html = f.read()

card_html = """
            <a href="gemini-3-1-update.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Big Tech AI</span>
                    <img src="https://logo.clearbit.com/google.com?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">Google Gemini 3.1 Pro: The Agentic Shift</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">Google drops Gemini 3.1 Pro and Flash-Lite. What this means for Founders and Business Analysts.</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 4 min read</span>
                    <span>🚨 Breaking</span>
                </div>
            </a>
"""

# Insert right after the opening of the grid
index_html = index_html.replace('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">', '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">\n' + card_html)

with open('blog/index.html', 'w') as f:
    f.write(index_html)

# Update founders hub
with open('use-cases/ai-for-founders.html', 'r') as f:
    founders_html = f.read()

hub_card = """
            <a href="/blog/gemini-3-1-update.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Big Tech AI</span>
                    <img src="https://logo.clearbit.com/google.com?size=64" onerror="this.style.display='none'" class="w-10 h-10 rounded-lg shadow-sm border border-border object-cover" alt="Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">Google Gemini 3.1 Pro</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">Google's new agentic workflows explained for lean startup teams and founders.</p>
                <div class="flex justify-between items-center text-sm font-semibold text-primary pt-4 border-t border-border">
                    <span>Read Breakdown &rarr;</span>
                </div>
            </a>
"""

founders_html = founders_html.replace('<div class="grid grid-cols-1 md:grid-cols-2 gap-8">', '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">\n' + hub_card)

with open('use-cases/ai-for-founders.html', 'w') as f:
    f.write(founders_html)

# Update sitemap
with open('sitemap.xml', 'r') as f:
    sitemap = f.read()
    
new_sitemap_entry = """    <url>
        <loc>https://biztoolzai.com/blog/gemini-3-1-update.html</loc>
        <lastmod>2026-03-24</lastmod>
        <priority>0.8</priority>
    </url>
</urlset>"""

sitemap = sitemap.replace('</urlset>', new_sitemap_entry)
with open('sitemap.xml', 'w') as f:
    f.write(sitemap)

print("Gemini update published successfully!")
