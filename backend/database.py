import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./government_spending.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Category model
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    allocated_budget = Column(Float, nullable=False)
    remaining_budget = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Proposal model (Phase 2)
class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    ministry = Column(String, index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    requested_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending", nullable=False)  # Pending/Approved/Rejected
    approved_amount = Column(Float, nullable=True)
    decision_notes = Column(String, nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables

def create_tables():
    Base.metadata.create_all(bind=engine)

    # Lightweight migration for SQLite: add new columns if missing
    try:
        conn = sqlite3.connect(engine.url.database)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(proposals)")
        cols = {row[1] for row in cur.fetchall()}
        migrations = []
        if "approved_amount" not in cols:
            migrations.append("ALTER TABLE proposals ADD COLUMN approved_amount REAL")
        if "decision_notes" not in cols:
            migrations.append("ALTER TABLE proposals ADD COLUMN decision_notes TEXT")
        if "decided_at" not in cols:
            migrations.append("ALTER TABLE proposals ADD COLUMN decided_at DATETIME")
        for sql in migrations:
            cur.execute(sql)
        if migrations:
            conn.commit()
    except Exception as e:
        # Best-effort; on failure, proceed (dev environment)
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

# Database dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
