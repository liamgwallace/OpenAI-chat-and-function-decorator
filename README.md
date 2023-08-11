
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

(Existing content remains the same)

## Function Collection

(Existing content remains the same)

## Example Files

The repository includes example files demonstrating the usage of these classes, including `math_funcs.py`, `weather_funcs.py`, `main.py`, and `chat_example.py`. Feel free to explore and modify them to understand how to use the package effectively.
