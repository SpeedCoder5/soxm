# Lab08 - stories.py
# First, copy this lab to your notebooks folder.
# Then modify the parameters with your user namee and other values to your liking.
params = {
    'user': '5pghcqn52v@privaterelay.appleid.com',
    'model': 'gpt-3.5-turbo',
    'stories_count': 4,
    'topics': ['dogs', 'cats', 'birds'],
}

import io  # Importing the io module to enable in-memory file operations
import json
import pandas as pd
from dotenv import dotenv_values
import openai
from openai import OpenAI
from googleapiclient.http import MediaIoBaseUpload  # Importing the correct module for in-memory uploads
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import logging
from soxm.Paths import Paths

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the OpenAI API key exists
config = dotenv_values()
openai_api_key = config.get('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found in the environment variables.")

# Initialize OpenAI client
client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_api_key,
)

# Define a function to get a response from OpenAI API
def get_openai_response(input_text, model):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_text,
            }
        ],
        model=model,
    )
    return chat_completion.choices[0].message.content.strip()

# Define a function to get a story from OpenAI API
def get_openai_story(topic, model):
    prompt = f"Tell me a story about {topic}."
    response = get_openai_response(prompt, model)
    return response, prompt

# Collect stories in a list of dictionaries
stories = []
for topic in params['topics']:
    for _ in range(params['stories_count']):
        response, prompt = get_openai_story(topic, params['model'])
        stories.append({
            "Model": params['model'],
            "Topic": topic,
            "Prompt": prompt,
            "Response": response
        })

# Convert to a Pandas DataFrame
df = pd.DataFrame(stories)

# Set up Google Drive API
credentials_path = Paths.project('credentials.json') / 'credentials.json'
if not credentials_path.exists():
    raise ValueError(f"No credentials found. {credentials_path} must exist.")

scope = ["https://www.googleapis.com/auth/drive"]

logger.info('Authenticating with Google API using service account...')
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
drive_service = build('drive', 'v3', credentials=credentials)

# Your shared folder ID (replace with your actual folder ID)
parent_folder_id = config.get('DATA_RAW_FOLDER_ID')
if not parent_folder_id:
    raise ValueError("Google Drive folder ID not found in the environment variables.")

file_metadata = {
    'name': f'OpenAI_Stories_{params["user"]}.csv',
    'parents': [parent_folder_id],
    'mimeType': 'text/csv'
}

# Save the DataFrame to a CSV file in memory
csv_content = io.BytesIO()  # Using an in-memory file
df.to_csv(csv_content, index=False, encoding='utf-8')
csv_content.seek(0)  # Move the cursor to the beginning of the in-memory file

# Create the file in the specified folder
media = MediaIoBaseUpload(csv_content, mimetype='text/csv')  # Properly format the media_body
file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()

file_id = file.get('id')
webview_link = file.get('webViewLink')
logger.info(f"Uploaded CSV to Google Drive: {webview_link}")

