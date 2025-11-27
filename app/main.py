# MAIN API LINK POINT
from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.ingestion import router as ingest_router
from app.rag.vector_store import create_collection_if_not_exist, reset_qdrant_collection
from app.db.session import init_db

# fastapi instance -> app
app = FastAPI()

# including routing points for chat and ingestion APIs
app.include_router(chat_router, prefix="/chat")
app.include_router(ingest_router, prefix="/ingest")

# quick check for api
@app.get("/health")
def health():
    return {"status": "ok"}

# startup events
@app.on_event("startup")
async def startup_event():
    # drop and create sqlite DB
    init_db()
    # delete collection data if already exist
    reset_qdrant_collection()
    # create Qdrant DB
    create_collection_if_not_exist()
