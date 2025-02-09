from sqlmodel import Field, SQLModel
from datetime import datetime
from sqlalchemy import Text
    
class Chat(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    question: str = Field(sa_column=Text())   
    answer: str = Field(sa_column=Text()) 
    user_id: int = Field(nullable=False)
    topic_id: int = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)