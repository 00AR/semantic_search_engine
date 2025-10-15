from fastapi import FastAPI
from app.routers import search

app = FastAPI(title="Wikipedia Semantic Search Engine API")
app.include_router(search.router)


@app.get("/")
async def root():
    return {"message": "hello"}
