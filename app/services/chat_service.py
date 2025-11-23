from app.rag.retriever import RagRetriever
from app.rag.prompt_builder import PROMPT_TEMPLATE
from langchain_core.prompts import ChatPromptTemplate
from app.rag.llm_client import llm
from app.memory.chat_memory import add_message_to_chat_history, get_chat_history 

retriever = RagRetriever()

def create_response(query: str, session_id: str):
    history = get_chat_history(session_id)
    context = retriever.search(query=query)
    prompt_chat_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_chat_template.format(context = context, query=query, history = history)
    response = llm.invoke(prompt)
    add_message_to_chat_history(session_id, "user", query)
    add_message_to_chat_history(session_id, "didiAI", response.content)
    return response.content