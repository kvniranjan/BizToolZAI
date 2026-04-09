with open("blog/index.html", "r") as f:
    lines = f.readlines()

new_card = """            <a href="predis-ai-review.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Social Media AI</span>
                    <img src="https://logo.clearbit.com/predis.ai?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="Predis.ai Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">Predis.ai Review: The Best AI Social Media Generator in 2026?</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">Discover how Predis.ai can automate your social media content creation. Read our full review of its features, pros, cons, and see if it's worth it in 2026.</p>
                <div class="flex justify-between items-center text-sm font-semibold text-secondary pt-4 border-t border-border">
                    <span>📖 5 min read</span>
                    <span>🚀 New</span>
                </div>
            </a>
"""

for i, line in enumerate(lines):
    if '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">' in line:
        lines.insert(i + 1, new_card)
        break

with open("blog/index.html", "w") as f:
    f.writelines(lines)
