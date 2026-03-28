#!/usr/bin/env python3
"""
Post-processes reddit_leads.md to replace [INSERT X REVIEW LINK] 
with actual published URLs - derived from actual blog HTML files
"""
import os, csv, re, glob

BASE_URL = "https://biztoolzai.com/blog"

# Build tool -> URL map from ACTUAL html files in blog/
html_files = glob.glob('blog/*.html')
html_url_map = {}
for f in html_files:
    basename = os.path.basename(f).replace('.html', '')
    if basename in ('index',): continue
    # Extract tool name from filename (e.g. munch-ai-review -> munch ai)
    tool_key = basename.replace('-review', '').replace('-', ' ').strip()
    html_url_map[tool_key] = f"{BASE_URL}/{basename}"

# Also build from content_approval.csv for cross-referencing tool name -> html file
tool_url_map = {}
with open('content_approval.csv', 'r') as f:
    for row in csv.reader(f):
        if len(row) < 4: continue
        tool_name = row[1].strip().lower()
        draft_file = row[2].strip()
        status = row[3].strip()
        if status == 'Published' and draft_file and tool_name:
            # Find matching html file
            for html_key, url in html_url_map.items():
                # Match if tool name words appear in html key
                tool_words = tool_name.replace(' ai','').replace(' io','').strip()
                if tool_words in html_key or html_key in tool_words:
                    tool_url_map[tool_name] = url
                    break

# Merge both maps
for k, v in html_url_map.items():
    if k not in tool_url_map:
        tool_url_map[k] = v

print("URL map built:")
for k, v in sorted(tool_url_map.items()):
    print(f"  {k}: {v}")

def find_url(tool_hint):
    hint = tool_hint.lower().strip()
    hint_clean = hint.replace(' ai','').replace(' io','').strip()
    # Try direct match
    if hint in tool_url_map: return tool_url_map[hint]
    if hint_clean in tool_url_map: return tool_url_map[hint_clean]
    # Try partial match
    for key, url in tool_url_map.items():
        key_clean = key.replace(' ai','').replace(' io','').strip()
        if hint_clean in key_clean or key_clean in hint_clean:
            return url
    return None

# Read and update reddit leads
with open('content/reddit_leads.md', 'r') as f:
    content = f.read()

pattern = r'\[INSERT\s+(.+?)\s+REVIEW\s+LINK\]'
replacements = 0

def replace_link(match):
    global replacements
    tool_hint = match.group(1)
    url = find_url(tool_hint)
    if url:
        replacements += 1
        return f"[{tool_hint} Full Review]({url})"
    return f"[{tool_hint} Review — Coming Soon](https://biztoolzai.com/blog/)"

content = re.sub(pattern, replace_link, content, flags=re.IGNORECASE)

# Also fix any already-injected wrong URLs
content = content.replace('](https://biztoolzai.com/blog/munch-review)', '](https://biztoolzai.com/blog/munch-ai-review)')

with open('content/reddit_leads.md', 'w') as f:
    f.write(content)

print(f"\n✅ {replacements} URLs injected")
