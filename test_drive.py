from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'serviceAccountKey.json'
FOLDER_ID = '10pRP2bL5IuhjgHqirZ_UIUftQdZqFA5-'

def test_upload():
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)
        
        # Create a dummy file
        with open("test_upload.txt", "w") as f:
            f.write("Google Drive API integration successful!")
            
        file_metadata = {
            'name': 'connection_test.txt',
            'parents': [FOLDER_ID]
        }
        
        media = MediaFileUpload('test_upload.txt', mimetype='text/plain')
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        print(f"✅ Success! File ID: {file.get('id')}")
        os.remove("test_upload.txt")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    test_upload()
