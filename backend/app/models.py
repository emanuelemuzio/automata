from sqlmodel import Field, SQLModel
from pydantic import BaseModel
import uuid as uuid_pkg
from datetime import datetime
from sqlalchemy import Text

class DocumentBase(SQLModel):
    filename: str
    extension: str
    
class Document(DocumentBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashname: str = Field(unique=True)
    visible: bool = Field(default=True)
    user_id: int = Field(default=None)

class UserBase(SQLModel):
    username: str = Field(unique=True)
    full_name: str | None = None
    pwd : str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    disabled: bool = Field(default=False) 
    role: str = Field(default='USER')
    
class UserInDB(UserBase):
    hashed_password: str 
    
class LangChainCollection(SQLModel, table=True):
    
    __tablename__ = "langchain_pg_collection"
    
    uuid : uuid_pkg.UUID = Field(primary_key=True, index=True, nullable=False)
    name : str = Field(default=None)
    
class ChatQuestion(BaseModel):
    question : str
    
class RefreshToken(BaseModel):
    refresh_token : str
    
class Chat(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    question: str = Field(sa_column=Text())   
    answer: str = Field(sa_column=Text()) 
    user_id: int = Field(nullable=False)
    topic_id: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime)
    
class ChatTopic(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100, nullable=False)
    user_id: int = Field(nullable=False)
    
class ChatTopicCreate(BaseModel):
    name: str