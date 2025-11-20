# upload file is a class file is a dependency used for ingesting documents
from fastapi import APIRouter, UploadFile, File

# router instance
router = APIRouter()

# routing url
@router.post("")
# func to handle ingestion route
async def handleIngest(file: UploadFile = File(...)):
    return {"message": "ingest router successful!"}