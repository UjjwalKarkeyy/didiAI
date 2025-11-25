# upload file is a class file is a dependency used for ingesting documents
from fastapi import APIRouter, UploadFile, File, Depends
from app.services.ingestion_service import ingest_document_text
from app.db.schemas import DocumentIngestResponse
from app.db.db_session import get_db
from sqlalchemy.orm import Session
from app.services.file_reader_service import FileReader

# router instance
router = APIRouter()

# routing url
@router.post("", response_model = DocumentIngestResponse)
# func to handle ingestion route
# Depends is a dependency injection. It tells FastAPI to run a function argument meaning pass whatever get_db returns 
async def handleIngest(file: UploadFile = File(...), db: Session = Depends(get_db)): 
    # read file
    fileReader = FileReader(file=file)  
    text = await fileReader.read_file() 

    # pass text to ingest document function
    status = ingest_document_text(text = text, db = db, file_name=file.filename) # strategy = recursive by default

    if not status:
        return DocumentIngestResponse(status = "Failed")
    return DocumentIngestResponse(status = "Success")