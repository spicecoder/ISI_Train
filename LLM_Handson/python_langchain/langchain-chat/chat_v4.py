# chat_v4.py
from uuid import uuid4

class ChatSession:
    def __init__(self, session_id=None):
        self.session_id = session_id or str(uuid4())
        self.start_time = datetime.now()
        self.message_count = 0
        
    @property
    def session_info(self):
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "message_count": self.message_count
        }

class EnhancedChatHistory(ChatHistory):
    def __init__(self, filename="chat_history.json"):
        super().__init__(filename)
        self.current_session = ChatSession()
    
    def add_exchange(self, user_input, assistant_response):
        exchange = {
            "session_id": self.current_session.session_id,
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "assistant": assistant_response
        }
        self.history.append(exchange)
        self.current_session.message_count += 1
        self._save_history()
    
    def get_session_history(self, session_id=None):
        sid = session_id or self.current_session.session_id
        return [msg for msg in self.history if msg["session_id"] == sid]

def main():
    chain = create_chain()
    chat_history = EnhancedChatHistory()
    
    print(f"Welcome to SimpleChat with Sessions!")
    print(f"Session ID: {chat_history.current_session.session_id}")
    print("Type 'quit' to exit, 'status' for session info")
    
    while True:
        try:
            with get_openai_callback() as cb:
                user_input = input("\nYou: ")
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'status':
                    print("\nSession Info:", chat_history.current_session.session_info)
                    continue
                
                response = chain.predict(input=user_input)
                chat_history.add_exchange(user_input, response)
                
                print(f"\nAssistant: {response}")
                print(f"\nTokens used: {cb.total_tokens}")
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
if __name__ == "__main__":
    main()