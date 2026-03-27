import os, json, requests, base64, subprocess
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

GEMINI_KEY = "AIzaSyDtm_wNCZD77H5PsKs6Y_eG1jck9-FOc1k"
ELEVENLABS_KEY = "2430b417f4d4a39161a9164953d80c62ff4d5cf19734e73a9dba9094ac474949"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

os.makedirs("videos/audio", exist_ok=True)
os.makedirs("videos/images", exist_ok=True)
os.makedirs("videos/final", exist_ok=True)

# Step 1: Load existing Dyatlov script
script = {
    "title": "The Dyatlov Pass Incident",
    "voiceover": "February 1959. Nine experienced Russian hikers venture into the frozen Dyatlov Pass. They never return. Weeks later, search parties discover their camp abandoned, its tent slashed open from the inside. Their belongings left behind. Footprints lead into the deadly snow, some bare, some clad only in socks. Two bodies found near a dying fire. Others scattered, partially clothed. Some with catastrophic internal injuries yet no visible external wounds. One woman missing her tongue and eyes. Traces of radiation on their clothing. The official Soviet conclusion — a compelling unknown natural force. Over sixty years later, the truth of Dyatlov Pass remains buried. What do you believe happened?",
    "image_prompts": [
        "Cinematic ultra-realistic dark photo of nine bundled Russian hikers smiling in a bleak snowy mountain landscape, 1950s style, foreboding atmosphere, 9:16 vertical",
        "Cinematic ultra-realistic dark photo of an abandoned canvas tent in a snowy mountain pass, slashed open, equipment scattered, cold harsh lighting, 9:16 vertical",
        "Cinematic ultra-realistic dark photo of a dying campfire in a desolate snowy forest at night, shadows of trees, ominous and eerie, 9:16 vertical",
        "Cinematic ultra-realistic dark photo of weathered Soviet-era documents, blurred handwritten text, mysterious diagrams, dark moody lighting, 9:16 vertical"
    ]
}

# Step 2: Generate images via Imagen 4
print("🖼️  Generating images via Imagen 4...")
image_files = []
for i, prompt in enumerate(script["image_prompts"]):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={GEMINI_KEY}"
    payload = {"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1, "aspectRatio": "9:16"}}
    r = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    if r.status_code == 200:
        img_b64 = r.json()["predictions"][0]["bytesBase64Encoded"]
        img_path = f"videos/images/scene_{i+1}.jpg"
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(img_b64))
        image_files.append(img_path)
        print(f"  ✅ Scene {i+1} saved")
    else:
        print(f"  ❌ Scene {i+1} failed: {r.text[:100]}")

print(f"\n✅ {len(image_files)} images ready")

# Step 3: Voiceover already exists, check or regenerate
audio_file = "videos/audio/voiceover.mp3"
if not os.path.exists(audio_file):
    print("🎙️  Generating voiceover...")
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
        json={"text": script["voiceover"], "model_id": "eleven_monolingual_v1", "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}
    )
    if r.status_code == 200:
        with open(audio_file, "wb") as f: f.write(r.content)
        print("  ✅ Voiceover saved")
else:
    print("🎙️  Using existing voiceover")

# Step 4: Get audio duration
result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", audio_file], capture_output=True, text=True)
audio_duration = float(result.stdout.strip())
print(f"\n⏱️  Audio duration: {audio_duration:.1f}s")

# Step 5: Build ffmpeg command - Ken Burns zoom on each image + fade transitions
n = len(image_files)
dur_per_img = audio_duration / n
print(f"🎬  Rendering video ({n} scenes × {dur_per_img:.1f}s each)...")

# Build filter complex for Ken Burns effect + crossfade
filter_parts = []
overlay_parts = []

for i, img in enumerate(image_files):
    # Slow zoom in effect
    filter_parts.append(
        f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"zoompan=z='min(zoom+0.0007,1.5)':d={int(dur_per_img*25)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25,"
        f"setsar=1,fade=t=in:st=0:d=0.5,fade=t=out:st={dur_per_img-0.5:.2f}:d=0.5[v{i}]"
    )

concat_inputs = "".join([f"[v{i}]" for i in range(n)])
filter_parts.append(f"{concat_inputs}concat=n={n}:v=1:a=0[vout]")

filter_complex = ";".join(filter_parts)

# Input args
input_args = []
for img in image_files:
    input_args += ["-loop", "1", "-t", str(dur_per_img + 1), "-i", img]
input_args += ["-i", audio_file]

output_file = f"videos/final/dyatlov_pass.mp4"

cmd = ["ffmpeg", "-y"] + input_args + [
    "-filter_complex", filter_complex,
    "-map", "[vout]",
    "-map", f"{n}:a",
    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
    "-c:a", "aac", "-b:a", "192k",
    "-t", str(audio_duration),
    "-pix_fmt", "yuv420p",
    output_file
]

result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    size = os.path.getsize(output_file) / (1024*1024)
    print(f"\n🏆 VIDEO RENDERED: {output_file} ({size:.1f} MB)")
else:
    print("❌ ffmpeg error:", result.stderr[-500:])
