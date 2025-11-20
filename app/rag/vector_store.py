from qdrant_client import QdrantClient
from app.config import QDRANT_API, QDRANT_HOST

# Initialize Qdrant client
client = QdrantClient(
    host= QDRANT_HOST,
    api_key= QDRANT_API,
)