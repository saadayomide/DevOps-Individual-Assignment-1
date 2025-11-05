from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# Pydantic models for API
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Category name")
    allocated_budget: float = Field(..., gt=0, description="Allocated budget must be positive")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200, description="Category name")
    allocated_budget: float | None = Field(None, gt=0, description="Allocated budget must be positive")


class Category(CategoryBase):
    id: int
    remaining_budget: float
    created_at: datetime

    class Config:
        from_attributes = True


# ------------------ Phase 2: Proposal Schemas ------------------


class ProposalBase(BaseModel):
    category_id: int = Field(..., gt=0, description="Category ID must be positive")
    title: str = Field(..., min_length=1, max_length=200, description="Proposal title")
    description: str | None = Field(None, max_length=1000, description="Proposal description")
    requested_amount: float = Field(..., gt=0, description="Requested amount must be positive")


class ProposalCreate(ProposalBase):
    ministry_id: int | None = None  # Either ministry_id or ministry_name
    ministry_name: str | None = None  # Either ministry_id or ministry_name


class ProposalUpdate(BaseModel):
    ministry_id: int | None = Field(None, gt=0, description="Ministry ID must be positive if provided")
    category_id: int | None = Field(None, gt=0, description="Category ID must be positive if provided")
    title: str | None = Field(None, min_length=1, max_length=200, description="Proposal title")
    description: str | None = Field(None, max_length=1000, description="Proposal description")
    requested_amount: float | None = Field(None, gt=0, description="Requested amount must be positive if provided")
    status: str | None = None  # still Pending in Phase 2


class Proposal(ProposalBase):
    id: int
    status: str
    approved_amount: float | None = None
    decision_notes: str | None = None
    decided_at: datetime | None = None
    created_at: datetime
    ministry: Optional["Ministry"] = None

    class Config:
        from_attributes = True


class ProposalApprove(BaseModel):
    approved_amount: float = Field(..., gt=0, description="Approved amount must be positive")
    decision_notes: str | None = Field(None, max_length=1000, description="Decision notes")


class ProposalReject(BaseModel):
    decision_notes: str | None = Field(None, max_length=1000, description="Decision notes")


class ProposalDelete(BaseModel):
    reason: str  # Required reason for deletion


# Ministry Models
class MinistryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Ministry name")
    description: str | None = Field(None, max_length=1000, description="Ministry description")


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
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="Email address")
    role: str = Field(..., description="User role: 'ministry' or 'finance'")
    ministry_id: int | None = Field(None, gt=0, description="Ministry ID must be positive if provided")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Basic email validation."""
        if "@" not in v or "." not in v.split("@")[1]:
            raise ValueError("Invalid email format")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is either 'ministry' or 'finance'."""
        if v not in ("ministry", "finance"):
            raise ValueError("Role must be 'ministry' or 'finance'")
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=3, max_length=100, description="Password (min 3 characters)")


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    ministry: Ministry | None = None  # Include ministry relationship

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    username: str | None = None
