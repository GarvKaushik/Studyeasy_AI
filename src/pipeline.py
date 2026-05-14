
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv  
load_dotenv()  
from typing import Dict, Any

from src.search import RAGRetriever
from src.embeddings import EmbeddingManager
from src.vectorstore import VectorStore
from src.prompts import RAG_PROMPT

#Initilize components
embedding_manager = None

def get_embedding_manager():
    global embedding_manager

    if embedding_manager is None:
        embedding_manager = EmbeddingManager()

    return embedding_manager
### initialize groq llm

groq_api_key=os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError(
        "GROQ_API_KEY not found in environment variables."
    )


llm=ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",temperature=0.1,
    max_tokens=1024)
# --- Advanced RAG Pipeline: Streaming, Citations, History, Summarization ---

class AdvancedRAGPipeline:
    def __init__(
            self,
            get_embedding_manager,
            llm):
        self.embedding_manager = None
        self.llm = llm
        self.history = []  # Store query history

    def query(
            self,
            question: str,
            session_id: str,
            top_k: int = 10,
            min_score: float = 0.0,
            summarize: bool = False) -> Dict[str, Any]:
        vector_store = VectorStore(
            collection_name=session_id
        )
        if self.embedding_manager is None:
           self.embedding_manager = get_embedding_manager()
        retriever = RAGRetriever(
            vector_store,
            self.embedding_manager
        )
        # Retrieve relevant documents
        results = retriever.retrieve(
            question,
            top_k=top_k,
            score_threshold=min_score)
        if not results:
            answer = "No relevant context found."
            sources = []
            context = ""
        else:
            context = "\n\n".join([doc['content'] for doc in results])
            MAX_CONTEXT_CHARS = 12000
            context = context[:MAX_CONTEXT_CHARS]

            sources = [
                {
                'source': doc['metadata'].get(
                    'source_file',
                    doc['metadata'].get('source', 'unknown')),
                'page': doc['metadata'].get(
                    'page',
                    'unknown'),
                'score': doc['similarity_score'],
                'preview': doc['content'][:120] + '...'
            } for doc in results]
            # Streaming answer simulation
            prompt = RAG_PROMPT.format(
            context=context,
            question=question
        )
            response = self.llm.invoke(prompt)
            answer = response.content

        # Add citations to answer
        citations = [f"[{i+1}] {src['source']} (page {src['page']})" for i, src in enumerate(sources)]


       

       
        # Store query history
        self.history.append({
            'question': question,
            'answer': answer,
            'sources': sources,
           
        })

        return {
            'question': question,
            'answer': answer,
            'sources': sources,
        
            'history': self.history,
            'citations': citations
        }

# Example usage:
rag_pipeline = AdvancedRAGPipeline(get_embedding_manager, llm)
