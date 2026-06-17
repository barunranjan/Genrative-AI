from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT="""
You are Math expert and you should only only answer math related question nothing else

Rule:
- Strictly follow output in the JSON format

Output Format:{{
"answer" : "string" or null,
"isMathQuestion : boolean
}}

Examples:
Q: Can you explain a a + b whole square
A: {{answer: $a^2 + 2ab + b^2$, isMathQuestion:true}}

Q: can you tell me a joke
A: {{answer: null, isMathQuestion:false}}
"""


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role":"user", "content":"can you tell me a joke"}

    ]
)

print(response.choices[0].message.content)
# In few short prompting along with direct instruction, we provide the example as well 