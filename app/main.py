from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.routers import search

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(title="Wikipedia Semantic Search Engine API")
app.include_router(search.router)


@app.get("/", include_in_schema=False)
async def root():
    # return {"message": "hello"}
    return RedirectResponse(url="/search")
