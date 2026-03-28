import requests, json, os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load token
with open("youtube_token.json") as f:
    t = json.load(f)

creds = Credentials(
    token=t["token"],
    refresh_token=t["refresh_token"],
    token_uri=t["token_uri"],
    client_id=t["client_id"],
    client_secret=t["client_secret"],
    scopes=t["scopes"]
)

# Refresh if needed
if creds.expired:
    creds.refresh(Request())
    t["token"] = creds.token
    with open("youtube_token.json", "w") as f:
        json.dump(t, f)

youtube = build("youtube", "v3", credentials=creds)

VIDEO_FILE = "videos/final/dyatlov_premium.mp4"

body = {
    "snippet": {
        "title": "The Dyatlov Pass Incident: Russia's Unsolved Horror #Shorts",
        "description": """In 1959, 9 experienced hikers ventured into the frozen Dyatlov Pass in the Soviet mountains. They never returned.

Their tent was slashed open from the inside. Footprints leading barefoot into deadly snow. Catastrophic internal injuries with no external wounds. Traces of radiation on their clothing.

The Soviet government's conclusion: "A compelling unknown natural force."

Over 60 years later — no one knows what really happened.

🔔 Subscribe to Obscured History for more dark mysteries buried by time.

#ObscuredHistory #DyatlovPass #UnsolvedMystery #TrueHistory #DarkHistory #Mystery #Shorts #Scary #History""",
        "tags": ["dyatlov pass", "unsolved mystery", "dark history", "scary history", "shorts", "mystery", "horror history"],
        "categoryId": "22",
        "defaultLanguage": "en"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    }
}

print(f"📤 Uploading {VIDEO_FILE} ({os.path.getsize(VIDEO_FILE)/1024/1024:.1f} MB)...")

media = MediaFileUpload(VIDEO_FILE, mimetype="video/mp4", resumable=True, chunksize=1024*1024)
request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"  Upload progress: {int(status.progress() * 100)}%")

video_id = response["id"]
print(f"\n🏆 UPLOADED SUCCESSFULLY!")
print(f"📺 Video URL: https://www.youtube.com/watch?v={video_id}")
print(f"📱 Shorts URL: https://www.youtube.com/shorts/{video_id}")
