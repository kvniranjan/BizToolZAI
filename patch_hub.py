import sys, os

slug = "synthesia-2026-05-02"
title = "Synthesia AI Video Generator Review 2026: Is It Worth It?"
meta = "Discover how Synthesia allows you to create professional AI videos from text in minutes. Read our full 2026 review to see if it's right for your business."

hub_path = "use-cases/ai-for-video-creators.html"
with open(hub_path, "r") as f:
    hub_idx = f.read()

hub_card_html = f"""
            <a href="/blog/{slug}.html" class="bg-white border border-gray-200 p-6 rounded-2xl shadow-sm hover:shadow-md transition-all group flex flex-col h-full">
                <div class="flex items-center justify-between mb-3">
                    <span class="text-xs font-bold text-blue-600 uppercase tracking-wider">Video Generation</span>
                    <img src="https://logo.clearbit.com/synthesia.io?size=64" class="w-10 h-10 rounded-md border border-gray-100" alt="Synthesia Logo">
                </div>
                <h3 class="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">{title}</h3>
                <p class="text-gray-600 text-sm mb-6 flex-grow">{meta}</p>
            </a>
"""

if '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">' in hub_idx:
    hub_idx = hub_idx.replace('<div class="grid grid-cols-1 md:grid-cols-2 gap-8">', '<div class="grid grid-cols-1 md:grid-cols-2 gap-8">\n' + hub_card_html)
    with open(hub_path, "w") as f:
        f.write(hub_idx)
    print("Hub updated")
else:
    print("Could not find grid")
