import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData,text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

load_dotenv()
DATABASE_URL = os.getenv("POSTGRES_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
metadata = Base.metadata

def create_tables():
    """
    Create tables if they don't exist.
    """
    metadata.create_all(bind=engine)

def get_db():
    """
    Provide a session
    """
    return SessionLocal()

def ping_db() -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except OperationalError:
        return False
