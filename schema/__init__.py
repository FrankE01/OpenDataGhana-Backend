# isort:skip_file
from schema.base import Base, Page
from schema.dataset import Dataset, Tag
from schema.user import User, UserModel, UserModelBase
from schema.metadata import Metadata
from core import db

Base.metadata.create_all(db.engine)
