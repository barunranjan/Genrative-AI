from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"user", "content":"Hey there, can you tell me the llm model name, through which you are sending response"}
    ]
)
print(response.choices[0].message.content)