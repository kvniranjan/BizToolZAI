#!/usr/bin/env python3
"""
Weekly YouTube Performance Review
Runs every Sunday at 10 AM UTC.
Analyzes video performance and generates actionable recommendations.
"""
import json, os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

WORKSPACE = "/root/.openclaw/workspace"
# Key loaded from config.py

with open(f"{WORKSPACE}/youtube_token.json") as f:
    tok = json.load(f)

creds = Credentials(token=tok["token"], refresh_token=tok["refresh_token"],
    token_uri=tok["token_uri"], client_id=tok["client_id"],
    client_secret=tok["client_secret"], scopes=tok["scopes"])
if creds.expired:
    creds.refresh(Request())

yt = build("youtube","v3",credentials=creds)

# Get channel stats
ch = yt.channels().list(part="statistics,snippet", mine=True).execute()
ch_stats = ch["items"][0]["statistics"]

# Get all videos
search = yt.search().list(part="snippet", forMine=True, type="video", maxResults=20).execute()
videos = []
for v in search.get("items", []):
    vid_id = v["id"]["videoId"]
    vs = yt.videos().list(part="statistics,snippet", id=vid_id).execute()
    if vs["items"]:
        item = vs["items"][0]
        videos.append({
            "title": item["snippet"]["title"],
            "published": item["snippet"]["publishedAt"][:10],
            "views": int(item["statistics"].get("viewCount", 0)),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0)),
        })

videos.sort(key=lambda x: x["views"], reverse=True)

# Ask Gemini for analysis
import requests
video_data = "\n".join([f"- {v['title']} | Views: {v['views']} | Likes: {v['likes']} | Published: {v['published']}" for v in videos])

prompt = f"""You are a YouTube growth strategist for "Obscured History" — a dark history/mystery Shorts channel.

Channel stats:
- Subscribers: {ch_stats.get('subscriberCount', 0)}
- Total views: {ch_stats.get('viewCount', 0)}
- Videos: {ch_stats.get('videoCount', 0)}

Video performance (last 20 videos):
{video_data}

Analyze the data and provide:
1. Top 3 best-performing videos and WHY they worked
2. Bottom 3 worst-performing videos and WHY they underperformed
3. 3 specific, actionable recommendations to increase views this week
4. Suggested topic angles based on what's working

Be specific, data-driven, and actionable. Keep it concise."""

r = requests.post(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}",
    headers={"Content-Type":"application/json"},
    json={"contents":[{"parts":[{"text":prompt}]}]}
)
analysis = r.json()["candidates"][0]["content"]["parts"][0]["text"]

report = f"""📊 *Obscured History — Weekly Performance Review*
_{datetime.now().strftime('%B %d, %Y')}_

*Channel Overview:*
👥 Subscribers: {ch_stats.get('subscriberCount', 0)}
👁 Total Views: {ch_stats.get('viewCount', 0)}
🎬 Videos: {ch_stats.get('videoCount', 0)}

*Top Video This Week:*
🏆 {videos[0]['title'] if videos else 'N/A'}
👁 {videos[0]['views'] if videos else 0} views

---
{analysis}
---
_Weekly review by Ravi ☀️_"""

with open(f"{WORKSPACE}/pending_notification.json", "w") as f:
    json.dump({"message": report, "type": "weekly_review"}, f)

print("✅ Weekly review complete")
print(report)
