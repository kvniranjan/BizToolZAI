import os, requests, json, time
from dotenv import load_dotenv

load_dotenv()
KIE_API_KEY = os.getenv("KIE_API_KEY")

headers = {
    "Authorization": f"Bearer {KIE_API_KEY}",
    "Content-Type": "application/json"
}

# The payload format inferred from the provided response example
# Sometimes the model name IS the taskType or it expects an exact endpoint
payload = {
    "model": "midjourney", 
    "input": {
        "prompt": "Generate an Orléans landscape image",
        "aspectRatio": "1:1",
        "speed": "fast",
        "stylization": 100,
        "taskType": "mj_txt2img",
        "version": "7"
    }
}

models_to_test = ["midjourney-v6", "midjourney-v7", "mj-txt2img", "midjourney/txt2img", "mj/txt2img"]

for m in models_to_test:
    payload["model"] = m
    r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=payload, headers=headers)
    print(f"{m}: {r.status_code} {r.text[:100]}")
