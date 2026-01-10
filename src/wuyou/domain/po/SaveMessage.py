import sqlalchemy.dialects.postgresql as postgresql
from sqlmodel import SQLModel, Field, Column

class SaveMessage(SQLModel,table=True):
    __tablename__ = "save_messages"
    id: int = Field(
        sa_column=Column(postgresql.INTEGER,
                         primary_key=True,
                         unique=True,
                         autoincrement=True),
    )
    type: str
    content: str