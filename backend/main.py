from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from database import get_db, create_tables, Category as DBCategory, Proposal as DBProposal
from models import Category, CategoryCreate, CategoryUpdate, Proposal, ProposalCreate, ProposalUpdate

# Create FastAPI app
app = FastAPI(title="Government Spending Tracker", version="1.0.0")
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# CRUD endpoints for categories
@app.get("/categories", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    """Get all budget categories"""
    categories = db.query(DBCategory).all()
    return categories

@app.post("/categories", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new budget category"""
    # Check if category name already exists
    existing = db.query(DBCategory).filter(DBCategory.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category name already exists")
    
    # Create new category with remaining_budget = allocated_budget initially
    db_category = DBCategory(
        name=category.name,
        allocated_budget=category.allocated_budget,
        remaining_budget=category.allocated_budget
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    category = db.query(DBCategory).filter(DBCategory.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.put("/categories/{category_id}", response_model=Category)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    """Update a category"""
    db_category = db.query(DBCategory).filter(DBCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Update fields if provided
    if category_update.name is not None:
        # Check if new name already exists (excluding current category)
        existing = db.query(DBCategory).filter(
            DBCategory.name == category_update.name,
            DBCategory.id != category_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category name already exists")
        db_category.name = category_update.name
    
    if category_update.allocated_budget is not None:
        # Update remaining budget proportionally
        old_allocated = db_category.allocated_budget
        new_allocated = category_update.allocated_budget
        ratio = new_allocated / old_allocated if old_allocated > 0 else 1
        db_category.remaining_budget = db_category.remaining_budget * ratio
        db_category.allocated_budget = new_allocated
    
    db.commit()
    db.refresh(db_category)
    return db_category

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category"""
    db_category = db.query(DBCategory).filter(DBCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}

# Health check endpoint
@app.get("/")
def root():
    return {"message": "Government Spending Tracker API"}



# ------------------ Phase 2: Proposal Endpoints ------------------

@app.get("/proposals", response_model=List[Proposal])
def list_proposals(db: Session = Depends(get_db), ministry: str | None = None, category_id: int | None = None, status: str | None = None):
    query = db.query(DBProposal)
    if ministry:
        query = query.filter(DBProposal.ministry == ministry)
    if category_id:
        query = query.filter(DBProposal.category_id == category_id)
    if status:
        query = query.filter(DBProposal.status == status)
    return query.order_by(DBProposal.created_at.desc()).all()

@app.post("/proposals", response_model=Proposal)
def create_proposal(payload: ProposalCreate, db: Session = Depends(get_db)):
    # Validate category exists
    category = db.query(DBCategory).filter(DBCategory.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")
    # Validate amount
    if payload.requested_amount is None or payload.requested_amount <= 0:
        raise HTTPException(status_code=400, detail="Requested amount must be greater than 0")

    proposal = DBProposal(
        ministry=payload.ministry,
        category_id=payload.category_id,
        title=payload.title,
        description=payload.description,
        requested_amount=payload.requested_amount,
        status="Pending",
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal

@app.get("/proposals/{proposal_id}", response_model=Proposal)
def get_proposal(proposal_id: int, db: Session = Depends(get_db)):
    proposal = db.query(DBProposal).filter(DBProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal

@app.put("/proposals/{proposal_id}", response_model=Proposal)
def update_proposal(proposal_id: int, payload: ProposalUpdate, db: Session = Depends(get_db)):
    proposal = db.query(DBProposal).filter(DBProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    # Only edits in Pending state in Phase 2
    if proposal.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending proposals can be edited in Phase 2")

    if payload.ministry is not None:
        proposal.ministry = payload.ministry
    if payload.category_id is not None:
        category = db.query(DBCategory).filter(DBCategory.id == payload.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")
        proposal.category_id = payload.category_id
    if payload.title is not None:
        proposal.title = payload.title
    if payload.description is not None:
        proposal.description = payload.description
    if payload.requested_amount is not None:
        if payload.requested_amount <= 0:
            raise HTTPException(status_code=400, detail="Requested amount must be greater than 0")
        proposal.requested_amount = payload.requested_amount
    # Ignore status changes in Phase 2 unless staying Pending
    if payload.status is not None and payload.status != "Pending":
        raise HTTPException(status_code=400, detail="Status changes are not allowed in Phase 2")

    db.commit()
    db.refresh(proposal)
    return proposal

@app.delete("/proposals/{proposal_id}")
def delete_proposal(proposal_id: int, db: Session = Depends(get_db)):
    proposal = db.query(DBProposal).filter(DBProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if proposal.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending proposals can be deleted in Phase 2")
    db.delete(proposal)
    db.commit()
    return {"message": "Proposal deleted successfully"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
