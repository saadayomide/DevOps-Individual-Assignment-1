import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database setup
DATABASE_URL = "sqlite:///./government_spending.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Ministry model
class Ministry(Base):
    __tablename__ = "ministries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    users = relationship("User", back_populates="ministry")
    proposals = relationship("Proposal", back_populates="ministry")

# Category model
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    allocated_budget = Column(Float, nullable=False)
    remaining_budget = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    proposals = relationship("Proposal", back_populates="category")


# User model (Authentication)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "ministry" or "finance"
    ministry_id = Column(Integer, ForeignKey("ministries.id"), nullable=True)  # Foreign key to Ministry
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ministry = relationship("Ministry", back_populates="users")


# Proposal model (Phase 2)
class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    ministry_id = Column(Integer, ForeignKey("ministries.id"), nullable=False)  # Foreign key to Ministry
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    requested_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending", nullable=False)  # Pending/Approved/Rejected
    approved_amount = Column(Float, nullable=True)
    decision_notes = Column(String, nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ministry = relationship("Ministry", back_populates="proposals")
    category = relationship("Category", back_populates="proposals")

# Create tables

def create_tables():
    """Create all database tables including the new Ministry table."""
    from database import User as DBUser, Ministry as DBMinistry
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create default ministries and users if they don't exist
    from auth import get_password_hash
    from sqlalchemy.orm import sessionmaker
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Create default ministry
        education_ministry = db.query(DBMinistry).filter(DBMinistry.name == "Ministry of Education").first()
        if not education_ministry:
            education_ministry = DBMinistry(
                name="Ministry of Education",
                description="Government ministry responsible for education policy and funding"
            )
            db.add(education_ministry)
            db.flush()  # Get the ID
        
        # Create default finance user
        finance_user = db.query(DBUser).filter(DBUser.username == "finance").first()
        if not finance_user:
            finance_user = DBUser(
                username="finance",
                email="finance@gov.com",
                hashed_password=get_password_hash("fin"),
                role="finance",
                ministry_id=None  # Finance users don't belong to a ministry
            )
            db.add(finance_user)
        
        # Create default ministry user
        ministry_user = db.query(DBUser).filter(DBUser.username == "ministry").first()
        if not ministry_user:
            ministry_user = DBUser(
                username="ministry",
                email="ministry@gov.com",
                hashed_password=get_password_hash("min"),
                role="ministry",
                ministry_id=education_ministry.id  # Link to Ministry of Education
            )
            db.add(ministry_user)
        
        db.commit()
        print("Default ministries and users created successfully")
    except Exception as e:
        print(f"Error creating default ministries and users: {e}")
        db.rollback()
    finally:
        db.close()

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
