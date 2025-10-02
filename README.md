# Government Spending Tracker

A web application that simulates how government ministries submit budget proposals to the Ministry of Finance. Finance can approve, partially approve, or reject requests. The system updates category budgets in real time and provides dashboards, history views, and CSV exports for transparency.

## Overview

- **Ministries** are government departments that can submit budget proposals
- **Categories** represent budget lines (e.g., Education, Health). Each category has an allocated and remaining budget.
- **Ministries submit proposals** against categories with automatic ministry creation
- **Finance users** review proposals and decide: Approved, Partially Approved, or Rejected.
- **Approved amounts** are deducted from the category's remaining budget.
- **Dashboards** visualize allocations and approvals; history views allow filtering and export.

## Architecture

- Frontend: React (Create React App), Axios, Chart.js
- Backend: FastAPI, SQLAlchemy, SQLite (local dev)
- Storage: Local file upload parsing (JSON/CSV)

## Project Structure

```
DevOps-Individual-Assignment-1/
├── backend/
│   ├── main.py                # FastAPI app (endpoints)
│   ├── database.py            # SQLAlchemy models and DB helpers
│   ├── models.py              # Pydantic models
│   ├── auth.py                # Authentication and authorization
│   ├── requirements.txt       # Backend dependencies
│   └── government_spending.db # SQLite database
├── frontend/
│   ├── src/
│   │   ├── api.js             # API clients (ministries, categories, proposals, uploads, history)
│   │   ├── CategoryManager.js # Category CRUD UI
│   │   ├── ProposalForm.js    # Proposal submission UI with ministry auto-creation
│   │   ├── ProposalsList.js   # Pending proposals with actions (Approve/Reject/Edit)
│   │   ├── ApprovalDialog.js  # Approve/Reject dialog
│   │   ├── EditProposalDialog.js # Edit proposal dialog for ministry users
│   │   ├── ContractUpload.js  # Upload and parse JSON/CSV into proposal drafts
│   │   ├── Dashboard.js       # Charts and KPIs
│   │   ├── HistoryView.js     # History with filters and CSV export
│   │   ├── Login.js           # Authentication UI
│   │   ├── UserContext.js     # User state management
│   │   ├── RoleGuard.js       # Role-based access control
│   │   ├── Sidebar.js         # Navigation sidebar
│   │   ├── CategoryManager.css# Styling
│   │   └── App.js             # Main application component
│   └── package.json
├── DATABASE_ERD.md            # Database schema documentation
├── sample_contracts.csv       # Sample contract data
├── sample_contracts.json      # Sample contract data
└── README.md
```

## Getting Started

### Backend

1) Install dependencies

```
cd backend
pip3 install -r requirements.txt
```

2) Run the API

```
cd backend
python3 main.py
```

The API runs at http://localhost:8000

### Frontend

1) Install dependencies (created with Create React App)

```
cd frontend
npm install
```

2) Start the dev server

```
npm start
```

The app runs at http://localhost:3000

## Authentication & User Roles

The system supports two user roles with comprehensive access control:

### Default Users
- **Finance User**: `finance` / `fin` - Can approve/reject proposals and manage categories
- **Ministry User**: `ministry` / `min` - Can submit and edit proposals (Ministry of Education)

### Capabilities
- **Finance Users**: 
  - Approve/reject proposals with custom amounts and notes
  - Manage categories and budget allocations
  - View comprehensive dashboards and analytics
  - Create new ministries
- **Ministry Users**: 
  - Submit proposals with automatic ministry creation
  - Edit pending proposals (with time-based restrictions)
  - View proposal history and status
  - Upload and parse contract files (CSV/JSON)

### Key Features
- **Ministry Auto-Creation**: When submitting proposals, ministries are automatically created if they don't exist
- **Role-Based Access**: Different UI and API access based on user role
- **Secure Authentication**: JWT-based authentication with password hashing
- **Foreign Key Integrity**: Proper database relationships between users, ministries, and proposals

## Features by Phase

### Phase 1 — Categories (CRUD)
- Create, read, update, delete categories
- remaining_budget initialized to allocated_budget; proportional update on allocation change

### Phase 2 — Proposal Submission
- Ministries submit proposals (title, category, description, requested_amount)
- Proposals start in Pending status

### Phase 3 — Approval Workflow
- Approve, partially approve, or reject pending proposals
- Validation: approved_amount > 0 and ≤ min(requested_amount, remaining_budget)
- Deduct approved_amount from the category's remaining_budget
- Record decision notes and decided_at

### Phase 4 — Contract Upload and Parsing
- Endpoint: `POST /contracts/parse` (multipart/form-data)
- Accepts JSON/CSV contracts, supports common field aliases, returns normalized drafts
- Frontend: upload, parse preview, inline fix for invalid rows, Create Proposal per row, Create All Valid

### Phase 5 — Visualization Dashboard
- Endpoint: `GET /dashboard/summary`
- Charts:
  - Allocated vs Remaining per category
  - Requested vs Approved by ministry
- KPI totals and auto-refresh after actions

### Phase 6 — History and Export
- Endpoint: `GET /history/proposals` (filters: ministry, category_id, status, date_from, date_to)
- CSV exports:
  - `GET /reports/proposals.csv`
  - `GET /reports/approvals.csv`
- Frontend: filters, sortable columns, pagination, export buttons

## API Summary

Categories
- `GET /categories`
- `POST /categories`
- `GET /categories/{id}`
- `PUT /categories/{id}`
- `DELETE /categories/{id}`

Proposals
- `GET /proposals`
- `POST /proposals`
- `GET /proposals/{id}`
- `PUT /proposals/{id}` (Pending only)
- `DELETE /proposals/{id}` (Pending only)
- `POST /proposals/{id}/approve`
- `POST /proposals/{id}/reject`

Upload and Parsing
- `POST /contracts/parse`

Dashboard
- `GET /dashboard/summary`

History and Exports
- `GET /history/proposals`
- `GET /reports/proposals.csv`
- `GET /reports/approvals.csv`

## Typical Workflow

1) Define categories and allocations
2) Submit proposals for categories
3) Approve or reject proposals
4) Review Dashboard for allocations and approvals
5) Review History and export CSV reports

## Testing

### Backend Unit Tests

**Backend unit tests are mandatory to achieve max grade. Code coverage should be over 90%.**

#### Installing Test Dependencies

```bash
cd backend
pip install pytest pytest-cov pytest-asyncio httpx
```

#### Running Tests

```bash
# Run all tests with coverage
pytest --cov=. --cov-report=term-missing --cov-report=html --cov-fail-under=90

# Run tests with verbose output
pytest -v --cov=. --cov-report=term-missing

# Run specific test file
pytest tests/test_auth.py --cov=. --cov-report=term-missing

# Run tests without coverage (faster development)
pytest
```

#### Test Coverage Reports

After running tests with coverage, you can view detailed reports:

- **Terminal Report**: Coverage summary displayed in terminal
- **HTML Report**: Detailed HTML report generated in `htmlcov/` directory
  ```bash
  open htmlcov/index.html  # macOS
  # or navigate to htmlcov/index.html in your browser
  ```

#### Test Categories

The test suite should include:

1. **Authentication Tests** (`test_auth.py`)
   - Password hashing and verification
   - User authentication
   - JWT token creation and validation
   - Role-based access control

2. **Database Model Tests** (`test_database.py`)
   - User model validation and constraints
   - Category model with budget constraints
   - Proposal model with status consistency
   - Model relationships

3. **API Endpoint Tests** (`test_api_endpoints.py`)
   - Authentication endpoints (login, current user)
   - Category CRUD operations
   - Proposal management and filtering
   - Dashboard summary
   - Contract parsing (CSV/JSON)
   - Error handling and validation

#### Coverage Requirements

- **Minimum Coverage**: 90% code coverage required
- **Test Database**: Use separate SQLite test database
- **Cleanup**: Tests should clean up after themselves
- **Isolation**: Each test should be independent

## Database Schema

For detailed information about the database schema and entity relationships, see:
- **`DATABASE_ERD.md`** - Complete database schema documentation with ERD

The current schema includes:
- **3 tables**: `categories`, `users`, `proposals`
- **Simple relationships**: Categories have many proposals, users create proposals
- **Basic constraints**: Unique usernames/emails, foreign key relationships

## Notes and Limitations

- SQLite is used for local development; Postgres is recommended for multi-user deployments
- FastAPI `on_event` startup is currently used; consider lifespan handlers in future refactors
- **Unit tests are required for maximum grade achievement**

## Roadmap (Optional next steps)

- Phase 7: Simulation mode, overspending alerts, and basic roles
- DevOps: Docker, docker-compose, CI pipeline, Postgres migrations
- Tests: unit tests for approvals, parsing, and summary aggregation
- UX: drill-down from charts to filtered history, saved filter presets

