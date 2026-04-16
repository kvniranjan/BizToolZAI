import re

file_path = '/root/.openclaw/workspace/broke_economist_daily_bytedance.py'

with open(file_path, 'r') as f:
    content = f.read()

new_reddit_injector = """
log("7. Pushing to External Traffic Sources (Reddit)...")
try:
    with open('/root/.openclaw/workspace/content/broke_economist/reddit_queue.txt', 'a') as rf:
        rf.write(f"{data.get('title')} - {yt_url}\\n")
    subprocess.run(["/root/.openclaw/workspace/venv/bin/python3", "/root/.openclaw/workspace/reddit_shorts_poster.py"], timeout=60)
except Exception as e:
    log(f"Failed to seed to reddit: {e}")
"""

content = content.replace('log(f"✅ YouTube Upload Success: {yt_url}")', f'log(f"✅ YouTube Upload Success: {{yt_url}}"){new_reddit_injector}')

with open(file_path, 'w') as f:
    f.write(content)

print("Reddit external traffic integration applied to main pipeline.")
