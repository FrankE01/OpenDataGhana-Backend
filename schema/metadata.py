from typing import Any

from sqlalchemy import JSON, String
from sqlmodel import Field

from schema import Base


# Table to store application metadata
class Metadata(Base, table=True):
    __tablename__ = "metadata"

    item: str = Field(sa_type=String(100), unique=True, nullable=False)

    value: Any = Field(sa_type=JSON, nullable=False)

    def __repr__(self):
        return f"<Metadata(item={self.item}, value={self.value})>"
