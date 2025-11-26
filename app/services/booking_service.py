from app.services.booking_extractors import extract_date, extract_email, extract_name
from app.rag.llm_client import classifier_llm as llm
from app.db.models import Bookings
from datetime import datetime, timezone, time
from sqlalchemy.orm import Session
from app.db.schemas import AnyResponse

def ask_slot(slot_name: str, current_slots: dict) -> AnyResponse:
    """
    Strict, controlled prompt that ONLY asks for the missing slot.
    """
    return llm.invoke(f"""
        You are an assistant helping to book an interview.
        
        Your ONLY task is to ask the user for the missing field.
        
        Allowed fields:
        - name
        - email
        - date
        
        Current slot values: {current_slots}
        
        Rules:
        - Ask ONLY for the missing field: {slot_name}.
        - Do NOT ask for any other fields (no phone number, no extra info).
        - Do NOT mention already-filled fields.
        - Keep the reply short and clear.
        - Do NOT talk about JSON, formats, or internal structures.
        
        Now, ask the user for: {slot_name}.
        """)

def handle_booking_turn(user_message: str, slots: dict) -> tuple[dict, AnyResponse]:
    # 1. Try to fill slots from this message
    if not slots.get("name"):
        name = extract_name(user_message)
        if name:
            slots["name"] = name

    if not slots.get("email"):
        email = extract_email(user_message)
        if email:
            slots["email"] = email

    if not slots.get("date"):
        date = extract_date(user_message)
        if date:
            slots["date"] = date

    # Ask for missing slots in order
    if not slots.get("name"):
        resp = ask_slot("name", slots)
        return slots, resp

    if not slots.get("email"):
        resp = ask_slot("email", slots)
        return slots, resp

    if not slots.get("date"):
        resp = ask_slot("date", slots)
        return slots, resp

    # 3. All filled → state_flow will finalize
    return slots, None

def create_booking_from_slots(db: Session, session_id: str, slots: dict):
    """
    Saves a booking into the database using the collected slot values.
    slots["date"] is expected to be 'YYYY-MM-DD'.
    """

    try:
        date_only = datetime.strptime(slots["date"], "%Y-%m-%d").date()
    except Exception:
        raise ValueError(f"Invalid date format: {slots['date']}")

    date_time = datetime.combine(
        date_only,
        time(hour=10, minute=0, second=0, tzinfo=timezone.utc),
    )

    booking = Bookings(
        name=slots["name"],
        email=slots["email"],
        date_time=date_time,
        session_id=session_id,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking
