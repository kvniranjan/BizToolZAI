import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers = {
    "Authorization": f"Bearer {KIE_API_KEY}",
    "Content-Type": "application/json"
}

taskId = "1dd3669a5a56a1105a0b2b8ecd11bcbf"
url = f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={taskId}"

resp = requests.get(url, headers=headers).json()
print(resp['data']['state'])
if resp['data']['state'] == 'success':
    print(resp['data']['resultJson'])
