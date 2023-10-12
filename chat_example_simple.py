import os
from dotenv import load_dotenv
from openai_chat_interface import OpenAI_LLM, create_message, calculate_cost

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Let's prompt the user for their name
user_name = input("Please enter your name: ")

# Content dictionary with the user's name
content_dict = {"name": user_name}

# Define the system and user messages
system_message = 'You are a general chatbot. Assist the user.'
user_message = 'Answer the query from {name}: {user_query}'

# Creating an LLM instance
llm_general = OpenAI_LLM(api_key=api_key, system_message=system_message, user_message=user_message)

# Choose which LLM to use (in this case, we only have one, but you can expand as needed)
llm = llm_general

while True:
    # Collecting user input
    user_input = input(f"\nHello {content_dict['name']}, what would you like to know?\n")
    content_dict["user_query"] = user_input  # Add user_input to content_dict
    
    # Running the chatbot with the user's message and content_dict
    llm.run(content_dict=content_dict)
    
    # Printing the AI's response
    print(f"\nAI response: \n{llm.response_content}\n")
    
    # Checking if the finish reason is 'finish'
    if llm.finish_reason == 'finish':
        print("The AI has finished its response.")
    
    # Monitoring costs
    print(f"Tokens used in this interaction: {llm.running_tokens}")
    print(f"Cost of this interaction: {llm.running_cost} GBP")
    
    # Example of using message history
    choice = input("\nWould you like to continue with the current chat history? (y/n)\n")
    if choice.lower() == 'n':
        llm.clear_memory()
        print("Chat history cleared!")
