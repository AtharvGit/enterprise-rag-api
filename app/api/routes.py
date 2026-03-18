import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.document_processor import DocumentProcessor
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService

router = APIRouter()

doc_processor = DocumentProcessor()
retrieval_service = RetrievalService()
llm_service = LLMService()

@router.post('/upload', status_code=201)
async def upload_document(file: UploadFile = File(...)):


    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are supported')
    
    file_path = os.path.join('data', 'raw', file.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        chunks = doc_processor.process_pdf(file_path)
        retrieval_service.ingest_documents(chunks)
        return {"message":f"successfully processed '{file.filename}' and stored {len(chunks)} text chunks"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
    

@router.post('/query', response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    try:
        context_docs = retrieval_service.search_context(request.question)
        answer = llm_service.generate_answer(request.question, context_docs)
        return QueryResponse(question=request.question, answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail = f'failed to generate answer: {str(e)}')

