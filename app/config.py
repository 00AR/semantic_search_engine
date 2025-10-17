import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Use pydantic 'BaseSettings' to load these from .env file

MODEL_NAME = os.getenv("MODEL_NAME", "all-MiniLM-L6-v2")
EMBEDDING_DIM = 384
TOP_K = int(os.getenv("TOP_K", 5))
MAX_TEXT_LENGTH = 20
EMBEDDINGS_FILE = os.getenv("EMBEDDINGS_FILE", "app/data/wiki_embeddings.faiss")
METADATA_FILE = os.getenv("METADATA_FILE", "app/data/wiki_metadata.npy")
