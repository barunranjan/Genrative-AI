from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
     api_key="VALID_API_KEY",
     base_url="https://generativelanguage.googleapis.com/v1beta/"

)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"user", "content":"Hey there, can you tell me the llm model name, through which you are sending response"}
    ]
)
print(response.choices[0].message.content)