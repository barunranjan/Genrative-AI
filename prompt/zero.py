from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

SYSTEM_PROMPT="You are Math expert and you should only only answer math related question nothing else"

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role":"user", "content":"can you tell me a joke"}

    ]
)

print(response.choices[0].message.content)
# In zero short prompting we give message to the model withour any prior example