import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
from dateutil import parser

with open('/root/.openclaw/workspace/youtube_token.json') as f:
    t = json.load(f)

creds = Credentials(token=t['token'], refresh_token=t['refresh_token'],
    token_uri=t['token_uri'], client_id=t['client_id'],
    client_secret=t['client_secret'], scopes=t['scopes'])

if creds.expired:
    creds.refresh(Request())

yt = build('youtube','v3',credentials=creds)
ch = yt.channels().list(part='contentDetails', mine=True).execute()
uploads_playlist_id = ch['items'][0]['contentDetails']['relatedPlaylists']['uploads']

playlist_res = yt.playlistItems().list(part='snippet', playlistId=uploads_playlist_id, maxResults=50).execute()
video_ids = [item['snippet']['resourceId']['videoId'] for item in playlist_res.get('items', [])]

if video_ids:
    vs = yt.videos().list(part='statistics,snippet', id=','.join(video_ids)).execute()
    now = datetime.datetime.now(datetime.timezone.utc)
    for item in vs.get('items', []):
        view_count = int(item['statistics'].get('viewCount', 0))
        pub_time = parser.parse(item['snippet']['publishedAt'])
        age_hours = (now - pub_time).total_seconds() / 3600
        if view_count == 0 and age_hours > 24:
            print(f"DEAD VIDEO (>24h, 0 views): {item['snippet']['title']} (ID: {item['id']}, Age: {age_hours:.1f}h)")
