import re
import json
from app.rag.llm_client import classifier_llm as llm
from datetime import date

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def extract_email(text: str) -> str | None:
    match = re.search(EMAIL_REGEX, text)
    if match:
        return match.group(0)
    return None

curr_date = date.today().strftime("%Y-%m-%d")

def extract_date(text: str) -> str | None:
    prompt = f"""
        You are a precise date extraction tool.

        Today's date is {curr_date}.  
        The user will give a natural-language date like:
        - "coming Thursday"
        - "next Monday"
        - "this Friday at 3 PM"
        - "day after tomorrow"
        - "2nd February"
        - "on the 25th"

        Your task:
        1. Understand the user's message.
        2. Calculate the exact calendar date based on today's date.
        3. RETURN ONLY the date in this exact format: YYYY-MM-DD
        4. Do NOT include time.
        5. Do NOT add explanations.
        6. Do NOT output anything except the date.

        User message: "{text}"
    """

    raw = llm.invoke(prompt).content.strip()

    # remove ``` wrappers if Gemini adds them
    raw = re.sub(r"```.*?\n|```", "", raw).strip()

    # validate YYYY-MM-DD
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return raw

    return None


def extract_name(text: str) -> str | None:
    prompt = f"""
    The user is giving their full name. 
    Extract ONLY the name, with no extra text.

    User message: "{text}"
    """
    result = llm.invoke(prompt).content.strip()
    # basic check
    if 2 <= len(result.split()) <= 5:
        return result
    return None

