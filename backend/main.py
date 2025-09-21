from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from database import get_db, create_tables, Category as DBCategory
from models import Category, CategoryCreate, CategoryUpdate

# Create FastAPI app
app = FastAPI(title="Government Spending Tracker", version="1.0.0")

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
