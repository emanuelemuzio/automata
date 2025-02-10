from pydantic import BaseModel
    
class PasswordUpdate(BaseModel):
    user_id : int
    pwd : str