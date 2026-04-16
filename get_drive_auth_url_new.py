import json
from oauthlib.oauth2 import WebApplicationClient

with open("client_secret_drive.json", "r") as f:
    creds = json.load(f)["installed"]

client = WebApplicationClient(creds["client_id"])
auth_url = client.prepare_request_uri(
    "https://accounts.google.com/o/oauth2/auth",
    redirect_uri="http://localhost",
    scope=["https://www.googleapis.com/auth/drive.file"],
    access_type="offline",
    prompt="consent"
)
print(auth_url)
