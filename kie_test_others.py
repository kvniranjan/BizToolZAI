import os, requests
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")
headers = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}

models_to_test = [
    "runway/gen3",
    "kling-1.0/video",
    "kling-1.5/video",
    "kling-2.0/video",
    "luma-dream-machine/video"
]

for model in models_to_test:
    payload = {"model": model, "input": {"prompt": "test"}}
    r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=payload, headers=headers)
    print(f"Model: {model} -> {r.status_code} {r.text[:100]}")
