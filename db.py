import os
from langchain_community.vectorstores import Chroma
from embbed import embeddings
from split import g
from dotenv import load_dotenv

load_dotenv()

PERSIST_DIR = "chroma_db"

if not os.path.exists(PERSIST_DIR):
    print("⚠️ No DB found. Creating new vectorstore...")

    vectorstore = Chroma.from_documents(
        documents=g,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    vectorstore.persist()
    print("✅ DB created and saved.")

else:
    print("✅ Loading existing DB...")

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

# Retriever
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 2, "fetch_k": 4}
)