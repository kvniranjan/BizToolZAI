import os, requests, json
from dotenv import load_dotenv

load_dotenv('/root/.openclaw/workspace/.env')
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers_kie = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}
payload = {
    "model": "luma/ray-2-720p",
    "params": {
        "prompt": "a simple test image of a red apple",
    }
}

print("Testing Kie.ai API Luma...")
try:
    r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=payload, headers=headers_kie, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")
