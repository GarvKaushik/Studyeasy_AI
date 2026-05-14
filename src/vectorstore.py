import chromadb
import uuid
import numpy as np
from typing import List, Any


### vector store using chromadb
class VectorStore:
    def __init__(
            self,collection_name:str="pdf_embeddings",persist_directory:str="../data/vector_store"):
        self.collection_name=collection_name
        self.persist_directory=persist_directory

        self.client=None
        self.collection=None

        self._initialize_store()

    def _initialize_store(self):
        try:
          
            self.client=chromadb.PersistentClient(
                path=self.persist_directory
                )
            
            self.collection=self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={
                "hnsw:space": "cosine",
                "description":"Collection of PDF document embeddings"}
                                                                
            )
            print(f"Initialized vector store with collection name: {self.collection_name}")
            print(f"existing documents in store:{self.collection.count()}")
           
        except Exception as e:

            print(f"Error initializing vector store: {e}")
            raise

    def add_documents(
            self,
            documents:List[Any],
            embeddings:np.ndarray):
        """Add documents and their embeddings to the vector store"""

        if len(documents) != len(embeddings):
            raise ValueError(
                "Documents and embeddings count mismatch."
            )
        
        ids=[]
        metadatas=[]
        documents_text=[]
        embeddings_list=[]

        for i,(doc,embedding ) in enumerate(
            zip(documents,embeddings)):
            doc_id=f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)

            metadata=dict(doc.metadata)
            metadata['doc_index']=i
            metadata['content_length']=len(doc.page_content)
            metadatas.append(metadata)

            documents_text.append(doc.page_content)

            embeddings_list.append(embedding.tolist())
        try:
            self.collection.add(
                ids=ids,
                embeddings=embeddings_list,metadatas=metadatas,documents=documents_text)
            print(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            print(f"Error adding documents to vector store: {e}")
            raise 

def delete_collection(self):
        """Delete current collection."""

        try:
            self.client.delete_collection(
                name=self.collection_name
            )

            print(
                f"Deleted collection: "
                f"{self.collection_name}"
            )

        except Exception as e:
            print(f"Error deleting collection: {e}")