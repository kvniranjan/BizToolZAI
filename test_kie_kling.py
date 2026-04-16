import os
import requests
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers = {
    "Authorization": f"Bearer {KIE_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "kling-3.0/video",
    "input": {
        "mode": "std",
        "prompt": "A cat walking on a keyboard, cinematic lighting",
        "multi_shots": "0",
        "sound": "0",
        "duration": 5,
        "aspect_ratio": "9:16"
    }
}

try:
    resp = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=payload, headers=headers)
    print(resp.status_code, resp.text)
except Exception as e:
    print(e)
