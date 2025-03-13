from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import config
from auth.models import Base

# Create SQLAlchemy engine
engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Create all tables
Base.metadata.create_all(bind=engine)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 