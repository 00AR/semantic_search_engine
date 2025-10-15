from fastapi import APIRouter, Query
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def root():
    return {"message": "Wikipedia Semantic Search Engine is running."}


@router.get("/search")
async def search(query: str = Query(...)):
    logger.info(f"Query received: {query}")
    results = "Awaited"
    return {"query": query, "results": results}