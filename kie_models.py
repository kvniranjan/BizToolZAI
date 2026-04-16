import os
import requests
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers = {
    "Authorization": f"Bearer {KIE_API_KEY}",
    "Content-Type": "application/json"
}

url = "https://api.kie.ai/api/v1/models"
try:
    resp = requests.get(url, headers=headers)
    print(f"Status Code: {resp.status_code}")
    print(resp.json())
except Exception as e:
    print(f"Error: {e}")
