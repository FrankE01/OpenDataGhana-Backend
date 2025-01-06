from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID


class Base(SQLModel):
    id: UUID = Field(sa_type=SQLAlchemyUUID(as_uuid=True), primary_key=True, default_factory=uuid4)
    created_at: datetime = Field(sa_type=DateTime, default=datetime.now(tz=timezone.utc))
    updated_at: datetime = Field(sa_type=DateTime, default=datetime.now(tz=timezone.utc), sa_column_kwargs={"onupdate":datetime.now(tz=timezone.utc)})
    deleted_at: datetime = Field(sa_type=DateTime, nullable=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def delete(self):
        self.deleted_at = datetime.now(tz=timezone.utc)
        self.name = f"{self.name}_{self.deleted_at.timestamp()}"

    def get_ignored_fields():
        return ["id", "created_at", "updated_at", "deleted_at"]