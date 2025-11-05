"""
Service for contract parsing business logic.
Handles CSV/JSON file parsing, normalization, and validation.
"""

import csv
import io
import json
from typing import Any

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from database import Category as DBCategory
from database import Ministry as DBMinistry
from repositories.categories import CategoryRepository
from repositories.ministries import MinistryRepository
from repositories.proposals import ProposalRepository


class ContractParserService:
    """Service for parsing contract files (CSV/JSON)."""

    @staticmethod
    def parse_contract(db: Session, file: UploadFile) -> dict[str, list[dict[str, Any]]]:
        """
        Parse a contract file (CSV or JSON) and return normalized draft proposals.

        Returns:
            Dictionary with 'drafts' key containing list of normalized proposal records
            with validation errors flagged.
        """
        filename = file.filename or ""
        content = file.file.read()
        drafts = []

        # Mapping functions
        def map_category_id(category_name: str | None) -> int | None:
            """Map category name to ID (case-insensitive, partial match)."""
            if not category_name:
                return None

            # Try exact match first
            category = CategoryRepository.get_by_name(db, category_name)
            if category:
                return category.id

            # Try partial match
            category = (
                db.query(DBCategory).filter(DBCategory.name.ilike(f"%{category_name}%")).first()
            )
            return category.id if category else None

        def map_ministry_id(ministry_name: str | None) -> int | None:
            """Map ministry name to ID (case-insensitive, creates if not found)."""
            if not ministry_name:
                return None

            # Try exact match first
            ministry = MinistryRepository.get_by_name(db, ministry_name)
            if ministry:
                return ministry.id

            # Try partial match
            ministry = (
                db.query(DBMinistry).filter(DBMinistry.name.ilike(f"%{ministry_name}%")).first()
            )
            if ministry:
                return ministry.id

            # Create new ministry if not found
            ministry = MinistryRepository.find_or_create(db, ministry_name)
            return ministry.id

        def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
            """Normalize a record from contract file into proposal draft format."""
            # Normalize field names (support multiple variations)
            ministry_name = (
                record.get("ministry") or record.get("dept") or record.get("ministry_name")
            )
            category_name = (
                record.get("category") or record.get("category_name") or record.get("dept_category")
            )
            title = record.get("title") or record.get("project") or record.get("subject")
            description = record.get("description") or record.get("details")

            # Normalize amount (try multiple field names)
            amount = record.get("requested_amount")
            if amount in (None, ""):
                amount = record.get("amount") or record.get("value") or record.get("requested")

            # Parse amount to float
            try:
                requested_amount = float(amount) if amount not in (None, "") else None
            except (ValueError, TypeError):
                requested_amount = None

            # Map to IDs
            category_id = map_category_id(category_name)
            ministry_id = map_ministry_id(ministry_name)

            # Validate and collect errors
            errors = []
            if not ministry_name:
                errors.append("missing ministry")
            if not title:
                errors.append("missing title")
            if requested_amount is None or requested_amount <= 0:
                errors.append("invalid amount")
            if category_id is None:
                errors.append("unknown category")

            # Check for duplicates
            if ministry_id and title and requested_amount is not None:
                duplicate = ProposalRepository.check_duplicate(
                    db, ministry_id, title, requested_amount
                )
                if duplicate:
                    errors.append("possible duplicate")

            return {
                "ministry_name": ministry_name,
                "ministry_id": ministry_id,
                "category_id": category_id,
                "category_name": category_name,
                "title": title,
                "description": description,
                "requested_amount": requested_amount,
                "errors": errors,
                "valid": len(errors) == 0,
            }

        # Parse file based on extension
        try:
            if filename.lower().endswith(".json"):
                data = json.loads(content.decode("utf-8"))
                records = data if isinstance(data, list) else [data]
                for record in records:
                    drafts.append(normalize_record(record))
            elif filename.lower().endswith(".csv"):
                text = content.decode("utf-8")
                reader = csv.DictReader(io.StringIO(text))
                for record in reader:
                    drafts.append(normalize_record(record))
            else:
                raise HTTPException(
                    status_code=400, detail="Unsupported file type. Use .json or .csv"
                )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to parse file: {str(e)}"
            ) from e

        return {"drafts": drafts}
