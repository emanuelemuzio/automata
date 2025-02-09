from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    disabled: bool = Field(default=False) 
    role: str = Field(default='USER')
    username: str = Field(unique=True)
    full_name: str | None = None
    pwd : str