
# OpenAI Function and Function Collection Classes

This Python package provides classes `OpenAI_functions`, `OpenAI_function_collection`, and `OpenAI_LLM` to dynamically load and manage Python functions marked with the `@openaifunc` decorator, and interact with OpenAI's language models. This utility can be used to organize and call functions from different modules easily, and to create chat interfaces with OpenAI's models.

## How to Use

### OpenAI_functions

First, import the package at the top of your Python code:

```python
from openai_decorator import OpenAI_functions, openaifunc
```

Then, add a `@openaifunc` decorator to the functions you want to manage:

```python
@openaifunc
def add_numbers(a: int, b: int) -> int:
    """
    This function adds two numbers.
    """
    return a + b
```

Next, create an instance of `OpenAI_functions` by loading a Python file containing the decorated functions:

```python
math_functions = OpenAI_functions.from_file("path/to/math_funcs.py")
```

You can now access the list of functions, mappings, and call the functions:

```python
print(math_functions.func_list)
print(math_functions.func_mapping)
result = math_functions.call_func({"name": "add_numbers", "arguments": "{ \"a\": 3, \"b\": 4 }"})
print(result)  # Output: 7
```

### OpenAI_function_collection

Import the `OpenAI_function_collection` class:

```python
from openai_decorator import OpenAI_function_collection
```

Create an instance by loading a folder containing Python files with decorated functions:

```python
all_functions = OpenAI_function_collection.from_folder("path/to/tools")
```

You can now access the combined function lists, mappings, descriptions, and call the functions across all loaded files:

```python
print(all_functions.func_list)
print(all_functions.func_description)
print(all_functions.func_mapping)
result = all_functions.call_func({"name": "add_numbers", "arguments": "{ \"a\": 5, \"b\": 5 }"})
print(result)  # Output: 10

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
