from sqlmodel import Field, SQLModel
from datetime import datetime

class ChatTopic(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100, nullable=False)
    user_id: int = Field(nullable=False) 
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)