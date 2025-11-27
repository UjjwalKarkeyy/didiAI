# DEFINES CHAT MEMORY USING REDIS: ADDITION AND HISTORY FETCH
from app.memory.redis_client import r
from datetime import datetime, timezone
import json

# adds msg to redis history
def add_message_to_chat_history(session_id, sender, content):
    # Add a message to a chat session's history using a Redis List
    message = {
        "sender": sender,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(), 
    }
    r.rpush(f"chat:session:{session_id}:messages", json.dumps(message))

# gets top 10 recent chat history
def get_chat_history(session_id, count=10):
    # Retrieve the most recent messages from a chat session's history
    messages_json = r.lrange(f"chat:session:{session_id}:messages", -count, -1) # -count means msg from end, -1 means last msg
    return [json.loads(msg) for msg in messages_json]
