from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
    )
response = client.models.generate_content(
    model="gemini-2.5-flash", contents="explain how AI works in few word, can you tell me the llm model name, through which you are sending response"
)
print(response.text)