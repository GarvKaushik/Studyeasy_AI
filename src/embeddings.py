import os

import numpy as np

from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class EmbeddingManager:
    def __init__(self):
        jina_api_key = os.getenv(
            "JINA_API_KEY"
        )

        if not jina_api_key:
            raise ValueError(
                "JINA_API_KEY not found."
            )

        self.client = OpenAI(
            api_key=jina_api_key,
            base_url="https://api.jina.ai/v1"
        )

        self.model_name = "jina-embeddings-v2-base-en"

   

    def generate_embeddings(self,texts:List[str])->np.ndarray:
        """Generate embeddings for a list of texts"""
        response = self.client.embeddings.create(
            model=self.model_name,
            input=texts
        )

        embeddings = np.array([
            item.embedding
            for item in response.data
        ])
        print(f"Generated embeddings for {len(texts)} texts")
        print(f"embedding shape:{embeddings.shape}")
        return embeddings



