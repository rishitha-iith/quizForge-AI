# backend/database.py

from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# PostgreSQL connection string stored in .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Function to create all tables from models
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency to get DB session
def get_session():
    return Session(engine)
