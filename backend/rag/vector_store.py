from dotenv import load_dotenv
from langchain_postgres import PGVector
import os
from embeddings import get_embeddings
from uuid import uuid4

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB_PGV")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))
TABLE_NAME = os.getenv("TABLE_NAME")
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

CONNECTION_STRING = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

def get_vectore_store():

    vector_store = PGVector(
        connection=CONNECTION_STRING,
        collection_name=COLLECTION_NAME,
        embeddings=get_embeddings(),
        use_jsonb=True
    )
    
    return vector_store

def store_documents(documents):
    
    uuids = [str(uuid4()) for _ in range(len(documents))]
    
    vector_store = get_vectore_store()
    vector_store.add_documents(documents=documents, ids=uuids)
    
    return True