from tavily import TavilyClient
from groq import Groq
import json
import requests
import re

def get_weather(location=None, lat=None, lon=None):
    if location:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid=[YOUR_API_KEY]"
    elif lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=[YOUR_API_KEY]"
    else:
        return "Error: Either location or lat/lon must be provided"
    
    response = requests.get(url)
    data = response.json()
    return data["main"]["temp"]

def web_search(query: str):
    tavily_client = TavilyClient(api_key="tavily_api_key")
    response = tavily_client.search(query)
    return json.dumps(response, indent=2)

def faq_db():
    with open('faq_db.txt', 'r') as file:
        content = file.read()
    return content

def call_function(name, args):
    try:    
        if name == "get_weather":
            return get_weather(**args)
        elif name == "web_search":
            return web_search(**args)
        elif name == "faq_db":
            return faq_db()
    except Exception as e:
        return f"Something went wrong"

def call_llm(prompt: str) -> str:
    client = Groq(api_key="grok_api_key")
    MODEL = 'qwen/qwen3-32b'

    tools = [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Perform a web search using the Tavily API to retrieve relevant information based on a query.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query string to look up on the web. Example: 'What is agentic AI?'",
                        },
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Retrieve current weather information for a specific location using the OpenWeather API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The name of the city or location to get the weather for. Example: 'London, UK'. Optional if lat and lon are provided.",
                        },
                        "lat": {
                            "type": "number",
                            "description": "Latitude of the location. Example: 51.5072",
                        },
                        "lon": {
                            "type": "number",
                            "description": "Longitude of the location. Example: -0.1276",
                        },
                    },
                    "required": ["location"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "faq_db",
                "description": "Retrieve the FAQ knowledge base content.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's question or query that needs to be answered using the FAQ database. Example: 'How can I reset my password?'"
                        }
                    },
                    "required": []
                }
            }
        }
    ]

    
    input_messages = [
        {"role": "system", "content": "Answer only with the final result. Do not show your thinking, reasoning, or process. Be extremely brief and direct."},
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=input_messages,
        tools=tools,
        tool_choice="auto",
    )
    
    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            function_result = call_function(function_name, function_args)

            input_messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call],
            })

            input_messages.append({
                "role": "function",
                "name": function_name,
                "content": str(function_result),
            })

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=input_messages,
    )

    text = final_response.choices[0].message.content
    cleaned = re.sub(r".*?</think>\s*", "", text, flags=re.DOTALL)
    return cleaned

calling_time = call_llm("Do you guys provide any trial?")
print(calling_time)