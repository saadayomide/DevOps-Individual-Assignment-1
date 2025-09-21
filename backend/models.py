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
