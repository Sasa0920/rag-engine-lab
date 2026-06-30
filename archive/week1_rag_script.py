from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
import os

# Load document
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "document.txt")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

documents = [Document(page_content=text, metadata={"source": file_path})]

# Split document
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

# Embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Vector store
vectorstore = QdrantVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    location=":memory:",
    collection_name="demo"
)

# Retriever
retriever = vectorstore.as_retriever()

# LLM
llm = ChatOllama(
    model="llama3"
)

# QA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)

print("\nRAG Pipeline initialized. Ask any question about the document (type 'exit' or 'quit' to quit).")

while True:
    try:
        question = input("\nQuestion: ")
        if not question.strip():
            continue
        if question.lower().strip() in ["exit", "quit"]:
            print("Exiting. Goodbye!")
            break
            
        print("Thinking...")
        response = qa.invoke({"query": question})
        answer = response["result"]
        
        print("\nAnswer:")
        print(answer)
    except KeyboardInterrupt:
        print("\nExiting. Goodbye!")
        break
    except Exception as e:
        print(f"\nError: {e}")