from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from datetime import timedelta
from auth import (
    authenticate_user, create_access_token, get_current_user, 
    get_password_hash, require_finance_role, require_ministry_role
)
from models import UserCreate, UserLogin, Token, User as UserModel
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import csv
import json
import io
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from database import get_db, create_tables, Category as DBCategory, Proposal as DBProposal, User as DBUser
from models import Category, CategoryCreate, CategoryUpdate, Proposal, ProposalCreate, ProposalUpdate, ProposalApprove, ProposalReject, ProposalDelete

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

# ------------------ Authentication Endpoints ------------------

@app.post("/auth/register", response_model=UserModel)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if username already exists
    existing_user = db.query(DBUser).filter(DBUser.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    existing_email = db.query(DBUser).filter(DBUser.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate role
    if user_data.role not in ["ministry", "finance"]:
        raise HTTPException(status_code=400, detail="Role must be 'ministry' or 'finance'")
    
    # Validate ministry field for ministry users
    if user_data.role == "ministry" and not user_data.ministry:
        raise HTTPException(status_code=400, detail="Ministry field is required for ministry users")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = DBUser(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
        ministry=user_data.ministry
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=Token)
def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login a user and return JWT token."""
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/auth/me", response_model=UserModel)
def get_current_user_info(current_user: DBUser = Depends(get_current_user)):
    """Get current user information."""
    return current_user



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


# ------------------ Phase 3: Approval Endpoints ------------------

@app.post("/proposals/{proposal_id}/approve", response_model=Proposal)
def approve_proposal(proposal_id: int, body: ProposalApprove, db: Session = Depends(get_db), current_user: DBUser = Depends(require_finance_role)):
    proposal = db.query(DBProposal).filter(DBProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if proposal.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending proposals can be approved")
    if body.approved_amount is None or body.approved_amount <= 0:
        raise HTTPException(status_code=400, detail="approved_amount must be > 0")
    if body.approved_amount > proposal.requested_amount:
        raise HTTPException(status_code=400, detail="approved_amount exceeds requested amount")
    category = db.query(DBCategory).filter(DBCategory.id == proposal.category_id).with_for_update(nowait=False).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")
    if body.approved_amount > category.remaining_budget:
        raise HTTPException(status_code=400, detail="Insufficient remaining budget")
    # Apply decision atomically
    category.remaining_budget = category.remaining_budget - body.approved_amount
    proposal.status = "Approved"
    proposal.approved_amount = body.approved_amount
    proposal.decision_notes = body.decision_notes
    proposal.decided_at = datetime.utcnow()
    db.commit()
    db.refresh(proposal)
    return proposal

@app.post("/proposals/{proposal_id}/reject", response_model=Proposal)
def reject_proposal(proposal_id: int, body: ProposalReject, db: Session = Depends(get_db), current_user: DBUser = Depends(require_finance_role)):
    proposal = db.query(DBProposal).filter(DBProposal.id == proposal_id).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    if proposal.status != "Pending":
        raise HTTPException(status_code=400, detail="Only pending proposals can be rejected")
    proposal.status = "Rejected"
    proposal.approved_amount = None
    proposal.decision_notes = body.decision_notes
    proposal.decided_at = datetime.utcnow()
    db.commit()
    db.refresh(proposal)
    return proposal


# ------------------ Phase 4: Contract Upload & Parsing ------------------

@app.post("/contracts/parse")
def parse_contract(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: DBUser = Depends(require_ministry_role)):
    filename = file.filename or ""
    content = file.file.read()
    drafts = []

    def map_category_id(category_name: str | None):
        if not category_name:
            return None
        q = db.query(DBCategory).filter(DBCategory.name.ilike(category_name)).first()
        if q:
            return q.id
        q = db.query(DBCategory).filter(DBCategory.name.ilike(f"%{category_name}%")).first()
        return q.id if q else None

    def normalize_record(r: dict):
        ministry = r.get('ministry') or r.get('dept') or r.get('ministry_name')
        category_name = r.get('category') or r.get('category_name') or r.get('dept_category')
        title = r.get('title') or r.get('project') or r.get('subject')
        description = r.get('description') or r.get('details')
        amount = r.get('requested_amount')
        if amount in (None, ''):
            amount = r.get('amount') or r.get('value') or r.get('requested')
        try:
            requested_amount = float(amount) if amount not in (None, '') else None
        except Exception:
            requested_amount = None
        category_id = map_category_id(category_name)
        errors = []
        if not ministry:
            errors.append('missing ministry')
        if not title:
            errors.append('missing title')
        if requested_amount is None or requested_amount <= 0:
            errors.append('invalid amount')
        if category_id is None:
            errors.append('unknown category')
        dup = None
        if ministry and title and requested_amount is not None:
            dup = db.query(DBProposal).filter(
                DBProposal.ministry == ministry,
                DBProposal.title == title,
                DBProposal.requested_amount == requested_amount,
            ).first()
            if dup:
                errors.append('possible duplicate')
        return {
            'ministry': ministry,
            'category_id': category_id,
            'category_name': category_name,
            'title': title,
            'description': description,
            'requested_amount': requested_amount,
            'errors': errors,
            'valid': len(errors) == 0,
        }

    try:
        if filename.lower().endswith('.json'):
            import json
            data = json.loads(content.decode('utf-8'))
            records = data if isinstance(data, list) else [data]
            for r in records:
                drafts.append(normalize_record(r))
        elif filename.lower().endswith('.csv'):
            import csv, io
            text = content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(text))
            for r in reader:
                drafts.append(normalize_record(r))
        else:
            raise HTTPException(status_code=400, detail='Unsupported file type. Use .json or .csv')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Failed to parse file: {str(e)}')

    return {'drafts': drafts}


# ------------------ Phase 5: Dashboard Summary ------------------

@app.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db), current_user: DBUser = Depends(require_finance_role)):
    # Per-category aggregates
    categories = db.query(DBCategory).all()
    # Sum approved amounts grouped by category_id
    from sqlalchemy import func
    approved_sums = dict(
        db.query(DBProposal.category_id, func.coalesce(func.sum(DBProposal.approved_amount), 0.0))
          .filter(DBProposal.status == "Approved")
          .group_by(DBProposal.category_id)
          .all()
    )
    category_stats = []
    for c in categories:
        approved_total = float(approved_sums.get(c.id, 0.0) or 0.0)
        category_stats.append({
            "id": c.id,
            "name": c.name,
            "allocated_budget": float(c.allocated_budget),
            "remaining_budget": float(c.remaining_budget),
            "approved_total": approved_total,
        })

    # Per-ministry aggregates (requested vs approved)
    requested = dict(
        db.query(DBProposal.ministry, func.coalesce(func.sum(DBProposal.requested_amount), 0.0))
          .group_by(DBProposal.ministry)
          .all()
    )
    approved_by_ministry = dict(
        db.query(DBProposal.ministry, func.coalesce(func.sum(DBProposal.approved_amount), 0.0))
          .filter(DBProposal.status == "Approved")
          .group_by(DBProposal.ministry)
          .all()
    )
    ministries = sorted(set(list(requested.keys()) + list(approved_by_ministry.keys())))
    ministry_stats = []
    for m in ministries:
        ministry_stats.append({
            "ministry": m,
            "requested_total": float(requested.get(m, 0.0) or 0.0),
            "approved_total": float(approved_by_ministry.get(m, 0.0) or 0.0),
        })

    # Overall KPIs
    total_allocated = float(sum(c.allocated_budget for c in categories))
    total_remaining = float(sum(c.remaining_budget for c in categories))
    total_approved = float(sum(x[1] for x in approved_sums.items()))

    return {
        "categories": category_stats,
        "ministries": ministry_stats,
        "kpis": {
            "total_allocated": total_allocated,
            "total_remaining": total_remaining,
            "total_approved": total_approved,
        },
    }
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
