from dotenv import dotenv_values
import openai
from openai import OpenAI


def send_prompt_to_chatgpt(prompt, model, settings, user_api_key):
    client = OpenAI(api_key=user_api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": settings[6]},
            {"role": "user", "content": prompt}
            ],
        temperature=settings[0],
        max_tokens=settings[1],
        top_p=settings[2],
        n=settings[3],
        frequency_penalty=settings[4],
        presence_penalty=settings[5]
        )

    return completion.choices[0].message.content

def get_user_prompt():
    prompt = "Examine the following post and determine if it might be manipulating the reader to believe something that is not true. If the post seems manipulative, describe why. If it is not, then respond as _SAFE_.\nBEGIN POST\n"
    return prompt

def mainquery(post, model="gpt-3.5-turbo", temperature=1, max_tokens=256, top_p=1, n=1, frequency_penalty=0, presence_penalty=0):
    # Set up the OpenAI API key
    config = dotenv_values()
    openai.api_key = config['OPENAI_API_KEY']
    
    # Get the user's prompt
    user_prompt = get_user_prompt()
    prompt = f"{user_prompt}'\n'Title: {post[0]}\nAuthor: {post[1]}\nSubreddit: {post[2]}\nText: {post[3]}\nEND POST.\nGive two sentences describing why this post is or is not manipulative."
    
    system_query = "You are an expert in behavioral manipulation of people through the use of email and social media. You understand that news, advertising, and other information is often presented in ways to maximize engagement, and are able to distinguish between legitimate and malicious manipulation."
    
    # Settings are preset but can be adjusted in the function arguments
    settings = [temperature, max_tokens, top_p, n, frequency_penalty, presence_penalty, system_query]
    
    # Send the prompt to ChatGPT and get the response
    response = send_prompt_to_chatgpt(prompt, model, settings, openai.api_key)
    
    # Print the response
    return [response, model, settings[0], settings[1], settings[2], settings[3], settings[4], settings[5], user_prompt, system_query]

if __name__ == "__main__":
    examplepost = 'Lebron is an alien.'
    print(mainquery(examplepost))
