from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, json

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

# Exchange the auth code for tokens
code = "4/1Aci98E_UHtyTSvG8gqauWzp25FHubT3dk-Bta7O6j_dMMps_IabOjTmD0pM"
flow.fetch_token(code=code)

creds = flow.credentials
with open("youtube_token.pickle", "wb") as f:
    pickle.dump(creds, f)

print("✅ Token saved!")
print(f"Access token: {creds.token[:30]}...")
print(f"Refresh token exists: {bool(creds.refresh_token)}")
print(f"Expires: {creds.expiry}")
