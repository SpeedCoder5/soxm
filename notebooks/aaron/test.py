# Lab08 - stories.py
# First, copy this lab to your notebooks folder.
# Then modify the parameters with your user namee and other values to your liking.
params = {
    'user': 'aaron',
    'model': 'gpt-3.5-turbo',
    'stories_count': 4,
    'topics': ['lebron james', 'russell westbrook', 'steph curry'],
    'cluster_count': 3,
    'file_id':'1tyMEt6aHKwNA5Y0A9y6k7uYGbAn3Pxl-', # Replace with your actual file ID
    'n_components': 2, # UMAP setting
    'n_neighbors': 3, # UMAP setting
    'min_dist': 0.001, # UMAP setting
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
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import umap
import plotly.express as px
from sklearn.neighbors import NearestNeighbors
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import re

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


#def extract_file_id_from_link(link):
    #pattern = r"https://drive\.google\.com/file/d/([^/]+)/"
    #match = re.search(pattern, link)
    #if match:
        #return match.group(1)
    #return None

# Extract the file ID from the webview link
#extracted_file_id = extract_file_id_from_link(webview_link)
# print(extracted_file_id)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure the OpenAI API key exists
config = dotenv_values()
openai_api_key = config.get('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found in the environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Function to get embeddings from OpenAI API
def get_embeddings(text):
    response = client.embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

# Set up Google Drive API
credentials_path = Paths.project('credentials.json') / 'credentials.json'
if not credentials_path.exists():
    raise ValueError(f"No credentials found. {credentials_path} must exist.")

scope = ["https://www.googleapis.com/auth/drive"]

logger.info('Authenticating with Google API using service account...')
credentials = Credentials.from_service_account_file(credentials_path, scopes=scope)
drive_service = build('drive', 'v3', credentials=credentials)

# Your shared folder ID (replace with your actual folder ID)
parent_folder_id = config.get('DATA_RAW_FOLDER_ID')
if not parent_folder_id:
    raise ValueError("Google Drive folder ID not found in the environment variables.")

# ID of the file to read (replace with your actual file ID)
file_id = params['file_id']  

# Export the Google Sheet as a CSV file content from Google Drive
# request = drive_service.files().export_media(fileId=file_id, mimeType='text/csv') # use export_media if reading a google sheet as csv
request = drive_service.files().get_media(fileId=file_id) # use get_media to get a raw csv
csv_content = io.BytesIO()
downloader = MediaIoBaseDownload(csv_content, request)
done = False
while not done:
    status, done = downloader.next_chunk()
    logger.info(f"Download {int(status.progress() * 100)}% complete.")

csv_content.seek(0)  # Move the cursor to the beginning of the in-memory file

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_content)

# Create a new DataFrame to store results
results = []

# Iterate through each row in the DataFrame and generate embeddings
for index, row in df.iterrows():
    story = row['Response']
    embedding = get_embeddings(story)
    results.append({
        "Model": row['Model'],
        "Topic": row['Topic'],
        "Prompt": row['Prompt'],
        "Response": story,
        "Embedding": embedding
    })

# Convert the results to a DataFrame
df = pd.DataFrame(results)

# Display the results DataFrame
# print(df.head())

embedding_list = df['Embedding'].tolist()  # Directly use the 'Embedding' column as a list
umap_model = umap.UMAP(n_components=params['n_components'], n_neighbors=params['n_neighbors'], min_dist=params['min_dist'])
embedding_2d = umap_model.fit_transform(embedding_list)
# print(embedding_2d)
# print(embedding_2d.shape)

kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(embedding_2d)
# print(df.info())
# print(df)
# cluster2 = df[df['cluster'] == 2]
# print(cluster2)
# print(cluster2['Response'])
# responses = ' '.join(cluster2['Response'])
# print(responses)
# prompt = responses + " Please summarize the above text into a main topic in 4 words or less"
# print(prompt)
# topic = get_openai_response(prompt, 'gpt-3.5-turbo')
# print(topic)

# print(params['cluster_count'])
for x in range(params['cluster_count']):
    cluster = df[df['cluster'] == x]
    # print(cluster)
    # print(cluster['Response'])
    responses = ' '.join(cluster['Response'])
    # print(responses)
    prompt = responses + " Please summarize the above text into a main topic in 7 words or less"
    # print(prompt)
    topic = get_openai_response(prompt, params['model'])
    # print(topic)
    df.loc[df['cluster'] == x,'Summary'] = topic
print(df)