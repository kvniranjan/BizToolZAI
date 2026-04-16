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
    
    # Resize and crop to 9:16 vertical format (1080x1920) for YouTube Shorts
    loaded_clips = []
    for f in stock_files:
        clip = VideoFileClip(f)
        # Crop center to 9:16
        w, h = clip.size
        target_ratio = 1080 / 1920
        clip_ratio = w / h
        if clip_ratio > target_ratio:
            # Crop width
            new_w = int(h * target_ratio)
            x_center = w / 2
            clip = clip.crop(x1=x_center - new_w/2, y1=0, x2=x_center + new_w/2, y2=h)
        else:
            # Crop height
            new_h = int(w / target_ratio)
            y_center = h / 2
            clip = clip.crop(x1=0, y1=y_center - new_h/2, x2=w, y2=y_center + new_h/2)
        
        clip = clip.resize((1080, 1920))
        loaded_clips.append(clip)

    
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