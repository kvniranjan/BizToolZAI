import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# Using a professional/authoritative voice ID (Placeholder ID, defaulting to an ElevenLabs standard if needed, or using Adam/Antoni)
# "pNInz6obpgDQGcFmaJgB" is Adam (deep, authoritative)
VOICE_ID = "pNInz6obpgDQGcFmaJgB" 

SCRIPT_PATH = "/root/.openclaw/workspace/content/broke_economist/scripts/buy_borrow_die.md"
AUDIO_OUTPUT = "/root/.openclaw/workspace/content/broke_economist/audio/buy_borrow_die.mp3"

def extract_audio_text(md_filepath):
    print(f"Reading script from {md_filepath}...")
    with open(md_filepath, "r") as f:
        content = f.read()
    
    # Extract lines that start with **Audio:** or **Audio (Voiceover):**
    audio_lines = []
    for line in content.split("\n"):
        if line.startswith("**Audio"):
            # Strip out the bold prefix and quotes
            clean_text = re.sub(r'\*\*Audio.*?\:\*\*\s*', '', line).strip(' "')
            audio_lines.append(clean_text)
            
    full_audio = " ".join(audio_lines)
    print(f"Extracted {len(full_audio)} characters of audio text.")
    return full_audio

def generate_tts(text, output_path):
    print(f"Calling ElevenLabs API for {len(text)} characters...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Successfully saved audio to {output_path}")
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    print("🚀 Starting The Broke Economist Audio Engine...")
    text_to_speak = extract_audio_text(SCRIPT_PATH)
    if text_to_speak:
        generate_tts(text_to_speak, AUDIO_OUTPUT)
    else:
        print("No audio text found in script.")
