import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

WORKSPACE = "/root/.openclaw/workspace"

with open(f"{WORKSPACE}/youtube_token.json") as f:
    tok = json.load(f)

creds = Credentials(token=tok["token"], refresh_token=tok["refresh_token"],
    token_uri=tok["token_uri"], client_id=tok["client_id"],
    client_secret=tok["client_secret"], scopes=tok["scopes"])

if creds.expired:
    creds.refresh(Request())

yt = build("youtube", "v3", credentials=creds)

channel_res = yt.channels().list(part="id", mine=True).execute()
channel_id = channel_res['items'][0]['id']

response = yt.commentThreads().list(
    part="snippet",
    allThreadsRelatedToChannelId=channel_id,
    maxResults=20,
    order="time"
).execute()

print("RECENT COMMENTS:")
for item in response.get("items", []):
    comment = item["snippet"]["topLevelComment"]["snippet"]
    print(f"[{comment['authorDisplayName']}]: {comment['textDisplay']}")
