# 🏛️ Government Spending Tracker

A comprehensive web application that simulates the government budget proposal and approval process. Government ministries submit budget requests, which are reviewed and approved by the Ministry of Finance. The system maintains real-time budget tracking, provides detailed analytics, and ensures transparency through comprehensive audit trails.

## 🎯 **What It Does**

The Government Spending Tracker streamlines the government budget management process by:

- **Digitizing Budget Proposals**: Ministries submit budget requests through an intuitive web interface
- **Automating Ministry Management**: New ministries are automatically created when needed
- **Real-time Budget Tracking**: Live monitoring of allocated vs remaining budgets across categories
- **Streamlined Approval Process**: Finance department reviews and approves/rejects proposals with custom amounts
- **Comprehensive Reporting**: Dashboards, analytics, and CSV exports for transparency
- **File Processing**: Bulk proposal creation through CSV/JSON file uploads

## 🏗️ **Architecture & Technology Stack**

### **Frontend (React)**
- **Framework**: React with Create React App
- **Styling**: Custom CSS with responsive design
- **State Management**: React Context API for user authentication
- **HTTP Client**: Axios for API communication
- **Charts**: Chart.js for data visualization
- **Authentication**: JWT token management

### **Backend (FastAPI)**
- **Framework**: FastAPI with automatic API documentation
- **Database**: SQLite with SQLAlchemy ORM + Alembic migrations
- **Authentication**: JWT tokens with bcrypt password hashing (secure, production-ready)
- **Architecture**: Service layer + Repository pattern (SOLID principles)
- **Configuration**: Environment-based settings (no hardcoded values)
- **Validation**: Pydantic models for data validation
- **File Processing**: CSV/JSON upload and parsing with smart field mapping
- **Error Handling**: Domain exceptions with proper HTTP status codes

### **Database Design**
- **SQLite** with proper foreign key relationships
- **4 Core Tables**: ministries, categories, users, proposals
- **Referential Integrity**: All relationships properly maintained
- **Auto-creation**: Ministries created automatically during proposal submission

## Project Structure

```
DevOps-Individual-Assignment-1/
├── backend/
│   ├── main.py                # FastAPI app (thin routers)
│   ├── database.py            # SQLAlchemy models and DB helpers
│   ├── models.py              # Pydantic models
│   ├── auth.py                # Authentication and authorization (bcrypt)
│   ├── settings.py            # Environment configuration (pydantic-settings)
│   ├── exceptions.py          # Domain exceptions
│   ├── services/              # Business logic layer
│   │   ├── approvals.py       # Approval/rejection logic
│   │   ├── proposals.py       # Proposal CRUD operations
│   │   └── parser.py          # Contract parsing logic
│   ├── repositories/          # Data access layer
│   │   ├── proposals.py       # Proposal data access
│   │   ├── categories.py      # Category data access
│   │   └── ministries.py      # Ministry data access
│   ├── alembic/               # Database migrations
│   │   ├── versions/          # Migration files
│   │   └── env.py             # Alembic configuration
│   ├── alembic.ini            # Alembic configuration file
│   ├── requirements.txt       # Backend dependencies
│   ├── test_requirements.txt  # Test dependencies
│   ├── pytest.ini            # Pytest configuration
│   ├── government_spending.db # SQLite database
│   └── tests/                 # Test suite
│       ├── conftest.py        # Test fixtures and configuration
│       ├── test_auth.py       # Authentication tests
│       ├── test_database.py   # Database model tests
│       └── test_api_endpoints.py # API endpoint tests
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

```bash
cd backend
pip3 install -r requirements.txt
```

2) Configure environment (optional)

Create a `.env` file in the `backend/` directory (optional, defaults provided):

```bash
# backend/.env
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///./government_spending.db
CORS_ORIGINS=http://localhost:3000
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3) Run database migrations (creates tables automatically)

```bash
cd backend
alembic upgrade head
```

Or the API will run migrations automatically on startup.

4) Run the API

```bash
cd backend
uvicorn main:app --reload
```

Or:

```bash
cd backend
python3 -m uvicorn main:app --reload
```

The API runs at http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

### Frontend

1) Install dependencies (created with Create React App)

```bash
cd frontend
npm install
```

2) Configure environment (optional)

Create a `.env` file in the `frontend/` directory (optional, defaults to localhost:8000):

```bash
# frontend/.env
REACT_APP_API_BASE_URL=http://localhost:8000
```

3) Start the dev server

```bash
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
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing (production-ready)
- **Foreign Key Integrity**: Proper database relationships between users, ministries, and proposals
- **Finance-Only Access**: Category creation/update/deletion restricted to finance users
- **Clean Architecture**: Service layer + Repository pattern for maintainability and testability
- **Database Migrations**: Alembic for version-controlled schema changes
- **Environment Configuration**: No hardcoded values - all configurable via environment variables

## 🚀 **Core Features**

### **1. Ministry Management**
- **Auto-Creation**: Type any ministry name → automatically created if new
- **Unique Names**: Prevents duplicate ministries with case-insensitive matching
- **Foreign Key Integrity**: Proper database relationships maintained
- **Flexible Input**: No need to pre-create ministries before submission
- **Ministry API**: Full CRUD operations for finance users

### **2. Budget Category Management**
- **CRUD Operations**: Create, read, update, delete categories
- **Budget Tracking**: Allocated vs remaining budget with real-time updates
- **Validation**: Prevents overspending and negative budgets
- **Proportional Updates**: Budget changes update remaining amounts automatically
- **Category Analytics**: Track spending patterns across categories

### **3. Proposal Workflow**
- **Smart Submission**: Ministries submit proposals with automatic ministry creation
- **Status Tracking**: Pending → Approved/Rejected with timestamps
- **Edit Capability**: Ministry users can edit pending proposals
- **Time Restrictions**: Edit locks after finance review begins
- **Audit Trail**: Complete history of all proposal changes
- **Validation**: Comprehensive input validation and business rule enforcement

### **4. Approval Process**
- **Flexible Decisions**: Approve, partially approve, or reject proposals
- **Custom Amounts**: Can approve less than requested amount
- **Decision Notes**: Required explanations for all decisions
- **Budget Integration**: Approved amounts automatically deducted from categories
- **Validation**: Prevents overspending and invalid approvals
- **Real-time Updates**: All changes reflected immediately across the system

### **5. File Upload & Parsing**
- **Multiple Formats**: Support for CSV and JSON files
- **Smart Parsing**: Handles various field names and formats automatically
- **Auto-Mapping**: Maps ministry names to existing ministries or creates new ones
- **Validation**: Comprehensive error checking and duplicate detection
- **Batch Creation**: Create multiple proposals at once from parsed data
- **Preview Mode**: Review and edit parsed data before creating proposals

### **6. Dashboard & Analytics**
- **Visual Charts**: Category budgets and ministry spending overview
- **Key Performance Indicators**: Total requested, approved, and remaining amounts
- **Real-time Updates**: Dashboard refreshes automatically after actions
- **Per-Ministry Views**: Detailed breakdown by government department
- **Budget Health**: Visual indicators for budget utilization
- **Trend Analysis**: Historical spending patterns and projections

### **7. History & Reporting**
- **Complete History**: All proposals with full details and timestamps
- **Advanced Filtering**: By category, status, date range, amount range
- **CSV Export**: Download filtered data for external analysis
- **Statistics**: Comprehensive proposal and approval statistics
- **Search Functionality**: Find specific proposals quickly
- **Audit Compliance**: Complete documentation for transparency

## 📊 **Database Schema**

### **Tables & Relationships:**

```sql
ministries
├── id (Primary Key)
├── name (Unique, Indexed)
├── description
├── created_at
└── is_active

categories  
├── id (Primary Key)
├── name
├── allocated_budget
├── remaining_budget
└── created_at

users
├── id (Primary Key)
├── username (Unique)
├── email
├── hashed_password
├── role (ministry/finance)
├── ministry_id (Foreign Key → ministries.id)
└── created_at

proposals
├── id (Primary Key)
├── ministry_id (Foreign Key → ministries.id)
├── category_id (Foreign Key → categories.id)
├── title
├── description
├── requested_amount
├── status (Pending/Approved/Rejected)
├── approved_amount
├── decision_notes
├── decided_at
└── created_at
```

### **Key Relationships:**
- **One-to-Many**: Ministry → Users (a ministry can have multiple users)
- **One-to-Many**: Ministry → Proposals (a ministry can submit multiple proposals)
- **One-to-Many**: Category → Proposals (a category can receive multiple proposals)
- **Foreign Key Constraints**: Ensure data integrity and prevent orphaned records

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

## 🔄 **Complete Workflow**

### **Typical User Journey:**

#### **For Ministry Users:**
1. **Login**: Authenticate with ministry credentials
2. **Submit Proposal**: 
   - Type ministry name (auto-created if new)
   - Select category and enter proposal details
   - Submit proposal (status: Pending)
3. **Track Status**: Monitor proposal through approval process
4. **Edit if Needed**: Modify pending proposals before finance review
5. **View Results**: See final decision and approved amount

#### **For Finance Users:**
1. **Login**: Authenticate with finance credentials
2. **Review Proposals**: View all pending proposals requiring attention
3. **Make Decisions**: Approve, partially approve, or reject with notes
4. **Monitor Budgets**: Track category budgets and remaining amounts
5. **Generate Reports**: Export data and view comprehensive analytics

### **File Upload Workflow:**
1. **Upload Contract**: Select CSV/JSON file with proposal data
2. **Parse & Validate**: System processes and validates all data
3. **Review Drafts**: User reviews parsed proposals for accuracy
4. **Fix Errors**: Edit any invalid or missing data
5. **Batch Creation**: Create all valid proposals at once
6. **Auto-Creation**: New ministries created automatically as needed

### **Traditional Workflow:**
1) Define categories and allocations
2) Submit proposals for categories
3) Approve or reject proposals
4) Review Dashboard for allocations and approvals
5) Review History and export CSV reports

## 🔄 Phase 1 Improvements (Assignment 2)

Phase 1 focused on code quality, refactoring, and infrastructure improvements:

### ✅ Completed Improvements

1. **Environment Configuration**
   - ✅ Removed all hardcoded values (SECRET_KEY, DATABASE_URL, CORS_ORIGINS)
   - ✅ Added `settings.py` with pydantic-settings for environment variable management
   - ✅ Frontend reads API base URL from `REACT_APP_API_BASE_URL`
   - ✅ All configuration now comes from environment variables or `.env` files

2. **Service Layer Refactoring**
   - ✅ Extracted business logic from routers into service layer
   - ✅ Created `services/approvals.py`, `services/proposals.py`, `services/parser.py`
   - ✅ Routers are now thin HTTP layers (follows SOLID principles)
   - ✅ Removed code duplication and long methods

3. **Repository Layer**
   - ✅ Created data access layer: `repositories/proposals.py`, `repositories/categories.py`, `repositories/ministries.py`
   - ✅ Encapsulated database queries for better maintainability
   - ✅ Consistent query patterns across the codebase

4. **Security Improvements**
   - ✅ Replaced SHA256 with bcrypt for password hashing (production-ready)
   - ✅ Backward compatible (legacy SHA256 hashes still work)
   - ✅ Secure password storage with proper salting

5. **Database Migrations**
   - ✅ Set up Alembic for version-controlled database migrations
   - ✅ Created baseline migration capturing current schema
   - ✅ Replaced ad-hoc SQLite migration code
   - ✅ Database-agnostic (works with PostgreSQL, MySQL, etc.)

6. **Exception Handling**
   - ✅ Created domain exceptions (`exceptions.py`)
   - ✅ Centralized exception handlers in `main.py`
   - ✅ Proper HTTP status code mapping (404 for not found, 400 for validation, etc.)

7. **Business Logic Enforcement**
   - ✅ Finance-only category creation/update/deletion
   - ✅ Role-based access control properly enforced

### 📊 Code Quality Metrics

- **Code Smells Removed**: Hardcoded values, duplication, long methods
- **SOLID Principles**: Applied Single Responsibility, Dependency Inversion
- **Architecture**: Clean separation of concerns (routers → services → repositories)
- **Security**: Production-ready password hashing
- **Maintainability**: Improved with service/repository pattern

### 📝 Migration Commands

```bash
# Check current migration status
cd backend
alembic current

# View migration history
alembic history

# Apply all pending migrations
alembic upgrade head

# Create new migration (after changing models)
alembic revision --autogenerate -m "description_of_changes"
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Testing

### Backend Unit Tests

**Backend unit tests are mandatory to achieve max grade. Code coverage should be at least 70% (Phase 2 target).**

#### Installing Test Dependencies

```bash
cd backend
pip install -r test_requirements.txt
```

Or install manually:
```bash
cd backend
pip install pytest pytest-cov pytest-asyncio httpx fastapi
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
- **Current Coverage**: 91.69% (exceeds requirement)
- **Test Database**: Use separate SQLite test database
- **Cleanup**: Tests should clean up after themselves
- **Isolation**: Each test should be independent

#### Current Test Results

The test suite includes **80 comprehensive tests** with the following coverage:
- **Authentication**: 98% coverage
- **Database Models**: 100% coverage
- **API Endpoints**: 100% coverage
- **Main Application**: 86% coverage
- **Overall**: 91.69% coverage ✅

## 🎯 **Project Highlights**

- ✅ **Production-Ready**: Complete, fully functional application
- ✅ **User-Centered Design**: Intuitive interface with role-based access
- ✅ **Scalable Architecture**: Proper database design with relationships
- ✅ **Secure**: Comprehensive authentication and authorization
- ✅ **Flexible**: Auto-creation and bulk processing capabilities
- ✅ **Professional**: Government-grade interface and functionality
- ✅ **Well-Documented**: Comprehensive documentation and code comments
- ✅ **Testable**: Built with testing requirements in mind
- ✅ **Maintainable**: Clean code structure and separation of concerns


## 🔧 **Development Notes**

- **SQLite**: Used for local development; PostgreSQL recommended for production
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **React**: Component-based frontend with modern hooks and context
- **Testing**: Comprehensive test suite required for maximum grade
- **Security**: JWT authentication with proper password hashing
- **Validation**: Both client-side and server-side input validation

## 🚀 **Deployment Considerations**

- **Database**: Consider PostgreSQL for multi-user production deployments
- **Authentication**: Implement proper session management for production
- **File Storage**: Consider cloud storage for file uploads in production
- **Monitoring**: Add logging and monitoring for production deployment
- **Backup**: Implement regular database backups for production
- **SSL**: Use HTTPS for all production deployments

## 📋 **API Endpoints Summary**

### **Authentication**
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### **Ministries**
- `GET /ministries` - Get all ministries
- `POST /ministries` - Create new ministry (Finance only)
- `POST /ministries/find-or-create` - Find or create ministry by name

### **Categories**
- `GET /categories` - Get all categories
- `POST /categories` - Create new category (Finance only)
- `GET /categories/{id}` - Get category by ID
- `PUT /categories/{id}` - Update category (Finance only)
- `DELETE /categories/{id}` - Delete category (Finance only)

### **Proposals**
- `GET /proposals` - Get proposals with filters
- `POST /proposals` - Create new proposal
- `GET /proposals/{id}` - Get proposal by ID
- `PUT /proposals/{id}` - Update proposal (Ministry, Pending only)
- `DELETE /proposals/{id}` - Delete proposal (Ministry, Pending only)
- `POST /proposals/{id}/approve` - Approve proposal (Finance only)
- `POST /proposals/{id}/reject` - Reject proposal (Finance only)

### **File Processing**
- `POST /contracts/parse` - Parse CSV/JSON contract files

### **Analytics & Reporting**
- `GET /dashboard/summary` - Dashboard analytics (Finance only)
- `GET /history/proposals` - Proposal history with filters
- `GET /reports/proposals.csv` - Export proposals to CSV
- `GET /reports/approvals.csv` - Export approvals to CSV

---

This Government Spending Tracker represents a complete, production-ready budget management system that demonstrates modern web development practices, proper database design, security considerations, and user-centered design principles.

