# DEFINES DOCUMENT INGESTION AND ALSO CREATES VECTOR POINTS
# UUID: Universal Unique Identifier (string type)
import uuid
from typing import List, Tuple
from qdrant_client.models import PointStruct
from langchain_core.documents import Document
from app.rag.chunking import chunk_entry
from app.rag.embeddings import embedding_function
from app.rag.vector_store import upsert_points

# create vector points
def create_vector_points(chunks: List[Document], embeddings: List[List[float]], document_id: int,) -> Tuple[List[PointStruct], List[str]]:

    points: List[PointStruct] = []
    vector_ids: List[str] = []
    # use chunks and embeddings
    for chunk_index, (chunk, emb_vec) in enumerate(zip(chunks, embeddings)):
        vector_id = str(uuid.uuid4())
        vector_ids.append(vector_id)
        # what Qdrant returns
        payload = {
            "document_id": document_id,
            "chunk_index": chunk_index,
            "text": chunk.text,
            "start_index": chunk.metadata.get("start_index"),
            "source": chunk.metadata.get("source"),
        }
        # a single point structure
        point = PointStruct(
            id = vector_id,
            vector = emb_vec,
            payload = payload,
        )

        points.append(point)
    
    return points, vector_ids

# ingest document
def ingest_document_text(text: str, document_id: int, strategy: str = "recursive") -> Tuple[List[str], List[Document]]:
    # chunk document
    chunks: List[Document] = chunk_entry(text, strategy=strategy)

    if not chunks:
        return [], []
    
    chunk_texts: List[str] = [c.page_content for c in chunks]
    # create embeddings
    embeddings: List[List[float]] = embedding_function.embed_documents(chunk_texts)
    # create points
    points, vector_ids = create_vector_points(
        chunks = chunks,
        embeddings= embeddings,
        document_id=document_id,
    )
    # insert points in Qdrant collection
    upsert_points(points)
    return vector_ids, chunks