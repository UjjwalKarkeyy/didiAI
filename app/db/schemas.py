# DEFINES PYDANTIC SCHEMAS FOR DATA VALIDATION
from pydantic import BaseModel
from datetime import datetime, date, time

# pydantic schema for chatrequest
# from API
class ChatRequest(BaseModel):
    session_id : str
    message : str

# pydantic schema for chatresponse
# to user (response)
class ChatResponse(BaseModel):
    answer: str
    booking_created: bool = False
    booking: "BookingRead | None" = None

# pydantic schema for documentingestresponse
# to program
class DocumentIngestResponse(BaseModel):
    document_id: int
    chunks: int
    status: str  # "success"

# pydantic schema for bookinginfo
# to user (response)
class BookingInfo(BaseModel):
    name : str
    email : str
    date : date
    time : time

# pydantic schema for bookingcreate
# to program
class BookingCreate(BaseModel):
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