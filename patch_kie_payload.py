import re

with open('/root/.openclaw/workspace/broke_economist_daily_bytedance.py', 'r') as f:
    code = f.read()

# Fix the payload structure in broke_economist_daily_bytedance.py
old_payload = '''    payload = {
        "model": "bytedance/seedance-2-fast",
        "params": {
            "prompt": p,
            "aspect_ratio": "9:16",
            "duration": 5,
            "web_search": False,
            "nsfw_checker": False
        }
    }'''

new_payload = '''    payload = {
        "model": "bytedance/seedance-2-fast",
        "input": {
            "prompt": p,
            "aspect_ratio": "9:16",
            "duration": 5,
            "web_search": False,
            "nsfw_checker": False
        }
    }'''

code = code.replace(old_payload, new_payload)

with open('/root/.openclaw/workspace/broke_economist_daily_bytedance.py', 'w') as f:
    f.write(code)

print("Kie API Payload patch applied!")
