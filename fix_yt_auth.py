import sys, json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
]

if len(sys.argv) < 2:
    print("Please provide the full redirected localhost URL or the auth code as an argument.")
    sys.exit(1)

code_input = sys.argv[1]
if "code=" in code_input:
    # Extract code from URL if they pasted the whole thing
    import urllib.parse as urlparse
    parsed = urlparse.urlparse(code_input)
    code = urlparse.parse_qs(parsed.query)['code'][0]
else:
    code = code_input

flow = InstalledAppFlow.from_client_secrets_file("/root/.openclaw/workspace/client_secret.json", SCOPES)
flow.redirect_uri = "http://localhost"
flow.fetch_token(code=code)

creds = flow.credentials

tok = {
    "token": creds.token,
    "refresh_token": creds.refresh_token,
    "client_id": creds.client_id,
    "client_secret": creds.client_secret,
    "token_uri": creds.token_uri,
    "scopes": SCOPES
}

with open("/root/.openclaw/workspace/youtube_token.json", "w") as f:
    json.dump(tok, f)

print("✅ Success! Token has been refreshed with the new scopes.")
