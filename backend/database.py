from datetime import UTC, datetime
from urllib.parse import urlparse

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from settings import settings

# Database setup
db_url = settings.DATABASE_URL
parsed_db = urlparse(db_url)
masked_host = parsed_db.hostname or "unknown"
masked_db = (parsed_db.path or "/").lstrip("/") or "unknown"
print(f"[database] Using driver={parsed_db.scheme} host={masked_host} db={masked_db}")
connect_args = {}

if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # For PostgreSQL, add connection pooling and timeout settings
    connect_args = {
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }

# Add connection pool settings for better reliability
engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False,          # Set to True for SQL query logging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Ministry model
class Ministry(Base):
    __tablename__ = "ministries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
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
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

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
    ministry_id = Column(
        Integer, ForeignKey("ministries.id"), nullable=True
    )  # Foreign key to Ministry
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationships
    ministry = relationship("Ministry", back_populates="users")


# Proposal model (Phase 2)
class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    ministry_id = Column(
        Integer, ForeignKey("ministries.id"), nullable=False
    )  # Foreign key to Ministry
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    requested_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending", nullable=False)  # Pending/Approved/Rejected
    approved_amount = Column(Float, nullable=True)
    decision_notes = Column(String, nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    # Relationships
    ministry = relationship("Ministry", back_populates="proposals")
    category = relationship("Category", back_populates="proposals")


# Create tables


def create_tables():
    """
    Create all database tables using Alembic migrations and seed default data.

    This function:
    1. Runs Alembic migrations to ensure schema is up-to-date
    2. Creates default ministries and users if they don't exist
    """
    from alembic import command
    from alembic.config import Config
    from auth import get_password_hash
    from database import Ministry as DBMinistry
    from database import User as DBUser

    # Run Alembic migrations to ensure schema is up-to-date
    try:
        print("[startup] Loading Alembic configuration...")
        alembic_cfg = Config("alembic.ini")
        print("[startup] Running Alembic migrations to head...")
        command.upgrade(alembic_cfg, "head")
        print("[startup] Database migrations applied successfully")
    except Exception as e:
        # If migrations fail, fall back to creating tables directly
        # This is useful for initial setup or if Alembic isn't configured
        print(f"[startup] Warning: Alembic migration failed: {e}")
        import traceback
        print(f"[startup] Traceback: {traceback.format_exc()}")
        print("[startup] Falling back to direct table creation...")
        Base.metadata.create_all(bind=engine)
        print("[startup] Direct table creation completed")

    # Create default ministries and users if they don't exist
    db = SessionLocal()

    try:
        # Create default ministries
        default_ministries = [
            {
                "name": "Ministry of Education",
                "description": "Government ministry responsible for education policy and funding"
            },
            {
                "name": "Ministry of Health",
                "description": "Government ministry responsible for healthcare policy and public health"
            },
            {
                "name": "Ministry of Infrastructure",
                "description": "Government ministry responsible for infrastructure development and maintenance"
            },
            {
                "name": "Ministry of Defense",
                "description": "Government ministry responsible for national defense and security"
            },
            {
                "name": "Ministry of Finance",
                "description": "Government ministry responsible for financial policy and economic planning"
            },
            {
                "name": "Ministry of Transportation",
                "description": "Government ministry responsible for transportation systems and logistics"
            },
            {
                "name": "Ministry of Energy",
                "description": "Government ministry responsible for energy policy and resource management"
            },
            {
                "name": "Ministry of Agriculture",
                "description": "Government ministry responsible for agricultural policy and food security"
            }
        ]

        # Create ministries if they don't exist
        created_ministries = {}
        for ministry_data in default_ministries:
            existing = db.query(DBMinistry).filter(DBMinistry.name == ministry_data["name"]).first()
            if not existing:
                ministry = DBMinistry(**ministry_data)
                db.add(ministry)
                db.flush()  # Get the ID
                created_ministries[ministry_data["name"]] = ministry
            else:
                created_ministries[ministry_data["name"]] = existing

        # Get Ministry of Education for default user (or use first created)
        education_ministry = created_ministries.get("Ministry of Education")
        if not education_ministry:
            education_ministry = db.query(DBMinistry).filter(DBMinistry.name == "Ministry of Education").first()

        # Create default finance user
        finance_user = db.query(DBUser).filter(DBUser.username == "finance").first()
        if not finance_user:
            finance_user = DBUser(
                username="finance",
                email="finance@gov.com",
                hashed_password=get_password_hash("fin"),
                role="finance",
                ministry_id=None,  # Finance users don't belong to a ministry
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
                ministry_id=education_ministry.id,  # Link to Ministry of Education
            )
            db.add(ministry_user)

        db.commit()
        print("Default ministries and users created successfully")
    except Exception as e:
        print(f"Error creating default ministries and users: {e}")
        db.rollback()
    finally:
        db.close()


# Database dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
