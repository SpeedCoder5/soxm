import json
import praw
from soxm.Paths import Paths

# Ensure the credentials exist
credentials_path = Paths.project('reddit_credentials.json') / 'reddit_credentials.json'

# Read the reddit_credentials.json file
with open(credentials_path) as f:
    reddit_credentials = json.load(f)

# Initialize a Reddit instance using the credentials
reddit = praw.Reddit(
    client_id=reddit_credentials['client_id'],
    client_secret=reddit_credentials['client_secret'],
    user_agent=reddit_credentials['user_agent'],
    username=reddit_credentials['username'],
    password=reddit_credentials['password']
)
def searchreddit(keyword, limit=10):
    # Search for posts across all subreddits
    search_results =  reddit.subreddit(keyword).hot(limit=100)
    # print(search_results)

    # Create a list for things to pass to ChatGPT
    postlist = []
    
    # Print the details of the found posts
    for i, post in enumerate(search_results, 1):
        itemslist = []
        # print(f"Post {i}:")
        # print(f"Title: {post.title}")
        itemslist.append(post.title)
        # print(f"Author: {post.author}")
        itemslist.append(post.author)
        # print(f"Score: {post.score}")
        # print(f"Subreddit: {post.subreddit}")
        itemslist.append(post.subreddit)
        # print(f"URL: {post.url}")
        # print(f"Selftext: {post.selftext}\n")
        itemslist.append(post.selftext)
        postlist.append(itemslist)

    # Alternative: Narrow down the search to specific subreddits:
    # subreddits_to_search = ['nba', 'sports', 'basketball']
    # for subreddit in subreddits_to_search:
    #     search_results = reddit.subreddit(subreddit).search(keyword, sort='new', limit=10)
    #     # Print or process results as needed
    
    return postlist
    
if __name__ == '__main__':
    searchreddit(input("Reddit Search Keyword: "))