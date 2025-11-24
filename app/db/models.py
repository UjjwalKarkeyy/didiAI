# DEFINES WHAT TABLES (MODELS) TO USE
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from datetime import datetime, timezone

# document table in sqlite
class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(200), nullable=False)
    chunk_strategy = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone = True), default=datetime.now(timezone.utc))

# metadata table in sqlite
class ChunkMetadata(Base):
    __tablename__ = "chunk_metadata"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    vector_id = Column(String(200), unique=True)   # ID used in vector DB
 
# booking table in sqlite
class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    date_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100), nullable=False)

