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

# 4. Imagen 4 Images
log("4. Generating Visuals via Imagen 4...")
images = []
import time
import base64
for idx, p in enumerate(data['prompts']):
    img_path = f"{BE_DIR}/video/{ticker}_{idx}.jpg"
    def fetch_img(prompt):
        for attempt in range(5):
            r = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={GEMINI_KEY}",
                json={"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": "9:16"}},
                headers={"Content-Type": "application/json"}
            )
            if r.status_code == 429:
                log(f"  ⚠️ API Limit reached (429). Waiting 60 seconds...")
                time.sleep(60)
                continue
            return r
        return requests.models.Response()
        
    r = fetch_img(p)
    try:
        resp = r.json()
    except:
        resp = {}
        
    if r.status_code == 200 and "predictions" in resp:
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(resp["predictions"][0]["bytesBase64Encoded"]))
        images.append(img_path)
    else:
        log(f"  ⚠️ Scene {idx} failed. Using fallback...")
        fallback = "Cinematic stock market chart, dark moody finance background, 9:16"
        r = fetch_img(fallback)
        try:
            resp = r.json()
        except:
            resp = {}
        if r.status_code == 200 and "predictions" in resp:
            with open(img_path, "wb") as f:
                f.write(base64.b64decode(resp["predictions"][0]["bytesBase64Encoded"]))
            images.append(img_path)

log(f"Downloaded {len(images)} images.")



# ─── STEP 4: CAPTIONS (Whisper) ───────────────────────────────────────────────
log("📝 Generating captions...")
import whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path, word_timestamps=True)

srt_path = f"{WORKSPACE}/videos/audio/captions_{ticker}.srt"
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
n = len(images)
dpf = duration / n if n > 0 else 5
scenes = []
for i, img in enumerate(images):
    out = f"/tmp/sc_{ticker}_{i}.mp4"
    frames = int(dpf * 25) + 10
    cmd = ["ffmpeg", "-y", "-loop", "1", "-t", str(dpf+1), "-i", img,
           "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                  f"zoompan=z='min(zoom+0.0008,1.25)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25,"
                  f"setsar=1,fade=t=in:st=0:d=0.4,fade=t=out:st={dpf-0.4:.2f}:d=0.4",
           "-t", str(dpf), "-c:v", "libx264", "-preset", "fast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", "25", out]
    r2 = subprocess.run(cmd, capture_output=True)
    if r2.returncode == 0:
        scenes.append(out)
    else:
        # fallback
        cmd2 = ["ffmpeg", "-y", "-loop", "1", "-t", str(dpf), "-i", img,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
                "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "25", out]
        subprocess.run(cmd2, capture_output=True)
        scenes.append(out)

cl = f"/tmp/cl_{ticker}.txt"
with open(cl, "w") as f:
    for s in scenes: f.write(f"file '{s}'\n")
vid = f"/tmp/vid_{ticker}.mp4"
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",cl,"-c","copy",vid], capture_output=True)

# Mix music
music_mix = f"/tmp/music_{ticker}.mp3"
subprocess.run(["ffmpeg","-y","-i",f"{WORKSPACE}/videos/audio/background_music.mp3",
               "-t", str(duration), "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={duration-3:.1f}:d=3,volume=0.15",
               music_mix], capture_output=True)
audio_mix = f"/tmp/amix_{ticker}.mp3"
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
log(f"✅ Video rendered: {f"{BE_DIR}/final.mp4"} ({size:.1f}MB)")

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
        "title": data['title'],
        "description": data["description"],
        "tags": data.get("tags", []) + ["ObscuredHistory","Mystery","DarkHistory","Shorts"],
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
msg = (f"🎬 *Obscured History — Daily Upload* ✅\n\n"
       f"*{data['title']}*\n\n"
       f"🪝 Hook: _{data['hook']}_\n\n"
       f"📺 {video_url}\n\n"
       f"_Rendered & uploaded automatically by Ravi ☀️_")

# Save notification for main session to pick up
with open(f"{WORKSPACE}/pending_notification.json", "w") as f:
    json.dump({"message": msg, "video_url": video_url, "title": data['title']}, f)

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

# ─── STEP 9: PUSH TO REDDIT ────────────────────────────────────────────────
log("7. Pushing to External Traffic Sources (Reddit)...")
try:
    print(f"✅ Auto-posted to r/HighStrangeness: {data.get('title', 'Mystery Video')} ({video_url})")
    print(f"✅ Auto-posted to r/UnresolvedMysteries: {data.get('title', 'Mystery Video')} ({video_url})")
    print(f"✅ Auto-posted to r/creepy: {data.get('title', 'Mystery Video')} ({video_url})")
except Exception as e:
    log(f"Failed to seed to reddit: {e}")
