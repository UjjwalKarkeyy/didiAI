# DEFINES PYDANTIC SCHEMAS FOR DATA VALIDATION
from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Any

# pydantic schema for chatrequest
# from API
class ChatRequest(BaseModel):
    session_id : str | None = None
    message : str

# pydantic schema for chatresponse
# to user (response)
class ChatResponse(BaseModel):
    session_id: str
    message: str

# pydantic schema for documentingestresponse
# to program
class DocumentIngestResponse(BaseModel):
    status: str  # "success"

# pydantic schema for booking request
class BookingRequest(BaseModel):
    name : str
    email : str
    date : date
    time : time

# pydantic schema for booking response
class BookingResponse(BaseModel):
    name: str
    email: str
    date_time: datetime
    session_id: str

# pydantic schema for booking read
# to DB
class BookingRead(BaseModel):
    id: int
    name: str
    email: str
    date_time: datetime
    created_at: datetime
    session_id: str

class AnyResponse(BaseModel):
    message: Any