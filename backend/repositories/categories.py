"""
Repository for category data access.
Encapsulates database queries related to categories.
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from database import Category as DBCategory, Proposal as DBProposal


class CategoryRepository:
    """Repository for category operations."""
    
    @staticmethod
    def get_all(db: Session) -> List[DBCategory]:
        """Get all categories."""
        return db.query(DBCategory).all()
    
    @staticmethod
    def get_by_id(db: Session, category_id: int) -> Optional[DBCategory]:
        """Get a category by ID."""
        return db.query(DBCategory).filter(DBCategory.id == category_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[DBCategory]:
        """Get a category by name (case-insensitive)."""
        return db.query(DBCategory).filter(DBCategory.name.ilike(name)).first()
    
    @staticmethod
    def create(db: Session, category_data: dict) -> DBCategory:
        """Create a new category."""
        category = DBCategory(**category_data)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    
    @staticmethod
    def update(db: Session, category: DBCategory, update_data: dict) -> DBCategory:
        """Update an existing category."""
        for key, value in update_data.items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category
    
    @staticmethod
    def delete(db: Session, category: DBCategory) -> None:
        """Delete a category."""
        db.delete(category)
        db.commit()
    
    @staticmethod
    def get_approved_total(db: Session, category_id: int) -> float:
        """Get total approved amount for a category."""
        result = db.query(func.coalesce(func.sum(DBProposal.approved_amount), 0.0)).filter(
            DBProposal.category_id == category_id,
            DBProposal.status == "Approved"
        ).scalar()
        return float(result or 0.0)

