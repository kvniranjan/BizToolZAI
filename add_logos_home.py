import re

domain_map = {
    'lovable-dev-review.html': 'lovable.dev',
    'answrr-ai-receptionist-review.html': 'tryanswrr.com',
    'reclaim-ai-review.html': 'reclaim.ai'
}

with open('index.html', 'r') as f:
    html = f.read()

def replacer(match):
    full_a_tag = match.group(0)
    href = match.group(1)
    
    if href in domain_map and 'logo.clearbit.com' not in full_a_tag:
        domain = domain_map[href]
        
        # Replace the letter box with the img tag
        def icon_replacer(icon_match):
            return f'<img src="https://logo.clearbit.com/{domain}?size=128" onerror="this.style.display=\'none\'" class="w-12 h-12 rounded-xl shadow-sm border border-border object-cover mb-4" alt="Logo">'
                
        # Regex to find the <div class="w-12 h-12 ...">...</div>
        new_a_tag = re.sub(r'<div class="w-12 h-12[^>]+>.*?</div>', icon_replacer, full_a_tag, count=1, flags=re.DOTALL)
        return new_a_tag
    return full_a_tag

# Since index.html doesn't wrap the whole card in an <a> tag (it's a div containing an <a> tag), we need to adapt.
# Actually, let's just do simple string replacements for index.html manually since there are only 3.
html = re.sub(r'<div class="w-12 h-12 bg-pink-100 text-pink-600 rounded-xl flex items-center justify-center font-bold text-xl mb-4">L</div>', 
              r'<img src="https://logo.clearbit.com/lovable.dev?size=128" onerror="this.style.display=\'none\'" class="w-12 h-12 rounded-xl shadow-sm border border-border object-cover mb-4" alt="Lovable Logo">', html)

html = re.sub(r'<div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-xl flex items-center justify-center font-bold text-xl mb-4">A</div>', 
              r'<img src="https://logo.clearbit.com/tryanswrr.com?size=128" onerror="this.style.display=\'none\'" class="w-12 h-12 rounded-xl shadow-sm border border-border object-cover mb-4" alt="Answrr Logo">', html)

html = re.sub(r'<div class="w-12 h-12 bg-purple-100 text-purple-600 rounded-xl flex items-center justify-center font-bold text-xl mb-4">R</div>', 
              r'<img src="https://logo.clearbit.com/reclaim.ai?size=128" onerror="this.style.display=\'none\'" class="w-12 h-12 rounded-xl shadow-sm border border-border object-cover mb-4" alt="Reclaim Logo">', html)

with open('index.html', 'w') as f:
    f.write(html)

print("Home logos updated!")
