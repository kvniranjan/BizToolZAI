import os
from moviepy.editor import *
import time

start = time.time()
clip = ColorClip(size=(1920, 1080), color=(15, 15, 15), duration=10)
txt = TextClip("Test", fontsize=70, color='white')
txt = txt.set_pos('center').set_duration(10)
video = CompositeVideoClip([clip, txt])
video.write_videofile("test.mp4", fps=24, preset='ultrafast')
print(f"Rendered in {time.time() - start} seconds")