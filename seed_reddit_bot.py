import subprocess

# Let's seed the videos to Reddit to force initial traffic and jumpstart the algorithm
videos = [
    {"title": "BNPL: The Broke Economist EXPOSES The Lie", "url": "https://www.youtube.com/shorts/gUeB6yDEqDo"},
    {"title": "Your Savings Account Is a SCAM!", "url": "https://www.youtube.com/shorts/aaTt0g9NngY"},
    {"title": "Inflation: Government's Stealth Tax Scam", "url": "https://www.youtube.com/shorts/XYElclaljUU"},
    {"title": "Budgeting Is A Scam: Blame Corporate Greed!", "url": "https://www.youtube.com/shorts/7-Kv_7sR5vw"}
]

print("Triggering Reddit Injector to seed initial traffic...")
with open('/root/.openclaw/workspace/content/broke_economist/reddit_queue.txt', 'a') as f:
    for v in videos:
        f.write(f"{v['title']} - {v['url']}\n")

# Run the injector
subprocess.run(["/root/.openclaw/workspace/venv/bin/python3", "/root/.openclaw/workspace/reddit_url_injector.py"], timeout=120)
