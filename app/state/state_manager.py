from app.memory.redis_client import r

def set_state(session_id: str, state: str):
    r.set(f"chat:session:{session_id}:state", state)

def get_state(session_id: str) -> str:
    state = r.get(f"chat:session:{session_id}:state")
    return state.decode("utf-8") if state else None


def clear_state(session_id: str):
    r.delete(f"chat:session:{session_id}:state")
