# lab03a_reddit.py - connects to reddit and retrieves a post from a subreddit
import json
import praw
from soxm.Paths import Paths

print('---- lab03a_reddit.py ----')
print('reading reddit_credentials.json')

# Ensure the credentials exist
credentials_path = Paths.project('reddit_credentials.json') / 'reddit_credentials.json'
if not credentials_path.exists():
    raise ValueError(f"No credentials found. {credentials_path} must exist.")

# Read the reddit_credentials.json file
with open(credentials_path) as f:
    reddit_credentials = json.load(f)

# Print the credentials
# print(reddit_credentials)

# Initialize a Reddit instance using the credentials
print('---- connecting to Reddit ----')
reddit = praw.Reddit(
    client_id=reddit_credentials['client_id'],
    client_secret=reddit_credentials['client_secret'],
    user_agent=reddit_credentials['user_agent'],
    username=reddit_credentials['username'],
    password=reddit_credentials['password']
)

# Specify the subreddit and the post ID you want to download
subreddit_name = 'clevelandcavs'
post_id = '1crdemj'

print(f'---- getting post {post_id} from subreddit {subreddit_name} ----')

# Get the subreddit
subreddit = reddit.subreddit(subreddit_name)

# Get the post
post = reddit.submission(id=post_id)

# Print the post details
print(f"Title: {post.title}")
print(f"Author: {post.author}")
print(f"Score: {post.score}")
print(f"URL: {post.url}")
print(f"Selftext: {post.selftext}")
print(f"Comments: {[comment.body for comment in post.comments]}")
