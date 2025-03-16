import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

# ✅ Path to Your Service Account JSON Key File
SERVICE_ACCOUNT_FILE = "service_account.json"

# ✅ Google Drive API Scopes (Permissions)
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# ✅ Authenticate & Create Google Drive Service
try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive_service = build("drive", "v3", credentials=credentials)
    print("✅ Google Drive API Connected Successfully!")
except Exception as e:
    print("❌ ERROR: Google Drive API Authentication Failed!")
    print(str(e))
    exit()

# ✅ Google Drive Folder ID (Replace with your actual Drive folder ID)
FOLDER_ID = "1GbLIPtvxGdGxlLmob2ksuvZ1PpZaBYII"  # Ensure this is your correct folder ID

def upload_file(file_path, folder_id=FOLDER_ID):
    """
    Uploads a file to the specified Google Drive folder.
    """
    try:
        file_name = os.path.basename(file_path)

        # File metadata for upload
        file_metadata = {
            "name": file_name,
            "parents": [folder_id]  # Uploads file to the specified folder
        }

        # Upload the file
        media = MediaFileUpload(file_path, resumable=True)

        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

       # ✅ Ensure this is properly indented!
        Print(f"✅ File '{file_name}' uploaded successfully! File ID: {uploaded_file['id']}") 

    except Exception as e:
        print("❌ ERROR: File upload failed!")
        print(str(e))

# ✅ Test Uploading a File (Change "testfile.pdf" to your actual file name)

if __name__ == "__main__":
    test_file = "testfile.pdf"  

    if os.path.exists(test_file):
        upload_file(test_file)
    else:
        print(f"❌ ERROR: File '{test_file}' not found in the current directory.")
