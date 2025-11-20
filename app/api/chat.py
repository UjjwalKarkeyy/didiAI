from fastapi import APIRouter

# router instance
router = APIRouter()

# router url
@router.get("")
# func to handle chat router
async def handleChat():
    return {"message": "chat router successful!"}