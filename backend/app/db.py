import os
from dotenv import load_dotenv
from sqlmodel import create_engine

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB_PG = os.getenv("POSTGRES_DB_PG")
POSTGRES_DB_PGV = os.getenv("POSTGRES_DB_PGV")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT"))

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_PG}"
DB_VECTOR_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_PGV}"

engine = create_engine(DB_URL)
vector_engine = create_engine(DB_VECTOR_URL)
