from sqlmodel import Field, SQLModel
import uuid as uuid_pkg

class LangChainCollection(SQLModel, table=True):
    
    __tablename__ = "langchain_pg_collection"
    
    uuid : uuid_pkg.UUID = Field(primary_key=True, index=True, nullable=False)
    name : str = Field(default=None)