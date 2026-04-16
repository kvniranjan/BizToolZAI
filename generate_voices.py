import os, requests, concurrent.futures
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ELEVENLABS_API_KEY")

VOICES = {
    "Charlie": "IKne3meq5aSn9XLyUdCD",
    "George": "JBFqnCBsd6RMkjVDRZzb",
    "Eric": "cjVigY5qzO86Huf0OWal"
}

text = "The system is rigged, and they don't want you to know the formula. Buy, borrow, die."

def gen_voice(name_id):
    name, voice_id = name_id
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    data = {"text": text, "model_id": "eleven_monolingual_v1"}
    resp = requests.post(url, json=data, headers=headers)
    with open(f"{name}.mp3", "wb") as f:
        f.write(resp.content)
    return f"{name}.mp3"

with concurrent.futures.ThreadPoolExecutor() as ex:
    list(ex.map(gen_voice, VOICES.items()))
