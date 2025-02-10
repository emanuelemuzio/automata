from sqlmodel import Session, SQLModel, select
from sqlmodel import create_engine
from fastapi import Depends 
from typing import Annotated
from .config import *
from .model.User import User

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

def create_default_user():
    user = SessionDep.exec(
        select(User)
        .where(User.username == "admin@admin.com")
    ).one_or_none()
    
    if user is not None:
        return
    
    user = User(
        full_name="Admin Admin",
        username="admin@admin.com",
        pwd="$2b$12$eZx7CwMf4HEqUMjYDBvzKuIH0y0Qm.7VZZ9jlc.jRlAQ6KIMWLxyW",
        role="ADMIN",
        disabled=False
    )
    
    SessionDep.add(user)
    SessionDep.commit()