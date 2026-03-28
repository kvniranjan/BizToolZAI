import os, requests, subprocess, json, re

ELEVENLABS_KEY = "sk_dfb370e328b5f99b4300f0f5635c250f76ec01e5c74218c3"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

# Clean script - NO markdown, pure spoken text
SCRIPT = """February 1959. Nine experienced Russian hikers venture into the frozen Dyatlov Pass. They never return.

Weeks later, search parties discover their camp abandoned. The tent slashed open from the inside. Their belongings left behind. Footprints lead into the deadly snow — some bare, some clad only in socks.

Two bodies found near a dying fire. Others scattered, partially clothed. Some with catastrophic internal injuries, yet no visible external wounds. One woman missing her tongue and eyes. Traces of radiation found on their clothing.

The official Soviet conclusion — a compelling unknown natural force.

Over sixty years later, the truth of Dyatlov Pass remains buried. What do you believe happened?"""

os.makedirs("videos/audio", exist_ok=True)
os.makedirs("videos/images", exist_ok=True)
os.makedirs("videos/final", exist_ok=True)

# Step 1: Generate clean voiceover
print("🎙️ Generating clean voiceover...")
r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
    headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
    json={"text": SCRIPT, "model_id": "eleven_monolingual_v1",
          "voice_settings": {"stability": 0.55, "similarity_boost": 0.75}}
)
if r.status_code == 200:
    with open("videos/audio/voiceover_final.mp3", "wb") as f:
        f.write(r.content)
    print("✅ Voiceover saved")
else:
    print("❌ ElevenLabs error:", r.text)
    exit(1)

# Get duration
result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", "videos/audio/voiceover_final.mp3"],
    capture_output=True, text=True)
duration = float(result.stdout.strip())
print(f"⏱️  Duration: {duration:.1f}s")

# Step 2: Generate captions with Whisper
print("📝 Generating captions with Whisper...")
import whisper
model = whisper.load_model("base")
result = model.transcribe("videos/audio/voiceover_final.mp3", word_timestamps=True)

# Build SRT subtitles - word by word for karaoke effect
srt_lines = []
idx = 1
for segment in result["segments"]:
    if "words" in segment:
        # Group into ~3 word chunks
        words = segment["words"]
        chunk_size = 3
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            start = chunk[0]["start"]
            end = chunk[-1]["end"]
            text = " ".join(w["word"].strip() for w in chunk).upper()
            
            def fmt_time(t):
                h, m, s = int(t//3600), int((t%3600)//60), t%60
                return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")
            
            srt_lines.append(f"{idx}\n{fmt_time(start)} --> {fmt_time(end)}\n{text}\n")
            idx += 1

srt_path = "videos/audio/captions.srt"
with open(srt_path, "w") as f:
    f.write("\n".join(srt_lines))
print(f"✅ Captions generated ({idx-1} chunks)")

# Step 3: Render each scene with Ken Burns zoom + dark vignette
image_files = sorted([f for f in os.listdir("videos/images") if f.startswith("scene_")])
image_files = [f"videos/images/{f}" for f in image_files]
n = len(image_files)
dur_per = duration / n
print(f"🎬 Rendering {n} scenes × {dur_per:.1f}s...")

scene_files = []
for i, img in enumerate(image_files):
    out = f"/tmp/scene_p{i}.mp4"
    # Ken Burns: slow zoom from 1.0 to 1.15 + dark vignette overlay
    zoom_expr = f"zoom='min(zoom+0.0005,1.15)'"
    vf = (
        f"scale=1200:2133:force_original_aspect_ratio=increase,"
        f"crop=1080:1920,"
        f"zoompan=z='{zoom_expr}':d={int(dur_per*25)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25,"
        f"curves=all='0/0 0.3/0.2 0.7/0.6 1/0.85',"
        f"vignette=angle=PI/4:mode=backward,"
        f"setsar=1,"
        f"fade=t=in:st=0:d=0.5,fade=t=out:st={dur_per-0.5:.2f}:d=0.5"
    )
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", img,
           "-vf", vf,
           "-t", str(dur_per + 0.5),
           "-c:v", "libx264", "-preset", "fast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-r", "25", out]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        scene_files.append(out)
        print(f"  ✅ Scene {i+1}")
    else:
        print(f"  ❌ Scene {i+1}: {res.stderr[-200:]}")

# Step 4: Concatenate scenes
concat_txt = "/tmp/concat_p.txt"
with open(concat_txt, "w") as f:
    for sf in scene_files:
        f.write(f"file '{sf}'\n")

video_only = "/tmp/video_only_p.mp4"
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
               "-c", "copy", video_only], capture_output=True)
print("✅ Scenes concatenated")

# Step 5: Trim background music and mix at low volume
music_trimmed = "/tmp/music_trimmed.mp3"
subprocess.run(["ffmpeg", "-y", "-i", "videos/audio/background_music.mp3",
               "-t", str(duration), "-af", "afade=t=in:st=0:d=2,afade=t=out:st={:.1f}:d=3,volume=0.08".format(duration-3),
               music_trimmed], capture_output=True)

# Mix voice + music
audio_mixed = "/tmp/audio_mixed.mp3"
subprocess.run(["ffmpeg", "-y",
               "-i", "videos/audio/voiceover_final.mp3",
               "-i", music_trimmed,
               "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout]",
               "-map", "[aout]", "-c:a", "aac", "-b:a", "192k", audio_mixed],
               capture_output=True)
print("✅ Audio mixed (voice + ambient music)")

# Step 6: Merge video + audio + burn captions
output = "videos/final/dyatlov_premium.mp4"

# Convert SRT to ASS for styled captions
ass_path = "/tmp/captions.ass"
subprocess.run(["ffmpeg", "-y", "-i", srt_path, ass_path], capture_output=True)

# Style the ASS captions - big, bold, centered, yellow
with open(ass_path, "r") as f:
    ass = f.read()
ass = ass.replace("Style: Default,Arial,20,", "Style: Default,Arial,72,")
ass = ass.replace("&H00FFFFFF", "&H0000FFFF")  # yellow
with open(ass_path, "w") as f:
    f.write(ass)

cmd = ["ffmpeg", "-y",
       "-i", video_only,
       "-i", audio_mixed,
       "-vf", f"ass={ass_path}",
       "-map", "0:v", "-map", "1:a",
       "-c:v", "libx264", "-preset", "fast", "-crf", "20",
       "-c:a", "copy", "-shortest", output]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    size = os.path.getsize(output) / (1024*1024)
    print(f"\n🏆 PREMIUM VIDEO DONE: {output} ({size:.1f} MB)")
else:
    print("❌ Final merge failed:", res.stderr[-400:])
