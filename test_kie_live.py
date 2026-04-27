import requests

KIE_API_KEY = "64c2816b293c1c6770848056e98c3b0a"
headers_kie = {"Authorization": f"Bearer {KIE_API_KEY}", "Content-Type": "application/json"}

# 1. Test balance
try:
    r = requests.get("https://api.kie.ai/api/v1/user/balance", headers=headers_kie, timeout=10)
    print("Balance Response:")
    print(r.text)
except Exception as e:
    print(f"Error checking balance: {e}")

# 2. Test createTask with "input" schema
payload = {
    "model": "bytedance/seedance-2-fast",
    "input": {
        "prompt": "a simple test image of a red apple, highly detailed, photorealistic",
        "aspect_ratio": "9:16",
        "duration": 5,
        "web_search": False,
        "nsfw_checker": False
    }
}

try:
    r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=payload, headers=headers_kie, timeout=10)
    print("\nCreateTask Response:")
    print(r.status_code)
    print(r.text)
except Exception as e:
    print(f"Error creating task: {e}")
