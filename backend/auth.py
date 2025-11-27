import logging
from datetime import datetime, timedelta
from typing import cast

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import User as DBUser
from database import get_db
from models import TokenData
from settings import settings

# Password hashing context - using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

# JWT token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash (supports both bcrypt and legacy SHA256)."""
    # Check if it's a bcrypt hash (starts with $2a$, $2b$, or $2y$)
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        # Try bcrypt verification
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            logger.exception("bcrypt verification failed")
            return False

    # Fallback to legacy SHA256 for backward compatibility
    # This allows existing users to login and migrate on next password change
    import hashlib

    legacy_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return legacy_hash == hashed_password


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str) -> DBUser | None:
    """Authenticate a user with username and password."""
    user: DBUser | None = db.query(DBUser).filter(DBUser.username == username).first()
    if not user:
        print(f"[AUTH] Login failed: user '{username}' not found")
        return None
    hashed_password = cast(str, user.hashed_password)
    if not verify_password(password, hashed_password):
        print(f"[AUTH] Login failed: invalid password for user '{username}'")
        return None
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> DBUser:
    """Get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception from None

    user: DBUser | None = (
        db.query(DBUser).filter(DBUser.username == token_data.username).first()
    )
    if user is None:
        raise credentials_exception
    return user


def require_finance_role(current_user: DBUser = Depends(get_current_user)) -> DBUser:
    """Require finance role."""
    if current_user.role != "finance":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Required role: finance",
        )
    return current_user


def require_ministry_role(current_user: DBUser = Depends(get_current_user)) -> DBUser:
    """Require ministry role."""
    if current_user.role != "ministry":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Required role: ministry",
        )
    return current_user
