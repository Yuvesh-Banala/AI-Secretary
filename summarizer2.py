
import os
from openai import OpenAI
import parsing

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN2"],
)


def summarize_text (text):
    completion = client.chat.completions.create(
        model="moonshotai/Kimi-K2-Instruct:groq",
        messages=[
            {
                "role": "user",
                "content": f"summarize the content of the following, {text}"
            }
        ],
)
    return completion.choices[0].message.content


# text = ""

# completion = client.chat.completions.create(
#     model="moonshotai/Kimi-K2-Instruct:groq",
#     messages=[
#         {
#             "role": "user",
#             "content": f"summarize the content of the following, {text}"
#         }
#     ],
# )

