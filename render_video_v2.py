import os, json, requests, base64, subprocess

GEMINI_KEY = "AIzaSyDYPMQD3puji9rX2sWAQpmt_FKk4J56_ow"
ELEVENLABS_KEY = "2430b417f4d4a39161a9164953d80c62ff4d5cf19734e73a9dba9094ac474949"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

os.makedirs("videos/audio", exist_ok=True)
os.makedirs("videos/images", exist_ok=True)
os.makedirs("videos/final", exist_ok=True)

# Get audio duration
audio_file = "videos/audio/voiceover.mp3"
result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", audio_file], capture_output=True, text=True)
audio_duration = float(result.stdout.strip())
print(f"⏱️  Audio duration: {audio_duration:.1f}s")

image_files = sorted([f for f in os.listdir("videos/images") if f.startswith("scene_")])
image_files = [f"videos/images/{f}" for f in image_files]
n = len(image_files)
dur_per_img = audio_duration / n
print(f"🖼️  {n} scenes × {dur_per_img:.1f}s each")

print("🎬 Rendering with simple scale+crossfade approach...")

# Build individual scene clips first, then concatenate
scene_files = []
for i, img in enumerate(image_files):
    out = f"/tmp/scene_{i}.mp4"
    # Simple: scale image to 1080x1920, display for dur_per_img seconds with fade in/out
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", img,
        "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fade=t=in:st=0:d=0.4,fade=t=out:st={dur_per_img-0.4:.2f}:d=0.4",
        "-t", str(dur_per_img),
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-r", "25",
        out
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        scene_files.append(out)
        print(f"  ✅ Scene {i+1} rendered")
    else:
        print(f"  ❌ Scene {i+1} failed: {result.stderr[-200:]}")

# Create concat list
concat_file = "/tmp/concat_list.txt"
with open(concat_file, "w") as f:
    for sf in scene_files:
        f.write(f"file '{sf}'\n")

# Concatenate all scenes
concat_output = "/tmp/video_only.mp4"
cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
       "-c", "copy", concat_output]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode != 0:
    print("❌ Concat failed:", result.stderr[-300:])
    exit(1)
print("✅ Scenes concatenated")

# Add audio
output_file = "videos/final/dyatlov_pass_v2.mp4"
cmd = ["ffmpeg", "-y",
       "-i", concat_output,
       "-i", audio_file,
       "-map", "0:v", "-map", "1:a",
       "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
       "-shortest",
       output_file]
result = subprocess.run(cmd, capture_output=True, text=True)
if result.returncode == 0:
    size = os.path.getsize(output_file) / (1024*1024)
    print(f"\n🏆 VIDEO RENDERED: {output_file} ({size:.1f} MB)")
else:
    print("❌ Audio merge failed:", result.stderr[-300:])
