# DEFINES THE INGESTION API
# upload file is a class file is a dependency used for ingesting documents
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.services.ingestion_service import ingest_document_text
from app.db.schemas import DocumentIngestResponse
from app.services.file_reader_service import FileReader
from sqlalchemy.orm import Session
from app.db.db_session import get_db
import uuid

# router instance
router = APIRouter()

# routing url
@router.post("", response_model = DocumentIngestResponse)
# func to handle ingestion route
# Depends is a dependency injection. It tells FastAPI to run a function argument meaning pass whatever get_db returns 
async def handleIngest(session_id: str | None = Form(None), file: UploadFile = File(...), db: Session = Depends(get_db)): 
    if not session_id:
        # new session
        session_id = str(uuid.uuid4())

    # read file
    fileReader = FileReader(file=file)  
    text = await fileReader.read_file() 

    # pass text to ingest document function
    status = ingest_document_text(session_id=session_id, text = text, db = db, file_name=file.filename) # strategy = recursive by default

    if not status:
        return DocumentIngestResponse(status = "Failed", session_id = session_id)
    return DocumentIngestResponse(status = "Success", session_id = session_id)