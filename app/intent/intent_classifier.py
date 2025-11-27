# INTENT CLASSIFIER USING CLASSIFIER LLM
from app.rag.llm_client import classifier_llm
import json
import re

# two intents: normal_chat (rag) or booking_interview
INTENTS = ["normal_chat", "book_interview"]

INTENT_PROMPT = """
You are an intent classification module.

Classify the user's message into exactly ONE allowed intent.

Return STRICTLY in JSON format:
{{"intent": "<label>"}}

Allowed labels:
- normal_chat
- book_interview

Do NOT output anything else.

User message: "{message}"
"""

# classifies intent
def classify_intent(message: str) -> str:
    prompt = INTENT_PROMPT.format(message=message)
    raw = classifier_llm.invoke(prompt).content.strip()

    # Remove ``` blocks if present
    raw_clean = re.sub(r"```.*?\n|```", "", raw).strip()

    # Parse JSON safely
    try:
        data = json.loads(raw_clean)
        intent = data.get("intent", "normal_chat")
    except Exception:
        print("JSON PARSE FAILED. RAW:", raw)
        return "normal_chat"

    # Enforce known intents only
    if intent not in INTENTS:
        return "normal_chat"

    return intent
