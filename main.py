import os
import uuid
from fastapi import FastAPI, HTTPException,UploadFile, File
from pydantic import BaseModel
import threading
import time
from src.pipeline import rag_pipeline,get_embedding_manager
from src.data_loader import (
    process_single_pdf,
    split_documents
)
from src.vectorstore import VectorStore

from src.session_manager import (
    create_session,
    update_session_access,
    is_session_expired,
    delete_session,
    sessions
)
app = FastAPI(
    title="RAG PDF Chat API",
    description="AI-powered PDF question answering system.",
    version="1.0.0"
)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def cleanup_expired_sessions():

    while True:

        expired_sessions = []

        for session_id in list(sessions.keys()):

            if is_session_expired(
                session_id
            ):

                expired_sessions.append(
                    session_id
                )

        for session_id in expired_sessions:

            vector_store = VectorStore(
                collection_name=session_id
            )

            vector_store.delete_collection()

            delete_session(session_id)

            print(
                f"Deleted expired session: "
                f"{session_id}"
            )

        time.sleep(300)


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5
    session_id: str

    min_score: float = 0.2
    summarize: bool = False

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

   
    if not file.filename.lower().endswith(".pdf"):
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
    MAX_FILE_SIZE = 100* 1024 * 1024
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds the limit of 100 MB"
        )

    with open(file_path, "wb") as f:
      
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
    os.remove(file_path)

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
    
cleanup_thread = threading.Thread(
    target=cleanup_expired_sessions,
    daemon=True
)

cleanup_thread.start()