from pydantic import BaseModel

class ChatRequest(BaseModel):
    question : str
    topic_id : int