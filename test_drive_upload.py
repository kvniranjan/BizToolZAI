import json, os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

with open("drive_token.json") as f:
    t_dr = json.load(f)

creds_dr = Credentials(
    token=t_dr["token"], refresh_token=t_dr["refresh_token"],
    token_uri=t_dr["token_uri"], client_id=t_dr["client_id"],
    client_secret=t_dr["client_secret"], scopes=t_dr["scopes"]
)
if creds_dr.expired:
    creds_dr.refresh(Request())

dr = build("drive", "v3", credentials=creds_dr)
file_metadata = {
    'name': 'Broke_Economist_Feline_Test.mp4',
    'parents': ['10pRP2bL5IuhjgHqirZ_UIUftQdZqFA5-']
}
media_dr = MediaFileUpload('be_pipeline_test.mp4', mimetype='video/mp4')
file = dr.files().create(body=file_metadata, media_body=media_dr, fields='id').execute()
print(f"✅ Drive Success: File ID {file.get('id')}")
