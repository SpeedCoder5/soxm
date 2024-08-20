import json
import praw
from soxm.Paths import Paths
from dotenv import dotenv_values
import openai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the Reddit credentials exist
reddit_credentials_path = Paths.project('reddit_credentials.json') / 'reddit_credentials.json'
if not reddit_credentials_path.exists():
    raise ValueError(f"No Reddit credentials found. {reddit_credentials_path} must exist.")

# Read the reddit_credentials.json file
with open(reddit_credentials_path) as f:
    reddit_credentials = json.load(f)

# Initialize a Reddit instance using the credentials
reddit = praw.Reddit(
    client_id=reddit_credentials['client_id'],
    client_secret=reddit_credentials['client_secret'],
    user_agent=reddit_credentials['user_agent'],
    username=reddit_credentials['username'],
    password=reddit_credentials['password']
)

# Ensure the OpenAI API key exists
config = dotenv_values()
openai_api_key = config.get('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found in the environment variables.")

# Initialize OpenAI client
openai.api_key = openai_api_key

# Define a function to get a response from OpenAI API
def get_openai_response(post_title, post_selftext, model):
    prompt = (f"You are an expert in behavioral maniupulation of people through the use of email and social media. You understand that news, advertising, and other information is often presented in ways to maximize engagement, and are able to distinguish between legitimate and malicious manipulation. If the there is no Selftext/content and you only receive the title of the article, respond with '_TEXTLESS_' unless the title itself manipulative, then you can continue on with the prompt. Examine the following post and determine if it might be manipulating the reader to believe something that is not true. If the post seems manipulative, describe why in less than two sentences."
              f"If it is not, then respond as '_SAFE_'.\n\n"
              f"Title: {post_title}\n\nContent: {post_selftext}")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"], prompt

# Set up Google Sheets and Drive API
credentials_path = Paths.project('credentials.json') / 'credentials.json'
if not credentials_path.exists():
    raise ValueError(f"No credentials found. {credentials_path} must exist.")

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

logger.info('Authenticating with Google API using service account...')
credentials = ServiceAccountCredentials.from_json_keyfile_name(str(credentials_path), scope)
gc = gspread.authorize(credentials)

drive_service = build('drive', 'v3', credentials=credentials)

# Your shared folder ID (replace with your actual folder ID)
parent_folder_id = config.get('DATA_RAW_FOLDER_ID')
if not parent_folder_id:
    raise ValueError("Google Drive folder ID not found in the environment variables.")

file_metadata = {
    'name': 'Reddit Lebron OpenAI Responses',
    'mimeType': 'application/vnd.google-apps.spreadsheet',
    'parents': [parent_folder_id]
}

# Create the file in the specified folder
file = drive_service.files().create(body=file_metadata, fields='id, webViewLink').execute()

spreadsheet_id = file.get('id')
webview_link = file.get('webViewLink')
logger.info(f"Created Google Sheet: {webview_link}")

# Open the newly created Google Sheet
sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.get_worksheet(0)

# Define the header
header = ["Title", "Author", "Score", "Subreddit", "URL", "Prompt", "Selftext", "OpenAI Response"]
worksheet.insert_row(header, 1)

# Keyword to search for on Reddit
keyword = "Lebron James"

# Search for posts across all subreddits
search_results = reddit.subreddit('all').search(keyword, sort='new', limit=10)

# Process and store the details of the found posts and OpenAI responses
model = "gpt-4-turbo"
for i, post in enumerate(search_results, 2):
    try:
        # Get OpenAI response for the post text
        openai_response, prompt = get_openai_response(post.title, post.selftext, model)

        # Prepare the data row
        row = [
            post.title,
            str(post.author),
            post.score,
            str(post.subreddit),
            post.url,
            prompt,
            post.selftext,
            openai_response
        ]

        # Insert the data into the sheet
        worksheet.insert_row(row, i)

    except Exception as e:
        logger.error(f"Error processing post: {post.url} - {e}")

# Adjust the column widths using the Sheets API
sheets_service = build('sheets', 'v4', credentials=credentials)

requests = [
    {
        "updateDimensionProperties": {
            "range": {
                "sheetId": worksheet.id,
                "dimension": "COLUMNS",
                "startIndex": 6,  # "Selftext" column (0-indexed)
                "endIndex": 7
            },
            "properties": {
                "pixelSize": 300
            },
            "fields": "pixelSize"
        }
    },
    {
        "updateDimensionProperties": {
            "range": {
                "sheetId": worksheet.id,
                "dimension": "COLUMNS",
                "startIndex": 7,  # "OpenAI Response" column (0-indexed)
                "endIndex": 8
            },
            "properties": {
                "pixelSize": 300
            },
            "fields": "pixelSize"
        }
    }
]

body = {
    'requests': requests
}

response = sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

logger.info(f"Data has been stored in Google Sheet: {webview_link}")
