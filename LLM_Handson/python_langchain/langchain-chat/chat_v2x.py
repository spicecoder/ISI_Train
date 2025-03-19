# chat_v2x.py
import os
from dotenv import load_dotenv
from langchain_community.callbacks.manager import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

def create_chain():
    chat = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
    memory = ConversationBufferMemory()
    return ConversationChain(
        llm=chat,
        memory=memory,
        verbose=True
    )

def main():
    chain = create_chain()
    
    print("Welcome to SimpleChat with Memory! (type 'quit' to exit)")
    while True:
        try:
            with get_openai_callback() as cb:
                user_input = input("\nYou: ")
                if user_input.lower() == 'quit':
                    break
                
                response = chain.predict(input=user_input)
                print(f"\nAssistant: {response}")
                print(f"\nTokens used: {cb.total_tokens}")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    main()