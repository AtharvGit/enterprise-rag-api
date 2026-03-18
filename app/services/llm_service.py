import os
from google import genai
from langchain_core.documents import Document
from typing import List

class LLMService:
    def __init__(self):
        # 1. Grab the key
        google_key = os.getenv("GOOGLE_API_KEY")
        
        # 2. Initialize the brand-new Google GenAI Client
        self.client = genai.Client(api_key=google_key)

    def generate_answer(self, question: str, context_documents: List[Document]) -> str:
        if not context_documents:
            return "I could not find any relevant information in the uploaded documents."
            
        # Extract the text from the LangChain document objects
        context_text = "\n\n".join([doc.page_content for doc in context_documents])
        
        # Build the prompt manually
        prompt = f"""You are a professional corporate assistant. Use the following context to answer the question. If you don't know the answer, just say you don't know. Do not make up an answer.
        
        Context: {context_text}
        
        Question: {question}"""
        
        print("Sending prompt using the NEW Google GenAI SDK...")
        try:
            # Call the new API endpoint
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"\n--- CRITICAL API ERROR --- \n{str(e)}\n--------------------------------")
            raise Exception(f"New Native LLM failed: {str(e)}")