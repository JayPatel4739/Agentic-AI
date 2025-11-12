from tavily import TavilyClient
from groq import Groq
import json
import requests
import re

def web_search(query: str):
    tavily_client = TavilyClient(api_key="tavily_api_key")
    response = tavily_client.search(query)
    return json.dumps(response, indent=2)

def call_function(name, args):
    try:    
        if name == "web_search":
            return web_search(**args)

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


search_1 = call_llm(prompt="What is the update in AI space in this week?")
print(search_1)