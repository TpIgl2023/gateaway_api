import re
from urllib.parse import urlparse

import requests
from starlette.responses import JSONResponse

from Core.Environment.pdfServiceEnv import PDF_SERVICE_API_KEY, PDF_SERVICE_API_URL
from Core.Shared.DatabaseOperations import Database
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from Core.Configuration.GoogleDriveConfiguration.googleDriveConfiguration import CREDENTIALS_FILE_PATH , TOKEN_FILE_PATH
import concurrent.futures


def is_url(input_string):
    try:
        result = urlparse(input_string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def is_int(input_string):
    try:
        int(input_string)
        return True
    except ValueError:
        return False

async def isModerator(id):
    response = await Database.getAllModerators()
    if response.status_code != 200:
        return JSONResponse(status_code=500,
            content={
                "message": "Error while getting moderators",
                "error": "getting all moderators returned 404 status code , check if the database-service is running"
            })

    moderators = response.json()
    moderators = moderators["moderators"]

    if len(moderators) == 0:
        return "No moderators found"

    isMod = False
    for moderator in moderators:
        if moderator["id"] == id:
            isMod = True
            break

    return isMod

class GoogleDriveHandler:
    @staticmethod
    def extractGoogleDownloadLink(file_id):
        return f"https://drive.google.com/uc?id={file_id}&export=download"

    @staticmethod
    def extractGoogleFileId(previewLink):
        # Extract file ID from the preview link
        return previewLink.split("/file/d/")[1].split("/view")[0]

    @staticmethod
    def extractFolderId(folder_link):
        # Split the link using "/" and get the last segment
        folder_id = folder_link.split("/")[-1]

        # Remove additional parameters (if any) after the folder ID
        folder_id = folder_id.split("?")[0]

        return folder_id

    @staticmethod
    def isDriveLink(link):
        # Regular expression for Google Drive folder link
        drive_folder_pattern = re.compile(r'https://drive\.google\.com/drive/u/\d+/folders/[\w-]+')

        # Check if the link matches the pattern
        return bool(drive_folder_pattern.match(link))

def getDriveFilesId(driveId):

  """returns an array of IDs of files in the drive
  """
  # If modifying these scopes, delete the file token.json.
  SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(TOKEN_FILE_PATH):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE_PATH, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          CREDENTIALS_FILE_PATH, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(TOKEN_FILE_PATH, "w") as token:
      token.write(creds.to_json())

  service = build("drive", "v3", credentials=creds)

  # Call the Drive v3 API
  results = (
    service.files()
    .list(
        q=f"'{driveId}' in parents",
        fields="nextPageToken, files(id)")
    .execute()
  )
  items = results.get("files", [])
  id_strings = [item['id'] for item in items]
  return id_strings


def processMultiplePdf(downloadLinkArray):


    headers = {'x-api-key': PDF_SERVICE_API_KEY}
    payload =  {"URL" : downloadLinkArray}

    response = requests.post(PDF_SERVICE_API_URL+"/multiple", headers=headers, json=payload)
    response_json = response.json()

    return response_json



