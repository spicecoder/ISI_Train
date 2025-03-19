# chat_v1.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # Updated import
from langchain_core.messages import HumanMessage, SystemMessage  # Updated import

# Load OpenAI API key
load_dotenv()
# chat_v1.py
from langchain_openai import ChatOpenAI

def create_chat():
    # Specify model explicitly here
    return ChatOpenAI(
        temperature=0.7,
        model="gpt-3.5-turbo"  # Add this line to specify the model
    )
def create_chat():
    return ChatOpenAI(temperature=0.7)

def main():
    chat = create_chat()
    
    print("Welcome to SimpleChat! (type 'quit' to exit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        messages = [
            SystemMessage(content="You are a helpful AI assistant always ready to give correct answer ,say you dont know if you are not sure."),
            HumanMessage(content=user_input)
        ]
        
        response = chat(messages)
        print(f"\nAssistant: {response.content}")

if __name__ == "__main__":
    main()