from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load the variables from your .env file into the environment
load_dotenv()

# Read the DATABASE_URL variable from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# create_engine is SQLAlchemy's way of connecting to the database.
# It doesn't open a connection immediately — it just sets up how to connect.
engine = create_engine(DATABASE_URL)

# A SessionLocal is a "conversation" with the database.
# Every time a request comes in, we open a session, do work, then close it.
# autocommit=False means changes aren't saved until we explicitly say so.
# autoflush=False means SQLAlchemy won't auto-send SQL before we're ready.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all your models (tables) will inherit from.
# SQLAlchemy uses it to track all your table definitions.
Base = declarative_base()

# This is a "dependency" — FastAPI will call this function for every
# request that needs database access. It opens a session, yields it
# to the route, then closes it when the request is done.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()