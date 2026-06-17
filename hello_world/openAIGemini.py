from openai import OpenAI 
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
     api_key=os.getenv("GEMINI_API_KEY"),
     base_url="https://generativelanguage.googleapis.com/v1beta/"

)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system", "content":"You are Math expert and you should only only answer math related question nothing else"},
        {"role":"user", "content":"give me answer of a + b whole square"}
    ]
)
print(response.choices[0].message.content)