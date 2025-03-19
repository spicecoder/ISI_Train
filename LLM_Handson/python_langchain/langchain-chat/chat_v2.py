# chat_v2.py
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

def create_chain():
    chat = ChatOpenAI(temperature=0.7)
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
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        response = chain.predict(input=user_input)
        print(f"\nAssistant: {response}")
if __name__ == "__main__":
    main()