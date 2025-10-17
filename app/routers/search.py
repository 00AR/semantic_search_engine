from fastapi import APIRouter, Query, Request
from fastapi.templating import Jinja2Templates
from app.core.indexing import SemanticIndex
from app.config import TOP_K
import logging


templates = Jinja2Templates(directory="app/templates")

router = APIRouter()
logger = logging.getLogger(__name__)


index_service = SemanticIndex()


@router.on_event("startup")
async def startup():
    index_service.load_index()


@router.get("/search")
async def search(request: Request, query: str = Query(None, min_length=1), top_k: int = Query(TOP_K, ge=1, le=20)):
    results = None
    if query:
        logger.info(f"Query received: {query}")
        results = index_service.search(query, top_k)
    # return {"query": query, "results": results}
    return templates.TemplateResponse(
        "search_results.html",
        {"request": request, "query": query, "results": results}
    )