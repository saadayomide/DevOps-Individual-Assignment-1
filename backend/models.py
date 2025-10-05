from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING

# Pydantic models for API
class CategoryBase(BaseModel):
    name: str
    allocated_budget: float

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    allocated_budget: Optional[float] = None

class Category(CategoryBase):
    id: int
    remaining_budget: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# ------------------ Phase 2: Proposal Schemas ------------------

class ProposalBase(BaseModel):
    category_id: int
    title: str
    description: Optional[str] = None
    requested_amount: float

class ProposalCreate(ProposalBase):
    ministry_id: Optional[int] = None  # Either ministry_id or ministry_name
    ministry_name: Optional[str] = None  # Either ministry_id or ministry_name

class ProposalUpdate(BaseModel):
    ministry_id: Optional[int] = None
    category_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    requested_amount: Optional[float] = None
    status: Optional[str] = None  # still Pending in Phase 2

class Proposal(ProposalBase):
    id: int
    status: str
    approved_amount: float | None = None
    decision_notes: str | None = None
    decided_at: datetime | None = None
    created_at: datetime
    ministry: Optional['Ministry'] = None

    class Config:
        from_attributes = True


class ProposalApprove(BaseModel):
    approved_amount: float
    decision_notes: str | None = None

class ProposalReject(BaseModel):
    decision_notes: str | None = None

class ProposalDelete(BaseModel):
    reason: str  # Required reason for deletion




# Ministry Models
class MinistryBase(BaseModel):
    name: str
    description: Optional[str] = None

class MinistryCreate(MinistryBase):
    pass

class Ministry(MinistryBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication Models
class UserBase(BaseModel):
    username: str
    email: str
    role: str  # "ministry" or "finance"
    ministry_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    ministry: Optional[Ministry] = None  # Include ministry relationship

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None

