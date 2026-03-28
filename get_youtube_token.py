from google_auth_oauthlib.flow import InstalledAppFlow
import json

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]

flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)

# Generate the auth URL manually (since we can't open a browser server-side)
flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

print("\n" + "="*60)
print("🔐 YOUTUBE AUTH REQUIRED")
print("="*60)
print("\n1. Open this URL in your browser (logged into obscuredhistoryofficial@gmail.com):")
print(f"\n{auth_url}\n")
print("2. Click 'Allow'")
print("3. Copy the authorization code shown")
print("4. Paste it back to BOSS in Telegram")
print("="*60)
