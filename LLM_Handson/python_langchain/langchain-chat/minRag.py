# minRAG_v2.py

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# 1. Load personal notes from markdown
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



# 2. Split into semantically coherent chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. Embed and store in temporary FAISS vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. Define a custom prompt template for clarity
custom_prompt = PromptTemplate.from_template("""
You are an expert assistant helping align personal goals with user notes.
Use the notes below to answer the user's question in a clear and actionable way.

Notes:
{context}

Question:
{question}
""")

# 5. Setup RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": custom_prompt},
    return_source_documents=True
)

# 6. Ask a meaningful question
query = "Does this plan align with my long-term vision?"
result = qa_chain.invoke(query)

# 7. Print response and sources
print("🔍 Answer:\n", result["result"])
print("\n📚 Source excerpts:")
for doc in result["source_documents"]:
    print("-", doc.page_content[:200], "...\n")
