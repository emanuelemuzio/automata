from sqlmodel import Session, SQLModel 
from sqlmodel import create_engine
from sqlmodel import Session, SQLModel 
from fastapi import Depends 
from typing import Annotated
from .config import *

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_PG}"
DB_VECTOR_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_PGV}"

engine = create_engine(DB_URL)
vector_engine = create_engine(DB_VECTOR_URL)

def get_session():
    with Session(engine) as session:
        yield session
        
def get_vector_session():
    with Session(vector_engine) as session:
        yield session
        
def create_db_and_tables(): 
    SQLModel.metadata.create_all(engine)
    
SessionDep = Annotated[Session, Depends(get_session)]
VecSessionDep = Annotated[Session, Depends(get_vector_session)]