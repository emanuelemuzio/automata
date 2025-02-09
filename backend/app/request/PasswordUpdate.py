from pydantic import BaseModel
    
class PasswordUpdate(BaseModel):
    user_id : int
    password : str