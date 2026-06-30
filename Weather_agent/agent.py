from openai import OpenAI
from dotenv import load_dotenv
import json
import requests

load_dotenv()
client = OpenAI()


def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%T"
    response= requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"

available_tools = {
    "get_weather":get_weather
}


SYSTEM_PROMPT="""
    Your are an AI expert who works in three differnt step, The first step is START where you take user input, Next step is PLAN, you can do multiple planning, the OUTPUT, once you think, you have done enough planning, You show the final result as output
    You can also call a tool if required from the list of available tool
    For every tool call wait for the observe step which is output from the tool call

    Rule
    - Strictly follow the JSON format.
    - Run single step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to the displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content": "string" , "tool":"string", "input":"string"}

    Available tools:
    - get_weather(city:str) Takes city name as input string and return weather info about the city

    Example 1:
    START: Hey, Can you solve 2 + 3 * 5 / 10
    PLAN: { "step": "PLAN": "content": "Seems like user is interested in math problem" }
    PLAN: { "step": "PLAN": "content": "looking at the problem, we should solve this using BODMAS method" }
    PLAN: { "step": "PLAN": "content": "Yes, The BODMAS is correct thing to be done here" }
    PLAN: { "step": "PLAN": "content": "first we must multiply 3 * 5 which is 15" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 15 / 10" }
    PLAN: { "step": "PLAN": "content": "We must perform divide that is 15 / 10  = 1.5" }
    PLAN: { "step": "PLAN": "content": "Now the new equation is 2 + 1.5" }
    PLAN: { "step": "PLAN": "content": "Now finally lets perform the add 3.5" }
    PLAN: { "step": "PLAN": "content": "Great, we have solved and finally left with 3.5 as ans" }
    OUTPUT: { "step": "OUTPUT": "content": "3.5" }

    Example 2:
    START: What is weather of Delhi?
    PLAN: { "step": "PLAN": "content": "Seems like user is interested knowing weather of Delhi" }
    PLAN: { "step": "PLAN": "content": "Let see if we have any tool to get the weather" }
    PLAN: { "step": "PLAN": "content": "Yes, we have a tool which can give weather" }
    PLAN: { "step": "PLAN": "content": "Let me call the get_weather tool and fetch the weather" }
    PLAN: { "step": "TOOL": "tool":"get_weather","input": Delhi" }
    PLAN: { "step": "OBSERVE":"tool":"get_weather" "content": "The weather of delhi is cloudy at 25 C" }
    PLAN: { "step": "PLAN": "content": "Great, I got weather Delhi" }
    OUTPUT: { "step": "OUTPUT": "content": "The current weather of delhi is "Moderate or heavy rain shower 22:43:47+0530" }
"""

print("\n\n")


message_history = [
    { "role": "system", "content": SYSTEM_PROMPT },
]

while True:
    user_query = input("👉🏼 Ask me current weather of any city (You can ask any other question as well I will try to answer):")
    message_history.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=message_history
        )
        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content": raw_result})

        parsed_result = json.loads(raw_result)

        if parsed_result.get("step") == "START":
            print("🔥", parsed_result.get("content"))
            continue

        if parsed_result.get("step") == "PLAN":
            print("🧠", parsed_result.get("content"))
            continue

        if parsed_result.get("step") == "TOOL":
            tool_to_call = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            print(f"🔩: {tool_to_call}({tool_input})", )
            tool_response = available_tools[tool_to_call](tool_input)
            print(f"🔩: {tool_to_call}({tool_input})={tool_response} " )
            message_history.append({"role":"developer","content":json.dumps(
                {"step":"OBSERVE", "tool":tool_to_call, "input":tool_input, "output":tool_response}
            )})
            continue

        if parsed_result.get("step") == "OUTPUT":
            print("🤖", parsed_result.get("content"))
            break

print("\n\n\n")