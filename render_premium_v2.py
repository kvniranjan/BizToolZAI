import os, requests, subprocess, re
import whisper

ELEVENLABS_KEY = "sk_dfb370e328b5f99b4300f0f5635c250f76ec01e5c74218c3"
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"

SCRIPT = """February 1959. Nine experienced Russian hikers venture into the frozen Dyatlov Pass. They never return.

Weeks later, search parties discover their camp abandoned. The tent slashed open from the inside. Footprints lead into the deadly snow — some bare, some clad only in socks.

Two bodies found near a dying fire. Others scattered, partially clothed. Some with catastrophic internal injuries, yet no visible external wounds. One woman missing her tongue and eyes.

The official Soviet conclusion — a compelling unknown natural force.

Over sixty years later, the truth remains buried. What do you believe happened?"""

duration_target = 50  # seconds target

# Step 1: Generate voiceover
print("🎙️ Generating voiceover...")
r = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
    headers={"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"},
    json={"text": SCRIPT, "model_id": "eleven_monolingual_v1",
          "voice_settings": {"stability": 0.55, "similarity_boost": 0.75}}
)
audio_path = "videos/audio/voiceover_final.mp3"
with open(audio_path, "wb") as f: f.write(r.content)

res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", audio_path], capture_output=True, text=True)
duration = float(res.stdout.strip())
print(f"✅ Voiceover done — {duration:.1f}s")

# Step 2: Whisper captions
print("📝 Transcribing for captions...")
model = whisper.load_model("base")
result = model.transcribe(audio_path, word_timestamps=True)

srt_lines = []
idx = 1
for seg in result["segments"]:
    if "words" not in seg: continue
    words = seg["words"]
    chunk = 3
    for i in range(0, len(words), chunk):
        w = words[i:i+chunk]
        start, end = w[0]["start"], w[-1]["end"]
        text = " ".join(x["word"].strip() for x in w).upper()
        def t(s): return f"{int(s//3600):02d}:{int((s%3600)//60):02d}:{s%60:06.3f}".replace(".",",")
        srt_lines.append(f"{idx}\n{t(start)} --> {t(end)}\n{text}\n")
        idx += 1
srt_path = "videos/audio/captions.srt"
with open(srt_path, "w") as f: f.write("\n".join(srt_lines))
print(f"✅ {idx-1} caption chunks")

# Step 3: Render scenes with simple zoompan
images = sorted([f for f in os.listdir("videos/images") if f.startswith("scene_")])
images = [f"videos/images/{f}" for f in images]
n = len(images)
dpf = duration / n
print(f"🎬 Rendering {n} scenes × {dpf:.1f}s (zoompan)...")

scenes = []
for i, img in enumerate(images):
    out = f"/tmp/sc{i}.mp4"
    frames = int(dpf * 25) + 10
    cmd = ["ffmpeg", "-y", "-loop", "1", "-t", str(dpf + 1), "-i", img,
           "-vf", f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                  f"zoompan=z='min(zoom+0.0004,1.12)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=25,"
                  f"setsar=1,fade=t=in:st=0:d=0.4,fade=t=out:st={dpf-0.4:.2f}:d=0.4",
           "-t", str(dpf),
           "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "25", out]
    r2 = subprocess.run(cmd, capture_output=True, text=True)
    if r2.returncode == 0:
        scenes.append(out)
        print(f"  ✅ Scene {i+1}")
    else:
        # Fallback: simple scale only
        cmd2 = ["ffmpeg", "-y", "-loop", "1", "-t", str(dpf), "-i", img,
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1",
                "-c:v", "libx264", "-preset", "fast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "25", out]
        subprocess.run(cmd2, capture_output=True)
        scenes.append(out)
        print(f"  ⚠️  Scene {i+1} (fallback - no zoom)")

# Concatenate scenes
cl = "/tmp/cl.txt"
with open(cl,"w") as f:
    for s in scenes: f.write(f"file '{s}'\n")
vid = "/tmp/vid.mp4"
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",cl,"-c","copy",vid], capture_output=True)
print("✅ Scenes merged")

# Mix background music
music_mix = "/tmp/music_mix.mp3"
subprocess.run(["ffmpeg","-y","-i","videos/audio/background_music.mp3",
               "-t", str(duration),
               "-af", f"afade=t=in:st=0:d=2,afade=t=out:st={duration-3:.1f}:d=3,volume=0.07",
               music_mix], capture_output=True)
audio_mix = "/tmp/amix.mp3"
subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_mix,
               "-filter_complex","[0:a][1:a]amix=inputs=2:duration=first[a]",
               "-map","[a]","-c:a","aac","-b:a","192k", audio_mix], capture_output=True)
print("✅ Audio mixed")

# Burn captions + merge audio
output = "videos/final/dyatlov_premium.mp4"
cmd = ["ffmpeg","-y",
       "-i", vid, "-i", audio_mix,
       "-vf", f"subtitles={srt_path}:force_style='FontName=Arial,FontSize=18,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1,Alignment=2,MarginV=60'",
       "-map","0:v","-map","1:a",
       "-c:v","libx264","-preset","fast","-crf","20",
       "-c:a","copy","-shortest", output]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    size = os.path.getsize(output)/1024/1024
    print(f"\n🏆 PREMIUM VIDEO: {output} ({size:.1f} MB)")
else:
    print("❌ Caption merge failed:", res.stderr[-300:])
    # Final fallback: no captions
    cmd2 = ["ffmpeg","-y","-i",vid,"-i",audio_mix,"-map","0:v","-map","1:a",
            "-c:v","libx264","-preset","fast","-crf","20","-c:a","copy","-shortest", output]
    res2 = subprocess.run(cmd2, capture_output=True)
    if res2.returncode == 0:
        size = os.path.getsize(output)/1024/1024
        print(f"✅ Video (no captions): {output} ({size:.1f} MB)")
