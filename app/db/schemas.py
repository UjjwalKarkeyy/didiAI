# DEFINES PYDANTIC SCHEMAS FOR DATA VALIDATION
from pydantic import BaseModel
from typing import Any

# pydantic schema for chatrequest
class ChatRequest(BaseModel):
    session_id : str | None = None
    message : str

# pydantic schema for chatresponse
class ChatResponse(BaseModel):
    session_id: str
    message: str

# pydantic schema for documentingestresponse
class DocumentIngestResponse(BaseModel):
    status: str  # "success"
    session_id: str

class AnyResponse(BaseModel):
    message: Any