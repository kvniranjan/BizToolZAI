import requests

API_KEY = "sk_dfb370e328b5f99b4300f0f5635c250f76ec01e5c74218c3"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
    headers={"xi-api-key": API_KEY, "Content-Type": "application/json"},
    json={
        "text": "Testing. February 1959. Nine hikers vanished in the frozen pass.",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.55, "similarity_boost": 0.75}
    }
)

if r.status_code == 200:
    with open("/tmp/test_audio.mp3", "wb") as f:
        f.write(r.content)
    print(f"✅ Key works! Audio generated ({len(r.content)/1024:.1f} KB)")
else:
    print(f"❌ Error: {r.status_code} — {r.text}")
