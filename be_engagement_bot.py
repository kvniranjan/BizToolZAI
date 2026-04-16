import time
import subprocess
import os

# Create a script that generates a provocative comment on the shorts video
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json

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

def post_comment(video_id, text):
    try:
        request = yt.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": text
                        }
                    }
                }
            }
        )
        response = request.execute()
        print(f"Comment posted to {video_id}!")
    except Exception as e:
        print(f"Failed to post comment: {e}")

# Post controversial pinned comments to the recent shorts to boost engagement
post_comment("7-Kv_7sR5vw", "If you still think a spreadsheet is going to make you rich while rent goes up 20% a year, you are the punchline. Prove me wrong 👇")
