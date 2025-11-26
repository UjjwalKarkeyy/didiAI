import json
from app.memory.redis_client import r

def get_slots(session_id: str) -> dict:
    raw = r.get(f"chat:session:{session_id}:slots")
    if not raw:
        return {"name": None, "email": None, "date": None}
    return json.loads(raw)

def save_slots(session_id: str, slots: dict):
    r.set(f"chat:session:{session_id}:slots", json.dumps(slots))

def clear_slots(session_id: str):
    r.delete(f"chat:session:{session_id}:slots")

