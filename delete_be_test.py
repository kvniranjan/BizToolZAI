import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

with open("youtube_token_be.json") as f:
    t_yt = json.load(f)

creds_yt = Credentials(
    token=t_yt["token"], refresh_token=t_yt["refresh_token"],
    token_uri=t_yt["token_uri"], client_id=t_yt["client_id"],
    client_secret=t_yt["client_secret"], scopes=t_yt["scopes"]
)
if creds_yt.expired:
    creds_yt.refresh(Request())

yt = build("youtube", "v3", credentials=creds_yt)
try:
    yt.videos().delete(id="5_5vd8nDb8M").execute()
    print("Deleted 5_5vd8nDb8M!")
except Exception as e:
    print(e)
