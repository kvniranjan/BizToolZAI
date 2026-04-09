import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

# Configuration
AUDIO_PATH = "/root/.openclaw/workspace/content/broke_economist/audio/buy_borrow_die.mp3"
PEXELS_DIR = "/root/.openclaw/workspace/content/broke_economist/images"
OUTPUT_PATH = "/root/.openclaw/workspace/content/broke_economist/output/buy_borrow_die_MASTER.mp4"

def build_master_video():
    print("🎬 Initializing Master Video Builder...")
    
    audio = AudioFileClip(AUDIO_PATH)
    total_duration = audio.duration
    print(f"🔊 Master Audio Duration: {total_duration} seconds")
    
    # Only load known good clips
    valid_clips = ['clip_0.mp4', 'clip_3.mp4', 'clip_4.mp4']
    stock_files = [os.path.join(PEXELS_DIR, f) for f in valid_clips]
    
    video_clips = []
    current_time = 0
    clip_duration = 5 
    
    # Pre-load clips to avoid constant disk reads/errors
    loaded_clips = [VideoFileClip(f).resize((1920, 1080)) for f in stock_files]
    
    while current_time < total_duration:
        raw_clip = random.choice(loaded_clips)
        
        # Make sure we don't request a subclip longer than the raw video
        max_start = max(0, raw_clip.duration - clip_duration)
        start_time = random.uniform(0, max_start)
        duration_needed = min(clip_duration, total_duration - current_time)
        
        # Extract subclip
        subclip = raw_clip.subclip(start_time, start_time + duration_needed)
        video_clips.append(subclip)
        
        current_time += duration_needed

    print(f"✂️ Stitched {len(video_clips)} individual cuts.")
    
    # 4. Concatenate the visual timeline
    final_visuals = concatenate_videoclips(video_clips, method="compose")
    
    # 5. Marry the Audio to the Visuals
    print("🎧 Merging Master Audio...")
    final_video = final_visuals.set_audio(audio)
    
    # 6. Render
    print(f"🔥 Rendering Master Video to {OUTPUT_PATH}...")
    # Lower fps and faster preset to ensure it renders without memory crashing
    final_video.write_videofile(OUTPUT_PATH, fps=24, preset='ultrafast', threads=2, audio_codec='aac', logger=None)
    print("✅ RENDER COMPLETE.")

if __name__ == "__main__":
    build_master_video()