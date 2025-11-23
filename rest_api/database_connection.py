from dotenv import load_dotenv
from fastapi import APIRouter
from pymongo import MongoClient
from config import Settings

load_dotenv()
settings = Settings()
properties_router = APIRouter()

DB_NAME = "apartamentos"
COLLECTION_NAME = "third_test_imoveis"

def get_properties_collection():
    cliente = MongoClient(settings.mongo_uri, serverSelectionTimeoutMS=30000, tls=True)
    print(settings.mongo_uri, flush=True)
    db = cliente[DB_NAME]
    colecao = db[COLLECTION_NAME]
    return colecao

def create_vector_search_index():
    """Create vector search index if it doesn't exist."""
    properties_collection = get_properties_collection()
    
    vector_index_definition = {
        "name": "property_vector_index",
        "type": "vectorSearch",
        "definition": {
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding_vector",
                    "numDimensions": 768,
                    "similarity": "cosine"
                }
            ]
        }
    }
    
    try:
        existing_indexes = list(properties_collection.list_search_indexes())
        index_exists = any(idx.get('name') == 'property_vector_index' for idx in existing_indexes)
        
        if not index_exists:
            properties_collection.create_search_index(vector_index_definition)
    except Exception as e:
        print(f"Unexpected error creating vector search index: {e}", flush=True)