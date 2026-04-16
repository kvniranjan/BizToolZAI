import os, subprocess, json, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

WORKSPACE = "/root/.openclaw/workspace"
BE_DIR = f"{WORKSPACE}/content/broke_economist/v4_test"
audio_path = f"{BE_DIR}/audio.mp3"
concat_vid = f"{BE_DIR}/concat.mp4"
srt_path = f"{BE_DIR}/captions.srt"
MUSIC_FILE = f"{WORKSPACE}/videos/audio/background_music.mp3"
audio_mix = f"{BE_DIR}/audio_mixed.mp3"

print("Mixing Audio...")
duration_str = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path], capture_output=True, text=True).stdout.strip()
total_duration = float(duration_str)

music_temp = f"{BE_DIR}/music_temp.mp3"
subprocess.run(["ffmpeg","-y","-i",MUSIC_FILE,
               "-t", str(total_duration), "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={total_duration-3:.1f}:d=3,volume=0.15",
               music_temp], capture_output=True)
               
subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_temp,
               "-filter_complex","[0:a]volume=1.0[v];[1:a]volume=1.0[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",
               "-map","[out]", audio_mix], capture_output=True)

final_vid = f"{BE_DIR}/final_music.mp4"
print("Rendering Final Video...")
cmd = [
    "ffmpeg", "-y", 
    "-i", concat_vid, 
    "-i", audio_mix,
    "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=20,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=3,Shadow=2,Alignment=2,MarginV=100'",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac",
    "-shortest", final_vid
]
res = subprocess.run(cmd, capture_output=True, text=True)

print("Uploading to YouTube...")
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

body = {
    "snippet": {
        "title": "Why Coffee Costs $8 Now #Shorts",
        "description": "Why coffee costs so much.\\n\\n#finance #economics #money",
        "tags": ["finance", "economics", "money", "wealth"],
        "categoryId": "27"
    },
    "status": {
        "privacyStatus": "unlisted",
        "selfDeclaredMadeForKids": False
    }
}

media_yt = MediaFileUpload(final_vid, mimetype="video/mp4", resumable=True)
request = yt.videos().insert(part="snippet,status", body=body, media_body=media_yt)

response = None
while response is None:
    status, response = request.next_chunk()

yt_url = f"https://www.youtube.com/shorts/{response['id']}"
print(f"✅ YouTube Upload Success: {yt_url}")
