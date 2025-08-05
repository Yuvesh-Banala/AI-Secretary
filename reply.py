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


#This function will take in the "reply code" value and then if the reply code is not 0
#it will skip over it
def checkreply(summary, subject, sender):
    reply_summary = "Reply Code: 0"

    if reply_summary in summary:
        return "No reply needed"
    
    elif "No summary available" in summary:
        return "No reply needed" 
    
    else:
        #Step 1: find out what is needed from the user
        response_query = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant preparing to write a reply to the following email."
            },
            {

                "role": "user",
                "content": f"""

                Context:
                - Sender: {sender}
                - Subject: {subject}
                - Summary: {summary}

                You are helping the user craft a reply to this email.
                Ask the user what personal details or information they need to provide to complete the reply 
                (for example, how they feel, which company they want to work for, etc.).
                The question should be direct, relevant, and assume the user is the one replying to the sender above.

                Return only the question.
                """
            }
            ],
            temperature=0.3,
            max_tokens=256
        )
        question = response_query.choices[0].message.content.strip()

        #Step 2: prompt back to the user and get a response
        print("\n📬 This email needs a reply.")
        print("🤖 The AI needs more information first:")
        print(f"👉 {question}\n")
        user_input = input("Your answer: ")

        #Step 3: return a final reply message from all the information
        
        reply_prompt = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are a helpful assistant writing a professional email reply.

                Email Summary:
                {summary}

                The user has provided this additional information:
                "{user_input}"

                You are writing in behalf of the user, who is responding to the email itself.
                The sender of the email  is who this email is being written for. 
                """
            }
            ],
            temperature=0.3,
            max_tokens=256
        )
    
        return reply_prompt.choices[0].message.content.strip()   


