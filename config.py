import weaviate
from dotenv import load_dotenv
import os

load_dotenv()

COLLECTION_NAME = "RAGCollection"
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")

def weaviate_client():
    return weaviate.connect_to_local(
        host=WEAVIATE_HOST,
        port=8080,
        grpc_port=50051,
    )