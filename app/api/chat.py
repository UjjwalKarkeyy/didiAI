from fastapi import APIRouter
from app.services.chat_service import create_response
from app.db.schemas import ChatRequest, ChatResponse
import uuid

# router instance
router = APIRouter()

# router url
@router.post("", response_model = ChatResponse)
# func to handle chat router
async def handleChat(request: ChatRequest):
    # create session id if not exist    
    session_id = request.session_id or str(uuid.uuid4())
    response = create_response(query=request.message, session_id=session_id)
    return ChatResponse(session_id=session_id, message=response)