from schema.base import Base
from schema.dataset import Dataset, Tag
from core import db

Base.metadata.create_all(db.engine)