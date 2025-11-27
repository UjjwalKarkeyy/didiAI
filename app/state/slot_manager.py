# DEFINES SLOT MANAGING
import json
from app.memory.redis_client import r

# get current slots (none if not filled)
def get_slots(session_id: str) -> dict:
    raw = r.get(f"chat:session:{session_id}:slots")
    if not raw:
        return {"name": None, "email": None, "date": None, "time": None, "phone": None}
    return json.loads(raw)

# save slots in chat session
def save_slots(session_id: str, slots: dict):
    r.set(f"chat:session:{session_id}:slots", json.dumps(slots))

# clear slot enteries
def clear_slots(session_id: str):
    r.delete(f"chat:session:{session_id}:slots")

