from together import Together
import os

#client = Together()
TOGETHER_API_KEY = os.getenv("TG_TOKEN")

def rank_emails(email_list):
    summaries = [] # will hold all the summaries from the email_list

    for email in email_list:
        summaries.append(email['summary'])
    
    #prompt the together api to rank the emails based on their summaries to my keywords
    keywords = ["College", "Scholarship" , "Internship"]

    #prompt the AI
    prompt = "You are helping prioritize emails for a Student. \n"
    prompt += f"The student is most interested in these keywords: {keywords}. \n"
    prompt += f"Here are the summaries: \n"

    for i, summary in enumerate(summaries):
        prompt += f"{i+1}. \"{summary}\"\n"


    prompt += "\nRank these emails from most to least important based on the keywords."
    prompt += f" Return your answer as a Python list of indices (0-based), like this: [2, 0, 1]"

    # Create the Together client
    client = Together(api_key=TOGETHER_API_KEY)

    # Model to use (you can swap this out if you like)
    MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=256
    )
    return completion.choices[0].message.content.strip()