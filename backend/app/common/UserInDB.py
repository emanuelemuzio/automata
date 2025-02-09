from sqlmodel import Field, SQLModel

class UserInDB(SQLModel):
    username: str = Field(unique=True)
    full_name: str | None = None
    pwd : str
    hashed_password: str 