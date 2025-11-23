from fastapi import APIRouter
from app.services.chat_service import create_response

# router instance
router = APIRouter()

# router url
@router.post("")
# func to handle chat router
async def handleChat(query: str = None):
    if query:
        response = create_response(query=query)
        return {"response": {response.content}}