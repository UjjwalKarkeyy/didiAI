# DEFINES VARIOUS EXTRACTOR FUNCTIONS FOR: DATE, EMAIL, NAME, TIME, AND PHONE NO.
import re
import json
from app.rag.llm_client import classifier_llm as llm
from datetime import date

# create email regex
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# extract email
def extract_email(text: str) -> str | None:
    match = re.search(EMAIL_REGEX, text)
    if match:
        return match.group(0)
    return None

# get current date
curr_date = date.today()

# extract date
def extract_date(text: str) -> str | None:
    """
    Extract and normalize a date from natural language input.
    Returns YYYY-MM-DD or None.
    """

    prompt = f"""
    You are a strict date extraction tool.

    Today's date is {curr_date}.

    The user may say things like:
    - "coming Thursday"
    - "next Monday"
    - "this Friday"
    - "day after tomorrow"
    - "2nd February"
    - "on the 25th"
    - "after 3 days"

    Your task:
    - Understand the user's message.
    - Convert it to an exact date.
    - Output ONLY the date in format YYYY-MM-DD.
    - No explanations.
    - No additional text.
    - No time.
    - If no valid date exists, return "NONE".

    User message: "{text}"
    """

    raw = llm.invoke(prompt).content.strip()

    # Remove ``` wrappers if model adds them
    raw = re.sub(r"```.*?\n|```", "", raw).strip()

    if raw.upper() == "NONE":
        return None

    # Validate correct format
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return raw

    return None

# extract name
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

# extract phone no. with proper format
def extract_phone(text: str) -> str | None:
    """
    Extract phone number using LLM + regex cleanup.
    Supports formats like:
    - 9841234567
    - +977-9812345678
    - (977) 9812345678
    - 981-234-5678
    """

    prompt = f"""
    Extract ONLY the phone number from this message.
    Return digits only, no spaces, no hyphens, no additional text.
    If no phone number is present, return "NONE".

    Message: "{text}"
    """

    result = llm.invoke(prompt).content.strip()

    # cleanup
    digits = re.sub(r"\D", "", result)

    if len(digits) >= 7 and len(digits) <= 15:
        return digits

    return None

# extrat interview timing
def extract_time(text: str) -> str | None:
    """
    Extract time from user message.
    Returns HH:MM in 24-hour format or None.
    """

    prompt = f"""
    You are a strict time extraction tool.

    Convert the user's natural language time into 24-hour HH:MM format.

    Rules:
    - If user gives "3 PM", return "15:00".
    - If "3:30 PM", return "15:30".
    - If "7", infer "07:00" unless AM/PM implied.
    - If fuzzy terms:
        morning → 09:00
        afternoon → 15:00
        evening → 19:00
        night / tonight → 21:00
        noon → 12:00
        midnight → 00:00
    - Output ONLY HH:MM.
    - No explanations.
    - No extra text.
    - If no time exists, return "NONE".

    User message: "{text}"
    """

    raw = llm.invoke(prompt).content.strip()
    raw = re.sub(r"```.*?\n|```", "", raw).strip()

    if raw.upper() == "NONE":
        return None

    # Basic regex for times
    match = re.findall(r"(\d{1,2})(?::(\d{2}))?\s*(AM|PM|am|pm)?", raw)

    if match:
        hour, minute, meridiem = match[0]

        hour = int(hour)
        minute = int(minute) if minute else 00

        if meridiem:
            meridiem = meridiem.lower()
            if meridiem == "pm" and hour != 12:
                hour += 12
            if meridiem == "am" and hour == 12:
                hour = 0

        if 0 <= hour < 24 and 0 <= minute < 60:
            return f"{hour:02d}:{minute:02d}"

    # Fuzzy keyword rules
    fuzzy = raw.lower()
    if "morning" in fuzzy:
        return "09:00"
    if "afternoon" in fuzzy:
        return "15:00"
    if "evening" in fuzzy:
        return "19:00"
    if "night" in fuzzy or "tonight" in fuzzy:
        return "21:00"
    if "noon" in fuzzy:
        return "12:00"
    if "midnight" in fuzzy:
        return "00:00"

    return None
