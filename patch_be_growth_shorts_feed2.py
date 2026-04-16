import re

file_path = '/root/.openclaw/workspace/broke_economist_daily_bytedance.py'

with open(file_path, 'r') as f:
    content = f.read()

# Undo the Reddit injector since the existing script is for the blog
# Let's fix the subtitles logic. The stacking might break the SRT format if it creates empty lines.
# Actually, the standard Hormozi style is 2-3 words per line. We'll leave it as we had it but add an emoji.

content = content.replace('text_chunk = "\\n".join([w[\'word\'].strip() for w in chunk]) # Stack words for fast reading', 'text_chunk = " ".join([w[\'word\'].strip() for w in chunk])')

with open(file_path, 'w') as f:
    f.write(content)

print("Reverted to 2-3 words, avoided SRT breaking.")
