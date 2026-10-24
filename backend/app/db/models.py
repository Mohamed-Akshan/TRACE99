from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, Text,
    DateTime, ForeignKey
)

from app.db.database import Base, engine


# Get the current date and time when saving records.
def current_time():
    return datetime.now(timezone.utc)


# Store user account information.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # Example: 101

    email = Column(
        String(255), unique=True, nullable=False
    )  # Example: engineer@gmail.com

    password_hash = Column(
        String(255), nullable=False
    )  # Example: encrypted-looking password hash

    role = Column(
        String(30), default="engineer", nullable=False
    )  # Example: engineer

    created_at = Column(
        DateTime(timezone=True), default=current_time
    )  # Example: 2026-10-22 10:30:00 UTC


# Store incidents created by users.
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True)  # Example: 201

    owner_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # Example: 101 (user who created this incident)

    title = Column(
        String(200), nullable=False
    )  # Example: Payment API Failure

    description = Column(
        Text, nullable=False
    )  # Example: Payment requests returning 503 errors

    service = Column(
        String(100), nullable=False
    )  # Example: payment-service

    severity = Column(
        String(20), nullable=False
    )  # Example: Critical

    status = Column(
        String(30), default="Open", nullable=False
    )  # Example: Open, Under Review, Resolved

    created_at = Column(
        DateTime(timezone=True), default=current_time
    )  # Example: When the incident was created

    updated_at = Column(
        DateTime(timezone=True),
        default=current_time,
        onupdate=current_time
    )  # Example: When the incident was last updated


# Create missing tables only when running this file directly.
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables are ready!")
