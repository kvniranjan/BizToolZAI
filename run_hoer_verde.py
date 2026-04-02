#!/usr/bin/env python3
import os, json, requests, base64, subprocess, sys
from config import GEMINI_KEY, ELEVENLABS_KEY
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

os.makedirs(f"{WORKSPACE}/videos/audio", exist_ok=True)
os.makedirs(f"{WORKSPACE}/videos/images", exist_ok=True)
os.makedirs(f"{WORKSPACE}/videos/final", exist_ok=True)

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

data = {
  "title": "The Town Where 600 People Vanished Overnight #Shorts",
  "hook": "Imagine walking into a town of 600 people... and finding absolutely no one.",
  "voiceover": "Imagine walking into a town of 600 people... and finding absolutely no one. In 1923, a group of travelers arrived at the Brazilian town of Hoer Verde. But the streets were dead silent. Food was still sitting on tables. Radios were left playing. Clothes were still hanging on the lines. There were no signs of a struggle, no blood, and no bodies. 600 people simply ceased to exist. But the investigators found two terrifying clues. A single gun that had been recently fired. And in the schoolhouse, a message scrawled on the chalkboard. It read: There is no salvation. To this day, no one knows what happened. What do you think took them?",
  "image_prompts": [
    "Cinematic ultra-realistic dark atmospheric historical photo of an abandoned Brazilian jungle village, misty, eerie silence, no people, moody lighting, 9:16 vertical",
    "Cinematic ultra-realistic dark atmospheric historical photo of a rustic dinner table set with untouched food, vintage 1920s Brazilian style, creepy atmosphere, 9:16 vertical",
    "Cinematic ultra-realistic dark atmospheric historical photo of an empty wooden schoolhouse classroom from the 1920s, a dusty chalkboard with faint Portuguese writing, creepy lighting, 9:16 vertical",
    "Cinematic ultra-realistic dark atmospheric historical photo of a single old revolver dropped in the dirt, dark moody lighting, mystery, 9:16 vertical"
  ],
  "description": "In 1923, the Brazilian town of Hoer Verde vanished entirely. 600 people gone without a trace. No struggle, no bodies. Just a single fired gun and a chilling message: 'There is no salvation.' What happened? #ObscuredHistory #Mystery #DarkHistory #Shorts #Unsolved",
  "tags": ["ObscuredHistory", "UnsolvedMystery", "DarkHistory", "TrueHistory", "Shorts", "HoerVerde"]
}

date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
audio_path = f"{WORKSPACE}/videos/audio/vo_{date_str}.mp3"
output_path = f"{WORKSPACE}/videos/final/obscured_{date_str}.mp4"

log("🎙️ Generating voiceover...")
r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
    headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
    json={"text": data["voiceover"], "model_id": "eleven_monolingual_v1",
          "voice_settings": {"stability": 0.55, "similarity_boost": 0.75}}
)
if r.status_code != 200:
    log(f"❌ ElevenLabs error: {r.text[:200]}")
    sys.exit(1)

with open(audio_path, "wb") as f:
    f.write(r.content)

res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", audio_path], capture_output=True, text=True)
duration = float(res.stdout.strip())
log(f"✅ Voiceover: {duration:.1f}s")

log("🖼️ Generating images via Imagen 4...")
images = []
for i, prompt in enumerate(data["image_prompts"]):
    img_path = f"{WORKSPACE}/videos/images/scene_{date_str}_{i+1}.jpg"
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={GEMINI_KEY}",
        json={"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": "9:16"}},
        headers={"Content-Type": "application/json"}
    )
    if r.status_code == 200:
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(r.json()["predictions"][0]["bytesBase64Encoded"]))
        images.append(img_path)
        log(f"  ✅ Scene {i+1}")
    else:
        log(f"  ❌ Scene {i+1}: {r.text[:100]}")

if not images:
    log("❌ No images generated")
    sys.exit(1)

log("📝 Generating captions...")
import whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path, word_timestamps=True)

srt_path = f"{WORKSPACE}/videos/audio/captions_{date_str}.srt"
srt_lines = []
idx = 1
for seg in result["segments"]:
    if "words" not in seg: continue
    words = seg["words"]
    for i in range(0, len(words), 3):
        w = words[i:i+3]
        start, end = w[0]["start"], w[-1]["end"]
        text = " ".join(x["word"].strip() for x in w).upper()
        def t(s): return f"{int(s//3600):02d}:{int((s%3600)//60):02d}:{s%60:06.3f}".replace(".",",")
        srt_lines.append(f"{idx}\n{t(start)} --> {t(end)}\n{text}\n")
        idx += 1
with open(srt_path, "w") as f:
    f.write("\n".join(srt_lines))
log(f"✅ {idx-1} caption chunks")

log("🎬 Rendering video...")
n = len(images)
dpf = duration / n
scenes = []
for i, img in enumerate(images):
    out = f"/tmp/sc_{date_str}_{i}.mp4"
    frames = int(dpf * 25) + 10
    cmd = ["ffmpeg", "-y", "-loop", "1", "-t", str(dpf+1), "-i", img,
           "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                  f"zoompan=z='min(zoom+0.0004,1.12)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25,"
                  f"setsar=1,fade=t=in:st=0:d=0.4,fade=t=out:st={dpf-0.4:.2f}:d=0.4",
           "-t", str(dpf), "-c:v", "libx264", "-preset", "fast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", "25", out]
    r2 = subprocess.run(cmd, capture_output=True)
    if r2.returncode == 0:
        scenes.append(out)
    else:
        cmd2 = ["ffmpeg", "-y", "-loop", "1", "-t", str(dpf), "-i", img,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
                "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "25", out]
        subprocess.run(cmd2, capture_output=True)
        scenes.append(out)

cl = f"/tmp/cl_{date_str}.txt"
with open(cl, "w") as f:
    for s in scenes: f.write(f"file '{s}'\n")
vid = f"/tmp/vid_{date_str}.mp4"
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",cl,"-c","copy",vid], capture_output=True)

music_mix = f"/tmp/music_{date_str}.mp3"
subprocess.run(["ffmpeg","-y","-i",f"{WORKSPACE}/videos/audio/background_music.mp3",
               "-t", str(duration), "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={duration-3:.1f}:d=3,volume=0.07",
               music_mix], capture_output=True)
audio_mix = f"/tmp/amix_{date_str}.mp3"
subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_mix,
               "-filter_complex","[1:a]volume=0.07[bg];[0:a][bg]amix=inputs=2:duration=first[out]",
               "-map","[out]", audio_mix], capture_output=True)

cmd = ["ffmpeg","-y","-i",vid,"-i",audio_mix,
       "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=18,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=60'",
       "-map","0:v","-map","1:a","-c:v","libx264","-preset","fast","-crf","20",
       "-c:a","copy","-shortest", output_path]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    subprocess.run(["ffmpeg","-y","-i",vid,"-i",audio_mix,
                   "-map","0:v","-map","1:a","-c:v","libx264","-preset","fast",
                   "-crf","20","-c:a","copy","-shortest", output_path], capture_output=True)

size = os.path.getsize(output_path)/1024/1024
log(f"✅ Video rendered: {output_path} ({size:.1f}MB)")

log("📤 Uploading to YouTube...")
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

with open(f"{WORKSPACE}/youtube_token.json") as f:
    tok = json.load(f)

creds = Credentials(token=tok["token"], refresh_token=tok["refresh_token"],
    token_uri=tok["token_uri"], client_id=tok["client_id"],
    client_secret=tok["client_secret"], scopes=tok["scopes"])

if creds.expired:
    creds.refresh(Request())
    tok["token"] = creds.token
    with open(f"{WORKSPACE}/youtube_token.json","w") as f: json.dump(tok,f)

yt = build("youtube","v3",credentials=creds)
body = {
    "snippet": {
        "title": data["title"],
        "description": data["description"],
        "tags": data["tags"],
        "categoryId": "22",
        "defaultLanguage": "en"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True
    }
}

media = MediaFileUpload(output_path, mimetype="video/mp4", resumable=True, chunksize=1024*1024)
req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
response = None
while response is None:
    status, response = req.next_chunk()

video_id = response["id"]
video_url = f"https://www.youtube.com/shorts/{video_id}"
log(f"✅ UPLOADED: {video_url}")

import random
hooks = [
    f"This one genuinely unsettles me. What do you think really happened? 👇",
    f"The more you research this, the stranger it gets. Drop your theory below 👇",
    f"Historians still can't agree on this. What's your take? 👇"
]
try:
    comment_body = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {
                "snippet": {"textOriginal": random.choice(hooks)}
            }
        }
    }
    comment = yt.commentThreads().insert(part="snippet", body=comment_body).execute()
    comment_id = comment["id"]
    log("✅ Comment posted")
except Exception as e:
    log(f"⚠️ Comment failed (non-critical): {e}")

print(f"\nSUCCESS_URL={video_url}")
