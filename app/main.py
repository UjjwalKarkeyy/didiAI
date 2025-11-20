from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.ingestion import router as ingest_router

app = FastAPI()

app.include_router(chat_router, prefix="/chat")
app.include_router(ingest_router, prefix="/ingest")

@app.get("/health")
def health():
    return {"status": "ok"}

