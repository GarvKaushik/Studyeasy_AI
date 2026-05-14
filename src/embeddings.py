import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List



class EmbeddingManager:
    def __init__(self,model_name:str="all-MiniLM-L6-v2"):
        self.model_name=model_name
        self.model=None
        self._load_model()

    def _load_model(self):
        self.model = SentenceTransformer(self.model_name)
        print(f"embedding dimension:{self.model.get_embedding_dimension()}")

    def generate_embeddings(self,texts:List[str])->np.ndarray:
        """Generate embeddings for a list of texts"""
        embeddings=self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            normalize_embeddings=True
            )
        print(f"Generated embeddings for {len(texts)} texts")
        print(f"embedding shape:{embeddings.shape}")
        return embeddings



