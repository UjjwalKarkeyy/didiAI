# DEFINES CUSTOM RAG RETRIEVER
from app.config import settings
from app.rag.embeddings import embedding_function
from app.rag.vector_store import client

# custom rag retriever class
class RagRetriever():
    def __init__(self, collection = settings.QDRANT_COLLECTION, embedding_func = embedding_function, top_k: int = 3):
        self.collection = collection
        self.embedding_func = embedding_func
        self.top_k = top_k # number of top results
        
    # vector embed user's query
    def query_to_vec(self, user_query):
        query_embed = self.embedding_func.embed_query(user_query)
        return query_embed
    
    # use Qdrant to search closest vectors
    def search(self, query: str, score_threshold: float = 0.0):
        query_embed = self.query_to_vec(query)
        try:
            results = client.search(
                collection_name = self.collection, 
                query_vector = query_embed, 
                limit = self.top_k
            )

            # process results
            retrieved_docs = []

            # process each ScorePoint
            for i, point in enumerate(results):
                chunk_text = point.payload.get("text", "")
                metadata = point.payload
                similarity_score = point.score
                id = point.id 

                if similarity_score < score_threshold:
                    continue
                retrieved_docs.append({
                    "id": id,
                    "content": chunk_text,
                    "metadata": metadata,
                    "similarity_score": similarity_score,
                    "rank": i+1
                })

                return retrieved_docs
            
        except Exception as e:
            print("Error in retriever: ", e)
            return []