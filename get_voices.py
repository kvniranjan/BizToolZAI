import os, requests
from dotenv import load_dotenv

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

headers = {"xi-api-key": ELEVENLABS_API_KEY}
resp = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
voices = resp.json().get("voices", [])

print("Available Voices:")
for v in voices:
    if v.get("category") == "premade" and v.get("labels", {}).get("gender") == "male":
        print(f"{v['name']} ({v['voice_id']}) - {v.get('labels', {}).get('description', '')}")
