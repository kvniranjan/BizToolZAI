import re

file_path = '/root/.openclaw/workspace/broke_economist_daily_bytedance.py'

with open(file_path, 'r') as f:
    content = f.read()

# YouTube Shorts heavily relies on the title and description for its initial seed audience.
# We need to make sure the title explicitly contains #Shorts, and we need an aggressive CTA.
# Also, we should add some sound effects/music via ffmpeg or ensure the pacing is even faster.
# For now, let's inject a Reddit auto-post script to get initial views manually.

new_reddit_injector = """
log("7. Seeding Initial Views via Reddit...")
try:
    with open('/root/.openclaw/workspace/content/broke_economist/reddit_queue.txt', 'a') as rf:
        rf.write(f"{data.get('title')} - {yt_url}\\n")
    subprocess.run(["/root/.openclaw/workspace/venv/bin/python3", "/root/.openclaw/workspace/reddit_url_injector.py", yt_url], timeout=120)
except Exception as e:
    log(f"Failed to seed to reddit: {e}")
"""

if "7. Seeding Initial Views via Reddit..." not in content:
    content = content.replace('log(f"\\n✅ YouTube Success: {yt_url}")', f'log(f"\\n✅ YouTube Success: {{yt_url}}"){new_reddit_injector}')

# And let's make the caption generation group words tightly (1-2 words per line)
old_whisper = """        text_chunk = " ".join([w['word'].strip() for w in chunk])
        srt_lines.append(text_chunk.upper())
        srt_lines.append("")"""

new_whisper = """        text_chunk = "\\n".join([w['word'].strip() for w in chunk]) # Stack words for fast reading
        srt_lines.append(text_chunk.upper())
        srt_lines.append("")"""

content = content.replace(old_whisper, new_whisper)

with open(file_path, 'w') as f:
    f.write(content)

print("Applied Reddit seeding & hyper-fast 1-word caption stacking.")
