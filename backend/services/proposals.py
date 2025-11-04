"""
Service for proposal business logic.
Handles proposal creation, updates, validation, and queries.
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from database import Proposal as DBProposal, Category as DBCategory, Ministry as DBMinistry
from repositories.proposals import ProposalRepository
from repositories.categories import CategoryRepository
from repositories.ministries import MinistryRepository
from models import ProposalCreate, ProposalUpdate
from exceptions import (
    ProposalNotFoundError,
    CategoryNotFoundError,
    MinistryNotFoundError,
    InvalidProposalStatusError,
    ValidationError,
    DuplicateProposalError
)


class ProposalService:
    """Service for handling proposal operations."""
    
    @staticmethod
    def list_proposals(
        db: Session,
        ministry_id: Optional[int] = None,
        category_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[DBProposal]:
        """List proposals with optional filters."""
        return ProposalRepository.get_all(db, ministry_id, category_id, status)
    
    @staticmethod
    def get_proposal(db: Session, proposal_id: int) -> DBProposal:
        """Get a proposal by ID."""
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")
        return proposal
    
    @staticmethod
    def create_proposal(db: Session, payload: ProposalCreate) -> DBProposal:
        """
        Create a new proposal.
        
        Validates:
        - Category exists
        - Ministry exists (or creates new one if ministry_name provided)
        - Requested amount is valid (> 0)
        """
        # Validate category exists
        category = CategoryRepository.get_by_id(db, payload.category_id)
        if not category:
            raise CategoryNotFoundError("Category does not exist")
        
        # Handle ministry - either by ID or name
        ministry = None
        if payload.ministry_id:
            # Find ministry by ID
            ministry = MinistryRepository.get_by_id(db, payload.ministry_id)
            if not ministry:
                raise MinistryNotFoundError("Ministry does not exist")
        elif payload.ministry_name:
            # Find or create ministry by name
            ministry_name = payload.ministry_name.strip()
            if not ministry_name:
                raise ValidationError("Ministry name cannot be empty")
            
            ministry = MinistryRepository.find_or_create(db, ministry_name)
        else:
            raise ValidationError("Either ministry_id or ministry_name is required")
        
        # Validate amount
        if payload.requested_amount is None or payload.requested_amount <= 0:
            raise ValidationError("Requested amount must be greater than 0")
        
        # Create proposal
        proposal_data = {
            "ministry_id": ministry.id,
            "category_id": payload.category_id,
            "title": payload.title,
            "description": payload.description,
            "requested_amount": payload.requested_amount,
            "status": "Pending",
        }
        
        return ProposalRepository.create(db, proposal_data)
    
    @staticmethod
    def update_proposal(
        db: Session,
        proposal_id: int,
        payload: ProposalUpdate
    ) -> DBProposal:
        """
        Update an existing proposal.
        
        Validates:
        - Proposal exists and is in Pending status
        - Updated fields are valid
        - Related entities (ministry, category) exist
        """
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")
        
        # Only edits in Pending state
        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be edited")
        
        update_data = {}
        
        if payload.ministry_id is not None:
            ministry = MinistryRepository.get_by_id(db, payload.ministry_id)
            if not ministry:
                raise MinistryNotFoundError("Ministry does not exist")
            update_data["ministry_id"] = payload.ministry_id
        
        if payload.category_id is not None:
            category = CategoryRepository.get_by_id(db, payload.category_id)
            if not category:
                raise CategoryNotFoundError("Category does not exist")
            update_data["category_id"] = payload.category_id
        
        if payload.title is not None:
            update_data["title"] = payload.title
        
        if payload.description is not None:
            update_data["description"] = payload.description
        
        if payload.requested_amount is not None:
            if payload.requested_amount <= 0:
                raise ValidationError("Requested amount must be greater than 0")
            update_data["requested_amount"] = payload.requested_amount
        
        # Ignore status changes (only allow Pending)
        if payload.status is not None and payload.status != "Pending":
            raise ValidationError("Status changes are not allowed")
        
        return ProposalRepository.update(db, proposal, update_data)
    
    @staticmethod
    def delete_proposal(db: Session, proposal_id: int) -> None:
        """
        Delete a proposal.
        
        Validates:
        - Proposal exists and is in Pending status
        """
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")
        
        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be deleted")
        
        ProposalRepository.delete(db, proposal)

