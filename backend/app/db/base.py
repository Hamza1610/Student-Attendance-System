from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Create a synchronous engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a synchronous sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()