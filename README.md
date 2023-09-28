
# OpenAI Chat Interface

The `openai_chat_interface.py` file contains the implementation of the `OpenAI_LLM` class, which provides an interface to interact with OpenAI's language models and manage chat interactions.

## Usage

To use the `OpenAI_LLM` class, import it as follows:

```python
from openai_chat_interface import OpenAI_LLM, create_message, calculate_cost
```

### Initialize OpenAI_LLM

Create an instance of `OpenAI_LLM`:

```python
llm = OpenAI_LLM(api_key=None, model="gpt-3.5-turbo", temperature=1.0, system_message='You are a helpful assistant. Answer the user query', user_message='{query}', functions=None, function_call=None)
```

The constructor takes the following parameters:

- `api_key` (optional): Your OpenAI API key. If not provided, it will attempt to load from the environment variable `OPENAI_API_KEY`.
- `model` (optional): The OpenAI language model to use. Default is "gpt-3.5-turbo".
- `temperature` (optional): The temperature value for generating responses. Default is 1.0.
- `system_message` (optional): The system message to be used in chat interactions. Default is `'You are a helpful assistant. Answer the user query'`.
- `user_message` (optional): The user message template to be used in chat interactions. Default is `'{query}'`.
- `functions` (optional): The list of functions to be used in chat interactions. Default is `None`.
- `function_call` (optional): The function call type to be used in chat interactions. Default is `"auto"`.

### Add Messages

Before running the model, you can add messages to the chat history. Use the `add_messages` method to add a list of messages:

```python
messages = [
    create_message("user", "What is the capital of France?"),
    create_message("assistant", "The capital of France is Paris.")
]
llm.add_messages(messages)
```

### Run the Model

To run the model and generate a response, use the `run` method:

```python
llm.run()
```

By default, this will use the user message template provided during initialization and generate a response based on the chat history.

You can also customize the user message used in this specific `run` call:

```python
llm.run(messages=[create_message("user", "What is the capital of Spain?")])
```

In this case, the provided messages will be used for this specific `run` call instead of the chat history.

### Access Response Content

After running the model, you can access the response content using the `response_content` property:

```python
response_content = llm.response_content
print(response_content)
```

### Access Response Message

You can access the response message object using the `response_message` property:

```python
response_message = llm.response_message
print(response_message)
```

### Access Response Function

If the response contains a function call, you can access the function call object using the `response_function` property:

```python
response_function = llm.response_function
print(response_function)
```

### Access Response Function Name

If the response contains a function call, you can access the function name using the `response_function_name` property:

```python
response_function_name = llm.response_function_name
print(response_function_name)
```

### Access Response Function Arguments

If the response contains a function call, you can access the function arguments using the `response_function_arguments` property:

```python
response_function_arguments = llm.response_function_arguments
print(response_function_arguments)
```

### Retrieve Finish Reason

After running the model, you can retrieve the finish reason using the `finish_reason` property:

```python
finish_reason = llm.finish_reason
print(finish_reason)
```

### Clear Memory

To clear the chat history, use the `clear_memory` method:

```python
llm.clear_memory()
```

## Example Files

The package provides example files that demonstrate the usage of the `OpenAI_LLM` class. You can refer to these examples to see how to utilize the chat interface effectively.

- `decorator_example.py`: Demonstrates the usage of the `@openaifunc` decorator and the `OpenAI_functions` class.
- `chat_and_func_example_single_tool_use.py`: Demonstrates the usage of the `OpenAI_LLM` class with a single tool use.
- `chat_and_func_example_multi_tool_use.py`: Demonstrates the usage of the `OpenAI_LLM` class with multiple tool uses.

Feel free to explore and modify these example files to understand how to use the `OpenAI_LLM` class effectively.



# OpenAI Function and Function Collection Classes

This Python package provides classes `OpenAI_functions`, `OpenAI_function_collection`, and `OpenAI_LLM` to dynamically load and manage Python functions marked with the `@openaifunc` decorator, and interact with OpenAI's language models. This utility can be used to organize and call functions from different modules easily, and to create chat interfaces with OpenAI's models.

## How to Use

### OpenAI_functions

(Existing content remains the same)

### OpenAI_function_collection

(Existing content remains the same)

### OpenAI_LLM

The `OpenAI_LLM` class provides an interface to interact with OpenAI's language models and manage chat interactions.

#### Example Usage

First, import the required classes and functions:

```python
from openai_chat_interface import OpenAI_LLM, create_message, calculate_cost
```

Create an instance of `OpenAI_LLM`:

```python
llm = OpenAI_LLM(api_key="your-api-key", system_message='You are a helpful assistant. Answer the user query')
```

You can run the model with user input:

```python
user_input = "What's the weather like today?"
llm.run(query=user_input)
print(llm.response_content)  # Outputs the model's response
```

You can add messages, clear messages, and perform various operations with the chat interface. See the `chat_example.py` file for a complete example.

## Function Descriptions

Function descriptions are extracted from the docstrings within the Python files. You can write standard Python docstrings to describe your functions:

```python
@openaifunc
def multiply_numbers(a: int, b: int) -> int:
    """
    This function multiplies two numbers.
    :param a: The first number to multiply
    :param b: The second number to multiply
    """
    return a * b
```

The `OpenAI_functions` class will automatically parse the docstrings and include them in the `func_description` property.

## Function Collection

The `OpenAI_function_collection` class allows you to manage multiple `OpenAI_functions` instances in one place. You can load functions from multiple files or an entire folder and access them all through the collection instance.

## Example Files

The repository includes example files demonstrating the usage of these classes, including `math_funcs.py`, `weather_funcs.py`, `main.py`, and `chat_example.py`. Feel free to explore and modify them to understand how to use the package effectively.
