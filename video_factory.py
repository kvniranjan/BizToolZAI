import os
import json
import requests
import subprocess
from datetime import datetime

# Configurations
API_KEY_GEMINI = "AIzaSyDYPMQD3puji9rX2sWAQpmt_FKk4J56_ow"
API_KEY_ELEVENLABS = "2430b417f4d4a39161a9164953d80c62ff4d5cf19734e73a9dba9094ac474949"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb" # Brian - Deep, documentary voice
CHANNEL_NAME = "Obscured History"

# Setup Directories
os.makedirs("videos/raw", exist_ok=True)
os.makedirs("videos/audio", exist_ok=True)
os.makedirs("videos/images", exist_ok=True)
os.makedirs("videos/final", exist_ok=True)

def generate_script_and_prompts():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 Generating Script & Image Prompts via Gemini 2.5 Flash...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY_GEMINI}"
    
    prompt = """
    You are a viral YouTube Shorts scriptwriter for a channel called "Obscured History". 
    Write a 45-second script about a creepy, unsolved historical mystery. 
    The tone must be dark, documentary-style, and highly engaging. 
    
    Output strictly in JSON format like this:
    {
        "title": "The Title of the Short",
        "voiceover": "The full spoken text of the script. Do not include any visual directions here, just the words to be spoken.",
        "image_prompts": [
            "A cinematic, ultra-realistic, creepy historical photo of [scene 1], dark lighting, 9:16 aspect ratio",
            "A cinematic, ultra-realistic, creepy historical photo of [scene 2], dark lighting, 9:16 aspect ratio",
            "A cinematic, ultra-realistic, creepy historical photo of [scene 3], dark lighting, 9:16 aspect ratio"
        ]
    }
    """
    
    response = requests.post(url, headers={'Content-Type': 'application/json'}, json={"contents": [{"parts": [{"text": prompt}]}]})
    
    if response.status_code == 200:
        try:
            text = response.json()['candidates'][0]['content']['parts'][0]['text']
            # Clean markdown code blocks if Gemini returned them
            text = text.replace('```json\n', '').replace('```', '').strip()
            return json.loads(text)
        except Exception as e:
            print("Error parsing Gemini JSON:", e)
            return None
    else:
        print("Gemini API Error:", response.text)
        return None

def generate_voiceover(text, filename="videos/audio/voiceover.mp3"):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎙️ Generating Voiceover via ElevenLabs...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": API_KEY_ELEVENLABS
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
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ Voiceover saved to {filename}")
        return True
    else:
        print("ElevenLabs API Error:", response.text)
        return False

# Test the pipeline
if __name__ == "__main__":
    print("🚀 Initializing Obscured History Video Factory...")
    data = generate_script_and_prompts()
    if data:
        print(f"\n🎬 Title: {data['title']}")
        print(f"📜 Script: {data['voiceover']}")
        print("\n🖼️ Image Prompts to Generate:")
        for idx, p in enumerate(data['image_prompts']):
            print(f"   {idx+1}. {p}")
            
        # Test Voice Generation
        generate_voiceover(data['voiceover'])
