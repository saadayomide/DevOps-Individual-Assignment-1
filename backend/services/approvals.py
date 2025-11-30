"""
Service for proposal approval and rejection business logic.
Handles the approval workflow, budget checks, and atomic updates.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from database import Proposal as DBProposal
from exceptions import (
    CategoryNotFoundError,
    InsufficientBudgetError,
    InvalidProposalStatusError,
    ProposalNotFoundError,
    ValidationError,
)
from repositories.proposals import ProposalRepository


class ApprovalService:
    """Service for handling proposal approvals and rejections."""

    @staticmethod
    def approve_proposal(
        db: Session, proposal_id: int, approved_amount: float, decision_notes: str | None = None
    ) -> DBProposal:
        """
        Approve a proposal with the given approved amount.

        Validates:
        - Proposal exists and is in Pending status
        - Approved amount is valid (> 0, <= requested_amount)
        - Category has sufficient remaining budget

        Atomically updates category remaining budget and proposal status.
        """
        # Get proposal
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")

        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be approved")

        # Validate approved amount
        if approved_amount is None or approved_amount <= 0:
            raise ValidationError("approved_amount must be > 0")

        if approved_amount > proposal.requested_amount:
            raise ValidationError("approved_amount exceeds requested amount")

        # Get category with lock for atomic update
        category = ProposalRepository.get_category_with_lock(db, proposal.category_id)
        if not category:
            raise CategoryNotFoundError("Category does not exist")

        # Check budget availability
        if approved_amount > category.remaining_budget:
            raise InsufficientBudgetError("Insufficient remaining budget")

        # Atomically apply decision
        category.remaining_budget = category.remaining_budget - approved_amount
        proposal.status = "Approved"
        proposal.approved_amount = approved_amount
        proposal.decision_notes = decision_notes
        proposal.decided_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(proposal)

        return proposal

    @staticmethod
    def reject_proposal(
        db: Session, proposal_id: int, decision_notes: str | None = None
    ) -> DBProposal:
        """
        Reject a proposal.

        Validates:
        - Proposal exists and is in Pending status

        Updates proposal status to Rejected.
        """
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")

        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be rejected")

        # Apply rejection
        proposal.status = "Rejected"
        proposal.approved_amount = None
        proposal.decision_notes = decision_notes
        proposal.decided_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(proposal)

        return proposal
