import os
import re

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
        /* Clean up old styles inside content */
        .article-content img {{ border-radius: 0.75rem; border: 1px solid #E2E8F0; }}
        .article-content h2 {{ margin-top: 2rem; color: #020617; font-weight: 700; }}
        .article-content h3 {{ margin-top: 1.5rem; color: #334155; font-weight: 600; }}
        .article-content .cta-box, .article-content .verdict-box {{ background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 1rem; padding: 2rem; margin: 2rem 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
    </style>
    
    {schemas}
    
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
                    <a href="/blog/" class="text-primary font-medium transition-colors">Reviews</a>
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
            <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-foreground mb-6 leading-tight">{h1}</h1>
            <p class="text-xl text-muted-foreground">{sub}</p>
        </div>

        <!-- Article Content -->
        <article class="prose prose-slate prose-lg max-w-none prose-headings:font-bold prose-a:text-primary hover:prose-a:text-primary-hover">
            {content}
        </article>
    </main>

    <!-- Newsletter -->
    <section id="newsletter" class="py-20 bg-white border-y border-border">
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
    <footer class="bg-white py-12">
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

for f in os.listdir('blog'):
    if f.endswith('.html') and f != 'index.html':
        filepath = os.path.join('blog', f)
        with open(filepath, 'r', encoding='utf-8') as file:
            html = file.read()
            
        title_m = re.search(r'<title>(.*?)</title>', html)
        title = title_m.group(1) if title_m else "BizToolz AI"
        
        desc_m = re.search(r'<meta name="description" content="(.*?)">', html)
        desc = desc_m.group(1) if desc_m else ""
        
        schemas = "".join(re.findall(r'<script type="application/ld\+json">.*?</script>', html, re.DOTALL))
        
        h1_m = re.search(r'<h1>(.*?)</h1>', html)
        h1 = h1_m.group(1) if h1_m else title
        
        cat_m = re.search(r'<span class="article-category">(.*?)</span>', html)
        cat = cat_m.group(1) if cat_m else "Review"
        
        date_m = re.search(r'<span class="article-date">(.*?)</span>', html)
        date = date_m.group(1) if date_m else "2026"
        
        sub_m = re.search(r'<p class="article-subtitle">(.*?)</p>', html)
        sub = sub_m.group(1) if sub_m else ""
        
        # Try to extract just the main article content (ignore old wrappers)
        content_match = re.search(r'<div class="article-content">(.*?)</div>\s*</div>\s*</article>', html, re.DOTALL)
        if not content_match:
            # fallback if structure varies
            content_match = re.search(r'<div class="article-content">(.*?)</article>', html, re.DOTALL)
            
        content = content_match.group(1) if content_match else ""
        
        # Remove old TOC and Related Posts if they slipped in
        content = re.sub(r'<div class="toc">.*?</div>', '', content, flags=re.DOTALL)
        content = re.sub(r'<section class="related-posts">.*?</section>', '', content, flags=re.DOTALL)
        
        # Only rewrite if we found content
        if content.strip():
            new_html = TEMPLATE.format(
                title=title, desc=desc, schemas=schemas,
                h1=h1, cat=cat, date=date, sub=sub, content=content
            )
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(new_html)

print("All blog posts updated!")
