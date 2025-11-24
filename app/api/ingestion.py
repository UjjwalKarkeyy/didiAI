# upload file is a class file is a dependency used for ingesting documents
from fastapi import APIRouter, UploadFile, File, Depends
from app.services.ingestion_service import ingest_document_text
from app.db.schemas import DocumentIngestResponse
from app.db.db_session import get_db
from sqlalchemy.orm import Session
import chardet

# router instance
router = APIRouter()

# routing url
@router.post("", response_model = DocumentIngestResponse)
# func to handle ingestion route
# Depends is a dependency injection. It tells FastAPI to run a function argument meaning pass whatever get_db returns 
async def handleIngest(file: UploadFile = File(...), db: Session = Depends(get_db)): 
    # read in bytes and convert to text
    file_bytes = await file.read()
    encode_result = chardet.detect(file_bytes) 
    encoding = encode_result.get("encoding") or "utf-8"
    text = file_bytes.decode(encoding, errors = "ignore")

    # pass text to ingest document function
    status = ingest_document_text(text = text, db = db, file_name=file.filename) # strategy = recursive by default

    if not status:
        return DocumentIngestResponse(status = "Failed")
    return DocumentIngestResponse(status = "Success")