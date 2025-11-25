from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import settings
from datetime import date

# initialize llm (gemini)
llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    api_key = settings.GEMINI_API_KEY,
)

classifier_llm = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash',
    api_key=settings.GEMINI_API_KEY,
)

# store today's date
curr_date = date.today()