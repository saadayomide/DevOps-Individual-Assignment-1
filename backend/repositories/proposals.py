"""
Repository for proposal data access.
Encapsulates database queries related to proposals.
"""
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from database import Proposal as DBProposal, Category as DBCategory, Ministry as DBMinistry


class ProposalRepository:
    """Repository for proposal operations."""
    
    @staticmethod
    def get_by_id(db: Session, proposal_id: int) -> Optional[DBProposal]:
        """Get a proposal by ID with relationships loaded."""
        return db.query(DBProposal).options(
            joinedload(DBProposal.ministry)
        ).filter(DBProposal.id == proposal_id).first()
    
    @staticmethod
    def get_all(
        db: Session,
        ministry_id: Optional[int] = None,
        category_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[DBProposal]:
        """Get all proposals with optional filters."""
        query = db.query(DBProposal).options(joinedload(DBProposal.ministry))
        
        if ministry_id:
            query = query.filter(DBProposal.ministry_id == ministry_id)
        if category_id:
            query = query.filter(DBProposal.category_id == category_id)
        if status:
            query = query.filter(DBProposal.status == status)
        
        return query.order_by(DBProposal.created_at.desc()).all()
    
    @staticmethod
    def create(db: Session, proposal_data: dict) -> DBProposal:
        """Create a new proposal."""
        proposal = DBProposal(**proposal_data)
        db.add(proposal)
        db.commit()
        db.refresh(proposal)
        return proposal
    
    @staticmethod
    def update(db: Session, proposal: DBProposal, update_data: dict) -> DBProposal:
        """Update an existing proposal."""
        for key, value in update_data.items():
            setattr(proposal, key, value)
        db.commit()
        db.refresh(proposal)
        return proposal
    
    @staticmethod
    def delete(db: Session, proposal: DBProposal) -> None:
        """Delete a proposal."""
        db.delete(proposal)
        db.commit()
    
    @staticmethod
    def check_duplicate(
        db: Session,
        ministry_id: int,
        title: str,
        requested_amount: float
    ) -> Optional[DBProposal]:
        """Check if a duplicate proposal exists."""
        return db.query(DBProposal).filter(
            DBProposal.ministry_id == ministry_id,
            DBProposal.title == title,
            DBProposal.requested_amount == requested_amount,
        ).first()
    
    @staticmethod
    def get_category_with_lock(db: Session, category_id: int) -> Optional[DBCategory]:
        """Get a category with row lock for atomic updates."""
        return db.query(DBCategory).filter(
            DBCategory.id == category_id
        ).with_for_update(nowait=False).first()

