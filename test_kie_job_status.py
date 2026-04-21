import os, requests, json
from dotenv import load_dotenv

load_dotenv('/root/.openclaw/workspace/.env')
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers_kie = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}

print("Testing Kie.ai Record Info endpoint...")
try:
    r = requests.get("https://api.kie.ai/api/v1/jobs/recordInfo?taskId=123", headers=headers_kie, timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")
