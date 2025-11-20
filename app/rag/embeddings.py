# DEFINES HUGGING FACE EMBEDDINGS AS EMBEDDING FUNCTION
from langchain_huggingface import HuggingFaceEmbeddings

# use HuggingFace Embedding Function
embedding_function = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)