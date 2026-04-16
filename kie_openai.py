import os, requests
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers = {
    "Authorization": f"Bearer {KIE_API_KEY}",
    "Content-Type": "application/json"
}

# The OpenAI compatible endpoint for text/image gen on Kie.ai
payload = {
    "model": "midjourney", 
    "prompt": "A cinematic shot of a banker crying --ar 9:16",
    "n": 1,
    "size": "1024x1024"
}

r = requests.post("https://api.kie.ai/v1/images/generations", json=payload, headers=headers)
print(f"Images endpoint: {r.status_code} {r.text[:200]}")
