from sqlalchemy import Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlmodel import Relationship, SQLModel, Field
from uuid import uuid4, UUID
from schema import Base
from typing import List



# Association table to link datasets with tags (many-to-many)
class DatasetTag(SQLModel, table=True):
    __tablename__ = 'dataset_tags'

    dataset_id: UUID = Field(sa_type=SQLAlchemyUUID(as_uuid=True), foreign_key='datasets.id', nullable=False, primary_key=True, default_factory=uuid4)
    tag_id: UUID = Field(sa_type=SQLAlchemyUUID(as_uuid=True), foreign_key='tags.id', nullable=False, primary_key=True, default_factory=uuid4)


# Table to store dataset information
class Dataset(Base, table=True):
    __tablename__ = 'datasets'

    name: str = Field(sa_type=String(255), nullable=False, unique=True)
    description: str = Field(sa_type=Text, nullable=False)
    source: str = Field(sa_type=String(255), nullable=False)
    license: str = Field(sa_type=String(50), nullable=False)
    format: str = Field(sa_type=String(50), nullable=False)
    size: int = Field(sa_type=Integer, nullable=True)  # Size in MB or row count

    # Relationship to tags
    tags: List["Tag"]  = Relationship(link_model=DatasetTag, back_populates="datasets")

    def __repr__(self):
        return f"<Dataset(name={self.name}, source={self.source}, license={self.license})>"
    

# Table to store tags for categorization
class Tag(Base, table=True):
    __tablename__ = 'tags'

    name: str = Field(sa_type=String(50), unique=True, nullable=False)

    # Relationship to datasets
    datasets: List["Dataset"] = Relationship(link_model=DatasetTag, back_populates='tags')

    def __repr__(self):
        return f"<Tag(name={self.name})>"

