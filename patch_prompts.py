import re

with open("/root/.openclaw/workspace/obscured_daily.py", "r") as f:
    content = f.read()

old_code = """images = []
for i, prompt in enumerate(data["image_prompts"]):
    img_path = f"{WORKSPACE}/videos/images/scene_{date_str}_{i+1}.jpg"
    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={GEMINI_KEY}",
        json={"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": "9:16"}},
        headers={"Content-Type": "application/json"}
    )
    if r.status_code == 200:
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(r.json()["predictions"][0]["bytesBase64Encoded"]))
        images.append(img_path)
        log(f"  ✅ Scene {i+1}")
    else:
        log(f"  ❌ Scene {i+1}: {r.text[:100]}")"""

new_code = """images = []
for i, prompt in enumerate(data["image_prompts"]):
    img_path = f"{WORKSPACE}/videos/images/scene_{date_str}_{i+1}.jpg"
    
    def fetch_img(p):
        return requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={GEMINI_KEY}",
            json={"instances": [{"prompt": p}], "parameters": {"sampleCount": 1, "aspectRatio": "9:16"}},
            headers={"Content-Type": "application/json"}
        )
        
    r = fetch_img(prompt)
    resp = r.json()
    
    if r.status_code == 200 and "predictions" in resp:
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(resp["predictions"][0]["bytesBase64Encoded"]))
        images.append(img_path)
        log(f"  ✅ Scene {i+1}")
    else:
        log(f"  ⚠️ Scene {i+1} failed (likely safety). Retrying with generic fallback prompt...")
        fallback = "Cinematic dark history background, atmospheric, moody, blank slate, highly detailed, 9:16 vertical"
        r = fetch_img(fallback)
        resp = r.json()
        if r.status_code == 200 and "predictions" in resp:
            with open(img_path, "wb") as f:
                f.write(base64.b64decode(resp["predictions"][0]["bytesBase64Encoded"]))
            images.append(img_path)
            log(f"  ✅ Scene {i+1} (Fallback)")
        else:
            log(f"  ❌ Scene {i+1}: {r.text[:100]}")"""

content = content.replace(old_code, new_code)

with open("/root/.openclaw/workspace/obscured_daily.py", "w") as f:
    f.write(content)
