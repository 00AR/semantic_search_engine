import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
import logging
import torch

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, model_name: str):
        if torch.cuda.is_available():
            device = "cuda"
            logger.info("GPU detected. Using CUDA for embeddings.")
        else:
            device = "cpu"
            logger.info("No GPU found. Using CPU for embeddings.")
        
        logger.info(f"Loading embedding model: {model_name} on {device}")
        self.model = SentenceTransformer(model_name, device=device)

    def encode_texts(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True
        ).astype("float32")
    
    def encode_query(self, query: str) -> np.ndarray:
        embeddings = self.encode_texts([query])
        return embeddings
