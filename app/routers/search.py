from fastapi import APIRouter, Query
from app.core.indexing import SemanticIndex
from app.config import TOP_K
import logging


router = APIRouter()
logger = logging.getLogger(__name__)


index_service = SemanticIndex()


@router.on_event("startup")
async def startup():
    index_service.load_index()


@router.get("/search")
async def search(query: str = Query(...), top_k: int = Query(TOP_K, ge=1, le=20)):
    logger.info(f"Query received: {query}")
    results = index_service.search(query, top_k)
    return {"query": query, "results": results}