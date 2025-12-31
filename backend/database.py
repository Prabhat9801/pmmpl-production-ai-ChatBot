"""
SQLite database setup for chat history.
Designed to be flexible for future migration to Supabase.
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class ChatHistory(Base):
    """
    Chat history model - flexible schema for Supabase migration.
    """
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=True)  # For future user sessions
    user_question = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    confidence = Column(Float, nullable=True)
    rows_found = Column(Integer, nullable=True)
    query_type = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Metadata for future extensibility
    metadata_json = Column(Text, nullable=True)  # JSON string for additional data


class QueryCache(Base):
    """
    Query cache model - stores responses for similar queries to reduce tokens.
    Cache cleared on data refresh, backend restart, or session deletion (95% similarity threshold).
    """
    __tablename__ = "query_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True, nullable=True)  # Track which session created this cache
    query_text = Column(Text, nullable=False, index=True)
    response = Column(Text, nullable=False)
    confidence = Column(Float, nullable=True)
    rows_found = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    hit_count = Column(Integer, default=1)  # Track cache hits


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
