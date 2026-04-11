import re

with open('use-cases/ai-for-video-creators.html', 'r') as f:
    content = f.read()

card_html = """
            <a href="/blog/deepbrain-ai.html" class="bg-card border border-border p-6 rounded-2xl shadow-subtle hover:shadow-hover transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-4">
                    <span class="text-xs font-bold text-primary uppercase tracking-wider">Video Creators</span>
                    <img src="https://logo.clearbit.com/deepbrain.io?size=64" onerror="this.style.display='none'" class="w-10 h-10 rounded-lg shadow-sm border border-border object-cover" alt="Deepbrain AI Logo">
                </div>
                <h3 class="text-xl font-bold text-foreground mb-3 group-hover:text-primary transition-colors">Deepbrain AI Review 2026: The Best AI Video Generator?</h3>
                <p class="text-muted-foreground text-sm mb-6 flex-grow">Discover how Deepbrain AI can scale your video production with AI avatars and text-to-video capabilities.</p>
                <div class="flex justify-between items-center text-sm font-semibold text-primary pt-4 border-t border-border">
                    <span>Read Breakdown &rarr;</span>
                </div>
            </a>
"""

new_content = content.replace('<div class="grid grid-cols-1 md:grid-cols-2 gap-8">', '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">' + card_html)

with open('use-cases/ai-for-video-creators.html', 'w') as f:
    f.write(new_content)

print("Updated use-cases/ai-for-video-creators.html")
