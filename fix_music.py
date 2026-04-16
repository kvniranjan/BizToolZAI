with open("obscured_daily.py", "r") as f:
    code = f.read()

# Fix the double-dipping volume
code = code.replace(
    'subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_mix,\n               "-filter_complex","[1:a]volume=0.07[bg];[0:a][bg]amix=inputs=2:duration=first[out]",\n               "-map","[out]", audio_mix], capture_output=True)',
    'subprocess.run(["ffmpeg","-y","-i",audio_path,"-i",music_mix,\n               "-filter_complex","[0:a]volume=1.0[v];[1:a]volume=1.0[bg];[v][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",\n               "-map","[out]", audio_mix], capture_output=True)'
)

# And let's bump the initial volume from 0.07 to 0.15 so it's actually audible.
code = code.replace('volume=0.07', 'volume=0.15')

with open("obscured_daily.py", "w") as f:
    f.write(code)

print("Music bug patched!")
