from sqlmodel import Field, SQLModel

class Document(SQLModel, table=True):
    filename: str
    extension: str
    id: int | None = Field(default=None, primary_key=True)
    hashname: str = Field(unique=True)
    visible: bool = Field(default=True)
    user_id: int = Field(default=None)