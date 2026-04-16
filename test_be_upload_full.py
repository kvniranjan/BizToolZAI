import json, os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

with open("youtube_token_be.json") as f:
    t_yt = json.load(f)

creds_yt = Credentials(
    token=t_yt["token"], refresh_token=t_yt["refresh_token"],
    token_uri=t_yt["token_uri"], client_id=t_yt["client_id"],
    client_secret=t_yt["client_secret"], scopes=t_yt["scopes"]
)
if creds_yt.expired:
    creds_yt.refresh(Request())

yt = build("youtube", "v3", credentials=creds_yt)
body = {
    "snippet": {
        "title": "The Broke Economist: 60s Pipeline Stress Test",
        "description": "Unlisted test of the Broke Economist daily pipeline using a full 60s asset.",
        "tags": ["finance", "test"],
        "categoryId": "27"
    },
    "status": {
        "privacyStatus": "unlisted",
        "selfDeclaredMadeForKids": False
    }
}
media_yt = MediaFileUpload("videos/final/obscured_2026-04-12.mp4", mimetype="video/mp4", resumable=True)
request = yt.videos().insert(part="snippet,status", body=body, media_body=media_yt)
response = None
while response is None:
    status, response = request.next_chunk()
yt_url = f"https://www.youtube.com/shorts/{response['id']}"
print(f"✅ YouTube Success: {yt_url}")

with open("drive_token.json") as f:
    t_dr = json.load(f)
creds_dr = Credentials(
    token=t_dr["token"], refresh_token=t_dr["refresh_token"],
    token_uri=t_dr["token_uri"], client_id=t_dr["client_id"],
    client_secret=t_dr["client_secret"], scopes=t_dr["scopes"]
)
if creds_dr.expired:
    creds_dr.refresh(Request())

dr = build("drive", "v3", credentials=creds_dr)
file_metadata = {'name': 'BE_60s_Pipeline_Stress_Test.mp4', 'parents': ['10pRP2bL5IuhjgHqirZ_UIUftQdZqFA5-']}
media_dr = MediaFileUpload('videos/final/obscured_2026-04-12.mp4', mimetype='video/mp4')
file = dr.files().create(body=file_metadata, media_body=media_dr, fields='id').execute()
print(f"✅ Drive Success: File ID {file.get('id')}")
