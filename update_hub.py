import sys

with open("use-cases/ai-for-video-creators.html", "r") as f:
    content = f.read()

card_html = """
            <a href="/blog/pictory-ai-2026-05-15.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full bg-white">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Video Creators</span>
                    <img src="https://logo.clearbit.com/pictory.ai?size=64" onerror="this.style.display='none'" class="w-10 h-10 rounded-md shadow-sm border border-border object-cover" alt="Pictory Logo">
                </div>
                <h3 class="text-xl font-bold mb-2 group-hover:text-primary transition-colors">Pictory AI Review (2026): Is It the Best AI Video Generator?</h3>
                <p class="text-muted-foreground text-sm mb-4 line-clamp-3">Discover how Pictory AI can turn your scripts and blog posts into high-quality videos in minutes. Read our full review and find out if it's worth the price in 2026.</p>
            </a>"""

idx = content.find('<div class="grid grid-cols-1 md:grid-cols-2 gap-8">')
if idx != -1:
    insert_idx = content.find('>', idx) + 1
    new_content = content[:insert_idx] + card_html + content[insert_idx:]
    with open("use-cases/ai-for-video-creators.html", "w") as f:
        f.write(new_content)
    print("Done")
else:
    print("Not found")
