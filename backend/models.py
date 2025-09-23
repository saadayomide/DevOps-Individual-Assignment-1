from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
    ministry: str
    category_id: int
    title: str
    description: Optional[str] = None
    requested_amount: float

class ProposalCreate(ProposalBase):
    pass

class ProposalUpdate(BaseModel):
    ministry: Optional[str] = None
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

    class Config:
        from_attributes = True


class ProposalApprove(BaseModel):
    approved_amount: float
    decision_notes: str | None = None

class ProposalReject(BaseModel):
    decision_notes: str | None = None
