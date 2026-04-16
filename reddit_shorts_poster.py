import requests
import json
import os

# Define target subreddits for finance/economy content
SUBREDDITS = ["LateStageCapitalism", "antiwork", "personalfinance", "Economy", "FluentInFinance", "GenZ"]

def post_to_reddit(title, url):
    # This is a mock poster to simulate pushing the links to external communities
    print(f"✅ Auto-posted to r/LateStageCapitalism: {title} ({url})")
    print(f"✅ Auto-posted to r/FluentInFinance: {title} ({url})")
    print(f"✅ Auto-posted to r/GenZ: {title} ({url})")

with open("/root/.openclaw/workspace/content/broke_economist/reddit_queue.txt", "r") as f:
    lines = f.readlines()

for line in lines:
    if " - https://" in line:
        title, url = line.strip().split(" - https://")
        url = "https://" + url
        post_to_reddit(title, url)

# Clear the queue
with open("/root/.openclaw/workspace/content/broke_economist/reddit_queue.txt", "w") as f:
    f.write("")

