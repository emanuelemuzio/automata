from sqlmodel import Field, SQLModel
from pydantic import BaseModel
import uuid as uuid_pkg
from datetime import datetime
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
    
class LangChainEmbedding(SQLModel, table=True):
    
    __tablename__ = "langchain_pg_embedding"
    
    collection_id : uuid_pkg.UUID = Field(nullable=False)
    id : str = Field(primary_key=True, index=True, nullable=False)
    document : str = Field(default=None)
    cmetadata : dict = Field(sa_type=JSONB, nullable=False) 