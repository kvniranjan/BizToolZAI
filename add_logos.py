import os
import re

domain_map = {
    'partnero-review.html': 'partnero.com',
    'munch-ai-review.html': 'getmunch.com',
    'reclaim-ai-review.html': 'reclaim.ai',
    'seedance-capcut-review.html': 'capcut.com',
    'lovable-dev-review.html': 'lovable.dev',
    'homesage-review.html': 'homesage.ai',
    'answrr-ai-receptionist-review.html': 'tryanswrr.com',
    'kling-ai-review.html': 'klingai.com',
    'wavespeed-ai-review.html': 'wavespeed.ai',
    'heygen-ai-avatar-review.html': 'heygen.com',
    'jasper-ai-review.html': 'jasper.ai',
    'granola-ai-review.html': 'granola.so',
}

# Update Blog Index
index_path = 'blog/index.html'
with open(index_path, 'r') as f:
    index_html = f.read()

def replacer(match):
    full_a_tag = match.group(0)
    href = match.group(1)
    
    if href in domain_map and 'logo.clearbit.com' not in full_a_tag:
        domain = domain_map[href]
        
        # Replace the span tracking-wider mb-2 with the flex container
        def span_replacer(span_match):
            inner_span = span_match.group(0).replace(' mb-2', '')
            return f'''<div class="flex items-center justify-between mb-3">
                    {inner_span}
                    <img src="https://logo.clearbit.com/{domain}?size=64" onerror="this.style.display='none'" class="w-8 h-8 rounded-md shadow-sm border border-border object-cover" alt="Logo">
                </div>'''
                
        # Regex to find the category span
        new_a_tag = re.sub(r'<span class="text-xs font-bold text-primary uppercase tracking-wider mb-2">.*?</span>', span_replacer, full_a_tag, count=1)
        return new_a_tag
    return full_a_tag

new_index_html = re.sub(r'<a href="([^"]+\.html)".*?</a>', replacer, index_html, flags=re.DOTALL)

with open(index_path, 'w') as f:
    f.write(new_index_html)

# Update Individual Blog Posts
for filename in os.listdir('blog'):
    if filename.endswith('.html') and filename != 'index.html':
        if filename in domain_map:
            domain = domain_map[filename]
            filepath = os.path.join('blog', filename)
            with open(filepath, 'r') as f:
                html = f.read()
            
            # Check if already added
            if 'logo.clearbit.com' not in html:
                # Find the H1 tag and insert the image right above it
                img_tag = f'<img src="https://logo.clearbit.com/{domain}?size=128" onerror="this.style.display=\'none\'" class="w-16 h-16 mx-auto mb-6 rounded-2xl shadow-sm border border-border object-cover" alt="Logo">\n            <h1'
                new_html = re.sub(r'<h1', img_tag, html, count=1)
                
                with open(filepath, 'w') as f:
                    f.write(new_html)

print("Logos added successfully!")
