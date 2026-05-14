import os
import uuid
from fastapi import FastAPI, HTTPException,UploadFile, File
from pydantic import BaseModel

from src.pipeline import rag_pipeline,get_embedding_manager
from src.data_loader import (
    process_single_pdf,
    split_documents
)
from src.vectorstore import VectorStore

from src.session_manager import (
    create_session,
    update_session_access
)
app = FastAPI(
    title="RAG PDF Chat API",
    description="AI-powered PDF question answering system.",
    version="1.0.0"
)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
class QueryRequest(BaseModel):
    question: str
    session_id: str

class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    session_id: str

    min_score: float = 0.2
    summarize: bool = False

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

   
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    session_id = (
        f"session_{uuid.uuid4().hex}"
    )

    file_path = (
        f"{UPLOAD_DIR}/{session_id}.pdf"
    )

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    docs = process_single_pdf(file_path)

    chunks = split_documents(docs)

    embeddings = (
        get_embedding_manager().generate_embeddings(
            [doc.page_content for doc in chunks]
        )
    )

    vector_store = VectorStore(
        collection_name=session_id
    )

    vector_store.add_documents(
        chunks,
        embeddings
    )

    create_session(session_id)

    return {
        "message": "PDF uploaded successfully",
        "session_id": session_id
    }

@app.get("/")
def root():
    return {
        "message": "RAG API is running."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: QueryRequest):

    try:

        update_session_access(
            request.session_id
        )

        response = rag_pipeline.query(
            question=request.question,
            session_id=request.session_id
        )

        return response

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )