"""
Service for proposal business logic.
Handles proposal creation, updates, validation, and queries.
"""

from sqlalchemy.orm import Session

from database import Proposal as DBProposal
from exceptions import (
    CategoryNotFoundError,
    InvalidProposalStatusError,
    MinistryNotFoundError,
    ProposalNotFoundError,
    ValidationError,
)
from models import ProposalCreate, ProposalUpdate
from repositories.categories import CategoryRepository
from repositories.ministries import MinistryRepository
from repositories.proposals import ProposalRepository


class ProposalService:
    """Service for handling proposal operations."""

    @staticmethod
    def list_proposals(
        db: Session,
        ministry_id: int | None = None,
        category_id: int | None = None,
        status: str | None = None,
    ) -> list[DBProposal]:
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
    def create_proposal(db: Session, payload: ProposalCreate, current_user) -> DBProposal:
        """
        Create a new proposal.

        Validates:
        - Category exists
        - Ministry exists (or creates new one if ministry_name provided)
        - Requested amount is valid (> 0)
        - Ministry users can only create proposals for their own ministry
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

            # Validate that ministry users can only create proposals for their own ministry
            if current_user.role == "ministry" and current_user.ministry_id != payload.ministry_id:
                raise ValidationError(
                    "You can only create proposals for your own ministry"
                )
        elif payload.ministry_name:
            # For ministry users, they must use their own ministry
            if current_user.role == "ministry":
                if not current_user.ministry_id:
                    raise ValidationError(
                        "You must be assigned to a ministry to create proposals"
                    )
                # Use the user's ministry instead of the provided name
                ministry = MinistryRepository.get_by_id(db, current_user.ministry_id)
                if not ministry:
                    raise MinistryNotFoundError("Your assigned ministry does not exist")
            else:
                # Finance users can create ministries by name (for contract uploads, etc.)
                ministry_name = payload.ministry_name.strip()
                if not ministry_name:
                    raise ValidationError("Ministry name cannot be empty")
                ministry = MinistryRepository.find_or_create(db, ministry_name)
        else:
            # If no ministry specified, use the current user's ministry (for ministry users)
            if current_user.role == "ministry":
                if not current_user.ministry_id:
                    raise ValidationError(
                        "You must be assigned to a ministry to create proposals"
                    )
                ministry = MinistryRepository.get_by_id(db, current_user.ministry_id)
                if not ministry:
                    raise MinistryNotFoundError("Your assigned ministry does not exist")
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
    def update_proposal(db: Session, proposal_id: int, payload: ProposalUpdate, current_user) -> DBProposal:
        """
        Update an existing proposal.

        Validates:
        - Proposal exists and is in Pending status
        - Updated fields are valid
        - Related entities (ministry, category) exist
        - Ministry users can only update proposals from their own ministry
        """
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")

        # Only edits in Pending state
        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be edited")

        # Validate that ministry users can only update proposals from their own ministry
        if current_user.role == "ministry":
            user_ministry_id = current_user.ministry_id or (current_user.ministry.id if current_user.ministry else None)
            proposal_ministry_id = proposal.ministry_id or (proposal.ministry.id if proposal.ministry else None)
            if user_ministry_id != proposal_ministry_id:
                raise ValidationError("You can only update proposals from your own ministry")

        update_data = {}

        if payload.ministry_id is not None:
            # Validate that ministry users can only update to their own ministry
            if current_user.role == "ministry":
                if current_user.ministry_id != payload.ministry_id:
                    raise ValidationError("You can only update proposals to your own ministry")
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
    def delete_proposal(db: Session, proposal_id: int, current_user) -> None:
        """
        Delete a proposal.

        Validates:
        - Proposal exists and is in Pending status
        - Ministry users can only delete proposals from their own ministry
        """
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")

        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be deleted")

        # Validate that ministry users can only delete proposals from their own ministry
        if current_user.role == "ministry":
            user_ministry_id = current_user.ministry_id or (current_user.ministry.id if current_user.ministry else None)
            proposal_ministry_id = proposal.ministry_id or (proposal.ministry.id if proposal.ministry else None)
            if user_ministry_id != proposal_ministry_id:
                raise ValidationError("You can only delete proposals from your own ministry")

        ProposalRepository.delete(db, proposal)
