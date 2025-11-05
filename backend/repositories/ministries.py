"""
Repository for ministry data access.
Encapsulates database queries related to ministries.
"""

from sqlalchemy.orm import Session, joinedload

from database import Ministry as DBMinistry


class MinistryRepository:
    """Repository for ministry operations."""

    @staticmethod
    def get_all_active(db: Session) -> list[DBMinistry]:
        """Get all active ministries."""
        return db.query(DBMinistry).filter(DBMinistry.is_active).all()

    @staticmethod
    def get_by_id(db: Session, ministry_id: int) -> DBMinistry | None:
        """Get a ministry by ID."""
        return db.query(DBMinistry).filter(DBMinistry.id == ministry_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> DBMinistry | None:
        """Get a ministry by name (case-insensitive)."""
        return db.query(DBMinistry).filter(DBMinistry.name.ilike(name)).first()

    @staticmethod
    def create(db: Session, ministry_data: dict) -> DBMinistry:
        """Create a new ministry."""
        ministry = DBMinistry(**ministry_data)
        db.add(ministry)
        db.commit()
        db.refresh(ministry)
        return ministry

    @staticmethod
    def find_or_create(db: Session, name: str) -> DBMinistry:
        """Find an existing ministry by name or create a new one."""
        ministry = db.query(DBMinistry).filter(DBMinistry.name.ilike(name)).first()
        if ministry:
            return ministry

        # Create new ministry
        ministry = DBMinistry(name=name.strip(), description=f"Ministry of {name.strip()}")
        db.add(ministry)
        db.commit()
        db.refresh(ministry)
        return ministry

    @staticmethod
    def get_with_proposals(db: Session) -> list[DBMinistry]:
        """Get all ministries with their proposals loaded."""
        return (
            db.query(DBMinistry)
            .options(joinedload(DBMinistry.proposals))
            .filter(DBMinistry.is_active)
            .all()
        )
