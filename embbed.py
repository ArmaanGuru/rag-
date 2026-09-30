from langchain_huggingface import HuggingFaceEmbeddings
from split import g
from dotenv import load_dotenv

load_dotenv()
embeddings=HuggingFaceEmbeddings(
    model_name="BAAI/bge-base-en")
texts=[doc.page_content for doc in g]

embeddings_list=embeddings.embed_documents(texts[0:1])

# print(embeddings_list[0])
