# DEFINES THE CHAT API + BOOKING 
from fastapi import APIRouter
from app.services.chat_service import create_response
from app.db.schemas import ChatRequest, ChatResponse
from app.state.state_manager import clear_state
from app.state.slot_manager import clear_slots
import uuid

# router instance
router = APIRouter()

# router url
@router.post("", response_model = ChatResponse)
# func to handle chat router
async def handleChat(request: ChatRequest):
    response = create_response(query=request.message, session_id=request.session_id)

    return ChatResponse(session_id=request.session_id, message=response)