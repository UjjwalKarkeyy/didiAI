# DEFINES STATE OVERALL MANAGEMENT
from app.memory.redis_client import r

# set the current state in chat session
def set_state(session_id: str, state: str):
    r.set(f"chat:session:{session_id}:state", state)

# get current chat session state
def get_state(session_id: str) -> str:
    state = r.get(f"chat:session:{session_id}:state")
    return state.decode("utf-8") if state else None

# clear state
def clear_state(session_id: str):
    r.delete(f"chat:session:{session_id}:state")
