import requests
import base64

API_KEY = "AIzaSyDYPMQD3puji9rX2sWAQpmt_FKk4J56_ow"
url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"

payload = {
    "instances": [
        {
            "prompt": "A professional YouTube channel logo for 'Obscured History'. Dark, moody, minimalist. A glowing ancient eye inside a cracked, weathered stone archway or circle. Deep black background. Subtle gold and crimson accents. Misty fog at the base. Cinematic, premium, mysterious aesthetic. Square format, centered composition. No text or letters."
        }
    ],
    "parameters": {
        "sampleCount": 1,
        "aspectRatio": "1:1"
    }
}

print("🎨 Generating Obscured History channel logo via Imagen 4...")
response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)

if response.status_code == 200:
    data = response.json()
    img_base64 = data["predictions"][0]["bytesBase64Encoded"]
    img_bytes = base64.b64decode(img_base64)
    with open("videos/images/channel_logo.png", "wb") as f:
        f.write(img_bytes)
    print("✅ Logo saved to videos/images/channel_logo.png")
else:
    print("❌ Error:", response.status_code, response.text)
