# DEFINES USE OF QDRANT FOR STORING VECTOR EMBEDDINGS OF DOCS
from qdrant_client import QdrantClient
from app.config import settings
from qdrant_client.http.models import Distance, VectorParams
from typing import List
from qdrant_client.models import PointStruct

# Initialize Qdrant client
client = QdrantClient(
    url = settings.QDRANT_URL,
    api_key = settings.QDRANT_API_KEY,
)

# func to check if collection exists
def collection_exists():
    try:
        client.get_collection(collection_name = settings.QDRANT_COLLECTION)
        return True
    except:
        return False

# func to create collection if it doesn't exist 
def create_collection_if_not_exist():
    if not collection_exists():
        client.create_collection(
            collection_name = settings.QDRANT_COLLECTION,
            vectors_config = VectorParams(size = 384, distance = Distance.COSINE)
        )

# func for upserting (aka inserting) points (vector embedded doc) to the collection
def upsert_points(points: List[PointStruct]):
    client.upsert(
        collection_name = settings.QDRANT_COLLECTION,
        points = points
    )

# func to delete Qdrant data during startup
def reset_qdrant_collection():
    try:
        if collection_exists():
            client.delete_collection(collection_name=settings.QDRANT_COLLECTION)

    except Exception as e:
        print(f"Exception: {e}")