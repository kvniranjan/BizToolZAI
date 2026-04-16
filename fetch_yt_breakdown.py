import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

with open("/root/.openclaw/workspace/youtube_token.json") as f:
    t_yt = json.load(f)

creds_yt = Credentials(
    token=t_yt["token"], refresh_token=t_yt["refresh_token"],
    token_uri=t_yt["token_uri"], client_id=t_yt["client_id"],
    client_secret=t_yt["client_secret"], scopes=t_yt["scopes"]
)
if creds_yt.expired:
    creds_yt.refresh(Request())

yt = build("youtube", "v3", credentials=creds_yt)

request = yt.search().list(
    part="snippet",
    forMine=True,
    type="video",
    order="viewCount",  # Get most viewed to see what spiked
    maxResults=10
)
response = request.execute()

print("Top 10 Most Viewed Videos on Channel:")
for item in response.get('items', []):
    video_id = item['id']['videoId']
    title = item['snippet']['title']
    
    # Fetch exact view count for each
    stat_req = yt.videos().list(part="statistics", id=video_id)
    stat_res = stat_req.execute()
    
    if stat_res['items']:
        stats = stat_res['items'][0]['statistics']
        views = stats.get('viewCount', '0')
        print(f"- {title[:40]}... : {views} views")
