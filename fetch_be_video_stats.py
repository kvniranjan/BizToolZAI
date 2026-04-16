import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

with open("/root/.openclaw/workspace/youtube_token_be.json") as f:
    t_yt = json.load(f)

creds_yt = Credentials(
    token=t_yt["token"], refresh_token=t_yt["refresh_token"],
    token_uri=t_yt["token_uri"], client_id=t_yt["client_id"],
    client_secret=t_yt["client_secret"], scopes=t_yt["scopes"]
)
if creds_yt.expired:
    creds_yt.refresh(Request())

yt = build("youtube", "v3", credentials=creds_yt)

# First get all video IDs
search_response = yt.search().list(
    part="id",
    channelId="UCTwOMzjrdwFNx2bW7B2Nvcw",
    maxResults=50,
    type="video"
).execute()

video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]

if video_ids:
    stats_response = yt.videos().list(
        part="statistics,snippet,status",
        id=",".join(video_ids)
    ).execute()
    print(json.dumps(stats_response, indent=2))
else:
    print('{"items": []}')
