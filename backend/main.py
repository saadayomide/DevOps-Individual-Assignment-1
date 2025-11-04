from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Request
from fastapi.responses import JSONResponse
from datetime import timedelta
from auth import (
    authenticate_user, create_access_token, get_current_user, 
    get_password_hash, require_finance_role, require_ministry_role
)
from models import UserCreate, UserLogin, Token, User as UserModel
from sqlalchemy.orm import Session
from typing import List
import uvicorn
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from database import get_db, create_tables, Category as DBCategory, Proposal as DBProposal, User as DBUser, Ministry as DBMinistry
from models import Category, CategoryCreate, CategoryUpdate, Proposal, ProposalCreate, ProposalUpdate, ProposalApprove, ProposalReject, ProposalDelete, Ministry, MinistryCreate
from settings import settings

# Import services and exceptions
from services.approvals import ApprovalService
from services.proposals import ProposalService
from services.parser import ContractParserService
from repositories.categories import CategoryRepository
from repositories.ministries import MinistryRepository
from exceptions import (
    ProposalNotFoundError,
    CategoryNotFoundError,
    MinistryNotFoundError,
    InsufficientBudgetError,
    InvalidProposalStatusError,
    ValidationError,
    DuplicateCategoryError,
    DuplicateMinistryError
)

# Create FastAPI app
app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)
app.add_middleware(CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    create_tables()

# Exception handler to convert domain errors to HTTP responses
@app.exception_handler(ProposalNotFoundError)
async def proposal_not_found_handler(request: Request, exc: ProposalNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(CategoryNotFoundError)
async def category_not_found_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(MinistryNotFoundError)
async def ministry_not_found_handler(request: Request, exc: MinistryNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(InsufficientBudgetError)
async def insufficient_budget_handler(request: Request, exc: InsufficientBudgetError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(InvalidProposalStatusError)
async def invalid_status_handler(request: Request, exc: InvalidProposalStatusError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(DuplicateCategoryError)
async def duplicate_category_handler(request: Request, exc: DuplicateCategoryError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(DuplicateMinistryError)
async def duplicate_ministry_handler(request: Request, exc: DuplicateMinistryError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

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
    
    # Validate ministry_id for ministry users
    if user_data.role == "ministry" and not user_data.ministry_id:
        raise HTTPException(status_code=400, detail="Ministry ID is required for ministry users")
    
    # Validate ministry exists if provided
    if user_data.ministry_id:
        ministry = db.query(DBMinistry).filter(DBMinistry.id == user_data.ministry_id).first()
        if not ministry:
            raise HTTPException(status_code=400, detail="Invalid ministry ID")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = DBUser(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role,
        ministry_id=user_data.ministry_id
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
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/auth/me", response_model=UserModel)
def get_current_user_info(current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user information."""
    # Load ministry relationship if user has ministry_id
    if current_user.ministry_id:
        from sqlalchemy.orm import joinedload
        user_with_ministry = db.query(DBUser).options(joinedload(DBUser.ministry)).filter(DBUser.id == current_user.id).first()
        return user_with_ministry
    return current_user



def startup_event():
    create_tables()

# CRUD endpoints for categories
@app.get("/categories", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    """Get all budget categories"""
    return CategoryRepository.get_all(db)

@app.post("/categories", response_model=Category)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role)
):
    """Create a new budget category (Finance users only)"""
    # Check if category name already exists
    existing = CategoryRepository.get_by_name(db, category.name)
    if existing:
        raise DuplicateCategoryError("Category name already exists")
    
    # Create new category with remaining_budget = allocated_budget initially
    category_data = {
        "name": category.name,
        "allocated_budget": category.allocated_budget,
        "remaining_budget": category.allocated_budget
    }
    return CategoryRepository.create(db, category_data)

@app.get("/categories/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID"""
    category = CategoryRepository.get_by_id(db, category_id)
    if not category:
        raise CategoryNotFoundError("Category not found")
    return category

@app.put("/categories/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role)
):
    """Update a category (Finance users only)"""
    db_category = CategoryRepository.get_by_id(db, category_id)
    if not db_category:
        raise CategoryNotFoundError("Category not found")
    
    update_data = {}
    
    # Update fields if provided
    if category_update.name is not None:
        # Check if new name already exists (excluding current category)
        existing = db.query(DBCategory).filter(
            DBCategory.name == category_update.name,
            DBCategory.id != category_id
        ).first()
        if existing:
            raise DuplicateCategoryError("Category name already exists")
        update_data["name"] = category_update.name
    
    if category_update.allocated_budget is not None:
        # Update remaining budget proportionally
        old_allocated = db_category.allocated_budget
        new_allocated = category_update.allocated_budget
        ratio = new_allocated / old_allocated if old_allocated > 0 else 1
        update_data["remaining_budget"] = db_category.remaining_budget * ratio
        update_data["allocated_budget"] = new_allocated
    
    return CategoryRepository.update(db, db_category, update_data)

@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role)
):
    """Delete a category (Finance users only)"""
    db_category = CategoryRepository.get_by_id(db, category_id)
    if not db_category:
        raise CategoryNotFoundError("Category not found")
    
    CategoryRepository.delete(db, db_category)
    return {"message": "Category deleted successfully"}

# ------------------ Ministry Endpoints ------------------

@app.get("/ministries", response_model=List[Ministry])
def get_ministries(db: Session = Depends(get_db)):
    """Get all active ministries"""
    return MinistryRepository.get_all_active(db)

@app.post("/ministries", response_model=Ministry)
def create_ministry(
    ministry: MinistryCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role)
):
    """Create a new ministry (Finance users only)"""
    # Check if ministry name already exists
    existing = MinistryRepository.get_by_name(db, ministry.name)
    if existing:
        raise DuplicateMinistryError("Ministry name already exists")
    
    ministry_data = {
        "name": ministry.name,
        "description": ministry.description
    }
    return MinistryRepository.create(db, ministry_data)

@app.post("/ministries/find-or-create", response_model=Ministry)
def find_or_create_ministry(
    ministry_name: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """Find existing ministry or create new one if not found"""
    if not ministry_name or not ministry_name.strip():
        raise ValidationError("Ministry name is required")
    
    return MinistryRepository.find_or_create(db, ministry_name.strip())

# Health check endpoint
@app.get("/")
def root():
    return {"message": "Government Spending Tracker API"}



# ------------------ Phase 2: Proposal Endpoints ------------------

@app.get("/proposals", response_model=List[Proposal])
def list_proposals(
    db: Session = Depends(get_db),
    ministry_id: int | None = None,
    category_id: int | None = None,
    status: str | None = None
):
    """List proposals with optional filters."""
    return ProposalService.list_proposals(db, ministry_id, category_id, status)

@app.post("/proposals", response_model=Proposal)
def create_proposal(payload: ProposalCreate, db: Session = Depends(get_db)):
    """Create a new proposal."""
    return ProposalService.create_proposal(db, payload)

@app.get("/proposals/{proposal_id}", response_model=Proposal)
def get_proposal(proposal_id: int, db: Session = Depends(get_db)):
    """Get a proposal by ID."""
    return ProposalService.get_proposal(db, proposal_id)

@app.put("/proposals/{proposal_id}", response_model=Proposal)
def update_proposal(proposal_id: int, payload: ProposalUpdate, db: Session = Depends(get_db)):
    """Update a proposal (only if status is Pending)."""
    return ProposalService.update_proposal(db, proposal_id, payload)

@app.delete("/proposals/{proposal_id}")
def delete_proposal(proposal_id: int, db: Session = Depends(get_db)):
    """Delete a proposal (only if status is Pending)."""
    ProposalService.delete_proposal(db, proposal_id)
    return {"message": "Proposal deleted successfully"}


# ------------------ Phase 3: Approval Endpoints ------------------

@app.post("/proposals/{proposal_id}/approve", response_model=Proposal)
def approve_proposal(
    proposal_id: int,
    body: ProposalApprove,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role)
):
    """Approve a proposal (Finance users only)."""
    return ApprovalService.approve_proposal(
        db, proposal_id, body.approved_amount, body.decision_notes
    )

@app.post("/proposals/{proposal_id}/reject", response_model=Proposal)
def reject_proposal(
    proposal_id: int,
    body: ProposalReject,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role)
):
    """Reject a proposal (Finance users only)."""
    return ApprovalService.reject_proposal(
        db, proposal_id, body.decision_notes
    )


# ------------------ Phase 4: Contract Upload & Parsing ------------------

@app.post("/contracts/parse")
def parse_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_ministry_role)
):
    """Parse a contract file (CSV or JSON) and return normalized draft proposals (Ministry users only)."""
    return ContractParserService.parse_contract(db, file)


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
    from sqlalchemy.orm import joinedload
    ministry_proposals = db.query(DBMinistry).options(joinedload(DBMinistry.proposals)).all()
    
    ministry_stats = []
    for ministry in ministry_proposals:
        proposals = ministry.proposals
        requested_total = sum(p.requested_amount for p in proposals)
        approved_total = sum(p.approved_amount for p in proposals if p.status == "Approved" and p.approved_amount)
        
        ministry_stats.append({
            "ministry_id": ministry.id,
            "ministry_name": ministry.name,
            "requested_total": float(requested_total),
            "approved_total": float(approved_total),
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
