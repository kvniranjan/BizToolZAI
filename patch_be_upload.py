file_path = '/root/.openclaw/workspace/broke_economist_daily_bytedance.py'
with open(file_path, 'r') as f:
    content = f.read()

# Make sure we add the YouTube upload block to the end of the script!
upload_block = """
log("6. Uploading to YouTube...")
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

with open("/root/.openclaw/workspace/youtube_token_be.json") as f:
    t_yt = json.load(f)

creds_yt = Credentials(
    token=t_yt["token"], refresh_token=t_yt["refresh_token"],
    token_uri=t_yt["token_uri"], client_id=t_yt["client_id"],
    client_secret=t_yt["client_secret"], scopes=t_yt["scopes"]
)
if creds_yt.expired:
    creds_yt.refresh(Request())

yt = build("youtube", "v3", credentials=creds_yt)

body = {
    "snippet": {
        "title": f"{data.get('title', 'The Broke Economist')} #Shorts",
        "description": f"{data.get('hook', '')}\\n\\n#finance #economics #money",
        "tags": ["finance", "economics", "money", "wealth"],
        "categoryId": "27"
    },
    "status": {
        "privacyStatus": "unlisted",
        "selfDeclaredMadeForKids": False
    }
}

media_yt = MediaFileUpload(final_vid, mimetype="video/mp4", resumable=True)
request = yt.videos().insert(part="snippet,status", body=body, media_body=media_yt)

response = None
while response is None:
    status, response = request.next_chunk()

yt_url = f"https://www.youtube.com/shorts/{response['id']}"
log(f"✅ YouTube Upload Success: {yt_url}")
"""

if "Uploading to YouTube" not in content:
    content += upload_block
    with open(file_path, 'w') as f:
        f.write(content)
    print("Added YouTube upload block to the daily script.")
else:
    print("YouTube upload block already exists.")
