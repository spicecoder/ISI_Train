# student_personal_rag.py
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import re
from langchain_community.callbacks.manager import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

load_dotenv()

class PersonalKnowledgeBase:
    """A simple knowledge base from student-uploaded text files"""
    
    def __init__(self, default_file="my_observations.txt"):
        self.default_file = default_file
        self.content = ""
        self.chunks = []
        self.chunk_size = 500  # Characters per chunk
        
    def load_file(self, filename=None):
        """Load content from a text file"""
        if filename is None:
            filename = self.default_file
        
        path = Path(filename)
        if not path.exists():
            print(f"File {filename} not found. Please create it with your observations.")
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            self._create_chunks()
            return True
        except Exception as e:
            print(f"Error loading file: {str(e)}")
            return False
    
    def _create_chunks(self):
        """Split the content into manageable chunks"""
        # Simple chunking by character count, preserving paragraph boundaries where possible
        paragraphs = self.content.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) < self.chunk_size:
                current_chunk += para + "\n\n"
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
                
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        self.chunks = chunks
    
    def simple_search(self, query, top_k=2):
        """Very simple keyword-based search to find relevant chunks"""
        if not self.chunks:
            return []
        
        # Clean and prepare the query
        query = query.lower()
        query_terms = re.findall(r'\w+', query)
        
        # Score each chunk based on term frequency
        chunk_scores = []
        for i, chunk in enumerate(self.chunks):
            chunk_lower = chunk.lower()
            score = sum(1 for term in query_terms if term in chunk_lower)
            chunk_scores.append((i, score))
        
        # Sort by score and return top k chunks
        chunk_scores.sort(key=lambda x: x[1], reverse=True)
        results = [self.chunks[idx] for idx, score in chunk_scores[:top_k] if score > 0]
        
        return results

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

def create_chain(chat_history, knowledge_base):
    chat = ChatOpenAI(temperature=0.7, model="gpt-3.5-turbo")
    memory = ConversationBufferMemory()
    
    # Load previous conversations into memory
    chat_history.load_into_memory(memory)
    
    # Define a custom prompt template that includes retrieved context
    template = """You are a helpful assistant for students.

{context}

Current conversation:
{history}
Human: {input}
AI Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "input", "context"],
        template=template
    )
    
    return ConversationChain(
        llm=chat,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

def main():
    kb = PersonalKnowledgeBase()
    
    # Try to load the default file
    file_loaded = kb.load_file()
    
    # If default file doesn't exist, ask to create or provide another
    if not file_loaded:
        while True:
            choice = input("Would you like to: \n1. Create a new observations file \n2. Specify existing file path \n3. Continue without personal knowledge \nChoice (1/2/3): ")
            
            if choice == "1":
                print(f"Please create a file named '{kb.default_file}' with your observations and restart the program.")
                return
            elif choice == "2":
                filepath = input("Enter the path to your observations file: ")
                if kb.load_file(filepath):
                    break
            elif choice == "3":
                print("Continuing without personal knowledge...")
                break
            else:
                print("Invalid choice, please try again.")
    
    chat_history = ChatHistory()
    chain = create_chain(chat_history, kb)
    
    print("\nWelcome to Student Personal RAG Chat! (type 'quit' to exit)")
    print(f"Loaded {len(chat_history.history)} previous messages from history")
    if kb.content:
        print(f"Loaded personal knowledge with {len(kb.chunks)} chunks of information")
    
    while True:
        try:
            with get_openai_callback() as cb:
                user_input = input("\nYou: ")
                if user_input.lower() == 'quit':
                    break
                
                # Retrieve relevant context from knowledge base
                relevant_chunks = kb.simple_search(user_input)
                context = "Personal Knowledge Context:\n" + "\n---\n".join(relevant_chunks) if relevant_chunks else "No relevant personal knowledge found."
                
                # Get response using the chain
                response = chain.predict(input=user_input, context=context)
                chat_history.add_exchange(user_input, response)
                
                print(f"\nAssistant: {response}")
                print(f"\nTokens used: {cb.total_tokens}")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")

if __name__ == "__main__":
    main()