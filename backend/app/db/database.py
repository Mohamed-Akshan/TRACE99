from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import get_settings


settings = get_settings()

# Connect to PostgreSQL.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True
)

# Create sessions to work with database records.
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

# Parent class for our database tables.
Base = declarative_base()


# Give each API request a database session.
def get_db():
    with SessionLocal() as db:
        yield db
