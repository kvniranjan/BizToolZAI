import re

file_path = '/root/.openclaw/workspace/broke_economist_daily.py'
with open(file_path, 'r') as f:
    content = f.read()

# Fix Voice ID
content = content.replace('VOICE_ID = "pNInz6obpgDQGcFmaJgB"', 'VOICE_ID = "JBFqnCBsd6RMkjVDRZzb" # George')

# Fix text extraction
old_extract = """            clean_text = re.sub(r'\\*\\*Audio.*?\\:\\*\\*\\s*', '', line).strip(' "')
            audio_lines.append(clean_text)"""

new_extract = """            clean_text = re.sub(r'\\*\\*Audio.*?\\:\\*\\*\\s*', '', line).strip(' "')
            # Strip remaining markdown asterisks so ElevenLabs doesn't read them
            clean_text = clean_text.replace('*', '').replace('#', '').strip()
            audio_lines.append(clean_text)"""

content = content.replace(old_extract, new_extract)

with open(file_path, 'w') as f:
    f.write(content)
print("Patched broke_economist_daily.py")
