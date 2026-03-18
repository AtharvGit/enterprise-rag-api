import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List

class RetrievalService:
    def __init__(self, persist_directory: str = "./data/processed/chroma_db"):
        self.persist_directory = persist_directory
        
        # Swapped to a free, highly efficient local embedding model
        print("Loading local embedding model (this may take a moment on the first run)...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def ingest_documents(self, chunks: List[Document]):
        if not chunks:
            raise ValueError("No document chunks provided for ingestion.")
            
        print(f"Embedding and storing {len(chunks)} chunks locally...")
        self.vector_store.add_documents(chunks)
        print("Successfully stored in ChromaDB.")

    def search_context(self, query: str, top_k: int = 3) -> List[Document]:
        print(f"Searching database for: '{query}'")
        results = self.vector_store.similarity_search(query, k=top_k)
        return results