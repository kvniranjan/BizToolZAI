import os
import requests
import random
from moviepy.editor import VideoClip, AudioFileClip, VideoFileClip, concatenate_videoclips
from dotenv import load_dotenv

load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def get_pexels_video(query):
    print(f"Searching Pexels for: {query}")
    url = f"https://api.pexels.com/videos/search?query={query}&per_page=15&orientation=landscape"
    headers = {"Authorization": PEXELS_API_KEY}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('videos') and len(data['videos']) > 0:
            # Pick a random video from the top results to keep it fresh
            video_info = random.choice(data['videos'])
            
            # Find an HD link (1920x1080)
            best_link = None
            for file in video_info.get('video_files', []):
                if file['quality'] == 'hd' and file['width'] >= 1920:
                    best_link = file['link']
                    break
            
            # Fallback to any HD if 1920x1080 isn't found
            if not best_link:
                for file in video_info.get('video_files', []):
                    if file['quality'] == 'hd':
                        best_link = file['link']
                        break
                        
            return best_link
    print(f"Failed to find video for {query}")
    return None

def download_video(url, filename):
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
        return True
    return False

# Test the API
if __name__ == "__main__":
    queries = ["luxury yacht", "wall street", "mansion", "money counting", "taxes"]
    os.makedirs("/root/.openclaw/workspace/content/broke_economist/images", exist_ok=True)
    
    for i, q in enumerate(queries):
        url = get_pexels_video(q)
        if url:
            download_video(url, f"/root/.openclaw/workspace/content/broke_economist/images/clip_{i}.mp4")
            print(f"Success for query: {q}")
