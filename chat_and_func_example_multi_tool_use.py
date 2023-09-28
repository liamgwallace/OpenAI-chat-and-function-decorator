import os
from openai_decorator import OpenAI_functions, OpenAI_function_collection
from openai_chat_interface import OpenAI_LLM, create_message, calculate_cost
from dotenv import load_dotenv
from pprint import pprint

def run_query(user_query, llm, all_functions, memory_persist = False):
    if not memory_persist:
        llm.clear_memory()
    first_pass = True
    while True:
        if first_pass:
            llm.run(query=user_query)
            first_pass = False
        else:
            llm.run(user_message=False)

        print(f"\nFinish reason: '{llm.finish_reason}'")
        
        if llm.finish_reason == 'function_call':        
            print(f"\nAI function call:")
            pprint(llm.response_function)
            function_call_result = all_functions.call_func(llm.response_function)
            print(f"\nFunction call result:")
            pprint(function_call_result)

            function_message = create_message(
                "function",
                llm_response_function=llm.response_function,
                function_call_result=function_call_result
            )

            llm.add_messages([function_message])
            print(f"\nllm memory:")
            pprint(llm.memory)
        else:
            llm.add_messages([llm.response_message])
            return(llm.response_content)
def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment
    api_key = os.getenv("OPENAI_API_KEY")

    # Load functions
    math_functions = OpenAI_functions.from_file("tools/math_funcs.py")
    weather_functions = OpenAI_functions.from_file("tools/weather_funcs.py")
    all_functions = OpenAI_function_collection.from_folder("tools")

    # Initialize the language model with desired functions and parameters
    llm = OpenAI_LLM(api_key=api_key, model="gpt-3.5-turbo-16k", system_message='Utilize the tools and functions available to you only once to collect the necessary information for answering the users question. After obtaining a result from a function, use that information directly to provide an answer. Check if there is a response to your next function in the messages provided, do not repetitively call the same function.', functions=all_functions.func_list)


    while True:
        user_query = input(f"\ninput?\n")
        response = run_query(user_query, llm, all_functions, memory_persist=False)
        print(f"\nAI response: \n{response}")      
        print(f"\nRunning tokens: {llm.running_tokens}")
        print(f"Running cost: {llm.running_cost}")


if __name__ == "__main__":
    main()
