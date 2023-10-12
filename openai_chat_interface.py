from openai_decorator import OpenAI_functions, OpenAI_function_collection
from tenacity import retry, wait_random_exponential, stop_after_attempt
from pprint import pprint
import copy
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

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

def create_message(role, content="", name=None, function_call=None, llm_response_function=None, function_call_result=None):
    message = {}
    message["role"] = role
    message["content"] = content
    if name:
        message["name"] = name
    if function_call:
        message["function_call"] = function_call
    if llm_response_function:
        message["name"] = llm_response_function.get('name')
        # Convert the function details to a string format
        func_detail = f"Function Name: {llm_response_function.get('name')}, Arguments: {llm_response_function.get('arguments')}"
        message["content"] += f"\n{func_detail}"
    if function_call_result:
        message["content"] += f"\nFunction Result: {function_call_result}"
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
        self.choices = None
        self.response = None  # Initialize the response attribute
        self.running_tokens = 0
        self.running_cost = 0

    def add_messages(self, messages):
        self.memory.extend(messages)

    def clear_memory(self):
        self.memory = []
        
    #@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(10))
    def _create_chat_completion(self, **kwargs_dict):
            # print(f"\n#################################\nkwargs_dict:")
            # print(kwargs_dict)
            # print(f"kwargs_dict end\n#################################\n")
            return openai.ChatCompletion.create(**kwargs_dict)
        
    def run(self, messages=None, functions=None, function_call=None, user_message=True, content_dict=None):
        if user_message:
            if messages is None:
                messages = [copy.deepcopy(self.user_message)]
            else:
                messages = copy.deepcopy(messages)
        else:
            messages = []

        processed_messages = []  # Store processed messages
        if messages:
            for message in messages:
                if content_dict:
                    try:
                        message['content'] = message['content'].format(**content_dict)
                    except KeyError as e:
                        print(f"KeyError: Keyword '{e.args[0]}' not provided. Message content: {message['content']}")
                processed_messages.append(message)

        combined_messages = [self.system_message] + self.memory + processed_messages
        kwargs_dict = {
            "model": self.model,
            "messages": combined_messages,
            "temperature": self.temperature
        }
        self.memory.extend(processed_messages)
        
        functions_to_use = functions if functions is not None else self.functions
        if functions_to_use:  # Check if the list is not empty
            kwargs_dict["functions"] = functions_to_use
            function_call_to_use = function_call if function_call is not None else self.function_call
            if function_call_to_use is not None:
                kwargs_dict["function_call"] = function_call_to_use
        try:
            response = self._create_chat_completion(**kwargs_dict)
            if response.choices and response.choices[0].message:
                self.choices = response.choices[0]
                self.response = response  # Store the whole response
                used_tokens = response['usage']['total_tokens']
                self.running_tokens += used_tokens
                self.running_cost += calculate_cost(self.model, used_tokens, "gbp")
        except openai.error.APIError as e:
            #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.error.APIConnectionError as e:
            #Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
            pass
        except openai.error.RateLimitError as e:
            #Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass

    @property
    def response_content(self):
        if self.choices:
            return self.choices['message']['content']
        else:
            return []

    @property
    def response_message(self):

        if self.choices:
            response_message_object = self.choices['message']
            response_message_dict = response_message_object.to_dict()
            return response_message_dict
        else:
            return []

    @property
    def response_function(self):
        if self.choices and 'function_call' in self.choices['message']:
            function_call_object = self.choices['message']['function_call']
            function_call_dict = function_call_object.to_dict()
            return function_call_dict
        else:
            return []

    @property
    def response_function_name(self):
        function_call_object = self.choices['message']['function_call']
        function_name = function_call_object['name'] if 'name' in function_call_object else None
        return function_name

    @property
    def response_function_arguments(self):
        function_call_object = self.choices['message']['function_call']
        function_arguments = function_call_object['arguments'].to_dict() if 'arguments' in function_call_object else None
        return function_arguments

    @property
    def finish_reason(self):
        if self.choices:
            return self.choices['finish_reason']
        else:
            return "No finish reason available"