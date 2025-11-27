import sys
from datetime import timedelta
from pathlib import Path

import pytest

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from database import User as DBUser


@pytest.mark.auth
class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_password_hashing(self):
        """Test that passwords are properly hashed with bcrypt"""
        password = "testpassword"
        hashed = get_password_hash(password)

        # Bcrypt hashes start with $2a$, $2b$, or $2y$ and are 60 characters
        assert hashed.startswith(("$2a$", "$2b$", "$2y$"))
        assert len(hashed) == 60
        assert hashed != password

        # Verify it's a valid bcrypt hash
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        assert pwd_context.verify(password, hashed)

    def test_password_verification(self):
        """Test password verification"""
        password = "testpassword"
        hashed = get_password_hash(password)

        # Correct password should verify
        assert verify_password(password, hashed) is True

        # Wrong password should not verify
        assert verify_password("wrongpassword", hashed) is False

        # Empty password should not verify
        assert verify_password("", hashed) is False

    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes"""
        password1 = "password1"
        password2 = "password2"

        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)

        assert hash1 != hash2
        # Bcrypt hashes are 60 characters
        assert len(hash1) == 60
        assert len(hash2) == 60
        # Both should be bcrypt hashes
        assert hash1.startswith(("$2a$", "$2b$", "$2y$"))
        assert hash2.startswith(("$2a$", "$2b$", "$2y$"))


@pytest.mark.auth
class TestTokenCreation:
    """Test JWT token creation and validation"""

    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "testuser"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0
        # JWT tokens have 3 parts separated by dots
        assert len(token.split(".")) == 3

    def test_token_with_expiration(self):
        """Test token creation with custom expiration"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_different_users(self):
        """Test that different users get different tokens"""
        data1 = {"sub": "user1"}
        data2 = {"sub": "user2"}

        token1 = create_access_token(data1)
        token2 = create_access_token(data2)

        assert token1 != token2


@pytest.mark.auth
class TestUserAuthentication:
    """Test user authentication functionality"""

    def test_authenticate_user_success(self, test_db, sample_user):
        """Test successful user authentication"""
        user = authenticate_user(test_db, "testuser", "testpassword")

        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_authenticate_user_wrong_password(self, test_db, sample_user):
        """Test authentication with wrong password"""
        user = authenticate_user(test_db, "testuser", "wrongpassword")

        assert user is None

    def test_authenticate_user_nonexistent(self, test_db):
        """Test authentication with nonexistent user"""
        user = authenticate_user(test_db, "nonexistent", "password")

        assert user is None

    def test_authenticate_user_empty_username(self, test_db):
        """Test authentication with empty username"""
        user = authenticate_user(test_db, "", "password")

        assert user is None

    def test_authenticate_user_empty_password(self, test_db, sample_user):
        """Test authentication with empty password"""
        user = authenticate_user(test_db, "testuser", "")

        assert user is None


@pytest.mark.auth
class TestCurrentUser:
    """Test get_current_user functionality"""

    def test_get_current_user_valid_token(self, test_db, sample_user):
        """Test getting current user with valid token"""
        # Create a valid token
        token = create_access_token({"sub": "testuser"})

        # Mock the HTTPAuthorizationCredentials dependency
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        user = get_current_user(credentials, test_db)

        assert user is not None
        assert user.username == "testuser"

    def test_get_current_user_invalid_token(self, test_db):
        """Test getting current user with invalid token"""
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, test_db)

        assert exc_info.value.status_code == 401

    def test_get_current_user_nonexistent_user(self, test_db):
        """Test getting current user with valid token but nonexistent user"""
        token = create_access_token({"sub": "nonexistent"})

        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, test_db)

        assert exc_info.value.status_code == 401

    def test_get_current_user_expired_token(self, test_db, sample_user):
        """Test getting current user with expired token"""
        token = create_access_token({"sub": "testuser"}, expires_delta=timedelta(hours=-1))

        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, test_db)

        assert exc_info.value.status_code == 401


@pytest.mark.auth
class TestRoleValidation:
    """Test role-based access validation"""

    def test_ministry_role_validation(self, test_db, sample_user):
        """Test ministry role validation"""
        assert sample_user.role == "ministry"
        assert sample_user.ministry_id is not None

    def test_finance_role_validation(self, test_db, finance_user):
        """Test finance role validation"""
        assert finance_user.role == "finance"
        assert finance_user.ministry_id is None

    def test_role_enum_values(self, test_db):
        """Test that only valid role values are accepted"""
        valid_roles = ["ministry", "finance"]

        for role in valid_roles:
            user = DBUser(
                username=f"test_{role}",
                email=f"test_{role}@example.com",
                hashed_password=get_password_hash("password"),
                role=role,
            )
            test_db.add(user)
            test_db.commit()
            test_db.refresh(user)

            assert user.role == role
            test_db.delete(user)
            test_db.commit()
