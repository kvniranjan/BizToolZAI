import sys

with open("blog/index.html", "r") as f:
    content = f.read()

card_html = """
        <div class="mb-8">
            <a href="pictory-ai-2026-05-15.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center gap-4 mb-4">
                    <img src="https://logo.clearbit.com/pictory.ai?size=64" alt="Pictory Logo" class="w-12 h-12 rounded-lg border border-border shadow-sm group-hover:scale-105 transition-transform" onerror="this.style.display='none'">
                    <h3 class="text-xl font-bold text-foreground group-hover:text-primary transition-colors">Pictory AI Review (2026): Is It the Best AI Video Generator?</h3>
                </div>
                <p class="text-muted-foreground flex-grow mb-4">Discover how Pictory AI can turn your scripts and blog posts into high-quality videos in minutes. Read our full review and find out if it's worth the price in 2026.</p>
                <div class="mt-auto flex items-center text-primary font-semibold text-sm">
                    Read Review <span class="ml-1 group-hover:translate-x-1 transition-transform">→</span>
                </div>
            </a>
        </div>
"""

idx = content.find('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="toolsGrid">')
if idx != -1:
    insert_idx = content.find('>', idx) + 1
    new_content = content[:insert_idx] + card_html + content[insert_idx:]
    with open("blog/index.html", "w") as f:
        f.write(new_content)
    print("Done")
else:
    print("Not found")
