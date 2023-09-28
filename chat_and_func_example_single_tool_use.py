from openai_decorator import OpenAI_functions, OpenAI_function_collection
from openai_chat_interface import OpenAI_LLM, create_message, calculate_cost
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Example usage
math_functions = OpenAI_functions.from_file("tools/math_funcs.py")
weather_functions = OpenAI_functions.from_file("tools/weather_funcs.py")
all_functions = OpenAI_function_collection.from_folder("tools")

llm_math = OpenAI_LLM(api_key=api_key, system_message='respond to the user in ALLCAPS', functions=math_functions.func_list)
llm_weather = OpenAI_LLM(api_key=api_key, system_message='respond to the user in ALLCAPS', functions=weather_functions.func_list)
llm_all = OpenAI_LLM(api_key=api_key, system_message='respond to the user in ALLCAPS', functions=all_functions.func_list)
llm = llm_all

user_prompt = [create_message("user", "{query}")]
while True:
    user_query = input(f"\ninput?\n")
    llm.run(query=user_query)
    print(f"\nFinish reason: '{llm.finish_reason}'")
    if llm.finish_reason == 'function_call':        
        print(f"\nAI function call: \n{llm.response_function}")
        function_call_result = all_functions.call_func(llm.response_function)
        print(f"\nFunction call result: \n{function_call_result}")
        function_message = {
            "role": "function",
            "name": llm.response_function_name,
            "content": str(function_call_result)
        }
        llm.add_messages([function_message])
        print(f"\nllm memory: \n{llm.memory}")
    else:
        llm.add_messages([llm.response_message])
        print(llm.response_content)

    print(f"\nRunning tokens: {llm.running_tokens}")
    print(f"Running cost: {llm.running_cost}")