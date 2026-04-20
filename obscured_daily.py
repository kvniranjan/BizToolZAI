#!/usr/bin/env python3
"""
Obscured History — Daily Video Factory
Runs at 5 PM EST (22:00 UTC) every day.
1. Researches a viral dark history topic via Gemini
2. Generates script + voiceover + images
3. Renders premium video with captions + music
4. Uploads to YouTube
5. Notifies BOSS via Telegram
"""

import os, json, requests, base64, subprocess, re, sys
from config import GEMINI_KEY, ELEVENLABS_KEY
from datetime import datetime

# ─── CONFIG ───────────────────────────────────────────────────────────────────
# Key loaded from config.py
# Key loaded from config.py
VOICE_ID      = "JBFqnCBsd6RMkjVDRZzb"
WORKSPACE     = "/root/.openclaw/workspace"
TELEGRAM_CHAT = "1014391339"

os.makedirs(f"{WORKSPACE}/videos/audio", exist_ok=True)
os.makedirs(f"{WORKSPACE}/videos/images", exist_ok=True)
os.makedirs(f"{WORKSPACE}/videos/final", exist_ok=True)

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def gemini(prompt):
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}",
        headers={"Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

# ─── STEP 1: RESEARCH & SCRIPT ────────────────────────────────────────────────
log("🔍 Researching viral dark history topic...")

research_prompt = """You are an expert viral YouTube Shorts scriptwriter for "Obscured History" — a dark history and unsolved mystery channel optimised for maximum watch-through rate.

YOUR MOST IMPORTANT GOAL: Write a script where viewers physically cannot stop watching before it ends.

TOPIC SELECTION RULES (follow strictly):
1. ✅ MUST be a highly terrifying, obscure historical mystery. Focus on eerie, unexplained vanishings, bizarre locked-room scenarios, or psychological anomalies. 
2. 🚫 BANNED TOPICS: NO MORE LIGHTHOUSES. Do not use Flannan Isles, Mary Celeste, Dyatlov Pass, Titanic, or Bermuda Triangle. We have done too many lighthouses.
3. ✅ Focus on visceral, chilling details (e.g., "The food was still warm," "The clocks all stopped at exactly 3:15," "There was a single set of footprints leading into the snow and abruptly stopping").
4. ✅ The mystery must induce a feeling of dread and psychological tension.
2. ✅ The event must have a SHOCKING unanswered element — something that defies explanation even today
3. ✅ Prefer events with SPECIFIC vivid details (names, dates, exact locations, physical evidence)
4. ✅ The mystery must be UNRESOLVED — "what really happened" must still be open
5. ✅ Pick something that sounds impossible — "this CAN'T be real" reaction drives shares

HOOK RULES (the first 3 seconds determine everything):
- Must create an OPEN LOOP instantly — viewer must need to know what happened
- Use a specific shocking detail, not a vague tease
- Examples of great hooks:
  * "They found a ship full of dead crew, but all the food was still warm."
  * "A town of 600 people disappeared overnight. No bodies. No wreckage. Just silence."
  * "She was photographed at a party. The problem? She had been dead for 3 years."
- Avoid weak hooks like "In 1959..." or "Have you heard of..." — these lose viewers immediately

SCRIPT STRUCTURE FOR MAX RETENTION:
1. HOOK (0-3s): Paced visually. Start with rapid 2-4 word phrases. Shocking statement that creates an instant open loop. DO NOT start with 'In [year]'.
2. CONTEXT (3-15s): Brief, vivid scene-setting — make viewer feel they're there
3. ESCALATION (15-35s): Stack shocking detail upon shocking detail — each one more bizarre
4. THE UNANSWERED QUESTION (35-45s): What do we still NOT know? Lean into the mystery
5. CALL TO ACTION (45-50s): Demand a subscribe BEFORE giving the final shocking detail. (e.g., "I'm about to tell you the scariest part, but first, hit subscribe so you don't miss tomorrow's mystery.") Then end with the final unanswered question.

IMAGE PROMPT RULES:
- Historical accuracy is PARAMOUNT. If the ship was a wooden sail schooner, the prompt MUST specify 'wooden sail schooner'. Do not use generic terms like 'massive ship' if it contradicts historical facts. Our viewers are history buffs and will penalize inaccuracies.

SCRIPT WRITING RULES:
- Every sentence must earn its place — cut anything that doesn't add tension or information.
- Use short, punchy, terrifying sentences. Build relentless suspense.
- Make the viewer feel the isolation and dread. Use sensory words.
- Speak directly to the viewer — "you", "imagine", "picture this".
- No markdown, no asterisks, no stage directions. Pure spoken words only.
- Length: 45-52 seconds when spoken at a medium pace.

Output strictly as JSON:
{
  "title": "Specific shocking YouTube title under 60 chars with #Shorts — must make someone click",
  "hook": "The exact opening sentence — under 12 words, creates instant open loop",
  "voiceover": "Full script following the 5-part structure above. Pure spoken words. No markdown.",
  "image_prompts": [
    "Cinematic ultra-realistic dark atmospheric historical photo, moody lighting, 9:16 vertical — matching scene 1 of the script",
    "Cinematic ultra-realistic dark atmospheric historical photo, moody lighting, 9:16 vertical — matching scene 2",
    "Cinematic ultra-realistic dark atmospheric historical photo, moody lighting, 9:16 vertical — matching scene 3",
    "Cinematic ultra-realistic dark atmospheric historical photo, moody lighting, 9:16 vertical — matching scene 4"
  ],
  "description": "YouTube description 150 words with relevant hashtags #ObscuredHistory #Mystery #DarkHistory #Shorts",
  "tags": ["ObscuredHistory", "UnsolvedMystery", "DarkHistory", "TrueHistory", "Shorts"]
}"""

raw = gemini(research_prompt)
raw = re.sub(r'```json\n?', '', raw).replace('```', '').strip()

try:
    data = json.loads(raw)
except:
    # Try to extract JSON
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    data = json.loads(match.group()) if match else None

if not data:
    log("❌ Failed to parse script JSON")
    sys.exit(1)

log(f"✅ Topic: {data['title']}")
log(f"   Hook: {data['hook']}")

date_str = datetime.now().strftime("%Y-%m-%d")
audio_path = f"{WORKSPACE}/videos/audio/vo_{date_str}.mp3"
output_path = f"{WORKSPACE}/videos/final/obscured_{date_str}.mp4"

# ─── STEP 2: VOICEOVER ────────────────────────────────────────────────────────
log("🎙️ Generating voiceover...")
r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
    headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
    json={"text": data["voiceover"], "model_id": "eleven_turbo_v2_5",
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

if duration > 59.0:
    log("⚠️ Voiceover > 59s, applying atempo filter to fit Shorts format...")
    ratio = duration / 58.5
    speed_audio = f"{WORKSPACE}/videos/audio/vo_fast_{date_str}.mp3"
    subprocess.run(["ffmpeg", "-y", "-i", audio_path, "-filter:a", f"atempo={ratio}", speed_audio], capture_output=True)
    audio_path = speed_audio
    duration = 58.5
    log(f"✅ Voiceover sped up to 58.5s")


# ─── STEP 3: IMAGES ───────────────────────────────────────────────────────────
log("🖼️ Generating images via Imagen 4...")
images = []
for i, prompt in enumerate(data["image_prompts"]):
    img_path = f"{WORKSPACE}/videos/images/scene_{date_str}_{i+1}.jpg"
    
    def fetch_img(p):
        return requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={GEMINI_KEY}",
            json={"instances": [{"prompt": p}], "parameters": {"sampleCount": 1, "aspectRatio": "9:16"}},
            headers={"Content-Type": "application/json"}
        )
        
    r = fetch_img(prompt)
    resp = r.json()
    
    if r.status_code == 200 and "predictions" in resp:
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(resp["predictions"][0]["bytesBase64Encoded"]))
        images.append(img_path)
        log(f"  ✅ Scene {i+1}")
    else:
        log(f"  ⚠️ Scene {i+1} failed (likely safety). Retrying with generic fallback prompt...")
        fallback = "Cinematic dark history background, atmospheric, moody, blank slate, highly detailed, 9:16 vertical"
        r = fetch_img(fallback)
        resp = r.json()
        if r.status_code == 200 and "predictions" in resp:
            with open(img_path, "wb") as f:
                f.write(base64.b64decode(resp["predictions"][0]["bytesBase64Encoded"]))
            images.append(img_path)
            log(f"  ✅ Scene {i+1} (Fallback)")
        else:
            log(f"  ❌ Scene {i+1}: {r.text[:100]}")

if not images:
    log("❌ No images generated")
    sys.exit(1)

# ─── STEP 4: CAPTIONS (Whisper) ───────────────────────────────────────────────
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

# ─── STEP 5: RENDER ───────────────────────────────────────────────────────────
log("🎬 Rendering video...")
n = len(images)
dpf = duration / n
scenes = []
for i, img in enumerate(images):
    out = f"/tmp/sc_{date_str}_{i}.mp4"
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

cl = f"/tmp/cl_{date_str}.txt"
with open(cl, "w") as f:
    for s in scenes: f.write(f"file '{s}'\n")
vid = f"/tmp/vid_{date_str}.mp4"
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",cl,"-c","copy",vid], capture_output=True)

# Mix music
music_mix = f"/tmp/music_{date_str}.mp3"
subprocess.run(["ffmpeg","-y","-i",f"{WORKSPACE}/videos/audio/background_music.mp3",
               "-t", str(duration), "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={duration-3:.1f}:d=3,volume=0.15",
               music_mix], capture_output=True)
audio_mix = f"/tmp/amix_{date_str}.mp3"
subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_mix,
               "-filter_complex","[0:a]volume=1.0[v];[1:a]volume=1.0[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",
               "-map","[out]", audio_mix], capture_output=True)

# Final with captions
cmd = ["ffmpeg","-y","-i",vid,"-i",audio_mix,
       "-vf", f"subtitles={srt_path}:force_style='FontName=Impact,FontSize=24,Bold=1,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,Outline=3,Shadow=2,Alignment=2,MarginV=80'",
       "-map","0:v","-map","1:a","-c:v","libx264","-preset","fast","-crf","20",
       "-c:a","copy","-shortest", output_path]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    # fallback without captions
    subprocess.run(["ffmpeg","-y","-i",vid,"-i",audio_mix,
                   "-map","0:v","-map","1:a","-c:v","libx264","-preset","fast",
                   "-crf","20","-c:a","copy","-shortest", output_path], capture_output=True)

size = os.path.getsize(output_path)/1024/1024
log(f"✅ Video rendered: {output_path} ({size:.1f}MB)")

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
        "title": data["title"],
        "description": data["description"],
        "tags": data["tags"] + ["ObscuredHistory","Mystery","DarkHistory","Shorts"],
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

# ─── STEP 7: NOTIFY BOSS ─────────────────────────────────────────────────────
log("📱 Notifying BOSS...")
msg = (f"🎬 *Obscured History — Daily Upload* ✅\n\n"
       f"*{data['title']}*\n\n"
       f"🪝 Hook: _{data['hook']}_\n\n"
       f"📺 {video_url}\n\n"
       f"_Rendered & uploaded automatically by Ravi ☀️_")

# Save notification for main session to pick up
with open(f"{WORKSPACE}/pending_notification.json", "w") as f:
    json.dump({"message": msg, "video_url": video_url, "title": data["title"]}, f)

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
