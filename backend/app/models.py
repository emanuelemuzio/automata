from sqlmodel import Field, SQLModel
from pydantic import BaseModel
import uuid as uuid_pkg

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
    
class UserInDB(UserBase):
    hashed_password: str 
    
class LangChainCollection(SQLModel, table=True):
    
    __tablename__ = "langchain_pg_collection"
    
    uuid : uuid_pkg.UUID = Field(primary_key=True, index=True, nullable=False)
    name : str = Field(default=None)
    
class ChatQuestion(BaseModel):
    question : str