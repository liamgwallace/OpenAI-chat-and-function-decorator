from openai_decorator import func_list_from_file, get_openai_funcs, openaifunc
from pprint import pprint
import copy
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

def calculate_cost(model_name, token_count, currency):
    model_data = {
        "gpt-4": {"usd": 0.045, "gbp": 0.045 * 0.79},
        "gpt-4-0613": {"usd": 0.045, "gbp": 0.045 * 0.79},
        "gpt-4-32k": {"usd": 0.090, "gbp": 0.090 * 0.79},
        "gpt-4-32k-0613": {"usd": 0.090, "gbp": 0.090 * 0.79},
        "gpt-3.5-turbo": {"usd": 0.00175, "gbp": 0.00175 * 0.79},
        "gpt-3.5-turbo-16k": {"usd": 0.00350, "gbp": 0.00350 * 0.79},
        "gpt-3.5-turbo-0613": {"usd": 0.00175, "gbp": 0.00175 * 0.79},
        "gpt-3.5-turbo-16k-0613": {"usd": 0.00350, "gbp": 0.00350 * 0.79}
    }
    
    model_currency_data = model_data.get(model_name.lower())
    if not model_currency_data:
        return "Invalid model name"
    
    cost = model_currency_data[currency.lower()] * (token_count / 1000)
    return cost

def create_message(role, content, name=None, function_call=None):
    message = {
        "role": role,
        "content": content
    }
    if name:
        message["name"] = name
    if function_call:
        message["function_call"] = function_call
    return message

class OpenAI_LLM:
    def __init__(self, api_key=None, model="gpt-3.5-turbo", temperature=1.0, system_message='You are a helpful assistant. Answer the user query', user_message='{query}', functions=None, function_call=None):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")  # Load from .env file if not provided
        openai.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.system_message = create_message('system', system_message)
        self.user_message = create_message('user', user_message)
        self.functions = functions if functions else []
        self.function_call = function_call if function_call else "auto"
        self.memory = []
        self.response = None  # Initialize the response attribute
        self.running_tokens = 0
        self.running_cost = 0

    def add_messages(self, messages):
        self.memory.extend(messages)

    def clear_messages(self):
        self.memory = []

    def run(self, messages=None, functions=None, function_call=None, **kwargs):
        if messages is None:
            messages = [copy.deepcopy(self.user_message)]
        tmp_messages = copy.deepcopy(messages)
        processed_messages = []  # Store processed messages
        for message in tmp_messages:
            if kwargs:
                try:
                    message['content'] = message['content'].format(**kwargs)
                except KeyError as e:
                    print(f"KeyError: Keyword '{e.args[0]}' not provided. Message content: {message['content']}")
            processed_messages.append(message)
        
        self.memory.extend(processed_messages)
        combined_messages = [self.system_message] + self.memory

        # Prepare the keyword arguments dictionary
        kwargs_dict = {
            "model": self.model,
            "messages": combined_messages,
            "temperature": self.temperature
        }
        # If functions are passed to the run method, use them; otherwise, use the class instance's functions
        functions_to_use = functions if functions is not None else self.functions

        # If there are functions to use, add them to kwargs_dict
        if functions_to_use is not None:
            kwargs_dict["functions"] = functions_to_use

            # If function_call is provided, use it; otherwise, use the class instance's function_call
            function_call_to_use = function_call if function_call is not None else self.function_call

            # If there's a function_call to use, add it to kwargs_dict
            if function_call_to_use is not None:
                kwargs_dict["function_call"] = function_call_to_use
        try:
            response = openai.ChatCompletion.create(**kwargs_dict)
            if response.choices and response.choices[0].message:
                self.response = response.choices[0].message
                used_tokens = response['usage']['total_tokens']
                self.running_tokens += used_tokens
                self.running_cost += calculate_cost(self.model, used_tokens, "gbp")
        except openai.error.OpenAIError as e:
            print("OpenAIError:", e)

    def get_response_content(self):
        if self.response:
            return self.response['content']
        else:
            return "No response available"

    def get_response_function(self):
        if self.response:
            return self.response['function_call']
        else:
            return "No function available"

# Example usage


# Create math_func_list from math_funcs.py
math_func_list, math_func_mapping = func_list_from_file("math_funcs.py")
weather_func_list, weather_func_mapping = func_list_from_file("weather_funcs.py")

llm = OpenAI_LLM(api_key, system_message='respond to the user in ALLCAPS', functions = weather_func_list)    

user_prompt = [
    create_message("user", "{foo}")
]
while True:
    user = input("input?")
    llm.run(query=user)
    print(llm.get_response_content())
    print(llm.get_response_function())
    print("Running tokens:", llm.running_tokens)
    print("Running cost:", llm.running_cost)

