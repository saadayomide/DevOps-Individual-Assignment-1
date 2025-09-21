# Government Spending Tracker

A web application that simulates how government ministries submit budget proposals to the Ministry of Finance, which then approves or rejects them based on available allocations.

## 🌍 Vision

The Government Spending Tracker demonstrates transparency in budget allocation through a workflow system (submission → review → approval/rejection) and real-time visualization of how contracts and spending affect budgets.

## ✨ Features

### Core Features (Phase 1 - ✅ COMPLETED)
- **Budget Categories (CRUD)** - Create and manage categories like Education, Health, Defense
- **Database Integration** - SQLite database with proper schema
- **REST API** - FastAPI backend with full CRUD endpoints

### Planned Features
- **Proposal Submission** - Ministries submit proposals/contracts
- **Approval Workflow** - Finance Ministry approves/rejects proposals
- **Contract Upload & Parsing** - Upload JSON/CSV contracts
- **Visualization Dashboard** - Charts for budget allocation
- **Proposal History Log** - Track all submissions and results
- **Export/Reporting** - CSV/PDF reports for transparency

## 🛠️ Technical Stack

- **Backend**: Python (FastAPI) for REST API
- **Frontend**: React (planned)
- **Database**: SQLite (will upgrade to Postgres for scaling)
- **Version Control**: Git with incremental commits

## 📁 Project Structure

```
DevOps-Individual-Assignment-1/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database models and connection
│   ├── models.py            # Pydantic models
│   ├── requirements.txt     # Python dependencies
│   └── government_spending.db # SQLite database (auto-created)
├── frontend/                # React app (planned)
└── README.md
```

## 🚀 Getting Started

### Backend Setup (✅ WORKING)

1. **Install Dependencies**
   ```bash
   cd backend
   pip3 install -r requirements.txt
   ```

2. **Run the Server**
   ```bash
   python3 main.py
   ```
   Server runs on: http://localhost:8000

3. **Test the API**
   ```bash
   # Get all categories
   curl http://localhost:8000/categories
   
   # Create a new category
   curl -X POST "http://localhost:8000/categories" \
        -H "Content-Type: application/json" \
        -d '{"name": "Education", "allocated_budget": 5000000}'
   ```

### API Endpoints (✅ TESTED)

- `GET /` - Health check
- `GET /categories` - List all budget categories
- `POST /categories` - Create new category
- `GET /categories/{id}` - Get specific category
- `PUT /categories/{id}` - Update category
- `DELETE /categories/{id}` - Delete category

## 📊 Development Progress

### Phase 1: Core CRUD (✅ COMPLETED)
- [x] Project structure setup
- [x] Database schema design
- [x] FastAPI backend with CRUD endpoints
- [x] SQLite database integration
- [x] API testing and validation

## 🔄 Workflow

1. **Setup** - Finance Ministry defines categories and allocations
2. **Submission** - Ministries submit spending proposals
3. **Review** - Finance Ministry reviews and approves/rejects
4. **Update** - Budget calculations update in real-time
5. **Transparency** - All actions logged and exportable

## 📝 Notes

- Built with Python 3.13 compatibility
- Uses modern FastAPI with Pydantic v2
- Database automatically creates tables on startup
- All endpoints tested and working
- Ready for frontend integration
