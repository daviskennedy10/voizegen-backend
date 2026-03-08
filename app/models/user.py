from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from datetime import datetime
import uuid

# This class represents the "users" table in your database.
# Every attribute with Column() becomes a column in the table.
class User(Base):
    __tablename__ = "users"  # The actual table name in PostgreSQL

    # UUID is a unique ID like "a3f2c1d4-...". Better than auto-incrementing
    # integers because IDs don't leak information about how many users you have.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String, unique=True, nullable=False)  # Must be unique, can't be empty
    google_id = Column(String, unique=True, nullable=False)  # Google's ID for this user
    created_at = Column(DateTime, default=datetime.utcnow)  # Auto-set when created