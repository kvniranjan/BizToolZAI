from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

flow = InstalledAppFlow.from_client_secrets_file("/root/.openclaw/workspace/client_secret.json", SCOPES)
flow.redirect_uri = "http://localhost"
auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

print(auth_url)
