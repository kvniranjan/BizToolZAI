import os, requests, json
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers = {
    "Authorization": f"Bearer {KIE_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "Generate an Orléans landscape image"
}

try:
    resp = requests.post("https://api.kie.ai/mj/submit/imagine", json=payload, headers=headers)
    print(f"Status Code: {resp.status_code}")
    print(resp.text[:200])
except Exception as e:
    print("Error:", e)
