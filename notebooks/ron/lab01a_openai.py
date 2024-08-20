# lab01a_openai.py - Calls the OpenAI library and queries for a chat completion.
# This lab assumes you have already created and OPENAI_API_KEY and stored it in the project .env file.

from dotenv import dotenv_values
import openai
from openai import OpenAI

print(f'Using openai {openai.__version__}')
config = dotenv_values()
openai_api_key = config['OPENAI_API_KEY']

# First, iIn CoLab Secrets create a key named 'openai_soxm'
# and set the value to your open ai api key
client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_api_key,
)

# Define a function to get a response from OpenAI API
def get_openai_response(client, input_text, model):
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

# Model
model="gpt-3.5-turbo"

# Input sentence
input_sentence = "Once upon a time, in a land far, far away,"

print(f'---- {model} chat_completion request ---- ')
print(input_sentence)

print('\n---- response ----')

# Get OpenAI response
response = get_openai_response(client, input_sentence, model)

# Print the response
print(response)
