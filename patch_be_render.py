file_path = '/root/.openclaw/workspace/build_be_master.py'
with open(file_path, 'r') as f:
    content = f.read()

# Change 1920x1080 to 1080x1920 with cropping
old_load = "loaded_clips = [VideoFileClip(f).resize((1920, 1080)) for f in stock_files]"
new_load = """
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
"""

if old_load in content:
    content = content.replace(old_load, new_load)
    with open(file_path, 'w') as f:
        f.write(content)
    print("Patched build_be_master.py for vertical video.")
else:
    print("Could not find line to patch in build_be_master.py")
