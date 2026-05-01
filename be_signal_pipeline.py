import os, sys, subprocess, json, time, re
import google.generativeai as genai
import requests

from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
KIE_API_KEY = os.getenv("KIE_API_KEY")

WORKSPACE = "/root/.openclaw/workspace"
BE_DIR = f"{WORKSPACE}/videos/broke_economist"
os.makedirs(BE_DIR, exist_ok=True)
os.makedirs(f"{BE_DIR}/audio", exist_ok=True)
os.makedirs(f"{BE_DIR}/video", exist_ok=True)
os.makedirs(f"{BE_DIR}/final", exist_ok=True)

VOICE_ID = "JBFqnCBsd6RMkjVDRZzb" # George

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

# 1. Run Signal Bot to get the latest alert
log("1. Running Waterfall Sniper Bot...")
result = subprocess.run(["venv/bin/python3", "signal_bot.py"], capture_output=True, text=True)
output = result.stdout

buy_match = re.search(r"🚨 BUY ALERT.*?Target: (\w+)\nPrice: \$([\d\.]+) \| 5-Day RSI: ([\d\.]+)\nWhy: (.*?)\n", output, re.DOTALL)
if not buy_match:
    log("No buy targets right now. Exiting.")
    sys.exit(0)

ticker, price, rsi, reason = buy_match.groups()
signal_info = f"BUY {ticker} at ${price}. RSI is {rsi}. Reason: {reason.strip()}"
log(f"Signal found: {signal_info}")

# 2. Generate Script
log("2. Generating Script via Gemini...")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

prompt = f"""You are 'The Broke Economist'. Write a fast-paced, highly engaging 45-second YouTube Short script about a hot stock alert.
The signal is: {signal_info}
Tone: cynical, dark humor, exposing the game, aggressive pacing. 
CRITICAL RULE 1: The first 3 seconds MUST be a high-retention hook. DO NOT say "Here's why", "Did you know", or "Welcome to". Start mid-thought.
CRITICAL RULE 2: Introduce a "villain" (Wall Street, hedge funds, etc). Make the viewer angry. Keep sentences to 5-8 words. High energy. Fast cuts.

Format the output EXACTLY as valid JSON with no markdown:
{{
  "title": "A viral, clickbaity YouTube Shorts title (under 50 chars)",
  "seo_tags": ["finance", "stocks", "{ticker.lower()}", "investing", "wallstreet"],
  "hook": "The first 3 seconds...",
  "voiceover": "The full voiceover text...",
  "prompts": [
    "Image/Video prompt 1 (describing scene of wall street greed or the specific stock's industry, cinematic, hyperrealistic)",
    "Image/Video prompt 2 (...)",
    "Image/Video prompt 3 (...)",
    "Image/Video prompt 4 (...)"
  ]
}}
"""

response = model.generate_content(prompt)
try:
    data = json.loads(response.text.strip('```json\n').strip('```'))
except Exception as e:
    log(f"JSON Parse failed: {e}")
    sys.exit(1)

log(f"Title: {data['hook']}")

# 3. ElevenLabs TTS
log("3. Generating Voiceover...")
tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
tts_headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
tts_data = {"text": data['voiceover'], "model_id": "eleven_monolingual_v1"}
r = requests.post(tts_url, json=tts_data, headers=tts_headers)
audio_path = f"{BE_DIR}/audio/{ticker}_voice.mp3"
with open(audio_path, "wb") as f:
    f.write(r.content)

# 4. Kie.ai Videos
log("4. Generating Visuals via Kie.ai (Bytedance Seedance 2.0 Fast)...")
headers_kie = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}
video_paths = []
task_ids = []

for idx, p in enumerate(data['prompts']):
    payload = {
        "model": "bytedance/seedance-2-fast",
        "input": {"prompt": p}
    }
    res = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=payload, headers=headers_kie).json()
    if res.get("data") and res["data"].get("taskId"):
        task_ids.append((idx, res["data"]["taskId"]))
    else:
        log(f"Failed to submit task: {res}")

import json
for idx, t in task_ids:
    while True:
        status_res = requests.get(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={t}", headers=headers_kie).json()
        state = status_res.get("data", {}).get("state", "").lower()
        if state == "success":
            try:
                res_json = json.loads(status_res["data"]["resultJson"])
                vid_url = res_json["resultUrls"][0]
                vid_data = requests.get(vid_url).content
                out_path = f"{BE_DIR}/video/{ticker}_{idx}.mp4"
                with open(out_path, "wb") as f:
                    f.write(vid_data)
                video_paths.append(out_path)
            except Exception as e:
                log(f"Failed to parse video URL: {e}")
            break
        elif state in ["fail", "failed", "canceled"]:
            log(f"Task {t} failed.")
            break
        time.sleep(10)

log(f"Downloaded {len(video_paths)} videos.")

# ─── STEP 4: CAPTIONS (Whisper) ───────────────────────────────────────────────
log("📝 Generating captions...")
import whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path, word_timestamps=True)

srt_path = f"{BE_DIR}/captions.srt"
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

# ─── STEP 5: RENDER ───────────────────────────────────────────────────────────
log("🎬 Rendering video...")
n = len(video_paths)
import subprocess
res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", audio_path], capture_output=True, text=True)
duration = float(res.stdout.strip())
dpf = duration / n
scenes = []
for i, clip in enumerate(video_paths):
    out = f"{BE_DIR}/sc_{i}.mp4"
    cmd = [
        "ffmpeg", "-y", 
        "-stream_loop", "-1",
        "-i", clip, 
        "-t", str(dpf),
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "25",
        out
    ]
    subprocess.run(cmd, capture_output=True)
    scenes.append(out)

cl = f"{BE_DIR}/cl.txt"
with open(cl, "w") as f:
    for s in scenes: f.write(f"file '{s}'\n")
vid = f"{BE_DIR}/vid.mp4"
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",cl,"-c","copy",vid], capture_output=True)

# Mix music
music_mix = f"{BE_DIR}/music.mp3"
subprocess.run(["ffmpeg","-y","-i",f"{WORKSPACE}/videos/audio/background_music.mp3",
               "-t", str(duration), "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={duration-3:.1f}:d=3,volume=0.15",
               music_mix], capture_output=True)
audio_mix = f"{BE_DIR}/amix.mp3"
subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_mix,
               "-filter_complex","[0:a]volume=1.0[v];[1:a]volume=1.0[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",
               "-map","[out]", audio_mix], capture_output=True)

# Final with captions
cmd = ["ffmpeg","-y","-i",vid,"-i",audio_mix,
       "-vf", f"subtitles={srt_path}:force_style='FontName=Impact,FontSize=24,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=3,Shadow=2,Alignment=2,MarginV=80'",
       "-map","0:v","-map","1:a","-c:v","libx264","-preset","fast","-crf","20",
       "-c:a","copy","-shortest", f"{BE_DIR}/final.mp4"]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    # fallback without captions
    subprocess.run(["ffmpeg","-y","-i",vid,"-i",audio_mix,
                   "-map","0:v","-map","1:a","-c:v","libx264","-preset","fast",
                   "-crf","20","-c:a","copy","-shortest", f"{BE_DIR}/final.mp4"], capture_output=True)

size = os.path.getsize(f"{BE_DIR}/final.mp4")/1024/1024
log(f"✅ Video rendered: {BE_DIR}/final.mp4 ({size:.1f}MB)")

# ─── STEP 6: UPLOAD TO YOUTUBE ────────────────────────────────────────────────
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
        "title": data["hook"],
        "description": f"BUY SIGNAL ALERT for {ticker} 🔥 Subscribe for more Sniper Bot alerts!",
        "tags": ["Finance", "Stocks", "Investing", "Shorts"],
        "categoryId": "22",
        "defaultLanguage": "en"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False,
        "containsSyntheticMedia": True
    }
}

media = MediaFileUpload(f"{BE_DIR}/final.mp4", mimetype="video/mp4", resumable=True, chunksize=1024*1024)
req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
response = None
while response is None:
    status, response = req.next_chunk()

video_id = response["id"]
video_url = f"https://www.youtube.com/shorts/{video_id}"
log(f"✅ UPLOADED: {video_url}")

# ─── STEP 7: NOTIFY BOSS ─────────────────────────────────────────────────────
log("📱 Notifying BOSS...")
msg = (f"🎬 *The Broke Economist — Live Trade Alert* ✅\n\n"
       f"*{data['hook']}*\n\n"
       f"🪝 Hook: _{data['hook']}_\n\n"
       f"📺 {video_url}\n\n"
       f"_Rendered & uploaded automatically by Ravi ☀️_")

# Save notification for main session to pick up
with open(f"{WORKSPACE}/pending_notification.json", "w") as f:
    json.dump({"message": msg, "video_url": video_url, "title": data["hook"]}, f)

# ─── STEP 8: PIN ENGAGEMENT COMMENT ─────────────────────────────────────────
log("💬 Posting pinned comment...")
try:
    import random
    hooks = [
        f"This one genuinely unsettles me. If you made it this far, hit SUBSCRIBE for daily mysteries. What do you think really happened? 👇",
        f"The more you research this, the stranger it gets. SUBSCRIBE to uncover more lost history. Drop your theory below 👇",
        f"Historians still can't agree on this. What's your take? 👇",
        f"This kept me up at night. Anyone else feel that? 👇",
        f"The official explanation never satisfied me. What do YOU think? 👇"
    ]
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
    # Pin the comment
    yt.comments().setModerationStatus(id=comment_id.split(".")[1] if "." in comment_id else comment_id,
                                       moderationStatus="published").execute()
    log("✅ Comment posted")
except Exception as e:
    log(f"⚠️ Comment failed (non-critical): {e}")

log("✅ ALL DONE!")
print(f"\nVIDEO_URL={video_url}")

# ─── STEP 9
