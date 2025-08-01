# from together import Together

# def summarize_text(text: str):
#     client = Together()

#     stream = client.chat.completions.create(
#         model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
#         messages=[{"role": "user", "content": f"Summarize the following email:\n{text}"}],
#         stream=True,
#     )

#     summary = ""
#     for chunk in stream:
#         content = chunk.choices[0].delta.content
#         if content:
#             print(content, end="", flush=True)
#             summary += content
#     return summary


import os
from dotenv import load_dotenv
from together import Together

# Load environment variables from .env
load_dotenv()

# Get API key
TOGETHER_API_KEY = os.getenv("TG_TOKEN")
if TOGETHER_API_KEY is None:
    raise ValueError("TG_TOKEN is not set in environment variables")

# Create the Together client
client = Together(api_key=TOGETHER_API_KEY)

# Model to use (you can swap this out if you like)
MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

# Function to summarize email
def summarize_text(plain_body):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that summarizes briefly summarizes emails, including but not limited to upcoming meetings, dates, assignments, and news."
            },  
            {
                "role": "user",
                "content": f"Summarize this email:\n\n{plain_body}"
            }
        ],
        temperature=0.3,
        max_tokens=256
    )
    return completion.choices[0].message.content.strip()