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

log(f"Title: {data['title']}")

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

# TODO: Add Whisper and FFmpeg stitching similar to obscured_daily
log("Pipeline integration complete! Ready for stitching.")
