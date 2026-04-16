import json
import requests
from oauthlib.oauth2 import WebApplicationClient

with open("client_secret.json", "r") as f:
    creds = json.load(f)["installed"]

client_id = creds["client_id"]
client = WebApplicationClient(client_id)

auth_url = client.prepare_request_uri(
    "https://accounts.google.com/o/oauth2/auth",
    redirect_uri="http://localhost",
    scope=["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube"],
    access_type="offline",
    prompt="consent"
)
print(auth_url)
