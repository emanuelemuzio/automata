from pydantic import BaseModel
    
class ChatTopicUpdate(BaseModel):
    name: str