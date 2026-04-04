import os
from moviepy.editor import VideoClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1920, 1080
audio = AudioFileClip('/root/.openclaw/workspace/content/broke_economist/audio/buy_borrow_die.mp3')
duration = audio.duration

# Try to use a nice font, or fallback to default
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
except:
    font = ImageFont.load_default()
    font_small = font

def make_frame(t):
    img = Image.new('RGB', (W, H), color=(18, 18, 18))
    draw = ImageDraw.Draw(img)
    
    # Calculate some visual changes based on time
    # We will do a pulsating subtle red gradient circle in the middle
    radius = 300 + 50 * np.sin(t * 2)
    
    # Just draw static text for now with a dynamic time counter
    title = "HOW BILLIONAIRES DODGE TAXES"
    subtitle = "BUY, BORROW, DIE"
    brand = "THE BROKE ECONOMIST"
    
    draw.text((W//2 - 600, H//2 - 100), title, font=font, fill=(255, 255, 255))
    draw.text((W//2 - 300, H//2 + 50), subtitle, font=font, fill=(255, 50, 50))
    draw.text((W//2 - 200, H - 100), brand, font=font_small, fill=(150, 150, 150))
    
    # Draw an audio wave simulation (randomish based on t)
    for i in range(40):
        h = 50 + 100 * abs(np.sin(t * 5 + i))
        draw.rectangle([W//2 - 400 + i*20, H//2 + 200 - h, W//2 - 400 + i*20 + 10, H//2 + 200 + h], fill=(200, 200, 200))
        
    return np.array(img)

clip = VideoClip(make_frame, duration=duration)
clip = clip.set_audio(audio)
clip.write_videofile('/root/.openclaw/workspace/content/broke_economist/output/buy_borrow_die_final.mp4', fps=10, preset='ultrafast', threads=4)
