## What to do to make ai workflows/agents with python?

1. Import your modules (just a basic step).
2. Make a function for the tool like for weather provide it access to any weather tool(i.e. openweather), for rag build it which has access to your data, etc.
3. Make a function to call the tool.
4. Then make a llm_call where you will have llm completion, then tool description.
5. Then just call the llm_call function.

This the 5 simple steps to make the ai workflows/agents with python.

So, for this all ai workflows/agents I have used GroqCloud's API because it is `FREE` 😂.
## Why I have used regex?

So, as I am using `qwen/qwen3-32b` model from GroqCloud, the output aslo contains the thinking of the model, so to extract the required answer from the output I have used regex.

## weather_tool

I have used openweather's api to get the weather information and for the ai model calls I have used GroqCloud. 

### Code explanation 
1. First I have imported the required modules like requests for api calls, json for handling json data.
2. Then I have made a function `get_weather`, now here I've made some conditions like if llm is not able to provide the latitudes and longitudes then it will take the location and provide me the weather information and if llm provides it then it will give me weather information according to that.
3. Then the function to call `get_weather` function.
4. Then the `llm_call` function where I have provided the llm completion and tool description. So, here for the first llm call the llm will provide the latitudes and longitudes if possible, it will make the argument for `call_function` which will then add that arguments into `get_weather` function, then the for the append part, the arguments provided by the llm and the result from the tool will be appended to input_messages, then the final llm call will provide the final answer.

## web_search

Here I have used tavily's API to search web.

### Code explanation 
It is same as previous one's just some changes in tool function and tool description and everything is same as previous ones.

## combined_agent

This is just the combination of all the above agents/workflow