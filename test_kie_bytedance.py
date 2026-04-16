import os, requests, json, time
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers = {
    "Authorization": f"Bearer {KIE_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "bytedance/seedance-2-fast",
    "input": {
        "prompt": "A cinematic shot of a greedy wall street banker counting money, dark moody lighting",
        "generate_audio": False,
        "resolution": "720p",
        "aspect_ratio": "9:16",
        "duration": 5,
        "web_search": False,
        "nsfw_checker": False
    }
}

try:
    print("Testing bytedance/seedance-2-fast via Kie.ai...")
    resp = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=payload, headers=headers)
    print("Create:", resp.status_code, resp.text)
    
    if resp.status_code == 200:
        data = resp.json()
        task_id = data.get('data', {}).get('taskId')
        if task_id:
            print(f"Task ID: {task_id}. Polling...")
            for _ in range(5):
                time.sleep(5)
                poll = requests.get(f"https://api.kie.ai/api/v1/jobs/recordInfo?taskId={task_id}", headers=headers).json()
                state = poll.get('data', {}).get('state')
                print(f"State: {state}")
                if state == 'success':
                    print("Success!", poll.get('data', {}).get('resultJson'))
                    break
except Exception as e:
    print("Error:", e)
