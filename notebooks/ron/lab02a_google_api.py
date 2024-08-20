# lab02a_google_api.py - write some data to a google sheet on a google drive
# Install required libraries
#!pip install gspread oauth2client

from dotenv import dotenv_values
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
from soxm.Paths import Paths

# Ensure the credentials exist
credentials_path = Paths.project('credentials.json') / 'credentials.json'
if not credentials_path.exists():
    raise ValueError(f"No credentials found. {credentials_path} must exist.")

# Define the scope and load credentials from the dictionary
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

print('Authenticating with Google API using service account...')
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)

# Example: Create a new Google Sheet in a shared folder
from googleapiclient.discovery import build

drive_service = build('drive', 'v3', credentials=credentials)

# Your shared folder ID (replace with your actual folder ID)
config = dotenv_values()
parent_folder_id = config['DATA_RAW_FOLDER_ID']

file_metadata = {
    'name': 'TestColabGoogleSheet',
    'mimeType': 'application/vnd.google-apps.spreadsheet',
    'parents': [parent_folder_id]
}

# Create the file in the specified folder
file = drive_service.files().create(body=file_metadata,
                                    fields='id, webViewLink').execute()

spreadsheet_id = file.get('id')
print(f"Created Google Sheet: {file.get('webViewLink')}")

# Open the newly created Google Sheet
sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.get_worksheet(0)

# Define the data to be inserted
data = [
    ["firstname", "lastname"],
    ["john", "smith"],
    ["jane", "doe"]
]

# Insert the data into the sheet
for i, row in enumerate(data):
    worksheet.insert_row(row, i + 1)

# Read data from the sheet to verify
all_values = worksheet.get_all_values()
print("Sheet Data:")
for row in all_values:
    print(row)
