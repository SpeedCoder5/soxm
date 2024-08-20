# lab03b_reddit.py - searches reddit for a keyword and print the results found
import json
import praw
from soxm.Paths import Paths

print('---- lab03b_reddit.py ----')
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
reddit = praw.Reddit(
    client_id=reddit_credentials['client_id'],
    client_secret=reddit_credentials['client_secret'],
    user_agent=reddit_credentials['user_agent'],
    username=reddit_credentials['username'],
    password=reddit_credentials['password']
)

# Keyword to search for
keyword = "LeBron James"

print(f'---- searchinng for "{keyword}" ----')

# Search for posts across all subreddits
search_results = reddit.subreddit('all').search(keyword, sort='new', limit=10)

# Print the details of the found posts
for i, post in enumerate(search_results, 1):
    print(f"Post {i}:")
    print(f"Title: {post.title}")
    print(f"Author: {post.author}")
    print(f"Score: {post.score}")
    print(f"Subreddit: {post.subreddit}")
    print(f"URL: {post.url}")
    print(f"Selftext: {post.selftext}\n")

# Alternative: Narrow down the search to specific subreddits:
# subreddits_to_search = ['nba', 'sports', 'basketball']
# for subreddit in subreddits_to_search:
#     search_results = reddit.subreddit(subreddit).search(keyword, sort='new', limit=10)
#     # Print or process results as needed
