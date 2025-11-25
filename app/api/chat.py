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
    # create session id if not exist  
    if request.session_id is None:
        # new session
        session_id = str(uuid.uuid4())
        clear_state(session_id)    
        clear_slots(session_id)
    else:      
        session_id =  request.session_id

    response = create_response(query=request.message, session_id=session_id)

    # DELETE THIS
    print("Incoming session_id:", session_id)
    from app.state.state_manager import get_state
    print(get_state(session_id))
    # TILL HERE

    return ChatResponse(session_id=session_id, message=response)