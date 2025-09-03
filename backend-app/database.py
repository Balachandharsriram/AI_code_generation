from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, func, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import os

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=func.now())
    description = Column(String)
    st_code = Column(Text, nullable=True)  
    ld_json = Column(Text, nullable=True)
    # --- ADDED COLUMN ---
    is_valid = Column(Boolean, nullable=True)

def create_db_tables():
    """Creates the tables in the database if they don't already exist."""
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        print("Please ensure your PostgreSQL server is running and the connection details in database.py are correct.")