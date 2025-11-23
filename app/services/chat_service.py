from app.rag.retriever import RagRetriever
from app.rag.prompt_builder import PROMPT_TEMPLATE
from langchain_core.prompts import ChatPromptTemplate
from app.rag.llm_client import llm

retriever = RagRetriever()

def create_response(query: str):
    context = retriever.search(query=query)
    prompt_chat_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_chat_template.format(context = context, query=query)
    return llm.invoke(prompt)