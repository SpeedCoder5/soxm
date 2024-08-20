import query
from write2sheets import write2sheets
from reddit import searchreddit

def makerow(post, response, keyword):
    # prompt contains a 
    row = []
    row.append(str(response[1])) # Model used for response
    row.append(str(response[9])) # System prompt
    row.append(str(response[2])) # Temperature setting
    row.append(str(response[3])) # Max Tokens setting
    row.append(str(response[4])) # Top_p setting
    row.append(str(response[5])) # n setting (number of responses)
    row.append(str(response[6])) # frequency penalty setting
    row.append(str(response[7])) # presence penalty setting
    row.append(str(response[8])) # Prompt sent to ChatGPT
    row.append(str(keyword))     # Keyword to search REddit
    # Append the details of the found posts
    row.append(str(post[0]))
    row.append(str(post[1]))
    row.append(str(post[2]))
    row.append(str(post[3]))
    # Append the ChatGPT response
    row.append(str(response[0])) # The actual generated ChatGPT response
    return [row]
    

if __name__ == '__main__':
    # Search for a Reddit post using a keyword
    
    keyword = input('Subreddit to search: ')
    print(f'Searching reddit for {keyword}...')
    reddit_search_results = searchreddit(keyword, limit=10)
    print('Reddit search complete.')
        
    print('Querying ChatGPT and storing responses in Google Sheets...')
    for post in reddit_search_results:
        response = query.mainquery(post) # The main function from the query program that queries ChatGPT
        row = makerow(post, response, keyword)
        write2sheets(row)
    print("Data written successfully to Google Sheets!")