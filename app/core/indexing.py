import math
import os
import faiss
import numpy as np
from datasets import load_dataset
import logging
from .embeddings import EmbeddingService
from app.config import *

logger = logging.getLogger(__name__)


class SemanticIndex:
    def __init__(self):
        self.index = None
        self.titles = []
        self.urls = []
        self.embedding_service = EmbeddingService(MODEL_NAME)

    def load_dataset(self):
        logger.info("Logging Wikipedia dataset...")
        try:
            cache_dir = os.path.join(os.getcwd(), "hf_cache")
            os.environ["HF_HOME"] = cache_dir
            os.makedirs(cache_dir, exist_ok=True)
            # data = load_dataset("AMead10/lvl_5_vital_wikipedia_articles", split="train[:1]")
            data = load_dataset("AMead10/lvl_5_vital_wikipedia_articles", split="train[:3]")
            self.titles = data["title"]
            self.urls = data["url"]
            combined_texts = [
                f"{item['title']}. {item['text'][:MAX_TEXT_LENGTH]}"
                for item in data
            ]
            return combined_texts
        except Exception as e:
            logger.error(f"Dataset loading failed: {e}")
            # TODO: remove dummy data
            self.titles = ["Fallback Title 1", "Fallback Title 2"]
            self.urls = ["/url1", "/url2"]
            return [f"{t}" for t in self.titles]

    def build_index(self):
        texts = self.load_dataset()
        embeddings = self.embedding_service.encode_texts(texts)
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.index.add(embeddings)
        os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
        faiss.write_index(self.index, EMBEDDINGS_FILE)
        np.save(METADATA_FILE, {"titles": self.titles, "urls": self.urls})
        logger.info(f"Index build and saved with {len(self.titles)} items.")

    def load_index(self):
        if not os.path.exists(EMBEDDINGS_FILE):
            logger.info("No existing index found. Creating a new one.")
            self.build_index()
        else:
            self.index = faiss.read_index(EMBEDDINGS_FILE)
            meta = np.load(METADATA_FILE, allow_pickle=True).item()
            self.titles, self.urls = meta["titles"], meta["urls"]
            logger.info(f"Loaded index with {self.index.ntotal} items.")

    def search(self, query:str, top_k: int = TOP_K):
        if self.index is None:
            raise ValueError("Index not initialized")
        
        query_emb = self.embedding_service.encode_query(query)
        distances, indices = self.index.search(query_emb, top_k)

        results = []
        for rank, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            dist = float(dist)
            if math.isfinite(dist):
                score = 1 - (dist ** 2) / 2
            else:
                score = 0.0  # fallback if NaN/inf appears

            # Clamp the value to [-1, 1] to avoid JSON issues
            score = float(np.clip(score, -1.0, 1.0))

            # score = 1 - (dist ** 2) / 2
            results.append({
                "rank": rank + 1,
                "title": self.titles[idx],
                "url": self.urls[idx],
                "similarity_score": round(float(score), 4)
            })
        return results
            