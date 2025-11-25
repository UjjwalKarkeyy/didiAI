from app.rag.retriever import RagRetriever
from app.rag.prompt_builder import PROMPT_TEMPLATE
from langchain_core.prompts import ChatPromptTemplate
from app.rag.llm_client import llm
from app.memory.chat_memory import add_message_to_chat_history, get_chat_history 
from app.intent.intent_classifier import classify_intent
from app.state.state_manager import get_state, set_state, clear_state
from app.memory.redis_client import r
from app.state.slot_manager import save_slots, get_slots, clear_slots
from app.services.booking_service import handle_booking_turn, create_booking_from_slots
from app.db.db_session import get_db

retriever = RagRetriever()

class SimpleResponse:
    def __init__(self, content):
        self.content = content

def define_intent(query: str):
    return classify_intent(query)

def create_response(query: str, session_id: str):
    intent = define_intent(query)
    history = get_chat_history(session_id)

    response = state_flow(
        intent=intent,
        session_id=session_id,
        query=query,
        history=history,
    )

    add_message_to_chat_history(session_id, "user", query)
    add_message_to_chat_history(session_id, "didiAI", response.content)

    return response.content

def rag_response(query: str, history):
    history_text = "\n".join([f"{m['sender']}: {m['content']}" for m in history])
    context = retriever.search(query=query)
    
    prompt_chat_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_chat_template.format(
        context=context,
        query=query,
        history=history_text,
    )

    return llm.invoke(prompt)

def state_flow(intent, session_id, query, history):
    state = get_state(session_id)
    slots = get_slots(session_id)

    # 1. No active flow yet
    if not state:
        if intent == "book_interview":
            set_state(session_id, "booking_active")
            save_slots(session_id, slots)  # init empty

            return SimpleResponse(
                "Sure! Let's book your interview. What is your full name?"
            )
        else:
            return rag_response(query, history)


    # 2. Booking flow is active → slot filling
    if state == "booking_active":

        # DELETE THIS
        print("---- BOOKING ACTIVE ----")
        print("SLOTS BEFORE:", slots)
        # TILL THIS

        updated_slots, response = handle_booking_turn(query, slots)
        save_slots(session_id, updated_slots)

        # DELETE THIS
        print("UPDATED SLOTS:", updated_slots)
        print("RESPONSE FROM SLOT_MANAGER:", response)
        # TILL THIS

        # If all slots filled, confirm and finish
        if all(updated_slots.values()):
            db_gen = get_db()
            db = next(db_gen)
            create_booking_from_slots(db, session_id, updated_slots)
            confirmation_msg = (
                f"Your interview has been successfully booked!\n\n"
                f"**Date:** {updated_slots['date']}\n"
                f"**Name:** {updated_slots['name']}\n"
                f"**Email:** {updated_slots['email']}\n\n"
                "Is there anything else I can help you with?"
            )           
            clear_state(session_id)
            clear_slots(session_id)
            db_gen.close()
            return SimpleResponse(content=confirmation_msg)

        else:
            # still missing info → response will ask next question
            return response

    # fallback
    return rag_response(query, history)
