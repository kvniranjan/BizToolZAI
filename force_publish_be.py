import json
import os
import sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

VIDEO_PATH = "/root/.openclaw/workspace/content/broke_economist/v4_test/final_music.mp4"
JSON_PATH = "/root/.openclaw/workspace/content/broke_economist/v4_test/script.json"

if not os.path.exists(VIDEO_PATH):
    print(f"Error: {VIDEO_PATH} not found.")
    sys.exit(1)

with open(JSON_PATH, "r") as f:
    script_data = json.load(f)

print(f"Uploading {VIDEO_PATH} to YouTube...")
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

title = f"{script_data.get('title', 'The Broke Economist')} #Shorts"
if len(title) > 100:
    title = title[:90] + " #Shorts"

body = {
    "snippet": {
        "title": title,
        "description": f"{script_data.get('hook', '')}\n\n#finance #economics #money",
        "tags": ["finance", "economics", "money", "wealth"],
        "categoryId": "27"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    }
}

media_yt = MediaFileUpload(VIDEO_PATH, mimetype="video/mp4", resumable=True)
request = yt.videos().insert(part="snippet,status", body=body, media_body=media_yt)

print("Uploading...")
response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"Uploaded {int(status.progress() * 100)}%.")

yt_url = f"https://www.youtube.com/shorts/{response['id']}"
print(f"\n✅ YouTube Success: {yt_url}")
