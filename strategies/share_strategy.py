from abc import abstractmethod
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
import httplib2
import os

class ShareStrategy:
    @abstractmethod
    def share(self, title, content):
        pass

class EmailShareStrategy(ShareStrategy):
    def share(self, title, content):
        print(f"Sharing via Email: Title: {title}, Content: {content}")

class SocialMediaShareStrategy(ShareStrategy):
    def share(self, title, content):
        print(f"Sharing via Social Media: Title: {title}, Content: {content}")

class GoogleDriveShareStrategy(ShareStrategy):
    def share(self, title, content):
        CLIENT_SECRETS_FILE = "client_secrets.json"
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        STORAGE_FILE = "mycreds.txt"
        storage = Storage(STORAGE_FILE)
        credentials = storage.get()

        if not credentials or credentials.invalid:
            flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
            storage.put(credentials)

        http = credentials.authorize(httplib2.Http())
        drive_service = build('drive', 'v3', http=http)

        file_path = f"{title}.txt"
        with open(file_path, "w") as f:
            f.write(content)
        
        file_metadata = {'name': f"{title}.txt", 'mimeType': 'text/plain'}
        media = MediaFileUpload(file_path, mimetype='text/plain')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded to Google Drive: File ID {file.get('id')}")
        os.remove(file_path)