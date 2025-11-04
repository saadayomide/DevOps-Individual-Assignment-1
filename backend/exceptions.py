"""
Custom exceptions for domain errors.
These will be caught and converted to appropriate HTTP responses in main.py.
"""


class DomainError(Exception):
    """Base exception for domain errors."""
    pass


class ProposalNotFoundError(DomainError):
    """Raised when a proposal is not found."""
    pass


class CategoryNotFoundError(DomainError):
    """Raised when a category is not found."""
    pass


class MinistryNotFoundError(DomainError):
    """Raised when a ministry is not found."""
    pass


class InsufficientBudgetError(DomainError):
    """Raised when there's insufficient budget in a category."""
    pass


class InvalidProposalStatusError(DomainError):
    """Raised when trying to perform an operation on a proposal with invalid status."""
    pass


class DuplicateProposalError(DomainError):
    """Raised when trying to create a duplicate proposal."""
    pass


class ValidationError(DomainError):
    """Raised when validation fails."""
    pass


class DuplicateCategoryError(DomainError):
    """Raised when trying to create a category with duplicate name."""
    pass


class DuplicateMinistryError(DomainError):
    """Raised when trying to create a ministry with duplicate name."""
    pass

