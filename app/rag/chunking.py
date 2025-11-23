# DEFINES CHUNKING STRATEGY: RECURSIVE AND FIXED CHUNK
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# func for recursive chunk
def recursive_chunk(text: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 100,
        length_function = len,
        add_start_index = True,
    )

    parent_doc = Document(
        page_content = text,
        metadata = {"source": "upload"}
    )

    chunks = text_splitter.split_documents([parent_doc])
    return chunks

# func for fixed chunk
def fixed_chunk(text: str, chunk_size = 300):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk_text = text[i:i+chunk_size]
        chunks.append(
            Document(
                page_content = chunk_text,
                metadata = {"start_index": i, "source": "upload"}
            )
        )
    return chunks

# func for condition for the two strategy
def chunk_entry(text: str, strategy: str):
    if strategy == "recursive":
        return recursive_chunk(text)
    
    elif strategy == "fixed":
        return fixed_chunk(text)
    
    else:
        raise ValueError("Unknown Strategy")