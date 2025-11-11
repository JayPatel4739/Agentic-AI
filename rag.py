from groq import Groq
import json
import re

def faq_db():
    with open('groq/faq_db.txt', 'r') as f:
        return json.load(f)
    
def call_function(name):
    try:
        if name == "faq_db":
            return faq_db()
        
    except Exception as e:
        return f"Something went wrong: {str(e)}"

def call_llm(prompt: str) -> str:
    client = Groq(api_key=["your_api_key"])
    MODEL = 'qwen/qwen3-32b'

    tools = [
        {
            "type": "function",
            "function": {
                "name": "faq_db",
                "description": "Retrieve the most relevant answer from the FAQ knowledge base using a Retrieval-Augmented Generation (RAG) system.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's question or query that needs to be answered using the FAQ database. Example: 'How can I reset my password?'"
                        }
                    },
                    "required": ["query"]
                }
            }
        }
    ]

    input_messages = [
        {"role": "system", "content": "You are a helpful assistant that provides answers based on the FAQ knowledge base. Use the provided function to retrieve relevant information."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=input_messages,
        tools=tools,
        tool_choice="auto",
        temperature=0
    )

    if response.choices[0].message.tool_calls:
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            function_result = call_function(function_name)

            input_messages.append({
                "role": "assistant",
                "content": f"Function {function_name} returned: {function_result}"
            })

        final_response = client.chat.completions.create(
            model=MODEL,
            messages=input_messages,
            temperature=0
        )

        text = final_response.choices[0].message.content
        cleaned = re.sub(r".*?</think>\s*", "", text, flags=re.DOTALL)
        return cleaned
    

result = call_llm(input("Enter your question: "))
print(result)

