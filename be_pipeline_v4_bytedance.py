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
prompt = """You are 'The Broke Economist'. Write a 45-second YouTube Short script about 'Why Coffee Costs $8 Now'.
Tone: cynical, dark humor, exposing the game, aggressive pacing but sarcastic.
Format the output EXACTLY as valid JSON with no markdown formatting:
{
  "hook": "The first 3 seconds...",
  "voiceover": "The full voiceover text including the hook. No asterisks, no sound effect notes.",
  "prompts": [
    "A cinematic animated shot of a sad millennial paying for coffee with a gold bar, dark moody lighting",
    "A cinematic animated shot of a giant corporate coffee cup crushing a small wallet, dark studio lighting",
    "A cinematic animated shot of a yacht made entirely out of coffee beans, hyperrealistic"
  ]
}
Provide EXACTLY 3 prompts. Make them highly cinematic, dynamic camera movements for Bytedance Seedance Video Generation."""

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
MUSIC_FILE = f"{WORKSPACE}/Charlie.mp3"  # Standard aggressive/suspenseful track we have lying around
audio_mix = f"{BE_DIR}/audio_mixed.mp3"
if os.path.exists(MUSIC_FILE):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", audio_path,
        "-i", MUSIC_FILE,
        "-filter_complex", "[0:a]volume=1.2[a1];[1:a]volume=0.15[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=2[aout]",
        "-map", "[aout]", audio_mix
    ], capture_output=True, check=True)
else:
    log("Warning: Charlie.mp3 not found. Rendering without music.")
    audio_mix = audio_path

final_vid = f"{BE_DIR}/final.mp4"
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
if res.returncode != 0:
    log(f"FFmpeg failed: {res.stderr}")
else:
    log(f"✅ V4 Pipeline Render Complete! Saved to {final_vid}")

