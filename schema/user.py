from pydantic import BaseModel
from sqlalchemy import String
from sqlmodel import Field

from schema import Base


class UserModelBase(BaseModel):
    email: str
    password: str


class UserModel(UserModelBase):
    username: str


# Table to store users
class User(Base, table=True):
    __tablename__ = "users"

    username: str = Field(sa_type=String(100), unique=True, nullable=False)

    email: str = Field(
        sa_type=String(100),
        unique=True,
        nullable=False,
        regex=r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",
    )

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
