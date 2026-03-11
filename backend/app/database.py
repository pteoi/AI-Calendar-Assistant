from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base

Base = declarative_base()

load_dotenv("backend\.env")

SQLACHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agenda.db")

engine = create_engine(
    SQLACHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
