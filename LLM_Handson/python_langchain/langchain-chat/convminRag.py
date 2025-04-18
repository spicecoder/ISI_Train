from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain

# # 1. Load personal notes
# loader = TextLoader("my_vision.txt")
# docs = loader.load()
# from langchain_community.document_loaders import TextLoader
# loader = TextLoader("my_vision.txt", encoding="utf-8")
from langchain_core.documents import Document

# Load and clean file manually
with open("my_vision.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw_text = f.read()

# Optional: strip non-ASCII chars (if you want to be very clean)
# raw_text = raw_text.encode("ascii", errors="ignore").decode()

# Wrap into LangChain document
docs = [Document(page_content=raw_text)]


# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. Create vectorstore
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. Setup conversational chain
llm = OpenAI(temperature=0)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# 5. Start conversation loop
chat_history = []
print("🤖 Chat with your notes! (type 'exit' to quit)\n")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break

    result = qa_chain.invoke({"question": query, "chat_history": chat_history})
    print("\n🤖", result["answer"], "\n")

    # Save conversation turn
    chat_history.append((query, result["answer"]))
