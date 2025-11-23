from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.ingestion import router as ingest_router
from app.rag.vector_store import create_collection_if_not_exist

app = FastAPI()

app.include_router(chat_router, prefix="/chat")
app.include_router(ingest_router, prefix="/ingest")

@app.get("/health")
def health():
    return {"status": "ok"}

# start Qdrant collection check during wep app startup
@app.on_event("startup")
async def startup_event():
    create_collection_if_not_exist()

    