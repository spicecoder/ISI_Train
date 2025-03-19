# chat_v3_improved.py
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.callbacks.manager import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

class ChatHistory:
    def __init__(self, filename="chat_history.json"):
        self.filename = filename
        self.history = self._load_history()
    
    def _load_history(self):
        path = Path(self.filename)
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        return []
    
    def add_exchange(self, user_input, assistant_response):
        exchange = {
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": assistant_response
        }
        self.history.append(exchange)
        self._save_history()
    
    def _save_history(self):
        with open(self.filename, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def load_into_memory(self, memory):
        """Load chat history into the conversation memory"""
        for exchange in self.history:
            # Add past exchanges to memory
            memory.chat_memory.add_user_message(exchange["user"])
            memory.chat_memory.add_ai_message(exchange["assistant"])
        return memory

def create_chain(chat_history):
    chat = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
    memory = ConversationBufferMemory()
    
    # Load previous conversations into memory
    chat_history.load_into_memory(memory)
    
    return ConversationChain(
        llm=chat,
        memory=memory,
        verbose=True
    )

def main():
    chat_history = ChatHistory()
    chain = create_chain(chat_history)
    
    print("Welcome to SimpleChat with Persistence! (type 'quit' to exit)")
    print(f"Loaded {len(chat_history.history)} previous messages from history")
    
    while True:
        try:
            with get_openai_callback() as cb:
                user_input = input("\nYou: ")
                if user_input.lower() == 'quit':
                    break
                
                response = chain.predict(input=user_input)
                chat_history.add_exchange(user_input, response)
                
                print(f"\nAssistant: {response}")
                print(f"\nTokens used: {cb.total_tokens}")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    main()