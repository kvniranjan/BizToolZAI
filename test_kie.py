import os
import requests
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers = {
    "Authorization": f"Bearer {KIE_API_KEY}",
    "Content-Type": "application/json"
}

try:
    response = requests.get("https://api.kie.ai/v1/models", headers=headers)
    print(response.json())
except Exception as e:
    print(e)
