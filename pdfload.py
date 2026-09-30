from langchain_community.document_loaders import PyPDFLoader
def load_pdf():
    loader=PyPDFLoader('upsc.pdf')
    return loader.load()