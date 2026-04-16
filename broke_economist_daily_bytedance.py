import os, json, requests, subprocess, sys, time, re
from dotenv import load_dotenv
import whisper
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
KIE_API_KEY = os.getenv("KIE_API_KEY")

WORKSPACE = "/root/.openclaw/workspace"
BE_DIR = f"{WORKSPACE}/content/broke_economist/v4_test"
os.makedirs(BE_DIR, exist_ok=True)

VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

log("1. Generating Script & Bytedance Prompts via Gemini...")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

import datetime
import random

# Generate a high-retention, controversial, or trend-jacking topic dynamically
topic_prompt = """You are a viral YouTube Shorts strategist for a finance channel called 'The Broke Economist'. 
Generate 1 highly controversial, contrarian, or cynical finance topic that exposes a 'scam' or hidden truth about money, real estate, investing, or corporate greed. It must be highly relatable to broke millennials/Gen Z.
Output ONLY the topic sentence, nothing else. Examples: 'Why your 401k is a trap designed to keep you working', 'The dark psychology of grocery store layouts', 'Why Dave Ramsey's advice is keeping you poor'."""

topic_resp = model.generate_content(topic_prompt)
selected_topic = topic_resp.text.strip().strip('"')
log(f"Dynamic Topic chosen: {selected_topic}")

prompt = f"""You are 'The Broke Economist'. Write a fast-paced, highly engaging 45-second YouTube Short script about: '{selected_topic}'.
Tone: cynical, dark humor, exposing the game, aggressive pacing. Hook the viewer in the first 2 seconds with a controversial statement.
Use short, punchy sentences. High energy.

Format the output EXACTLY as valid JSON with no markdown formatting:
{{
  "title": "A viral, clickbaity YouTube Shorts title (under 50 chars)",
  "seo_tags": ["finance", "tag2", "tag3", "tag4", "tag5"],
  "hook": "The first 3 seconds (must be controversial/curiosity-inducing)...",
  "voiceover": "The full voiceover text including the hook. No asterisks, no sound effect notes.",
  "prompts": [
    "A cinematic animated shot of...",
    "A cinematic animated shot of...",
    "A cinematic animated shot of..."
  ]
}}
Provide EXACTLY 3 prompts. Make them highly cinematic, dynamic camera movements, photorealistic, 9:16 aspect ratio."""


resp = model.generate_content(prompt)
try:
    text = resp.text.replace('```json', '').replace('```', '').strip()
    data = json.loads(text)
except Exception as e:
    log(f"Failed to parse Gemini JSON: {e}")
    sys.exit(1)

with open(f"{BE_DIR}/script.json", "w") as f:
    json.dump(data, f, indent=2)

log("2. Generating Voiceover...")
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {"Accept": "audio/mpeg", "Content-Type": "application/json", "xi-api-key": ELEVENLABS_API_KEY}
payload = {
    "text": data["voiceover"].replace('*', ''),
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
}
r = requests.post(url, json=payload, headers=headers)
audio_path = f"{BE_DIR}/audio.mp3"
with open(audio_path, 'wb') as f:
    f.write(r.content)

log("3. Generating Captions...")
wmodel = whisper.load_model("base")
result = wmodel.transcribe(audio_path, word_timestamps=True)
srt_path = f"{BE_DIR}/captions.srt"
srt_lines = []
idx = 1
for seg in result["segments"]:
    if "words" not in seg: continue
    words = seg["words"]
    for i in range(0, len(words), 3):
        chunk = words[i:i+3]
        if not chunk: continue
        start = chunk[0]['start']
        end = chunk[-1]['end']
        
        def fmt_ts(s):
            hrs = int(s // 3600)
            mins = int((s % 3600) // 60)
            secs = int(s % 60)
            ms = int((s % 1) * 1000)
            return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"
            
        srt_lines.append(str(idx))
        srt_lines.append(f"{fmt_ts(start)} --> {fmt_ts(end)}")
        text_chunk = " ".join([w['word'].strip() for w in chunk])
        srt_lines.append(text_chunk.upper())
        srt_lines.append("")
        idx += 1

with open(srt_path, "w") as f:
    f.write("\n".join(srt_lines))

log("4. Generating Videos with Kie.ai (Bytedance Seedance 2.0 Fast)...")
headers_kie = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}
tasks = []
for p in data["prompts"]:
    payload = {
        "model": "bytedance/seedance-2-fast",
        "input": {
            "prompt": p,
            "generate_audio": False,
            "resolution": "720p",
            "aspect_ratio": "9:16",
            "duration": 5,
            "web_search": False,
            "nsfw_checker": False
        }
    }
    r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=payload, headers=headers_kie).json()
    if 'data' in r and 'taskId' in r['data']:
        tasks.append(r['data']['taskId'])
        log(f"Started Bytedance task: {r['data']['taskId']}")
    else:
        log(f"Bytedance task failed to start: {r}")

log("Polling Bytedance tasks (this takes a few mins)...")
videos = []
for t in tasks:
    done = False
    for _ in range(60): # Up to 10 mins
        try:
            r = requests.get(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={t}", headers=headers_kie).json()
            state = r.get('data', {}).get('state')
            if state == 'success':
                res_json = json.loads(r['data']['resultJson'])
                v_url = res_json['resultUrls'][0]
                videos.append(v_url)
                log(f"Task {t} completed!")
                done = True
                break
            elif state == 'failed':
                log(f"Task {t} failed!")
                done = True
                break
        except Exception as e:
            log(f"Poll error: {e}")
        time.sleep(10)

log("Downloading videos...")
video_paths = []
for i, v_url in enumerate(videos):
    path = f"{BE_DIR}/clip_{i}.mp4"
    r = requests.get(v_url)
    with open(path, "wb") as f:
        f.write(r.content)
    video_paths.append(path)

if not video_paths:
    log("No videos generated. Exiting.")
    sys.exit(1)

log("5. Stitching Video...")
with open(f"{BE_DIR}/concat.txt", "w") as f:
    for _ in range(5): # Loop videos so it covers the audio track
        for vp in video_paths:
            f.write(f"file '{os.path.basename(vp)}'\n")

concat_vid = f"{BE_DIR}/concat.mp4"
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{BE_DIR}/concat.txt", "-c:v", "copy", concat_vid], check=True)


log("4.5 Mixing Music...")
MUSIC_FILE = f"{WORKSPACE}/videos/audio/background_music.mp3"
audio_mix = f"{BE_DIR}/audio_mixed.mp3"

if os.path.exists(MUSIC_FILE):
    # Get exact audio duration
    duration_str = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", audio_path], capture_output=True, text=True).stdout.strip()
    total_duration = float(duration_str)
    
    music_temp = f"{BE_DIR}/music_temp.mp3"
    subprocess.run(["ffmpeg","-y","-i",MUSIC_FILE,
                   "-t", str(total_duration), "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={total_duration-3:.1f}:d=3,volume=0.15",
                   music_temp], capture_output=True)
                   
    subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_temp,
                   "-filter_complex","[0:a]volume=1.0[v];[1:a]volume=1.0[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",
                   "-map","[out]", audio_mix], capture_output=True)
else:
    log("Warning: background_music.mp3 not found. Rendering without music.")
    audio_mix = audio_path

final_vid = f"{BE_DIR}/final.mp4"
cmd = [
    "ffmpeg", "-y", 
    "-i", concat_vid, 
    "-i", audio_mix,
    "-vf", f"zoompan=z='min(zoom+0.0005,1.1)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',subtitles={srt_path}:force_style='FontName=Impact,FontSize=24,Bold=1,PrimaryColour=&H0000D7FF,OutlineColour=&H00000000,Outline=4,Shadow=3,Alignment=2,MarginV=180'",
    "-map", "0:v", "-map", "1:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-c:a", "aac",
    "-shortest", final_vid
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    log(f"FFmpeg failed: {res.stderr}")
else:
    log(f"✅ V4 Pipeline Render Complete! Saved to {final_vid}")


log("6. Uploading to YouTube...")
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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
        "title": f"{data.get('title', 'The Broke Economist')} #Shorts",
        "description": f"{data.get('hook', '')}\n\n#finance #economics #money #investing #wealth",
        "tags": data.get('seo_tags', ["finance", "economics", "money", "wealth"]),
        "categoryId": "27"
    },
    "status": {
        "privacyStatus": "public",
        "selfDeclaredMadeForKids": False
    }
}

media_yt = MediaFileUpload(final_vid, mimetype="video/mp4", resumable=True)
request = yt.videos().insert(part="snippet,status", body=body, media_body=media_yt)

response = None
while response is None:
    status, response = request.next_chunk()

yt_url = f"https://www.youtube.com/shorts/{response['id']}"
log(f"✅ YouTube Upload Success: {yt_url}")
log("7. Pushing to External Traffic Sources (Reddit)...")
try:
    with open('/root/.openclaw/workspace/content/broke_economist/reddit_queue.txt', 'a') as rf:
        rf.write(f"{data.get('title')} - {yt_url}\n")
    subprocess.run(["/root/.openclaw/workspace/venv/bin/python3", "/root/.openclaw/workspace/reddit_shorts_poster.py"], timeout=60)
except Exception as e:
    log(f"Failed to seed to reddit: {e}")

