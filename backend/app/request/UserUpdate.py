from pydantic import BaseModel

class UserUpdate(BaseModel):
    username: str 
    full_name: str
    pwd : str