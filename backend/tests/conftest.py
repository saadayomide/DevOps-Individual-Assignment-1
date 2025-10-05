import pytest
import tempfile
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from database import Base, get_db, create_tables
from main import app
from models import UserCreate, MinistryCreate, CategoryCreate
from auth import get_password_hash

# Create test database
TEST_DB_FILE = tempfile.mktemp(suffix='.db')
TEST_ENGINE = create_engine(f"sqlite:///{TEST_DB_FILE}", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)

@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield TEST_ENGINE
    # Cleanup
    Base.metadata.drop_all(bind=TEST_ENGINE)
    os.unlink(TEST_DB_FILE)

@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with database dependency override"""
    def override_get_db():
        yield test_db
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def sample_ministry(test_db):
    """Create a sample ministry for testing"""
    from database import Ministry as DBMinistry
    ministry = DBMinistry(
        name="Test Ministry",
        description="Test Ministry for unit tests"
    )
    test_db.add(ministry)
    test_db.commit()
    test_db.refresh(ministry)
    return ministry

@pytest.fixture(scope="function")
def sample_category(test_db):
    """Create a sample category for testing"""
    from database import Category as DBCategory
    category = DBCategory(
        name="Test Category",
        allocated_budget=1000000.0,
        remaining_budget=1000000.0
    )
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    return category

@pytest.fixture(scope="function")
def sample_user(test_db, sample_ministry):
    """Create a sample user for testing"""
    from database import User as DBUser
    user = DBUser(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        role="ministry",
        ministry_id=sample_ministry.id
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture(scope="function")
def finance_user(test_db):
    """Create a finance user for testing"""
    from database import User as DBUser
    user = DBUser(
        username="finance",
        email="finance@example.com",
        hashed_password=get_password_hash("fin"),
        role="finance",
        ministry_id=None
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture(scope="function")
def auth_headers(client, sample_user):
    """Get authentication headers for test user"""
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def finance_headers(client, finance_user):
    """Get authentication headers for finance user"""
    response = client.post("/auth/login", json={
        "username": "finance",
        "password": "fin"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def sample_proposal(test_db, sample_ministry, sample_category):
    """Create a sample proposal for testing"""
    from database import Proposal as DBProposal
    proposal = DBProposal(
        ministry_id=sample_ministry.id,
        category_id=sample_category.id,
        title="Test Proposal",
        description="Test proposal for unit tests",
        requested_amount=500000.0,
        status="Pending"
    )
    test_db.add(proposal)
    test_db.commit()
    test_db.refresh(proposal)
    return proposal
