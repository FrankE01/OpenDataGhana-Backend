from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from core import logger

load_dotenv()

class Database:
    def __init__(self):
        self.USER = os.getenv("DATABASE_USER")
        self.PASSWORD = os.getenv("DATABASE_PASSWORD")
        self.HOST = os.getenv("DATABASE_HOST")
        self.PORT = os.getenv("DATABASE_PORT")
        self.DBNAME = os.getenv("DATABASE_NAME")
        self.MODE = os.getenv("MODE")

        self.DATABASE_URL = f"postgresql+psycopg2://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DBNAME}{'' if os.getenv('MODE') == 'dev' else '?sslmode=require'}"
        if not database_exists(self.DATABASE_URL):
            create_database(self.DATABASE_URL)

        # If using IPv4 direct connection, use the following connection string
        # self.engine = create_engine(self.DATABASE_URL, echo=True)
        # If using Transaction Pooler or Session Pooler, we want to ensure we disable SQLAlchemy client side pooling -
        # https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
        self.engine = create_engine(self.DATABASE_URL, poolclass=NullPool, echo=True)
        self.connection = self.engine.connect()

        # Test the connection
        try:
            with self.engine.connect() as self.connection:
                logger.info("Connection successful!")
        except Exception as e:
            logger.error(f"Failed to connect: {e}")


    def get_session(self):
        Session = sessionmaker(autoflush=False, autocommit=False, bind=self.engine)
        session = Session()
        try:
            yield session
        finally:
            session.close()

db = Database()