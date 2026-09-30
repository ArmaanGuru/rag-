from langchain_text_splitters import  CharacterTextSplitter
from pdfload import load_pdf
text_splitter=CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=10
)
text=load_pdf()
texts=text_splitter.split_documents(text)
# print(texts[0])
g=texts
# print(texts[1].metadata)
# print(len(texts))