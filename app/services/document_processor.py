import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap, length_function = len, separators = ["\n\n", "\n", " ", ""])

    def process_pdf(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'The file {file_path} doesnt exist')
        
        print(f'loading document:{file_path}')
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        print(f'spliting documents into chunks.....')
        chunks = self.text_splitter.split_documents(documents)

        print(f'successfully created {len(chunks)} chunks.')
        return chunks

        
        