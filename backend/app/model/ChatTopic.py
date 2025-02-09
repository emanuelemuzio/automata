from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class ChatTopic(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100, nullable=False)
    user_id: int = Field(nullable=False) 