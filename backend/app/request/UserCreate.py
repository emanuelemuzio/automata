from pydantic import BaseModel

class UserCreate(BaseModel):
    role : str
    username: str 
    full_name: str
    password : str