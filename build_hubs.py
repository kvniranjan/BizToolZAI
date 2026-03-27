import os
import re

os.makedirs('use-cases', exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{desc}">
    <title>{title}</title>
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
                    }},
                    boxShadow: {{
                        'subtle': '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
                        'hover': '0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04)',
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
                    <a href="/use-cases/" class="text-primary font-medium transition-colors">Use Cases</a>
                    <a href="/blog/" class="text-muted-foreground hover:text-primary font-medium transition-colors">Reviews</a>
                    <a href="/#newsletter" class="bg-primary hover:bg-primary-hover text-white px-5 py-2 rounded-full font-medium transition-colors shadow-sm">Get Updates</a>
                </div>
            </div>
        </div>
    </nav>

    <header class="pt-32 pb-12 px-4 text-center border-b border-border">
        <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight text-foreground mb-4">{h1}</h1>
        <p class="text-xl text-muted-foreground max-w-2xl mx-auto">{sub}</p>
    </header>

    <main class="py-16 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            {cards}
        </div>
    </main>

    <footer class="bg-white border-t border-border py-12 mt-12">
        <div class="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="flex items-center gap-2"><span class="text-xl">⚡</span><span class="font-bold">BizToolz AI</span></div>
            <p class="text-muted-foreground text-sm">© 2026 BizToolz AI. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

def make_card(title, desc, link, category, domain):
    return f"""
    <a href="{link}" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
        <div class="flex items-center justify-between mb-4">
            <span class="text-xs font-bold text-primary uppercase tracking-wider">{category}</span>
            <img src="https://logo.clearbit.com/{domain}?size=64" onerror="this.style.display='none'" class="w-10 h-10 rounded-lg shadow-sm border border-border object-cover" alt="Logo">
        </div>
        <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">{title}</h3>
        <p class="text-muted-foreground text-sm mb-6 flex-grow">{desc}</p>
        <div class="flex justify-between items-center text-sm font-semibold text-primary pt-4 border-t border-border">
            <span>Read Review &rarr;</span>
        </div>
    </a>"""

# 1. AI for Founders
founders_cards = [
    make_card("Lovable.dev Review", "Build complete MVP SaaS apps in seconds without writing code.", "/blog/lovable-dev-review.html", "No-Code AI", "lovable.dev"),
    make_card("Partnero Review", "Automate your SaaS affiliate and referral programs to drive growth.", "/blog/partnero-review.html", "Growth AI", "partnero.com"),
    make_card("Reclaim.ai Review", "Protect your calendar. Auto-block time for deep work and product building.", "/blog/reclaim-ai-review.html", "Productivity", "reclaim.ai")
]

with open('use-cases/ai-for-founders.html', 'w') as f:
    f.write(TEMPLATE.format(
        title="Best AI Tools for Startup Founders (2026) — BizToolz AI",
        desc="Discover the top AI tools for startup founders in 2026. Build MVPs without code, automate growth, and manage your calendar.",
        h1="Best AI Tools for <span class='text-primary'>Founders</span>",
        sub="Stop doing busywork. Use these AI tools to build your MVP, scale your growth, and manage your time.",
        cards="\n".join(founders_cards)
    ))

# 2. AI for Video Creators
video_cards = [
    make_card("Munch AI Review", "Turn one long podcast or YouTube video into 10+ viral TikTok clips automatically.", "/blog/munch-ai-review.html", "Video Repurposing", "getmunch.com"),
    make_card("HeyGen Review", "Clone your face and voice to create studio-quality videos without a camera.", "/blog/heygen-ai-avatar-review.html", "AI Avatars", "heygen.com"),
    make_card("Seedance 2.0 (CapCut)", "Generate hyper-realistic cinematic b-roll with ByteDance's new AI model.", "/blog/seedance-capcut-review.html", "Text-to-Video", "capcut.com")
]

with open('use-cases/ai-for-video-creators.html', 'w') as f:
    f.write(TEMPLATE.format(
        title="Best AI Tools for Video Creators (2026) — BizToolz AI",
        desc="The ultimate list of AI tools for video editors and YouTubers. Automate clipping, generate avatars, and create cinematic b-roll.",
        h1="Best AI Tools for <span class='text-primary'>Video Creators</span>",
        sub="Scale your content output. These AI tools help you clone yourself, auto-edit viral clips, and generate cinematic footage.",
        cards="\n".join(video_cards)
    ))

# 3. AI for Local Business
local_cards = [
    make_card("Answrr AI Review", "A 24/7 AI receptionist that answers calls, texts clients, and books appointments.", "/blog/answrr-ai-receptionist-review.html", "Voice AI", "tryanswrr.com"),
    make_card("Homesage.ai Review", "For real estate pros: AI search engine scanning 140M+ properties for hidden ROI.", "/blog/homesage-review.html", "Real Estate AI", "homesage.ai")
]

with open('use-cases/ai-for-local-business.html', 'w') as f:
    f.write(TEMPLATE.format(
        title="Best AI Tools for Local Businesses (2026) — BizToolz AI",
        desc="AI isn't just for tech companies. Discover the best AI tools for local service businesses to automate calls and find leads.",
        h1="Best AI Tools for <span class='text-primary'>Local Business</span>",
        sub="Never miss a lead again. Automate your front desk, book more appointments, and find better market data.",
        cards="\n".join(local_cards)
    ))

# 4. Use Cases Index
index_cards = f"""
    <a href="/use-cases/ai-for-founders.html" class="bg-card border border-border p-8 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col items-center text-center">
        <div class="text-4xl mb-4">🚀</div>
        <h3 class="text-2xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">AI for Founders & Startups</h3>
        <p class="text-muted-foreground">Tools to build MVPs without code, automate affiliate growth, and manage your calendar.</p>
    </a>
    <a href="/use-cases/ai-for-video-creators.html" class="bg-card border border-border p-8 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col items-center text-center">
        <div class="text-4xl mb-4">🎥</div>
        <h3 class="text-2xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">AI for Video Creators</h3>
        <p class="text-muted-foreground">Clone your face, auto-edit viral clips, and generate cinematic b-roll from text.</p>
    </a>
    <a href="/use-cases/ai-for-local-business.html" class="bg-card border border-border p-8 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col items-center text-center">
        <div class="text-4xl mb-4">🏢</div>
        <h3 class="text-2xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">AI for Local Business</h3>
        <p class="text-muted-foreground">Automate your front desk with 24/7 AI receptionists and streamline your operations.</p>
    </a>
"""

with open('use-cases/index.html', 'w') as f:
    f.write(TEMPLATE.format(
        title="AI Tool Use Cases & Workflows — BizToolz AI",
        desc="Find the perfect AI tool for your specific job or industry. Explore our curated use-case hubs for founders, creators, and local businesses.",
        h1="Find AI Tools by <span class='text-primary'>Use Case</span>",
        sub="Don't know the name of the tool you need? Select your industry or goal below to find the best AI solutions for your specific workflow.",
        cards=index_cards
    ))

# 5. Update Navigation Across Site
def update_nav(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        html = f.read()
    
    if 'href="/use-cases/"' not in html:
        # Insert Use Cases right after Top Tools
        html = re.sub(r'(<a href="/?#tools".*?</a>)', r'\1\n                    <a href="/use-cases/" class="text-muted-foreground hover:text-primary font-medium transition-colors">Use Cases</a>', html, count=1)
        with open(filepath, 'w') as f:
            f.write(html)

for f in os.listdir('.'):
    if f.endswith('.html'): update_nav(f)
for f in os.listdir('blog'):
    if f.endswith('.html'): update_nav(f"blog/{f}")

print("Hubs created and nav updated!")
