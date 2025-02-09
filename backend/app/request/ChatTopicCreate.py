from pydantic import BaseModel
    
class ChatTopicCreate(BaseModel):
    name: str