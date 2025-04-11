from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Load and clean your markdown/text file
with open("my_vision.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw_text = f.read()

# 2. Wrap into LangChain Document object
docs = [Document(page_content=raw_text)]

# 3. Split into semantic chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 4. Create FAISS vector store from chunks
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 5. Setup the LLM
llm = OpenAI(temperature=0)

# 6. Start conversation loop
chat_history = []
print("🤖 Chat with your notes! (type 'exit' to quit)\n")

while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break

    # Step 1: Retrieve matching chunks
    retriever = vectorstore.as_retriever()
    retrieved_docs = retriever.get_relevant_documents(query)

    # Step 2: Show retrieved content
    print("\n📚 Retrieved Chunks:")
    for i, doc in enumerate(retrieved_docs):
        print(f"--- Chunk {i+1} ---\n{doc.page_content[:300]}...\n")

    # Step 3: Build prompt with context + query
    context = "\n\n".join(doc.page_content for doc in retrieved_docs)
    full_prompt = f"""You are a helpful assistant. Use the context below to answer the user's question.

Context:
{context}

Question:
{query}

Answer:"""

    print("\n🧾 Final Prompt to LLM:\n", full_prompt[:800], "...\n")  # Truncate for readability

    # Step 4: Send prompt to LLM
    answer = llm.invoke(full_prompt)

    # Step 5: Display and record
    print("\n🤖", answer, "\n")
    chat_history.append((query, answer))
