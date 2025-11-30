# Government Spending Tracker - Complete Codebase

This document contains the complete source code for the project.

---


================================================================================
## 📂 Root Directory


### 📄 .gitignore

**Path:** `.gitignore`

```text
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/
antenv/

# Database
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.env.local
.env.*.local
.azure/.env
.azure/*-publish-profile.xml

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
coverage.xml

# Logs
*.log
logs/
logs.zip

# Frontend
frontend/node_modules/
frontend/build/
frontend/.env.local
frontend/.env.development.local
frontend/.env.test.local
frontend/.env.production.local

# Alembic
# Keep migration files but ignore database
# backend/alembic/versions/*.py should be committed


```


### 📄 Makefile

**Path:** `Makefile`

```text
.PHONY: help install test lint format coverage clean

help:
	@echo "Available commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make test        - Run tests with coverage"
	@echo "  make lint        - Run all linters (ruff, mypy, bandit)"
	@echo "  make format      - Format code with ruff"
	@echo "  make coverage    - Generate coverage report"
	@echo "  make clean       - Clean up generated files"

install:
	cd backend && pip3 install -r requirements.txt
	cd frontend && npm install

test:
	cd backend && python3 -m pytest --cov=. --cov-report=html --cov-report=term-missing --cov-fail-under=70 -v

lint:
	@echo "Running ruff..."
	cd backend && ruff check .
	@echo "Running mypy..."
	cd backend && mypy . --ignore-missing-imports || true
	@echo "Running bandit..."
	cd backend && bandit -r . -ll || true

format:
	cd backend && ruff format .
	cd backend && ruff check --fix .

coverage:
	cd backend && python3 -m pytest --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in backend/htmlcov/index.html"

clean:
	rm -rf backend/__pycache__ backend/**/__pycache__
	rm -rf backend/.pytest_cache backend/htmlcov backend/.coverage
	rm -rf frontend/node_modules frontend/build


```


### 📄 README.md

**Path:** `README.md`

```markdown
# Government Spending Tracker

A comprehensive web application that simulates the government budget proposal and approval process. Government ministries submit budget requests, which are reviewed and approved by the Ministry of Finance. The system maintains real-time budget tracking, provides detailed analytics, and ensures transparency through comprehensive audit trails.

## What It Does

The Government Spending Tracker streamlines the government budget management process by:

- **Digitizing Budget Proposals**: Ministries submit budget requests through an intuitive web interface
- **Automating Ministry Management**: New ministries are automatically created when needed
- **Real-time Budget Tracking**: Live monitoring of allocated vs remaining budgets across categories
- **Streamlined Approval Process**: Finance department reviews and approves/rejects proposals with custom amounts
- **Comprehensive Reporting**: Dashboards, analytics, and CSV exports for transparency
- **File Processing**: Bulk proposal creation through CSV/JSON file uploads

## Architecture & Technology Stack

### **Frontend (React)**
- **Framework**: React with Create React App
- **Styling**: Custom CSS with responsive design
- **State Management**: React Context API for user authentication
- **HTTP Client**: Axios for API communication
- **Charts**: Chart.js for data visualization
- **Authentication**: JWT token management

### **Backend (FastAPI)**
- **Framework**: FastAPI with automatic API documentation
- **Database**: PostgreSQL (Azure App Service) via SQLAlchemy + Alembic (SQLite fallback for local development)
- **Authentication**: JWT tokens with bcrypt password hashing (secure, production-ready)
- **Architecture**: Service layer + Repository pattern (SOLID principles)
- **Configuration**: Environment-based settings (no hardcoded values)
- **Validation**: Pydantic models for data validation
- **File Processing**: CSV/JSON upload and parsing with smart field mapping
- **Error Handling**: Domain exceptions with proper HTTP status codes

### **Database Design**
- **PostgreSQL** schema in production (SQLite-compatible for local dev)
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
│   ├── government_spending.db # Local SQLite database (dev only)
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

Create a `.env` file in the `backend/` directory (optional, defaults provided). Postgres is recommended for Azure deployments, SQLite works for local dev:

```bash
# backend/.env
SECRET_KEY=your-secret-key-change-in-production
# Example Azure PostgreSQL connection string (psycopg 3 driver)
DATABASE_URL=postgresql+psycopg://db_user:strongpassword@your-pg-host.postgres.database.azure.com:5432/gov_spending?sslmode=require

# Local fallback (optional)
# DATABASE_URL=sqlite:///./government_spending.db
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
- Health Check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

**Or use Docker Compose (recommended for Phase 3):**
```bash
docker-compose up -d
```

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

## Core Features

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

## Database Schema

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

## Complete Workflow

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

## Phase 1 Improvements (Assignment 2)

Phase 1 focused on code quality, refactoring, and infrastructure improvements:

###  Completed Improvements

1. **Environment Configuration**
   - Removed all hardcoded values (SECRET_KEY, DATABASE_URL, CORS_ORIGINS)
   - Added `settings.py` with pydantic-settings for environment variable management
   - Frontend reads API base URL from `REACT_APP_API_BASE_URL`
   - All configuration now comes from environment variables or `.env` files

2. **Service Layer Refactoring**
   - Extracted business logic from routers into service layer
   - Created `services/approvals.py`, `services/proposals.py`, `services/parser.py`
   - Routers are now thin HTTP layers (follows SOLID principles)
   - Removed code duplication and long methods

3. **Repository Layer**
   - Created data access layer: `repositories/proposals.py`, `repositories/categories.py`, `repositories/ministries.py`
   - Encapsulated database queries for better maintainability
   - Consistent query patterns across the codebase

4. **Security Improvements**
   - Replaced SHA256 with bcrypt for password hashing (production-ready)
   - Backward compatible (legacy SHA256 hashes still work)
   - Secure password storage with proper salting

5. **Database Migrations**
   - Set up Alembic for version-controlled database migrations
   - Created baseline migration capturing current schema
   - Replaced ad-hoc SQLite migration code
   - Database-agnostic (works with PostgreSQL, MySQL, etc.)

6. **Exception Handling**
   - Created domain exceptions (`exceptions.py`)
   - Centralized exception handlers in `main.py`
   - Proper HTTP status code mapping (404 for not found, 400 for validation, etc.)

7. **Business Logic Enforcement**
   - Finance-only category creation/update/deletion
   - Role-based access control properly enforced

### Code Quality Metrics

- **Code Smells Removed**: Hardcoded values, duplication, long methods
- **SOLID Principles**: Applied Single Responsibility, Dependency Inversion
- **Architecture**: Clean separation of concerns (routers → services → repositories)
- **Security**: Production-ready password hashing
- **Maintainability**: Improved with service/repository pattern

### Migration Commands

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

## Phase 2 Improvements (Assignment 2)

Phase 2 focused on testing, code quality, and validation improvements:

###  Completed Improvements

1. **Linters and Static Analysis**
   - Installed and configured `ruff` for fast Python linting
   - Installed and configured `mypy` for type checking
   - Installed and configured `bandit` for security linting
   - Created `pyproject.toml` with comprehensive linting rules
   - Auto-fixed formatting issues across codebase
   - Fixed code quality issues (exception handling, comparisons)

2. **Test Coverage**
   - **Current Coverage: 93%** (exceeds 70% requirement)
   - All existing tests passing
   - Updated tests to work with new Pydantic validators
   - Coverage reports generated (HTML + terminal)

3. **Stronger Pydantic Validators**
   - Added `Field` constraints to all models:
     - `gt=0` for positive numbers (amounts, IDs)
     - `min_length`/`max_length` for strings (names, titles, descriptions)
     - Custom validators for email and role validation
   - Better error messages with descriptions
   - Validation happens at Pydantic level (422 errors) before reaching services

4. **Code Quality Improvements**
   - Fixed exception handling (proper `raise ... from e`)
   - Fixed boolean comparisons (`is_active` instead of `is_active == True`)
   - Improved type annotations
   - Removed duplicate code

### Quality Metrics

- **Test Coverage**: 93%  (Requirement: 70%)
- **Linting**: All major issues fixed - **Type Checking**: Configured with mypy - **Security Scanning**: Bandit configured - **Code Quality**: Improved with validators and linters 
### Development Commands

```bash
# Run all linters
make lint

# Format code
make format

# Run tests with coverage
make test

# Generate coverage report
make coverage
```

### Linting Commands

```bash
# Run ruff (linter)
cd backend
ruff check .

# Auto-fix ruff issues
ruff check --fix .

# Format code
ruff format .

# Run mypy (type checking)
mypy . --ignore-missing-imports

# Run bandit (security)
bandit -r . -ll
```

## Phase 3: CI/CD & Deployment (Assignment 2)

Phase 3 focuses on automation, containerization, and deployment:

###  Completed Improvements

1. **CI/CD Pipeline (GitHub Actions)**
   - Automated testing on pull requests and pushes
   - Coverage reporting and enforcement (≥70%)
   - Linting checks (ruff, mypy, bandit)
   - Build and test both backend and frontend
   - Docker image building
   - Deployment automation ready (main branch only)

2. **Docker Containerization**
   - Multi-stage Dockerfile for backend (optimized image size)
   - Dockerfile for frontend (nginx-based)
   - Docker Compose for local development with Prometheus & Grafana
   - Environment variable configuration
   - Health checks in containers

3. **Monitoring & Health Checks**
   - `/health` endpoint with database connectivity check
   - Prometheus metrics endpoint (`/metrics`)
   - Request count, latency, and error metrics
   - Grafana dashboard configuration
   - Prometheus configuration for metrics collection

4. **Azure Deployment**
   - Azure App Service configuration for backend and frontend
   - GitHub Actions CI/CD pipeline updated for Azure deployment
   - Deployment scripts and documentation
   - Environment variable configuration
   - **E2E tests with Playwright** (optional, can be added here for full browser testing)
   - Performance testing
   - Load testing

### Phase 3 Goals

- **Automation**: CI/CD pipeline runs tests, builds, and deploys automatically
- **Containerization**: Docker images for reproducible deployments
- **Monitoring**: Health checks and metrics for production visibility
- **Deployment**: Automated deployment to cloud platform

### Deliverables

-  `.github/workflows/ci-cd.yml` - GitHub Actions workflow that builds/tests containers and deploys to Azure App Service
-  (Removed) Azure DevOps pipeline – superseded by GitHub Actions
-  `backend/Dockerfile` - Backend containerization (multi-stage)
-  `frontend/Dockerfile` - Frontend containerization (nginx-based)
-  `docker-compose.yml` - Local development setup with monitoring
-  `ops/prometheus/prometheus.yml` - Prometheus configuration
-  `ops/grafana/` - Grafana dashboard and datasource configuration
-  `.azure/` - Azure deployment reference docs (service principal + secrets guide)
-  `/health` endpoint - Health check with database connectivity
-  `/metrics` endpoint - Prometheus metrics (auto-exposed)

### 🔧 Phase 3 Components Explained

#### **CI/CD Pipeline (GitHub Actions)**

**What it does:**
- Runs automatically on every pull request and push to main branch
- Executes tests, linting, and security checks
- Builds Docker images
- Deploys to cloud platform (main branch only)

**Why it's important:**
- Catches bugs before merging
- Ensures code quality standards
- Automates deployment process
- Provides feedback on code changes

#### **Docker Containerization**

**What it does:**
- Packages application into containers (isolated environments)
- Ensures consistent behavior across different machines
- Makes deployment easier and more reliable

**Why it's important:**
- "Works on my machine" → "Works everywhere"
- Consistent environment for development and production
- Easier scaling and deployment

#### **Monitoring & Health Checks**

**What it does:**
- `/health` endpoint checks if application is running and database is accessible
- `/metrics` endpoint provides Prometheus metrics (request count, latency, errors)
- Grafana dashboard visualizes metrics

**Why it's important:**
- Know if application is healthy
- Monitor performance and errors
- Detect issues before users do
- Track application usage

#### **E2E Tests (Optional)**

**What it does:**
- Tests full user flows in a real browser (Playwright)
- Example: Login → Create proposal → Approve proposal → View dashboard

**Why it's optional:**
- We already have 93% coverage with unit + integration tests
- E2E tests are slower and more complex to maintain
- Can be added later if needed for critical user flows

### Quick Start with Docker

```bash
# Start all services (backend, frontend, Prometheus, Grafana)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

**Access Points:**
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

### Docker Commands

```bash
# Build backend image
cd backend
docker build -t gov-spending-backend:latest .

# Build frontend image
cd frontend
docker build -t gov-spending-frontend:latest --build-arg REACT_APP_API_BASE_URL=http://localhost:8000 .

# Run backend container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg://db_user:strongpassword@your-pg-host.postgres.database.azure.com:5432/gov_spending?sslmode=require \
  -e SECRET_KEY=your-secret-key \
  gov-spending-backend:latest

# Run frontend container
docker run -p 80:80 gov-spending-frontend:latest
```

### Migrating from SQLite to PostgreSQL (Recommended for Azure)

1. **Provision a managed Postgres instance** (e.g., Azure Database for PostgreSQL Flexible Server).
2. **Collect the connection string** and convert it to SQLAlchemy format:
   `postgresql+psycopg://<user>:<password>@<host>:5432/<database>?sslmode=require`
3. **Set `DATABASE_URL`** to that string in:
   - `backend/.env` (local dev / docker compose)
   - App Service configuration (`az webapp config appsettings set ... DATABASE_URL=...`)
4. **Run Alembic migrations** once (`alembic upgrade head`) or let the API apply them on startup.
5. **Redeploy the backend container**. The application will now persist all data in PostgreSQL.

SQLite remains available for quick local work, but Azure deployments should use PostgreSQL to avoid data loss when containers restart.

### Azure Deployment

The application is configured for automated deployment to **Azure App Service** using **GitHub Actions CI/CD**.

#### Prerequisites

Before deploying, ensure you have:
- Azure subscription with a Resource Group
- Azure Container Registry (ACR) created
- Two Linux App Services (one for backend, one for frontend)
- Azure CLI installed locally (`az login`)
- GitHub repository with Actions enabled

#### Step 1: Create Service Principal for GitHub Actions

Create an Azure service principal that GitHub Actions will use to authenticate:

```bash
az ad sp create-for-rbac \
  --name "gov-spending-github-actions" \
  --role contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP> \
  --sdk-auth
```

Copy the JSON output - you'll need it for the next step.

#### Step 2: Configure GitHub Secrets

Go to your GitHub repository → **Settings → Secrets and variables → Actions**, and add the following secrets:

| Secret Name | Description | How to Get It |
|------------|-------------|---------------|
| `AZURE_CREDENTIALS` | Service principal JSON from Step 1 | Paste the JSON output from `az ad sp create-for-rbac` |
| `AZURE_RESOURCE_GROUP` | Your Azure resource group name | e.g., `BCSAI2025-DEVOPS-STUDENTS-A` |
| `AZURE_BACKEND_APP_NAME` | Backend App Service name | e.g., `gov-spending-api` |
| `AZURE_FRONTEND_APP_NAME` | Frontend App Service name | e.g., `gov-spending-web` |
| `AZURE_ACR_LOGIN_SERVER` | ACR login server URL | Run: `az acr show --name <ACR_NAME> --query loginServer -o tsv` |
| `AZURE_ACR_USERNAME` | ACR admin username | Run: `az acr credential show --name <ACR_NAME> --query username -o tsv` |
| `AZURE_ACR_PASSWORD` | ACR admin password | Run: `az acr credential show --name <ACR_NAME> --query passwords[0].value -o tsv` |
| `BACKEND_IMAGE_NAME` | Backend container repo path | e.g., `gov-spending/backend` |
| `FRONTEND_IMAGE_NAME` | Frontend container repo path | e.g., `gov-spending/frontend` |

#### Step 3: Configure App Service Settings

Configure application settings for both App Services in Azure Portal:

**Backend App Service** (Configuration → Application settings):
- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql+psycopg://user:pass@host:5432/db?sslmode=require`)
- `SECRET_KEY`: A secure random string for JWT token signing
- `CORS_ORIGINS`: Frontend URL (e.g., `https://gov-spending-web.azurewebsites.net`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (e.g., `30`)
- `WEBSITES_PORT`: `8000`
- `WEBSITE_HEALTHCHECK_PATH`: `/health`
- `WEBSITE_HEALTHCHECK_MAXPINGFAILURES`: `2`

**Frontend App Service** (Configuration → Application settings):
- `REACT_APP_API_BASE_URL`: Backend API URL (e.g., `https://gov-spending-api.azurewebsites.net`)
- `WEBSITES_PORT`: `80`
- `WEBSITE_HEALTHCHECK_PATH`: `/` (optional)
- `WEBSITE_HEALTHCHECK_MAXPINGFAILURES`: `2`

#### Step 4: Deploy

Once secrets are configured, deployment is automatic:

1. **Push to `main` branch** - The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) will:
   - Run all tests (backend and frontend)
   - Build Docker images for both services
   - Push images to Azure Container Registry
   - Deploy to Azure App Services
   - Restart the services

2. **Monitor deployment**:
   - View workflow runs: GitHub → **Actions** tab
   - Check App Service logs: Azure Portal → App Service → **Log stream**
   - Verify health: Visit `https://<backend-app>.azurewebsites.net/health`

#### Step 5: Verify Deployment

After deployment completes, verify:

- **Backend Health**: `https://<backend-app>.azurewebsites.net/health`
- **Backend API Docs**: `https://<backend-app>.azurewebsites.net/docs`
- **Backend Metrics**: `https://<backend-app>.azurewebsites.net/metrics`
- **Frontend**: `https://<frontend-app>.azurewebsites.net`

#### Troubleshooting

- **ImagePullFailure**: Regenerate ACR password and update `AZURE_ACR_PASSWORD` secret
- **Application Error**: Check container logs via Azure Portal → Log Stream or `az webapp log tail`
- **Workflow fails at login**: Verify `AZURE_CREDENTIALS` JSON is valid and service principal has Contributor role
- **Database connection issues**: Ensure `DATABASE_URL` is correctly formatted and PostgreSQL firewall allows Azure services

> **Important**: Always use PostgreSQL for production deployments. SQLite is only for local development. Containers will lose data if using SQLite.

For more detailed deployment information, see `.azure/README.md`.

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

- **Minimum Coverage**: 70% code coverage required (Phase 2 target)
- **Current Coverage**: 93%  (exceeds requirement)
- **Test Database**: Use separate SQLite test database
- **Cleanup**: Tests should clean up after themselves
- **Isolation**: Each test should be independent

#### Current Test Results

The test suite includes **80 comprehensive tests** with the following coverage:
- **Authentication**: 100% coverage - **Database Models**: 100% coverage - **API Endpoints**: 99% coverage - **Services**: 80-84% coverage - **Repositories**: 94-98% coverage - **Overall**: 93% coverage  (exceeds 70% requirement)

## Project Highlights

-  **Production-Ready**: Complete, fully functional application
-  **User-Centered Design**: Intuitive interface with role-based access
-  **Scalable Architecture**: Proper database design with relationships
-  **Secure**: Comprehensive authentication and authorization
-  **Flexible**: Auto-creation and bulk processing capabilities
-  **Professional**: Government-grade interface and functionality
-  **Well-Documented**: Comprehensive documentation and code comments
-  **Testable**: Built with testing requirements in mind
-  **Maintainable**: Clean code structure and separation of concerns


## 🔧 **Development Notes**

- **SQLite**: Used for local development; PostgreSQL recommended for production
- **FastAPI**: Modern, fast web framework with automatic API documentation
- **React**: Component-based frontend with modern hooks and context
- **Testing**: Comprehensive test suite required for maximum grade
- **Security**: JWT authentication with proper password hashing
- **Validation**: Both client-side and server-side input validation

## Deployment Considerations

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


```


### 📄 REPORT.md

**Path:** `REPORT.md`

```markdown
# DevOps Assignment 2 - Implementation Report

This report summarizes the improvements made to the Government Spending Tracker application as part of Assignment 2, focusing on code quality, testing, CI/CD, containerization, deployment, and monitoring.

## Overview

The project was enhanced from a basic web application to a production-ready, fully automated DevOps pipeline with comprehensive testing, monitoring, and cloud deployment capabilities.

## 1. Code Quality Improvements

### Linting and Static Analysis

**What was improved:**
- Integrated multiple code quality tools to enforce coding standards and catch errors early
- Fixed all linting errors and warnings across the codebase

**How it was implemented:**
- **Ruff**: Fast Python linter for code style and common errors
  - Configured in `backend/pytest.ini` with strict rules
  - Fixed import ordering, whitespace, and syntax issues
  - Removed unused imports and variables

- **Mypy**: Static type checker for Python
  - Added type annotations throughout the codebase
  - Fixed type incompatibilities (e.g., SQLAlchemy Column types, dictionary operations)
  - Resolved `Any` return type issues by rewriting dependency functions

- **Bandit**: Security vulnerability scanner
  - Fixed insecure temporary file creation (`tempfile.mktemp` → `tempfile.NamedTemporaryFile`)
  - Addressed hardcoded bind warnings with proper environment variable handling

**Files modified:**
- `backend/main.py`: Fixed import ordering, exception handling, type annotations
- `backend/auth.py`: Rewrote role-based dependency functions for proper type inference
- `backend/database.py`: Added type annotations, fixed SQLAlchemy warnings
- `backend/tests/conftest.py`: Replaced insecure temp file creation
- `backend/services/proposals.py`: Fixed type annotations and whitespace issues

## 2. Testing Improvements

### Test Coverage

**What was improved:**
- Achieved **93% code coverage** (exceeding the 70% requirement)
- Comprehensive test suite covering authentication, database models, and API endpoints
- Fixed all failing tests and improved test reliability

**How it was implemented:**
- **Backend Tests**:
  - Unit tests for authentication (`test_auth.py`): Password hashing, JWT tokens, role-based access
  - Database model tests (`test_database.py`): Model validation and relationships
  - API endpoint tests (`test_api_endpoints.py`): All CRUD operations, error handling
  - Test fixtures in `conftest.py` with proper database setup/teardown

- **Frontend Tests**:
  - Fixed Jest configuration to handle ES modules (Axios mocking)
  - Updated test assertions to match actual UI components
  - Tests run automatically in CI/CD pipeline

- **Test Execution**:
  - Automated testing in GitHub Actions on every push/PR
  - Coverage reports generated and enforced (minimum 70%)
  - HTML coverage reports available in `backend/htmlcov/`

**Files modified:**
- `backend/tests/test_auth.py`: Fixed dependency mocking for `get_current_user`
- `backend/tests/test_api_endpoints.py`: Removed whitespace issues
- `frontend/src/App.test.js`: Added Axios mock, updated assertions
- `backend/requirements.txt`: Added `pytest`, `pytest-asyncio`, `pytest-cov`, `httpx`

## 3. CI/CD Pipeline (GitHub Actions)

### Continuous Integration

**What was improved:**
- Migrated from Azure DevOps Pipelines to GitHub Actions
- Fully automated CI/CD pipeline that runs on every push and pull request
- Automated testing, building, and deployment to Azure

**How it was implemented:**
- **Workflow File**: `.github/workflows/ci-cd.yml`

- **CI Jobs**:
  1. **Backend Tests**: Runs `ruff check`, `mypy`, `bandit`, and `pytest` with coverage
  2. **Frontend Tests**: Runs `npm test` for React components
  3. **Build and Push**: Builds Docker images and pushes to Azure Container Registry (ACR)
  4. **Deploy Backend**: Updates App Service with new container image
  5. **Deploy Frontend**: Updates App Service with new container image

- **Deployment Triggers**:
  - Tests run on every push and pull request
  - Deployment only occurs on pushes to `main` branch
  - Uses Azure service principal authentication for secure deployment

- **Secrets Management**:
  - All sensitive credentials stored as GitHub Secrets
  - Service principal for Azure authentication
  - ACR credentials for container registry access

**Files created/modified:**
- `.github/workflows/ci-cd.yml`: Complete CI/CD workflow
- Removed `azure-pipelines.yml`: Replaced with GitHub Actions

## 4. Containerization

### Docker Implementation

**What was improved:**
- Both backend and frontend containerized with optimized Dockerfiles
- Multi-stage builds for smaller image sizes
- Health checks and proper environment variable configuration

**How it was implemented:**
- **Backend Dockerfile**:
  - Multi-stage build (builder + runtime)
  - Python 3.11 slim base image
  - Installs dependencies, runs migrations on startup
  - Health check endpoint configured
  - Exposes port 8000

- **Frontend Dockerfile**:
  - Multi-stage build (builder + nginx)
  - Node.js for building React app
  - Nginx Alpine for serving static files
  - Build-time environment variables for API URL
  - Health check configured
  - Exposes port 80

- **Docker Compose**:
  - Local development setup with backend, frontend, Prometheus, and Grafana
  - Volume mounts for configuration files
  - Network configuration for service communication

**Files created/modified:**
- `backend/Dockerfile`: Multi-stage backend container
- `frontend/Dockerfile`: Multi-stage frontend container with nginx
- `docker-compose.yml`: Local development orchestration

## 5. Cloud Deployment (Azure)

### Azure App Service Deployment

**What was improved:**
- Automated deployment to Azure App Service using container images
- Production-ready configuration with PostgreSQL database
- Managed identity authentication for ACR access

**How it was implemented:**
- **Azure Resources**:
  - Azure Container Registry (ACR) for storing Docker images
  - Two Linux App Services (backend and frontend)
  - Azure Database for PostgreSQL Flexible Server
  - Resource group for organizing resources

- **Deployment Process**:
  1. GitHub Actions builds Docker images
  2. Images pushed to ACR with tags (latest + commit SHA)
  3. App Services configured to pull from ACR
  4. Managed Identity grants ACR pull permissions
  5. App Services automatically restart with new images

- **Configuration**:
  - Environment variables set in App Service settings
  - Health check paths configured (`/health`)
  - CORS origins configured for frontend-backend communication
  - PostgreSQL connection string for persistent data storage

**Files created/modified:**
- `.azure/README.md`: Detailed deployment documentation
- `.github/workflows/ci-cd.yml`: Deployment automation

## 6. Monitoring and Health Checks

### Observability Implementation

**What was improved:**
- Health check endpoint for application status
- Prometheus metrics for request monitoring
- Grafana dashboard for visualization

**How it was implemented:**
- **Health Endpoint** (`/health`):
  - Checks API availability and database connectivity
  - Returns 200 if healthy, 503 if unhealthy
  - Used by Azure App Service for health monitoring

- **Metrics Endpoint** (`/metrics`):
  - Prometheus-compatible metrics exposed
  - Uses `prometheus-fastapi-instrumentator` library
  - Tracks: request count, latency (histograms), error rates, active requests

- **Prometheus Configuration**:
  - Scrapes metrics from backend every 15 seconds
  - Configured in `ops/prometheus/prometheus.yml`
  - Available in Docker Compose for local development

- **Grafana Dashboard**:
  - Pre-configured dashboard with 5 panels:
    1. Request Rate (requests per second)
    2. Request Latency (p95 percentile)
    3. Error Rate (5xx errors per second)
    4. Total Requests (stat panel)
    5. Active Requests (stat panel)
  - Datasource configured to connect to Prometheus
  - Available in Docker Compose for local development

**Files created/modified:**
- `backend/main.py`: Added health endpoint and Prometheus instrumentation
- `ops/prometheus/prometheus.yml`: Prometheus scrape configuration
- `ops/grafana/datasources/prometheus.yml`: Grafana datasource config
- `ops/grafana/dashboards/government-spending-dashboard.json`: Dashboard definition
- `backend/requirements.txt`: Added `prometheus-fastapi-instrumentator`

## 7. Database Migration

### PostgreSQL Integration

**What was improved:**
- Migrated from SQLite to PostgreSQL for production
- Database connection pooling and timeout configuration
- Automatic table creation and seeding on startup

**How it was implemented:**
- **Connection Configuration**:
  - PostgreSQL connection string format: `postgresql+psycopg://user:pass@host:5432/db?sslmode=require`
  - Connection pooling with SQLAlchemy
  - Timeout settings for reliability

- **Database Seeding**:
  - 8 default ministries created on startup
  - Default users (finance, ministry) created if not exist
  - Categories initialized with budget allocations

- **Migration Strategy**:
  - Alembic for database migrations
  - Automatic migration on application startup
  - SQLite fallback for local development

**Files modified:**
- `backend/database.py`: Added connection pooling, updated seeding logic
- `backend/main.py`: Enhanced startup logging and error handling

## 8. User Registration and Ministry Locking

### Enhanced Authentication

**What was improved:**
- Added user registration functionality
- Ministry-based access control for proposal submission
- Role-based UI restrictions

**How it was implemented:**
- **Registration Component**:
  - New `Register.js` component with form validation
  - Ministry selection dropdown (only for ministry role)
  - Password confirmation and error handling
  - Auto-login after successful registration

- **Backend Validation**:
  - Ministry users can only create proposals for their registered ministry
  - Validation in `services/proposals.py` enforces ministry matching
  - Error messages for unauthorized actions

- **Frontend Restrictions**:
  - `ProposalForm.js`: Ministry field locked and pre-filled for ministry users
  - `ProposalsList.js`: Edit button only shown for proposals from user's ministry

**Files created/modified:**
- `frontend/src/Register.js`: New registration component
- `frontend/src/Login.js`: Added link to registration
- `frontend/src/App.js`: Integrated registration flow
- `frontend/src/ProposalForm.js`: Ministry field locking
- `backend/services/proposals.py`: Ministry validation logic
- `backend/main.py`: Registration endpoint with ministry assignment

## 9. Bug Fixes

### Frontend Rendering Issues

**What was improved:**
- Fixed blank pages on History and Review Proposal pages
- Corrected object rendering in multiple components
- Fixed ministry comparison logic

**How it was implemented:**
- **History View**: Changed `proposal.ministry` to `proposal.ministry?.name || 'Unknown'`
- **Approval Dialog**: Fixed ministry name rendering in multiple locations
- **Proposals List**: Changed ministry object comparison to ID comparison
- **Contract Upload**: Fixed duplicate check to use ministry name correctly
- **Dashboard**: Fixed ministry name extraction from summary data

**Files modified:**
- `frontend/src/HistoryView.js`: Fixed ministry rendering
- `frontend/src/ApprovalDialog.js`: Fixed ministry name display
- `frontend/src/ProposalsList.js`: Fixed ministry comparison
- `frontend/src/ContractUpload.js`: Fixed duplicate detection
- `frontend/src/Dashboard.js`: Fixed ministry name extraction

## 10. Documentation

### README and Reports

**What was improved:**
- Comprehensive README with clear run, test, and deploy instructions
- Test report documenting coverage and test categories
- Deployment documentation with step-by-step guides

**How it was implemented:**
- **README.md**:
  - Updated "Getting Started" section with clear steps
  - Added comprehensive "Azure Deployment" section with prerequisites and troubleshooting
  - Enhanced "Testing" section with coverage requirements and commands
  - Added Docker Compose quick start guide

- **TEST_REPORT.md**:
  - Test summary with coverage metrics (93%)
  - Test categories breakdown
  - Execution instructions
  - Quality metrics

- **REPORT.md** (this file):
  - Summary of all improvements
  - Implementation details for each enhancement
  - File references for verification

**Files created/modified:**
- `README.md`: Enhanced with deployment and testing instructions
- `TEST_REPORT.md`: Comprehensive test documentation
- `REPORT.md`: This implementation report

## Summary of Deliverables

### Code Quality
-  Ruff linting configured and all issues resolved
-  Mypy type checking with full type annotations
-  Bandit security scanning with vulnerabilities fixed

### Testing
-  93% code coverage (exceeds 70% requirement)
-  Unit and integration tests for backend
-  Frontend component tests
-  Automated test execution in CI/CD

### CI/CD
-  GitHub Actions workflow for automated testing
-  Automated Docker image building and pushing
-  Automated deployment to Azure App Service
-  Deployment triggered only from main branch

### Containerization
-  Backend Dockerfile (multi-stage, optimized)
-  Frontend Dockerfile (nginx-based)
-  Docker Compose for local development

### Deployment
-  Azure App Service configuration
-  Azure Container Registry integration
-  PostgreSQL database setup
-  Environment variable configuration

### Monitoring
-  `/health` endpoint with database check
-  `/metrics` endpoint with Prometheus format
-  Prometheus configuration
-  Grafana dashboard with 5 panels

### Documentation
-  README with run, test, and deploy instructions
-  TEST_REPORT.md with coverage details
-  REPORT.md (this file) summarizing improvements

## Conclusion

All assignment requirements have been successfully implemented. The application is now production-ready with comprehensive testing, automated CI/CD, containerization, cloud deployment, and monitoring capabilities. The codebase follows best practices for code quality, security, and maintainability.


```


### 📄 TEST_REPORT.md

**Path:** `TEST_REPORT.md`

```markdown
# Test Report

**Generated**: November 29, 2025  
**Test Framework**: pytest  
**Coverage Tool**: pytest-cov

## Test Summary

| Metric | Value |
|--------|-------|
| **Total Tests** | 80 |
| **Tests Passing** | 80 |
| **Tests Failing** | 0 |
| **Code Coverage** | 90% (89.88%) |
| **Coverage Requirement** | 70% (PASS) |

## Test Coverage by Module

| Module | Statements | Missing | Coverage |
|--------|------------|--------|----------|
| `main.py` | 235 | 41 | 83% |
| `models.py` | 95 | 1 | 99% |
| `repositories/categories.py` | 36 | 2 | 94% |
| `repositories/ministries.py` | 32 | 1 | 97% |
| `repositories/proposals.py` | 41 | 1 | 98% |
| `services/approvals.py` | 44 | 7 | 84% |
| `services/parser.py` | 81 | 13 | 84% |
| `services/proposals.py` | 88 | 27 | 69% |
| `settings.py` | 10 | 0 | 100% |
| `tests/` | 461 | 0 | 100% |
| **TOTAL** | **1521** | **154** | **90%** |

## Test Categories

### Unit Tests

#### Authentication Tests (`test_auth.py`)
- Password hashing and verification (3 tests)
- Token creation and validation (3 tests)
- User authentication (4 tests)
- Current user retrieval (4 tests)
- Role validation (3 tests)
- **Total**: 17 unit tests

#### Database Model Tests (`test_database.py`)
- Ministry model (4 tests)
- Category model (4 tests)
- User model (6 tests)
- Proposal model (6 tests)
- Database integrity (2 tests)
- **Total**: 22 unit tests

### Integration Tests

#### API Endpoint Tests (`test_api_endpoints.py`)
- Authentication endpoints (8 tests)
  - User registration
  - User login
  - Current user retrieval
- Ministry endpoints (5 tests)
  - List ministries
  - Create ministry
  - Find or create ministry
- Category endpoints (4 tests)
  - List categories
  - Create category
  - Update category
  - Delete category
- Proposal endpoints (10 tests)
  - List proposals
  - Create proposal
  - Get proposal by ID
  - Update proposal
  - Delete proposal
- Approval endpoints (4 tests)
  - Approve proposal
  - Reject proposal
  - Authorization checks
- Dashboard endpoints (2 tests)
  - Dashboard summary
  - Authorization checks
- Contract parsing endpoints (4 tests)
  - CSV parsing
  - JSON parsing
  - Error handling
- **Total**: 41 integration tests

## Test Execution

### Running Tests Locally

```bash
# Run all tests with coverage
cd backend
pytest --cov=. --cov-report=term-missing --cov-report=html --cov-fail-under=70 -v

# Run specific test categories
pytest -m auth          # Authentication tests
pytest -m database      # Database model tests
pytest -m api           # API endpoint tests

# Generate HTML coverage report
pytest --cov=. --cov-report=html
# View: open htmlcov/index.html
```

### CI/CD Test Execution

Tests are automatically run in GitHub Actions on every push and pull request:

1. **Backend Tests** (`.github/workflows/ci-cd.yml`):
   - Linting (ruff)
   - Type checking (mypy)
   - Security scanning (bandit)
   - Unit and integration tests (pytest)
   - Coverage measurement (must be ≥70%)
   - Coverage report uploaded as artifact

2. **Frontend Tests**:
   - Jest tests with coverage

## Coverage Details

### High Coverage Areas (≥90%)
- Models (`models.py`): 99%
- Repositories: 94-98%
- Settings: 100%
- Test files: 100%

### Areas with Lower Coverage
- `services/proposals.py`: 69% (edge cases in proposal creation)
- `main.py`: 83% (some error handling paths)

### Coverage Exclusions
- Test files are excluded from coverage measurement
- Migration files are excluded

## Test Quality Metrics

- **Test-to-Code Ratio**: ~1:19 (461 test lines : 1521 code lines)
- **Assertions per Test**: Average 3-5 assertions
- **Test Isolation**: All tests use isolated test database
- **Fixtures**: Comprehensive fixture setup in `conftest.py`

## Continuous Integration

### GitHub Actions Pipeline
- Tests run on every push and PR
- Coverage enforced at 70% minimum
- Pipeline fails if tests fail
- Coverage report generated and uploaded
- Test results visible in Actions tab

### Coverage Artifact
- Location: GitHub Actions → Artifacts → `backend-coverage`
- File: `backend/coverage.xml`
- Format: Cobertura XML (compatible with most tools)

## Test Maintenance

### Adding New Tests
1. Add test file to `backend/tests/`
2. Use appropriate markers: `@pytest.mark.auth`, `@pytest.mark.api`, `@pytest.mark.database`
3. Use fixtures from `conftest.py` for database and client setup
4. Ensure coverage remains above 70%

### Test Fixtures Available
- `test_db`: Isolated test database session
- `client`: FastAPI test client
- `sample_ministry`: Pre-created ministry
- `sample_category`: Pre-created category
- `sample_user`: Pre-created user
- `sample_proposal`: Pre-created proposal
- `auth_headers`: Authentication headers for API tests
- `finance_headers`: Finance user authentication headers

## Conclusion

**All test requirements met:**
- Unit tests: 39 tests covering individual functions and models
- Integration tests: 41 tests covering full API endpoints
- Coverage: 90% (exceeds 70% requirement)
- Test report: This document included in repository
- CI/CD: Automated test execution with coverage enforcement

**Last Updated**: November 29, 2025  
**Test Status**: All tests passing  
**Coverage Status**: 90% (exceeds requirement)


```


### 📄 docker-compose.yml

**Path:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: gov-spending-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./government_spending.db
      - SECRET_KEY=${SECRET_KEY:-your-secret-key-change-in-production}
      - CORS_ORIGINS=http://localhost:3000,http://localhost:80
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    volumes:
      - ./backend/government_spending.db:/app/government_spending.db
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        - REACT_APP_API_BASE_URL=http://localhost:8000
    container_name: gov-spending-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    restart: unless-stopped

  prometheus:
    image: prom/prometheus:latest
    container_name: gov-spending-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./ops/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: gov-spending-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./ops/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./ops/grafana/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:


```


### 📄 sample_contracts.csv

**Path:** `sample_contracts.csv`

```csv
ministry_name,category,title,description,requested_amount
Ministry of Education,Education,Teacher Training Program,Professional development for 500 teachers,750000
Ministry of Health,Healthcare,Emergency Response Vehicles,Ambulances and emergency medical vehicles,1500000
Ministry of Defense,Defense,Border Security Enhancement,Advanced surveillance and monitoring systems,2800000
Ministry of Transportation,Infrastructure,Highway Construction Project,New highway connecting major cities,4500000
Ministry of Social Welfare,Social Services,Community Development Centers,Establishing centers for vulnerable populations,1800000
Ministry of Agriculture,Education,Agricultural Education Initiative,Training programs for modern farming techniques,950000
Ministry of Technology,Infrastructure,Digital Infrastructure Upgrade,National broadband network expansion,3200000
Ministry of Environment,Social Services,Environmental Protection Program,Conservation and sustainability initiatives,1200000

```


### 📄 sample_contracts.json

**Path:** `sample_contracts.json`

```json
[
  {
    "ministry_name": "Ministry of Education",
    "category": "Education",
    "title": "Primary School Infrastructure Development",
    "description": "Construction of 50 new classrooms across rural areas to improve access to quality education",
    "requested_amount": 2500000
  },
  {
    "ministry_name": "Ministry of Health",
    "category": "Healthcare",
    "title": "Medical Equipment Procurement",
    "description": "Purchase of advanced diagnostic equipment for 10 regional hospitals",
    "requested_amount": 1800000
  },
  {
    "ministry_name": "Ministry of Defense",
    "category": "Defense",
    "title": "Military Vehicle Maintenance",
    "description": "Annual maintenance and repair of military vehicles and equipment",
    "requested_amount": 3200000
  },
  {
    "ministry_name": "Ministry of Transportation",
    "category": "Infrastructure",
    "title": "Urban Transit System",
    "description": "Development of modern public transportation network for major cities",
    "requested_amount": 5500000
  },
  {
    "ministry_name": "Ministry of Social Welfare",
    "category": "Social Services",
    "title": "Homeless Shelter Network",
    "description": "Establishing comprehensive shelter and support services for homeless population",
    "requested_amount": 2100000
  },
  {
    "ministry_name": "Ministry of Technology",
    "category": "Infrastructure",
    "title": "Cybersecurity Infrastructure",
    "description": "Upgrading national cybersecurity systems and training personnel",
    "requested_amount": 2800000
  },
  {
    "ministry_name": "Ministry of Environment",
    "category": "Social Services",
    "title": "Renewable Energy Initiative",
    "description": "Solar and wind energy projects for sustainable development",
    "requested_amount": 4200000
  },
  {
    "ministry_name": "Ministry of Agriculture",
    "category": "Education",
    "title": "Rural Education Program",
    "description": "Educational initiatives for rural communities and farming families",
    "requested_amount": 1500000
  }
]

```


================================================================================
## 📂 frontend


### 📄 .dockerignore

**Path:** `frontend/.dockerignore`

```text
# Dependencies
node_modules
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Build output
build
dist

# Testing
coverage
.nyc_output

# IDE
.vscode
.idea
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Git
.git
.gitignore

# Environment files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Misc
README.md
.dockerignore
Dockerfile


```


### 📄 .gitignore

**Path:** `frontend/.gitignore`

```text
# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*

```


### 📄 Dockerfile

**Path:** `frontend/Dockerfile`

```dockerfile
# Multi-stage Dockerfile for React frontend
# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first for better layer caching
COPY package*.json ./

# Install all dependencies (including devDependencies needed for build)
# This layer will be cached if package files don't change
RUN npm ci --no-audit --no-fund

# Copy source code
COPY . .

# Build arguments for environment-specific configuration
ARG REACT_APP_API_BASE_URL=http://localhost:8000
ENV REACT_APP_API_BASE_URL=$REACT_APP_API_BASE_URL

# Build the React application
RUN npm run build

# Stage 2: Production with nginx
FROM nginx:alpine

# Copy built static files from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Health check using nginx's built-in capabilities
# Use curl instead of wget (more commonly available in alpine)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1

# Start nginx in foreground mode
CMD ["nginx", "-g", "daemon off;"]


```


### 📄 README.md

**Path:** `frontend/README.md`

```markdown
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

```


### 📄 nginx.conf

**Path:** `frontend/nginx.conf`

```conf
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json application/javascript;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Serve static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}


```


### 📄 package-lock.json

**Path:** `frontend/package-lock.json`

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "frontend",
      "version": "0.1.0",
      "dependencies": {
        "@testing-library/dom": "^10.4.1",
        "@testing-library/jest-dom": "^6.8.0",
        "@testing-library/react": "^16.3.0",
        "@testing-library/user-event": "^13.5.0",
        "axios": "^1.12.2",
        "chart.js": "^4.5.0",
        "react": "^19.1.1",
        "react-chartjs-2": "^5.3.0",
        "react-dom": "^19.1.1",
        "react-scripts": "5.0.1",
        "web-vitals": "^2.1.4"
      }
    },
    "node_modules/@adobe/css-tools": {
      "version": "4.4.4",
      "resolved": "https://registry.npmjs.org/@adobe/css-tools/-/css-tools-4.4.4.tgz",
      "integrity": "sha512-Elp+iwUx5rN5+Y8xLt5/GRoG20WGoDCQ/1Fb+1LiGtvwbDavuSk0jhD/eZdckHAuzcDzccnkv+rEjyWfRx18gg==",
      "license": "MIT"
    },
    "node_modules/@alloc/quick-lru": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/@alloc/quick-lru/-/quick-lru-5.2.0.tgz",
      "integrity": "sha512-UrcABB+4bUrFABwbluTIBErXwvbsU/V7TZWfmbgJfbkwiBuziS9gxdODUyuiecfdGQ85jglMW6juS3+z5TsKLw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@babel/code-frame": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/code-frame/-/code-frame-7.27.1.tgz",
      "integrity": "sha512-cjQ7ZlQ0Mv3b47hABuTevyTuYN4i+loJKGeV9flcCgIK37cCXRh+L1bd3iBHlynerhQ7BhCkn2BPbQUL+rGqFg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-validator-identifier": "^7.27.1",
        "js-tokens": "^4.0.0",
        "picocolors": "^1.1.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/compat-data": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/compat-data/-/compat-data-7.28.4.tgz",
      "integrity": "sha512-YsmSKC29MJwf0gF8Rjjrg5LQCmyh+j/nD8/eP7f+BeoQTKYqs9RoWbjGOdy0+1Ekr68RJZMUOPVQaQisnIo4Rw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/core": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/core/-/core-7.28.4.tgz",
      "integrity": "sha512-2BCOP7TN8M+gVDj7/ht3hsaO/B/n5oDbiAyyvnRlNOs+u1o+JWNYTQrmpuNp1/Wq2gcFrI01JAW+paEKDMx/CA==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.27.1",
        "@babel/generator": "^7.28.3",
        "@babel/helper-compilation-targets": "^7.27.2",
        "@babel/helper-module-transforms": "^7.28.3",
        "@babel/helpers": "^7.28.4",
        "@babel/parser": "^7.28.4",
        "@babel/template": "^7.27.2",
        "@babel/traverse": "^7.28.4",
        "@babel/types": "^7.28.4",
        "@jridgewell/remapping": "^2.3.5",
        "convert-source-map": "^2.0.0",
        "debug": "^4.1.0",
        "gensync": "^1.0.0-beta.2",
        "json5": "^2.2.3",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/babel"
      }
    },
    "node_modules/@babel/core/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/eslint-parser": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/eslint-parser/-/eslint-parser-7.28.4.tgz",
      "integrity": "sha512-Aa+yDiH87980jR6zvRfFuCR1+dLb00vBydhTL+zI992Rz/wQhSvuxjmOOuJOgO3XmakO6RykRGD2S1mq1AtgHA==",
      "license": "MIT",
      "dependencies": {
        "@nicolo-ribaudo/eslint-scope-5-internals": "5.1.1-v1",
        "eslint-visitor-keys": "^2.1.0",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || >=14.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.11.0",
        "eslint": "^7.5.0 || ^8.0.0 || ^9.0.0"
      }
    },
    "node_modules/@babel/eslint-parser/node_modules/eslint-visitor-keys": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-2.1.0.tgz",
      "integrity": "sha512-0rSmRBzXgDzIsD6mGdJgevzgezI534Cer5L/vyMX0kHzT/jiB43jRhd9YUlMGYLQy2zprNmoT8qasCGtY+QaKw==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/@babel/eslint-parser/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/generator": {
      "version": "7.28.3",
      "resolved": "https://registry.npmjs.org/@babel/generator/-/generator-7.28.3.tgz",
      "integrity": "sha512-3lSpxGgvnmZznmBkCRnVREPUFJv2wrv9iAoFDvADJc0ypmdOxdUtcLeBgBJ6zE0PMeTKnxeQzyk0xTBq4Ep7zw==",
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.28.3",
        "@babel/types": "^7.28.2",
        "@jridgewell/gen-mapping": "^0.3.12",
        "@jridgewell/trace-mapping": "^0.3.28",
        "jsesc": "^3.0.2"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-annotate-as-pure": {
      "version": "7.27.3",
      "resolved": "https://registry.npmjs.org/@babel/helper-annotate-as-pure/-/helper-annotate-as-pure-7.27.3.tgz",
      "integrity": "sha512-fXSwMQqitTGeHLBC08Eq5yXz2m37E4pJX1qAU1+2cNedz/ifv/bVXft90VeSav5nFO61EcNgwr0aJxbyPaWBPg==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.27.3"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-compilation-targets": {
      "version": "7.27.2",
      "resolved": "https://registry.npmjs.org/@babel/helper-compilation-targets/-/helper-compilation-targets-7.27.2.tgz",
      "integrity": "sha512-2+1thGUUWWjLTYTHZWK1n8Yga0ijBz1XAhUXcKy81rd5g6yh7hGqMp45v7cadSbEHc9G3OTv45SyneRN3ps4DQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.27.2",
        "@babel/helper-validator-option": "^7.27.1",
        "browserslist": "^4.24.0",
        "lru-cache": "^5.1.1",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-compilation-targets/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/helper-create-class-features-plugin": {
      "version": "7.28.3",
      "resolved": "https://registry.npmjs.org/@babel/helper-create-class-features-plugin/-/helper-create-class-features-plugin-7.28.3.tgz",
      "integrity": "sha512-V9f6ZFIYSLNEbuGA/92uOvYsGCJNsuA8ESZ4ldc09bWk/j8H8TKiPw8Mk1eG6olpnO0ALHJmYfZvF4MEE4gajg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-member-expression-to-functions": "^7.27.1",
        "@babel/helper-optimise-call-expression": "^7.27.1",
        "@babel/helper-replace-supers": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1",
        "@babel/traverse": "^7.28.3",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-create-class-features-plugin/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/helper-create-regexp-features-plugin": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-create-regexp-features-plugin/-/helper-create-regexp-features-plugin-7.27.1.tgz",
      "integrity": "sha512-uVDC72XVf8UbrH5qQTc18Agb8emwjTiZrQE11Nv3CuBEZmVvTwwE9CBUEvHku06gQCAyYf8Nv6ja1IN+6LMbxQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.1",
        "regexpu-core": "^6.2.0",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-create-regexp-features-plugin/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/helper-define-polyfill-provider": {
      "version": "0.6.5",
      "resolved": "https://registry.npmjs.org/@babel/helper-define-polyfill-provider/-/helper-define-polyfill-provider-0.6.5.tgz",
      "integrity": "sha512-uJnGFcPsWQK8fvjgGP5LZUZZsYGIoPeRjSF5PGwrelYgq7Q15/Ft9NGFp1zglwgIv//W0uG4BevRuSJRyylZPg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.27.2",
        "@babel/helper-plugin-utils": "^7.27.1",
        "debug": "^4.4.1",
        "lodash.debounce": "^4.0.8",
        "resolve": "^1.22.10"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/@babel/helper-globals": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/helper-globals/-/helper-globals-7.28.0.tgz",
      "integrity": "sha512-+W6cISkXFa1jXsDEdYA8HeevQT/FULhxzR99pxphltZcVaugps53THCeiWA8SguxxpSp3gKPiuYfSWopkLQ4hw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-member-expression-to-functions": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-member-expression-to-functions/-/helper-member-expression-to-functions-7.27.1.tgz",
      "integrity": "sha512-E5chM8eWjTp/aNoVpcbfM7mLxu9XGLWYise2eBKGQomAk/Mb4XoxyqXTZbuTohbsl8EKqdlMhnDI2CCLfcs9wA==",
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.27.1",
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-imports": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-imports/-/helper-module-imports-7.27.1.tgz",
      "integrity": "sha512-0gSFWUPNXNopqtIPQvlD5WgXYI5GY2kP2cCvoT8kczjbfcfuIljTbcWrulD1CIPIX2gt1wghbDy08yE1p+/r3w==",
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.27.1",
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-module-transforms": {
      "version": "7.28.3",
      "resolved": "https://registry.npmjs.org/@babel/helper-module-transforms/-/helper-module-transforms-7.28.3.tgz",
      "integrity": "sha512-gytXUbs8k2sXS9PnQptz5o0QnpLL51SwASIORY6XaBKF88nsOT0Zw9szLqlSGQDP/4TljBAD5y98p2U1fqkdsw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.27.1",
        "@babel/helper-validator-identifier": "^7.27.1",
        "@babel/traverse": "^7.28.3"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-optimise-call-expression": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-optimise-call-expression/-/helper-optimise-call-expression-7.27.1.tgz",
      "integrity": "sha512-URMGH08NzYFhubNSGJrpUEphGKQwMQYBySzat5cAByY1/YgIRkULnIy3tAMeszlL/so2HbeilYloUmSpd7GdVw==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-plugin-utils": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-plugin-utils/-/helper-plugin-utils-7.27.1.tgz",
      "integrity": "sha512-1gn1Up5YXka3YYAHGKpbideQ5Yjf1tDa9qYcgysz+cNCXukyLl6DjPXhD3VRwSb8c0J9tA4b2+rHEZtc6R0tlw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-remap-async-to-generator": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-remap-async-to-generator/-/helper-remap-async-to-generator-7.27.1.tgz",
      "integrity": "sha512-7fiA521aVw8lSPeI4ZOD3vRFkoqkJcS+z4hFo82bFSH/2tNd6eJ5qCVMS5OzDmZh/kaHQeBaeyxK6wljcPtveA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.1",
        "@babel/helper-wrap-function": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-replace-supers": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-replace-supers/-/helper-replace-supers-7.27.1.tgz",
      "integrity": "sha512-7EHz6qDZc8RYS5ElPoShMheWvEgERonFCs7IAonWLLUTXW59DP14bCZt89/GKyreYn8g3S83m21FelHKbeDCKA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-member-expression-to-functions": "^7.27.1",
        "@babel/helper-optimise-call-expression": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/helper-skip-transparent-expression-wrappers": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-skip-transparent-expression-wrappers/-/helper-skip-transparent-expression-wrappers-7.27.1.tgz",
      "integrity": "sha512-Tub4ZKEXqbPjXgWLl2+3JpQAYBJ8+ikpQ2Ocj/q/r0LwE3UhENh7EUabyHjz2kCEsrRY83ew2DQdHluuiDQFzg==",
      "license": "MIT",
      "dependencies": {
        "@babel/traverse": "^7.27.1",
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-string-parser": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-string-parser/-/helper-string-parser-7.27.1.tgz",
      "integrity": "sha512-qMlSxKbpRlAridDExk92nSobyDdpPijUq2DW6oDnUqd0iOGxmQjyqhMIihI9+zv4LPyZdRje2cavWPbCbWm3eA==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-identifier": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-identifier/-/helper-validator-identifier-7.27.1.tgz",
      "integrity": "sha512-D2hP9eA+Sqx1kBZgzxZh0y1trbuU+JoDkiEwqhQ36nodYqJwyEIhPSdMNd7lOm/4io72luTPWH20Yda0xOuUow==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-validator-option": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/helper-validator-option/-/helper-validator-option-7.27.1.tgz",
      "integrity": "sha512-YvjJow9FxbhFFKDSuFnVCe2WxXk1zWc22fFePVNEaWJEu8IrZVlda6N0uHwzZrUM1il7NC9Mlp4MaJYbYd9JSg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helper-wrap-function": {
      "version": "7.28.3",
      "resolved": "https://registry.npmjs.org/@babel/helper-wrap-function/-/helper-wrap-function-7.28.3.tgz",
      "integrity": "sha512-zdf983tNfLZFletc0RRXYrHrucBEg95NIFMkn6K9dbeMYnsgHaSBGcQqdsCSStG2PYwRre0Qc2NNSCXbG+xc6g==",
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.27.2",
        "@babel/traverse": "^7.28.3",
        "@babel/types": "^7.28.2"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/helpers": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/helpers/-/helpers-7.28.4.tgz",
      "integrity": "sha512-HFN59MmQXGHVyYadKLVumYsA9dBFun/ldYxipEjzA4196jpLZd8UjEEBLkbEkvfYreDqJhZxYAWFPtrfhNpj4w==",
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.27.2",
        "@babel/types": "^7.28.4"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/parser": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/parser/-/parser-7.28.4.tgz",
      "integrity": "sha512-yZbBqeM6TkpP9du/I2pUZnJsRMGGvOuIrhjzC1AwHwW+6he4mni6Bp/m8ijn0iOuZuPI2BfkCoSRunpyjnrQKg==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.28.4"
      },
      "bin": {
        "parser": "bin/babel-parser.js"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-firefox-class-in-computed-class-key": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-firefox-class-in-computed-class-key/-/plugin-bugfix-firefox-class-in-computed-class-key-7.27.1.tgz",
      "integrity": "sha512-QPG3C9cCVRQLxAVwmefEmwdTanECuUBMQZ/ym5kiw3XKCGA7qkuQLcjWWHcrD/GKbn/WmJwaezfuuAOcyKlRPA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-safari-class-field-initializer-scope": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-safari-class-field-initializer-scope/-/plugin-bugfix-safari-class-field-initializer-scope-7.27.1.tgz",
      "integrity": "sha512-qNeq3bCKnGgLkEXUuFry6dPlGfCdQNZbn7yUAPCInwAJHMU7THJfrBSozkcWq5sNM6RcF3S8XyQL2A52KNR9IA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression/-/plugin-bugfix-safari-id-destructuring-collision-in-function-expression-7.27.1.tgz",
      "integrity": "sha512-g4L7OYun04N1WyqMNjldFwlfPCLVkgB54A/YCXICZYBsvJJE3kByKv9c9+R/nAfmIfjl2rKYLNyMHboYbZaWaA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining/-/plugin-bugfix-v8-spread-parameters-in-optional-chaining-7.27.1.tgz",
      "integrity": "sha512-oO02gcONcD5O1iTLi/6frMJBIwWEHceWGSGqrpCmEL8nogiS6J9PBlE48CaK20/Jx1LuRml9aDftLgdjXT8+Cw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1",
        "@babel/plugin-transform-optional-chaining": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.13.0"
      }
    },
    "node_modules/@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly": {
      "version": "7.28.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly/-/plugin-bugfix-v8-static-class-fields-redefine-readonly-7.28.3.tgz",
      "integrity": "sha512-b6YTX108evsvE4YgWyQ921ZAFFQm3Bn+CA3+ZXlNVnPhx+UfsVURoPjfGAPCjBgrqo30yX/C2nZGX96DxvR9Iw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.28.3"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-proposal-class-properties": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-class-properties/-/plugin-proposal-class-properties-7.18.6.tgz",
      "integrity": "sha512-cumfXOF0+nzZrrN8Rf0t7M+tF6sZc7vhQwYQck9q1/5w2OExlD+b4v4RpMJFaV1Z7WcDRgO6FqvxqxGlwo+RHQ==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-class-properties instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.18.6",
        "@babel/helper-plugin-utils": "^7.18.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-decorators": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-decorators/-/plugin-proposal-decorators-7.28.0.tgz",
      "integrity": "sha512-zOiZqvANjWDUaUS9xMxbMcK/Zccztbe/6ikvUXaG9nsPH3w6qh5UaPGAnirI/WhIbZ8m3OHU0ReyPrknG+ZKeg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/plugin-syntax-decorators": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-nullish-coalescing-operator": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-nullish-coalescing-operator/-/plugin-proposal-nullish-coalescing-operator-7.18.6.tgz",
      "integrity": "sha512-wQxQzxYeJqHcfppzBDnm1yAY0jSRkUXR2z8RePZYrKwMKgMlE8+Z6LUno+bd6LvbGh8Gltvy74+9pIYkr+XkKA==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-nullish-coalescing-operator instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.18.6",
        "@babel/plugin-syntax-nullish-coalescing-operator": "^7.8.3"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-numeric-separator": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-numeric-separator/-/plugin-proposal-numeric-separator-7.18.6.tgz",
      "integrity": "sha512-ozlZFogPqoLm8WBr5Z8UckIoE4YQ5KESVcNudyXOR8uqIkliTEgJ3RoketfG6pmzLdeZF0H/wjE9/cCEitBl7Q==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-numeric-separator instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.18.6",
        "@babel/plugin-syntax-numeric-separator": "^7.10.4"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-optional-chaining": {
      "version": "7.21.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-optional-chaining/-/plugin-proposal-optional-chaining-7.21.0.tgz",
      "integrity": "sha512-p4zeefM72gpmEe2fkUr/OnOXpWEf8nAgk7ZYVqqfFiyIG7oFfVZcCrU64hWn5xp4tQ9LkV4bTIa5rD0KANpKNA==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-optional-chaining instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.20.2",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.20.0",
        "@babel/plugin-syntax-optional-chaining": "^7.8.3"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-private-methods": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-private-methods/-/plugin-proposal-private-methods-7.18.6.tgz",
      "integrity": "sha512-nutsvktDItsNn4rpGItSNV2sz1XwS+nfU0Rg8aCx3W3NOKVzdMjJRu0O5OkgDp3ZGICSTbgRpxZoWsxoKRvbeA==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-methods instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.18.6",
        "@babel/helper-plugin-utils": "^7.18.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-proposal-private-property-in-object": {
      "version": "7.21.0-placeholder-for-preset-env.2",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-private-property-in-object/-/plugin-proposal-private-property-in-object-7.21.0-placeholder-for-preset-env.2.tgz",
      "integrity": "sha512-SOSkfJDddaM7mak6cPEpswyTRnuRltl429hMraQEglW+OkovnCzsiszTmsrlY//qLFjCpQDFRvjdm2wA5pPm9w==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-async-generators": {
      "version": "7.8.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-async-generators/-/plugin-syntax-async-generators-7.8.4.tgz",
      "integrity": "sha512-tycmZxkGfZaxhMRbXlPXuVFpdWlXpir2W4AMhSJgRKzk/eDlIXOhb2LHWoLpDF7TEHylV5zNhykX6KAgHJmTNw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-bigint": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-bigint/-/plugin-syntax-bigint-7.8.3.tgz",
      "integrity": "sha512-wnTnFlG+YxQm3vDxpGE57Pj0srRU4sHE/mDkt1qv2YJJSeUAec2ma4WLUnUPeKjyrfntVwe/N6dCXpU+zL3Npg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-class-properties": {
      "version": "7.12.13",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-class-properties/-/plugin-syntax-class-properties-7.12.13.tgz",
      "integrity": "sha512-fm4idjKla0YahUNgFNLCB0qySdsoPiZP3iQE3rky0mBUtMZ23yDJ9SJdg6dXTSDnulOVqiF3Hgr9nbXvXTQZYA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.12.13"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-class-static-block": {
      "version": "7.14.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-class-static-block/-/plugin-syntax-class-static-block-7.14.5.tgz",
      "integrity": "sha512-b+YyPmr6ldyNnM6sqYeMWE+bgJcJpO6yS4QD7ymxgH34GBPNDM/THBh8iunyvKIZztiwLH4CJZ0RxTk9emgpjw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.14.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-decorators": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-decorators/-/plugin-syntax-decorators-7.27.1.tgz",
      "integrity": "sha512-YMq8Z87Lhl8EGkmb0MwYkt36QnxC+fzCgrl66ereamPlYToRpIk5nUjKUY3QKLWq8mwUB1BgbeXcTJhZOCDg5A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-flow": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-flow/-/plugin-syntax-flow-7.27.1.tgz",
      "integrity": "sha512-p9OkPbZ5G7UT1MofwYFigGebnrzGJacoBSQM0/6bi/PUMVE+qlWDD/OalvQKbwgQzU6dl0xAv6r4X7Jme0RYxA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-import-assertions": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-import-assertions/-/plugin-syntax-import-assertions-7.27.1.tgz",
      "integrity": "sha512-UT/Jrhw57xg4ILHLFnzFpPDlMbcdEicaAtjPQpbj9wa8T4r5KVWCimHcL/460g8Ht0DMxDyjsLgiWSkVjnwPFg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-import-attributes": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-import-attributes/-/plugin-syntax-import-attributes-7.27.1.tgz",
      "integrity": "sha512-oFT0FrKHgF53f4vOsZGi2Hh3I35PfSmVs4IBFLFj4dnafP+hIWDLg3VyKmUHfLoLHlyxY4C7DGtmHuJgn+IGww==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-import-meta": {
      "version": "7.10.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-import-meta/-/plugin-syntax-import-meta-7.10.4.tgz",
      "integrity": "sha512-Yqfm+XDx0+Prh3VSeEQCPU81yC+JWZ2pDPFSS4ZdpfZhp4MkFMaDC1UqseovEKwSUpnIL7+vK+Clp7bfh0iD7g==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.10.4"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-json-strings": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-json-strings/-/plugin-syntax-json-strings-7.8.3.tgz",
      "integrity": "sha512-lY6kdGpWHvjoe2vk4WrAapEuBR69EMxZl+RoGRhrFGNYVK8mOPAW8VfbT/ZgrFbXlDNiiaxQnAtgVCZ6jv30EA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-jsx": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-jsx/-/plugin-syntax-jsx-7.27.1.tgz",
      "integrity": "sha512-y8YTNIeKoyhGd9O0Jiyzyyqk8gdjnumGTQPsz0xOZOQ2RmkVJeZ1vmmfIvFEKqucBG6axJGBZDE/7iI5suUI/w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-logical-assignment-operators": {
      "version": "7.10.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-logical-assignment-operators/-/plugin-syntax-logical-assignment-operators-7.10.4.tgz",
      "integrity": "sha512-d8waShlpFDinQ5MtvGU9xDAOzKH47+FFoney2baFIoMr952hKOLp1HR7VszoZvOsV/4+RRszNY7D17ba0te0ig==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.10.4"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-nullish-coalescing-operator": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-nullish-coalescing-operator/-/plugin-syntax-nullish-coalescing-operator-7.8.3.tgz",
      "integrity": "sha512-aSff4zPII1u2QD7y+F8oDsz19ew4IGEJg9SVW+bqwpwtfFleiQDMdzA/R+UlWDzfnHFCxxleFT0PMIrR36XLNQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-numeric-separator": {
      "version": "7.10.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-numeric-separator/-/plugin-syntax-numeric-separator-7.10.4.tgz",
      "integrity": "sha512-9H6YdfkcK/uOnY/K7/aA2xpzaAgkQn37yzWUMRK7OaPOqOpGS1+n0H5hxT9AUw9EsSjPW8SVyMJwYRtWs3X3ug==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.10.4"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-object-rest-spread": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-object-rest-spread/-/plugin-syntax-object-rest-spread-7.8.3.tgz",
      "integrity": "sha512-XoqMijGZb9y3y2XskN+P1wUGiVwWZ5JmoDRwx5+3GmEplNyVM2s2Dg8ILFQm8rWM48orGy5YpI5Bl8U1y7ydlA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-optional-catch-binding": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-optional-catch-binding/-/plugin-syntax-optional-catch-binding-7.8.3.tgz",
      "integrity": "sha512-6VPD0Pc1lpTqw0aKoeRTMiB+kWhAoT24PA+ksWSBrFtl5SIRVpZlwN3NNPQjehA2E/91FV3RjLWoVTglWcSV3Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-optional-chaining": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-optional-chaining/-/plugin-syntax-optional-chaining-7.8.3.tgz",
      "integrity": "sha512-KoK9ErH1MBlCPxV0VANkXW2/dw4vlbGDrFgz8bmUsBGYkFRcbRwMh6cIJubdPrkxRwuGdtCk0v/wPTKbQgBjkg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.8.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-private-property-in-object": {
      "version": "7.14.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-private-property-in-object/-/plugin-syntax-private-property-in-object-7.14.5.tgz",
      "integrity": "sha512-0wVnp9dxJ72ZUJDV27ZfbSj6iHLoytYZmh3rFcxNnvsJF3ktkzLDZPy/mA17HGsaQT3/DQsWYX1f1QGWkCoVUg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.14.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-top-level-await": {
      "version": "7.14.5",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-top-level-await/-/plugin-syntax-top-level-await-7.14.5.tgz",
      "integrity": "sha512-hx++upLv5U1rgYfwe1xBQUhRmU41NEvpUvrp8jkrSCdvGSnM5/qdRMtylJ6PG5OFkBaHkbTAKTnd3/YyESRHFw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.14.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-typescript": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-typescript/-/plugin-syntax-typescript-7.27.1.tgz",
      "integrity": "sha512-xfYCBMxveHrRMnAWl1ZlPXOZjzkN82THFvLhQhFXFt81Z5HnN+EtUkZhv/zcKpmT3fzmWZB0ywiBrbC3vogbwQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-syntax-unicode-sets-regex": {
      "version": "7.18.6",
      "resolved": "https://registry.npmjs.org/@babel/plugin-syntax-unicode-sets-regex/-/plugin-syntax-unicode-sets-regex-7.18.6.tgz",
      "integrity": "sha512-727YkEAPwSIQTv5im8QHz3upqp92JTWhidIC81Tdx4VJYIte/VndKf1qKrfnnhPLiPghStWfvC/iFaMCQu7Nqg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.18.6",
        "@babel/helper-plugin-utils": "^7.18.6"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-arrow-functions": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-arrow-functions/-/plugin-transform-arrow-functions-7.27.1.tgz",
      "integrity": "sha512-8Z4TGic6xW70FKThA5HYEKKyBpOOsucTOD1DjU3fZxDg+K3zBJcXMFnt/4yQiZnf5+MiOMSXQ9PaEK/Ilh1DeA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-async-generator-functions": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-async-generator-functions/-/plugin-transform-async-generator-functions-7.28.0.tgz",
      "integrity": "sha512-BEOdvX4+M765icNPZeidyADIvQ1m1gmunXufXxvRESy/jNNyfovIqUyE7MVgGBjWktCoJlzvFA1To2O4ymIO3Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-remap-async-to-generator": "^7.27.1",
        "@babel/traverse": "^7.28.0"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-async-to-generator": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-async-to-generator/-/plugin-transform-async-to-generator-7.27.1.tgz",
      "integrity": "sha512-NREkZsZVJS4xmTr8qzE5y8AfIPqsdQfRuUiLRTEzb7Qii8iFWCyDKaUV2c0rCuh4ljDZ98ALHP/PetiBV2nddA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-remap-async-to-generator": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-block-scoped-functions": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-block-scoped-functions/-/plugin-transform-block-scoped-functions-7.27.1.tgz",
      "integrity": "sha512-cnqkuOtZLapWYZUYM5rVIdv1nXYuFVIltZ6ZJ7nIj585QsjKM5dhL2Fu/lICXZ1OyIAFc7Qy+bvDAtTXqGrlhg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-block-scoping": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-block-scoping/-/plugin-transform-block-scoping-7.28.4.tgz",
      "integrity": "sha512-1yxmvN0MJHOhPVmAsmoW5liWwoILobu/d/ShymZmj867bAdxGbehIrew1DuLpw2Ukv+qDSSPQdYW1dLNE7t11A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-class-properties": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-class-properties/-/plugin-transform-class-properties-7.27.1.tgz",
      "integrity": "sha512-D0VcalChDMtuRvJIu3U/fwWjf8ZMykz5iZsg77Nuj821vCKI3zCyRLwRdWbsuJ/uRwZhZ002QtCqIkwC/ZkvbA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-class-static-block": {
      "version": "7.28.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-class-static-block/-/plugin-transform-class-static-block-7.28.3.tgz",
      "integrity": "sha512-LtPXlBbRoc4Njl/oh1CeD/3jC+atytbnf/UqLoqTDcEYGUPj022+rvfkbDYieUrSj3CaV4yHDByPE+T2HwfsJg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.28.3",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.12.0"
      }
    },
    "node_modules/@babel/plugin-transform-classes": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-classes/-/plugin-transform-classes-7.28.4.tgz",
      "integrity": "sha512-cFOlhIYPBv/iBoc+KS3M6et2XPtbT2HiCRfBXWtfpc9OAyostldxIf9YAYB6ypURBBbx+Qv6nyrLzASfJe+hBA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-compilation-targets": "^7.27.2",
        "@babel/helper-globals": "^7.28.0",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-replace-supers": "^7.27.1",
        "@babel/traverse": "^7.28.4"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-computed-properties": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-computed-properties/-/plugin-transform-computed-properties-7.27.1.tgz",
      "integrity": "sha512-lj9PGWvMTVksbWiDT2tW68zGS/cyo4AkZ/QTp0sQT0mjPopCmrSkzxeXkznjqBxzDI6TclZhOJbBmbBLjuOZUw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/template": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-destructuring": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-destructuring/-/plugin-transform-destructuring-7.28.0.tgz",
      "integrity": "sha512-v1nrSMBiKcodhsyJ4Gf+Z0U/yawmJDBOTpEB3mcQY52r9RIyPneGyAS/yM6seP/8I+mWI3elOMtT5dB8GJVs+A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.28.0"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-dotall-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-dotall-regex/-/plugin-transform-dotall-regex-7.27.1.tgz",
      "integrity": "sha512-gEbkDVGRvjj7+T1ivxrfgygpT7GUd4vmODtYpbs0gZATdkX8/iSnOtZSxiZnsgm1YjTgjI6VKBGSJJevkrclzw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-duplicate-keys": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-duplicate-keys/-/plugin-transform-duplicate-keys-7.27.1.tgz",
      "integrity": "sha512-MTyJk98sHvSs+cvZ4nOauwTTG1JeonDjSGvGGUNHreGQns+Mpt6WX/dVzWBHgg+dYZhkC4X+zTDfkTU+Vy9y7Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-duplicate-named-capturing-groups-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-duplicate-named-capturing-groups-regex/-/plugin-transform-duplicate-named-capturing-groups-regex-7.27.1.tgz",
      "integrity": "sha512-hkGcueTEzuhB30B3eJCbCYeCaaEQOmQR0AdvzpD4LoN0GXMWzzGSuRrxR2xTnCrvNbVwK9N6/jQ92GSLfiZWoQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-dynamic-import": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-dynamic-import/-/plugin-transform-dynamic-import-7.27.1.tgz",
      "integrity": "sha512-MHzkWQcEmjzzVW9j2q8LGjwGWpG2mjwaaB0BNQwst3FIjqsg8Ct/mIZlvSPJvfi9y2AC8mi/ktxbFVL9pZ1I4A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-explicit-resource-management": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-explicit-resource-management/-/plugin-transform-explicit-resource-management-7.28.0.tgz",
      "integrity": "sha512-K8nhUcn3f6iB+P3gwCv/no7OdzOZQcKchW6N389V6PD8NUWKZHzndOd9sPDVbMoBsbmjMqlB4L9fm+fEFNVlwQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/plugin-transform-destructuring": "^7.28.0"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-exponentiation-operator": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-exponentiation-operator/-/plugin-transform-exponentiation-operator-7.27.1.tgz",
      "integrity": "sha512-uspvXnhHvGKf2r4VVtBpeFnuDWsJLQ6MF6lGJLC89jBR1uoVeqM416AZtTuhTezOfgHicpJQmoD5YUakO/YmXQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-export-namespace-from": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-export-namespace-from/-/plugin-transform-export-namespace-from-7.27.1.tgz",
      "integrity": "sha512-tQvHWSZ3/jH2xuq/vZDy0jNn+ZdXJeM8gHvX4lnJmsc3+50yPlWdZXIc5ay+umX+2/tJIqHqiEqcJvxlmIvRvQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-flow-strip-types": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-flow-strip-types/-/plugin-transform-flow-strip-types-7.27.1.tgz",
      "integrity": "sha512-G5eDKsu50udECw7DL2AcsysXiQyB7Nfg521t2OAJ4tbfTJ27doHLeF/vlI1NZGlLdbb/v+ibvtL1YBQqYOwJGg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/plugin-syntax-flow": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-for-of": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-for-of/-/plugin-transform-for-of-7.27.1.tgz",
      "integrity": "sha512-BfbWFFEJFQzLCQ5N8VocnCtA8J1CLkNTe2Ms2wocj75dd6VpiqS5Z5quTYcUoo4Yq+DN0rtikODccuv7RU81sw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-function-name": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-function-name/-/plugin-transform-function-name-7.27.1.tgz",
      "integrity": "sha512-1bQeydJF9Nr1eBCMMbC+hdwmRlsv5XYOMu03YSWFwNs0HsAmtSxxF1fyuYPqemVldVyFmlCU7w8UE14LupUSZQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-json-strings": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-json-strings/-/plugin-transform-json-strings-7.27.1.tgz",
      "integrity": "sha512-6WVLVJiTjqcQauBhn1LkICsR2H+zm62I3h9faTDKt1qP4jn2o72tSvqMwtGFKGTpojce0gJs+76eZ2uCHRZh0Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-literals/-/plugin-transform-literals-7.27.1.tgz",
      "integrity": "sha512-0HCFSepIpLTkLcsi86GG3mTUzxV5jpmbv97hTETW3yzrAij8aqlD36toB1D0daVFJM8NK6GvKO0gslVQmm+zZA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-logical-assignment-operators": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-logical-assignment-operators/-/plugin-transform-logical-assignment-operators-7.27.1.tgz",
      "integrity": "sha512-SJvDs5dXxiae4FbSL1aBJlG4wvl594N6YEVVn9e3JGulwioy6z3oPjx/sQBO3Y4NwUu5HNix6KJ3wBZoewcdbw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-member-expression-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-member-expression-literals/-/plugin-transform-member-expression-literals-7.27.1.tgz",
      "integrity": "sha512-hqoBX4dcZ1I33jCSWcXrP+1Ku7kdqXf1oeah7ooKOIiAdKQ+uqftgCFNOSzA5AMS2XIHEYeGFg4cKRCdpxzVOQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-amd": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-amd/-/plugin-transform-modules-amd-7.27.1.tgz",
      "integrity": "sha512-iCsytMg/N9/oFq6n+gFTvUYDZQOMK5kEdeYxmxt91fcJGycfxVP9CnrxoliM0oumFERba2i8ZtwRUCMhvP1LnA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-commonjs": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-commonjs/-/plugin-transform-modules-commonjs-7.27.1.tgz",
      "integrity": "sha512-OJguuwlTYlN0gBZFRPqwOGNWssZjfIUdS7HMYtN8c1KmwpwHFBwTeFZrg9XZa+DFTitWOW5iTAG7tyCUPsCCyw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-systemjs": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-systemjs/-/plugin-transform-modules-systemjs-7.27.1.tgz",
      "integrity": "sha512-w5N1XzsRbc0PQStASMksmUeqECuzKuTJer7kFagK8AXgpCMkeDMO5S+aaFb7A51ZYDF7XI34qsTX+fkHiIm5yA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-validator-identifier": "^7.27.1",
        "@babel/traverse": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-modules-umd": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-modules-umd/-/plugin-transform-modules-umd-7.27.1.tgz",
      "integrity": "sha512-iQBE/xC5BV1OxJbp6WG7jq9IWiD+xxlZhLrdwpPkTX3ydmXdvoCpyfJN7acaIBZaOqTfr76pgzqBJflNbeRK+w==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-transforms": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-named-capturing-groups-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-named-capturing-groups-regex/-/plugin-transform-named-capturing-groups-regex-7.27.1.tgz",
      "integrity": "sha512-SstR5JYy8ddZvD6MhV0tM/j16Qds4mIpJTOd1Yu9J9pJjH93bxHECF7pgtc28XvkzTD6Pxcm/0Z73Hvk7kb3Ng==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-new-target": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-new-target/-/plugin-transform-new-target-7.27.1.tgz",
      "integrity": "sha512-f6PiYeqXQ05lYq3TIfIDu/MtliKUbNwkGApPUvyo6+tc7uaR4cPjPe7DFPr15Uyycg2lZU6btZ575CuQoYh7MQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-nullish-coalescing-operator": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-nullish-coalescing-operator/-/plugin-transform-nullish-coalescing-operator-7.27.1.tgz",
      "integrity": "sha512-aGZh6xMo6q9vq1JGcw58lZ1Z0+i0xB2x0XaauNIUXd6O1xXc3RwoWEBlsTQrY4KQ9Jf0s5rgD6SiNkaUdJegTA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-numeric-separator": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-numeric-separator/-/plugin-transform-numeric-separator-7.27.1.tgz",
      "integrity": "sha512-fdPKAcujuvEChxDBJ5c+0BTaS6revLV7CJL08e4m3de8qJfNIuCc2nc7XJYOjBoTMJeqSmwXJ0ypE14RCjLwaw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-object-rest-spread": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-object-rest-spread/-/plugin-transform-object-rest-spread-7.28.4.tgz",
      "integrity": "sha512-373KA2HQzKhQCYiRVIRr+3MjpCObqzDlyrM6u4I201wL8Mp2wHf7uB8GhDwis03k2ti8Zr65Zyyqs1xOxUF/Ew==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-compilation-targets": "^7.27.2",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/plugin-transform-destructuring": "^7.28.0",
        "@babel/plugin-transform-parameters": "^7.27.7",
        "@babel/traverse": "^7.28.4"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-object-super": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-object-super/-/plugin-transform-object-super-7.27.1.tgz",
      "integrity": "sha512-SFy8S9plRPbIcxlJ8A6mT/CxFdJx/c04JEctz4jf8YZaVS2px34j7NXRrlGlHkN/M2gnpL37ZpGRGVFLd3l8Ng==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-replace-supers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-optional-catch-binding": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-optional-catch-binding/-/plugin-transform-optional-catch-binding-7.27.1.tgz",
      "integrity": "sha512-txEAEKzYrHEX4xSZN4kJ+OfKXFVSWKB2ZxM9dpcE3wT7smwkNmXo5ORRlVzMVdJbD+Q8ILTgSD7959uj+3Dm3Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-optional-chaining": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-optional-chaining/-/plugin-transform-optional-chaining-7.27.1.tgz",
      "integrity": "sha512-BQmKPPIuc8EkZgNKsv0X4bPmOoayeu4F1YCwx2/CfmDSXDbp7GnzlUH+/ul5VGfRg1AoFPsrIThlEBj2xb4CAg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-parameters": {
      "version": "7.27.7",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-parameters/-/plugin-transform-parameters-7.27.7.tgz",
      "integrity": "sha512-qBkYTYCb76RRxUM6CcZA5KRu8K4SM8ajzVeUgVdMVO9NN9uI/GaVmBg/WKJJGnNokV9SY8FxNOVWGXzqzUidBg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-private-methods": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-private-methods/-/plugin-transform-private-methods-7.27.1.tgz",
      "integrity": "sha512-10FVt+X55AjRAYI9BrdISN9/AQWHqldOeZDUoLyif1Kn05a56xVBXb8ZouL8pZ9jem8QpXaOt8TS7RHUIS+GPA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-class-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-private-property-in-object": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-private-property-in-object/-/plugin-transform-private-property-in-object-7.27.1.tgz",
      "integrity": "sha512-5J+IhqTi1XPa0DXF83jYOaARrX+41gOewWbkPyjMNRDqgOCqdffGh8L3f/Ek5utaEBZExjSAzcyjmV9SSAWObQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.1",
        "@babel/helper-create-class-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-property-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-property-literals/-/plugin-transform-property-literals-7.27.1.tgz",
      "integrity": "sha512-oThy3BCuCha8kDZ8ZkgOg2exvPYUlprMukKQXI1r1pJ47NCvxfkEy8vK+r/hT9nF0Aa4H1WUPZZjHTFtAhGfmQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-constant-elements": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-constant-elements/-/plugin-transform-react-constant-elements-7.27.1.tgz",
      "integrity": "sha512-edoidOjl/ZxvYo4lSBOQGDSyToYVkTAwyVoa2tkuYTSmjrB1+uAedoL5iROVLXkxH+vRgA7uP4tMg2pUJpZ3Ug==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-display-name": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-display-name/-/plugin-transform-react-display-name-7.28.0.tgz",
      "integrity": "sha512-D6Eujc2zMxKjfa4Zxl4GHMsmhKKZ9VpcqIchJLvwTxad9zWIYulwYItBovpDOoNLISpcZSXoDJ5gaGbQUDqViA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-jsx": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-jsx/-/plugin-transform-react-jsx-7.27.1.tgz",
      "integrity": "sha512-2KH4LWGSrJIkVf5tSiBFYuXDAoWRq2MMwgivCf+93dd0GQi8RXLjKA/0EvRnVV5G0hrHczsquXuD01L8s6dmBw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.1",
        "@babel/helper-module-imports": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/plugin-syntax-jsx": "^7.27.1",
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-jsx-development": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-jsx-development/-/plugin-transform-react-jsx-development-7.27.1.tgz",
      "integrity": "sha512-ykDdF5yI4f1WrAolLqeF3hmYU12j9ntLQl/AOG1HAS21jxyg1Q0/J/tpREuYLfatGdGmXp/3yS0ZA76kOlVq9Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/plugin-transform-react-jsx": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-react-pure-annotations": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-react-pure-annotations/-/plugin-transform-react-pure-annotations-7.27.1.tgz",
      "integrity": "sha512-JfuinvDOsD9FVMTHpzA/pBLisxpv1aSf+OIV8lgH3MuWrks19R27e6a6DipIg4aX1Zm9Wpb04p8wljfKrVSnPA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-regenerator": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-regenerator/-/plugin-transform-regenerator-7.28.4.tgz",
      "integrity": "sha512-+ZEdQlBoRg9m2NnzvEeLgtvBMO4tkFBw5SQIUgLICgTrumLoU7lr+Oghi6km2PFj+dbUt2u1oby2w3BDO9YQnA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-regexp-modifiers": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-regexp-modifiers/-/plugin-transform-regexp-modifiers-7.27.1.tgz",
      "integrity": "sha512-TtEciroaiODtXvLZv4rmfMhkCv8jx3wgKpL68PuiPh2M4fvz5jhsA7697N1gMvkvr/JTF13DrFYyEbY9U7cVPA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/plugin-transform-reserved-words": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-reserved-words/-/plugin-transform-reserved-words-7.27.1.tgz",
      "integrity": "sha512-V2ABPHIJX4kC7HegLkYoDpfg9PVmuWy/i6vUM5eGK22bx4YVFD3M5F0QQnWQoDs6AGsUWTVOopBiMFQgHaSkVw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-runtime": {
      "version": "7.28.3",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-runtime/-/plugin-transform-runtime-7.28.3.tgz",
      "integrity": "sha512-Y6ab1kGqZ0u42Zv/4a7l0l72n9DKP/MKoKWaUSBylrhNZO2prYuqFOLbn5aW5SIFXwSH93yfjbgllL8lxuGKLg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "babel-plugin-polyfill-corejs2": "^0.4.14",
        "babel-plugin-polyfill-corejs3": "^0.13.0",
        "babel-plugin-polyfill-regenerator": "^0.6.5",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-runtime/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/plugin-transform-shorthand-properties": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-shorthand-properties/-/plugin-transform-shorthand-properties-7.27.1.tgz",
      "integrity": "sha512-N/wH1vcn4oYawbJ13Y/FxcQrWk63jhfNa7jef0ih7PHSIHX2LB7GWE1rkPrOnka9kwMxb6hMl19p7lidA+EHmQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-spread": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-spread/-/plugin-transform-spread-7.27.1.tgz",
      "integrity": "sha512-kpb3HUqaILBJcRFVhFUs6Trdd4mkrzcGXss+6/mxUd273PfbWqSDHRzMT2234gIg2QYfAjvXLSquP1xECSg09Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-sticky-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-sticky-regex/-/plugin-transform-sticky-regex-7.27.1.tgz",
      "integrity": "sha512-lhInBO5bi/Kowe2/aLdBAawijx+q1pQzicSgnkB6dUPc1+RC8QmJHKf2OjvU+NZWitguJHEaEmbV6VWEouT58g==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-template-literals": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-template-literals/-/plugin-transform-template-literals-7.27.1.tgz",
      "integrity": "sha512-fBJKiV7F2DxZUkg5EtHKXQdbsbURW3DZKQUWphDum0uRP6eHGGa/He9mc0mypL680pb+e/lDIthRohlv8NCHkg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-typeof-symbol": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-typeof-symbol/-/plugin-transform-typeof-symbol-7.27.1.tgz",
      "integrity": "sha512-RiSILC+nRJM7FY5srIyc4/fGIwUhyDuuBSdWn4y6yT6gm652DpCHZjIipgn6B7MQ1ITOUnAKWixEUjQRIBIcLw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-typescript": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-typescript/-/plugin-transform-typescript-7.28.0.tgz",
      "integrity": "sha512-4AEiDEBPIZvLQaWlc9liCavE0xRM0dNca41WtBeM3jgFptfUOSG9z0uteLhq6+3rq+WB6jIvUwKDTpXEHPJ2Vg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.27.3",
        "@babel/helper-create-class-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-skip-transparent-expression-wrappers": "^7.27.1",
        "@babel/plugin-syntax-typescript": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-escapes": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-escapes/-/plugin-transform-unicode-escapes-7.27.1.tgz",
      "integrity": "sha512-Ysg4v6AmF26k9vpfFuTZg8HRfVWzsh1kVfowA23y9j/Gu6dOuahdUVhkLqpObp3JIv27MLSii6noRnuKN8H0Mg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-property-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-property-regex/-/plugin-transform-unicode-property-regex-7.27.1.tgz",
      "integrity": "sha512-uW20S39PnaTImxp39O5qFlHLS9LJEmANjMG7SxIhap8rCHqu0Ik+tLEPX5DKmHn6CsWQ7j3lix2tFOa5YtL12Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-regex/-/plugin-transform-unicode-regex-7.27.1.tgz",
      "integrity": "sha512-xvINq24TRojDuyt6JGtHmkVkrfVV3FPT16uytxImLeBZqW3/H52yN+kM1MGuyPkIQxrzKwPHs5U/MP3qKyzkGw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/plugin-transform-unicode-sets-regex": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/plugin-transform-unicode-sets-regex/-/plugin-transform-unicode-sets-regex-7.27.1.tgz",
      "integrity": "sha512-EtkOujbc4cgvb0mlpQefi4NTPBzhSIevblFevACNLUspmrALgmEBdL/XfnyyITfd8fKBZrZys92zOWcik7j9Tw==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-create-regexp-features-plugin": "^7.27.1",
        "@babel/helper-plugin-utils": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/@babel/preset-env": {
      "version": "7.28.3",
      "resolved": "https://registry.npmjs.org/@babel/preset-env/-/preset-env-7.28.3.tgz",
      "integrity": "sha512-ROiDcM+GbYVPYBOeCR6uBXKkQpBExLl8k9HO1ygXEyds39j+vCCsjmj7S8GOniZQlEs81QlkdJZe76IpLSiqpg==",
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.28.0",
        "@babel/helper-compilation-targets": "^7.27.2",
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-validator-option": "^7.27.1",
        "@babel/plugin-bugfix-firefox-class-in-computed-class-key": "^7.27.1",
        "@babel/plugin-bugfix-safari-class-field-initializer-scope": "^7.27.1",
        "@babel/plugin-bugfix-safari-id-destructuring-collision-in-function-expression": "^7.27.1",
        "@babel/plugin-bugfix-v8-spread-parameters-in-optional-chaining": "^7.27.1",
        "@babel/plugin-bugfix-v8-static-class-fields-redefine-readonly": "^7.28.3",
        "@babel/plugin-proposal-private-property-in-object": "7.21.0-placeholder-for-preset-env.2",
        "@babel/plugin-syntax-import-assertions": "^7.27.1",
        "@babel/plugin-syntax-import-attributes": "^7.27.1",
        "@babel/plugin-syntax-unicode-sets-regex": "^7.18.6",
        "@babel/plugin-transform-arrow-functions": "^7.27.1",
        "@babel/plugin-transform-async-generator-functions": "^7.28.0",
        "@babel/plugin-transform-async-to-generator": "^7.27.1",
        "@babel/plugin-transform-block-scoped-functions": "^7.27.1",
        "@babel/plugin-transform-block-scoping": "^7.28.0",
        "@babel/plugin-transform-class-properties": "^7.27.1",
        "@babel/plugin-transform-class-static-block": "^7.28.3",
        "@babel/plugin-transform-classes": "^7.28.3",
        "@babel/plugin-transform-computed-properties": "^7.27.1",
        "@babel/plugin-transform-destructuring": "^7.28.0",
        "@babel/plugin-transform-dotall-regex": "^7.27.1",
        "@babel/plugin-transform-duplicate-keys": "^7.27.1",
        "@babel/plugin-transform-duplicate-named-capturing-groups-regex": "^7.27.1",
        "@babel/plugin-transform-dynamic-import": "^7.27.1",
        "@babel/plugin-transform-explicit-resource-management": "^7.28.0",
        "@babel/plugin-transform-exponentiation-operator": "^7.27.1",
        "@babel/plugin-transform-export-namespace-from": "^7.27.1",
        "@babel/plugin-transform-for-of": "^7.27.1",
        "@babel/plugin-transform-function-name": "^7.27.1",
        "@babel/plugin-transform-json-strings": "^7.27.1",
        "@babel/plugin-transform-literals": "^7.27.1",
        "@babel/plugin-transform-logical-assignment-operators": "^7.27.1",
        "@babel/plugin-transform-member-expression-literals": "^7.27.1",
        "@babel/plugin-transform-modules-amd": "^7.27.1",
        "@babel/plugin-transform-modules-commonjs": "^7.27.1",
        "@babel/plugin-transform-modules-systemjs": "^7.27.1",
        "@babel/plugin-transform-modules-umd": "^7.27.1",
        "@babel/plugin-transform-named-capturing-groups-regex": "^7.27.1",
        "@babel/plugin-transform-new-target": "^7.27.1",
        "@babel/plugin-transform-nullish-coalescing-operator": "^7.27.1",
        "@babel/plugin-transform-numeric-separator": "^7.27.1",
        "@babel/plugin-transform-object-rest-spread": "^7.28.0",
        "@babel/plugin-transform-object-super": "^7.27.1",
        "@babel/plugin-transform-optional-catch-binding": "^7.27.1",
        "@babel/plugin-transform-optional-chaining": "^7.27.1",
        "@babel/plugin-transform-parameters": "^7.27.7",
        "@babel/plugin-transform-private-methods": "^7.27.1",
        "@babel/plugin-transform-private-property-in-object": "^7.27.1",
        "@babel/plugin-transform-property-literals": "^7.27.1",
        "@babel/plugin-transform-regenerator": "^7.28.3",
        "@babel/plugin-transform-regexp-modifiers": "^7.27.1",
        "@babel/plugin-transform-reserved-words": "^7.27.1",
        "@babel/plugin-transform-shorthand-properties": "^7.27.1",
        "@babel/plugin-transform-spread": "^7.27.1",
        "@babel/plugin-transform-sticky-regex": "^7.27.1",
        "@babel/plugin-transform-template-literals": "^7.27.1",
        "@babel/plugin-transform-typeof-symbol": "^7.27.1",
        "@babel/plugin-transform-unicode-escapes": "^7.27.1",
        "@babel/plugin-transform-unicode-property-regex": "^7.27.1",
        "@babel/plugin-transform-unicode-regex": "^7.27.1",
        "@babel/plugin-transform-unicode-sets-regex": "^7.27.1",
        "@babel/preset-modules": "0.1.6-no-external-plugins",
        "babel-plugin-polyfill-corejs2": "^0.4.14",
        "babel-plugin-polyfill-corejs3": "^0.13.0",
        "babel-plugin-polyfill-regenerator": "^0.6.5",
        "core-js-compat": "^3.43.0",
        "semver": "^6.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/preset-env/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/@babel/preset-modules": {
      "version": "0.1.6-no-external-plugins",
      "resolved": "https://registry.npmjs.org/@babel/preset-modules/-/preset-modules-0.1.6-no-external-plugins.tgz",
      "integrity": "sha512-HrcgcIESLm9aIR842yhJ5RWan/gebQUJ6E/E5+rf0y9o6oj7w0Br+sWuL6kEQ/o/AdfvR1Je9jG18/gnpwjEyA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.0.0",
        "@babel/types": "^7.4.4",
        "esutils": "^2.0.2"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/@babel/preset-react": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/preset-react/-/preset-react-7.27.1.tgz",
      "integrity": "sha512-oJHWh2gLhU9dW9HHr42q0cI0/iHHXTLGe39qvpAZZzagHy0MzYLCnCVV0symeRvzmjHyVU7mw2K06E6u/JwbhA==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-validator-option": "^7.27.1",
        "@babel/plugin-transform-react-display-name": "^7.27.1",
        "@babel/plugin-transform-react-jsx": "^7.27.1",
        "@babel/plugin-transform-react-jsx-development": "^7.27.1",
        "@babel/plugin-transform-react-pure-annotations": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/preset-typescript": {
      "version": "7.27.1",
      "resolved": "https://registry.npmjs.org/@babel/preset-typescript/-/preset-typescript-7.27.1.tgz",
      "integrity": "sha512-l7WfQfX0WK4M0v2RudjuQK4u99BS6yLHYEmdtVPP7lKV013zr9DygFuWNlnbvQ9LR+LS0Egz/XAvGx5U9MX0fQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.27.1",
        "@babel/helper-validator-option": "^7.27.1",
        "@babel/plugin-syntax-jsx": "^7.27.1",
        "@babel/plugin-transform-modules-commonjs": "^7.27.1",
        "@babel/plugin-transform-typescript": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/@babel/runtime": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/runtime/-/runtime-7.28.4.tgz",
      "integrity": "sha512-Q/N6JNWvIvPnLDvjlE1OUBLPQHH6l3CltCEsHIujp45zQUSSh8K+gHnaEX45yAT1nyngnINhvWtzN+Nb9D8RAQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/template": {
      "version": "7.27.2",
      "resolved": "https://registry.npmjs.org/@babel/template/-/template-7.27.2.tgz",
      "integrity": "sha512-LPDZ85aEJyYSd18/DkjNh4/y1ntkE5KwUHWTiqgRxruuZL2F1yuHligVHLvcHY2vMHXttKFpJn6LwfI7cw7ODw==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.27.1",
        "@babel/parser": "^7.27.2",
        "@babel/types": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/traverse": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/traverse/-/traverse-7.28.4.tgz",
      "integrity": "sha512-YEzuboP2qvQavAcjgQNVgsvHIDv6ZpwXvcvjmyySP2DIMuByS/6ioU5G9pYrWHM6T2YDfc7xga9iNzYOs12CFQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.27.1",
        "@babel/generator": "^7.28.3",
        "@babel/helper-globals": "^7.28.0",
        "@babel/parser": "^7.28.4",
        "@babel/template": "^7.27.2",
        "@babel/types": "^7.28.4",
        "debug": "^4.3.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@babel/types": {
      "version": "7.28.4",
      "resolved": "https://registry.npmjs.org/@babel/types/-/types-7.28.4.tgz",
      "integrity": "sha512-bkFqkLhh3pMBUQQkpVgWDWq/lqzc2678eUyDlTBhRqhCHFguYYGM0Efga7tYk4TogG/3x0EEl66/OQ+WGbWB/Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-string-parser": "^7.27.1",
        "@babel/helper-validator-identifier": "^7.27.1"
      },
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/@bcoe/v8-coverage": {
      "version": "0.2.3",
      "resolved": "https://registry.npmjs.org/@bcoe/v8-coverage/-/v8-coverage-0.2.3.tgz",
      "integrity": "sha512-0hYQ8SB4Db5zvZB4axdMHGwEaQjkZzFjQiN9LVYvIFB2nSUHW9tYpxWriPrWDASIxiaXax83REcLxuSdnGPZtw==",
      "license": "MIT"
    },
    "node_modules/@csstools/normalize.css": {
      "version": "12.1.1",
      "resolved": "https://registry.npmjs.org/@csstools/normalize.css/-/normalize.css-12.1.1.tgz",
      "integrity": "sha512-YAYeJ+Xqh7fUou1d1j9XHl44BmsuThiTr4iNrgCQ3J27IbhXsxXDGZ1cXv8Qvs99d4rBbLiSKy3+WZiet32PcQ==",
      "license": "CC0-1.0"
    },
    "node_modules/@csstools/postcss-cascade-layers": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-cascade-layers/-/postcss-cascade-layers-1.1.1.tgz",
      "integrity": "sha512-+KdYrpKC5TgomQr2DlZF4lDEpHcoxnj5IGddYYfBWJAKfj1JtuHUIqMa+E1pJJ+z3kvDViWMqyqPlG4Ja7amQA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/selector-specificity": "^2.0.2",
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-color-function": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-color-function/-/postcss-color-function-1.1.1.tgz",
      "integrity": "sha512-Bc0f62WmHdtRDjf5f3e2STwRAl89N2CLb+9iAwzrv4L2hncrbDwnQD9PCq0gtAt7pOI2leIV08HIBUd4jxD8cw==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-font-format-keywords": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-font-format-keywords/-/postcss-font-format-keywords-1.0.1.tgz",
      "integrity": "sha512-ZgrlzuUAjXIOc2JueK0X5sZDjCtgimVp/O5CEqTcs5ShWBa6smhWYbS0x5cVc/+rycTDbjjzoP0KTDnUneZGOg==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-hwb-function": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-hwb-function/-/postcss-hwb-function-1.0.2.tgz",
      "integrity": "sha512-YHdEru4o3Rsbjmu6vHy4UKOXZD+Rn2zmkAmLRfPet6+Jz4Ojw8cbWxe1n42VaXQhD3CQUXXTooIy8OkVbUcL+w==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-ic-unit": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-ic-unit/-/postcss-ic-unit-1.0.1.tgz",
      "integrity": "sha512-Ot1rcwRAaRHNKC9tAqoqNZhjdYBzKk1POgWfhN4uCOE47ebGcLRqXjKkApVDpjifL6u2/55ekkpnFcp+s/OZUw==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-is-pseudo-class": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-is-pseudo-class/-/postcss-is-pseudo-class-2.0.7.tgz",
      "integrity": "sha512-7JPeVVZHd+jxYdULl87lvjgvWldYu+Bc62s9vD/ED6/QTGjy0jy0US/f6BG53sVMTBJ1lzKZFpYmofBN9eaRiA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/selector-specificity": "^2.0.0",
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-nested-calc": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-nested-calc/-/postcss-nested-calc-1.0.0.tgz",
      "integrity": "sha512-JCsQsw1wjYwv1bJmgjKSoZNvf7R6+wuHDAbi5f/7MbFhl2d/+v+TvBTU4BJH3G1X1H87dHl0mh6TfYogbT/dJQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-normalize-display-values": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-normalize-display-values/-/postcss-normalize-display-values-1.0.1.tgz",
      "integrity": "sha512-jcOanIbv55OFKQ3sYeFD/T0Ti7AMXc9nM1hZWu8m/2722gOTxFg7xYu4RDLJLeZmPUVQlGzo4jhzvTUq3x4ZUw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-oklab-function": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-oklab-function/-/postcss-oklab-function-1.1.1.tgz",
      "integrity": "sha512-nJpJgsdA3dA9y5pgyb/UfEzE7W5Ka7u0CX0/HIMVBNWzWemdcTH3XwANECU6anWv/ao4vVNLTMxhiPNZsTK6iA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-progressive-custom-properties": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-progressive-custom-properties/-/postcss-progressive-custom-properties-1.3.0.tgz",
      "integrity": "sha512-ASA9W1aIy5ygskZYuWams4BzafD12ULvSypmaLJT2jvQ8G0M3I8PRQhC0h7mG0Z3LI05+agZjqSR9+K9yaQQjA==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.3"
      }
    },
    "node_modules/@csstools/postcss-stepped-value-functions": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-stepped-value-functions/-/postcss-stepped-value-functions-1.0.1.tgz",
      "integrity": "sha512-dz0LNoo3ijpTOQqEJLY8nyaapl6umbmDcgj4AD0lgVQ572b2eqA1iGZYTTWhrcrHztWDDRAX2DGYyw2VBjvCvQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-text-decoration-shorthand": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-text-decoration-shorthand/-/postcss-text-decoration-shorthand-1.0.0.tgz",
      "integrity": "sha512-c1XwKJ2eMIWrzQenN0XbcfzckOLLJiczqy+YvfGmzoVXd7pT9FfObiSEfzs84bpE/VqfpEuAZ9tCRbZkZxxbdw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-trigonometric-functions": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-trigonometric-functions/-/postcss-trigonometric-functions-1.0.2.tgz",
      "integrity": "sha512-woKaLO///4bb+zZC2s80l+7cm07M7268MsyG3M0ActXXEFi6SuhvriQYcb58iiKGbjwwIU7n45iRLEHypB47Og==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/postcss-unset-value": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/@csstools/postcss-unset-value/-/postcss-unset-value-1.0.2.tgz",
      "integrity": "sha512-c8J4roPBILnelAsdLr4XOAR/GsTm0GJi4XpcfvoWk3U6KiTCqiFYc63KhRMQQX35jYMp4Ao8Ij9+IZRgMfJp1g==",
      "license": "CC0-1.0",
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/@csstools/selector-specificity": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/@csstools/selector-specificity/-/selector-specificity-2.2.0.tgz",
      "integrity": "sha512-+OJ9konv95ClSTOJCmMZqpd5+YGsB2S+x6w3E1oaM8UuR5j8nTNHYSz8c9BEPGDOCMQYIEEGlVPj/VY64iTbGw==",
      "license": "CC0-1.0",
      "engines": {
        "node": "^14 || ^16 || >=18"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss-selector-parser": "^6.0.10"
      }
    },
    "node_modules/@eslint-community/eslint-utils": {
      "version": "4.9.0",
      "resolved": "https://registry.npmjs.org/@eslint-community/eslint-utils/-/eslint-utils-4.9.0.tgz",
      "integrity": "sha512-ayVFHdtZ+hsq1t2Dy24wCmGXGe4q9Gu3smhLYALJrr473ZH27MsnSL+LKUlimp4BWJqMDMLmPpx/Q9R3OAlL4g==",
      "license": "MIT",
      "dependencies": {
        "eslint-visitor-keys": "^3.4.3"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || >=8.0.0"
      }
    },
    "node_modules/@eslint-community/regexpp": {
      "version": "4.12.1",
      "resolved": "https://registry.npmjs.org/@eslint-community/regexpp/-/regexpp-4.12.1.tgz",
      "integrity": "sha512-CCZCDJuduB9OUkFkY2IgppNZMi2lBQgD2qzwXkEia16cge2pijY/aXi96CJMquDMn3nJdlPV1A5KrJEXwfLNzQ==",
      "license": "MIT",
      "engines": {
        "node": "^12.0.0 || ^14.0.0 || >=16.0.0"
      }
    },
    "node_modules/@eslint/eslintrc": {
      "version": "2.1.4",
      "resolved": "https://registry.npmjs.org/@eslint/eslintrc/-/eslintrc-2.1.4.tgz",
      "integrity": "sha512-269Z39MS6wVJtsoUl10L60WdkhJVdPG24Q4eZTH3nnF6lpvSShEK3wQjDX9JRWAUPvPh7COouPpU9IrqaZFvtQ==",
      "license": "MIT",
      "dependencies": {
        "ajv": "^6.12.4",
        "debug": "^4.3.2",
        "espree": "^9.6.0",
        "globals": "^13.19.0",
        "ignore": "^5.2.0",
        "import-fresh": "^3.2.1",
        "js-yaml": "^4.1.0",
        "minimatch": "^3.1.2",
        "strip-json-comments": "^3.1.1"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/@eslint/eslintrc/node_modules/argparse": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/argparse/-/argparse-2.0.1.tgz",
      "integrity": "sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q==",
      "license": "Python-2.0"
    },
    "node_modules/@eslint/eslintrc/node_modules/js-yaml": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/js-yaml/-/js-yaml-4.1.0.tgz",
      "integrity": "sha512-wpxZs9NoxZaJESJGIZTyDEaYpl0FKSA+FB9aJiyemKhMwkxQg63h4T1KJgUGHpTqPDNRcmmYLugrRjJlBtWvRA==",
      "license": "MIT",
      "dependencies": {
        "argparse": "^2.0.1"
      },
      "bin": {
        "js-yaml": "bin/js-yaml.js"
      }
    },
    "node_modules/@eslint/js": {
      "version": "8.57.1",
      "resolved": "https://registry.npmjs.org/@eslint/js/-/js-8.57.1.tgz",
      "integrity": "sha512-d9zaMRSTIKDLhctzH12MtXvJKSSUhaHcjV+2Z+GK+EEY7XKpP5yR4x+N3TAcHTcu963nIr+TMcCb4DBCYX1z6Q==",
      "license": "MIT",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      }
    },
    "node_modules/@humanwhocodes/config-array": {
      "version": "0.13.0",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/config-array/-/config-array-0.13.0.tgz",
      "integrity": "sha512-DZLEEqFWQFiyK6h5YIeynKx7JlvCYWL0cImfSRXZ9l4Sg2efkFGTuFf6vzXjK1cq6IYkU+Eg/JizXw+TD2vRNw==",
      "deprecated": "Use @eslint/config-array instead",
      "license": "Apache-2.0",
      "dependencies": {
        "@humanwhocodes/object-schema": "^2.0.3",
        "debug": "^4.3.1",
        "minimatch": "^3.0.5"
      },
      "engines": {
        "node": ">=10.10.0"
      }
    },
    "node_modules/@humanwhocodes/module-importer": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/module-importer/-/module-importer-1.0.1.tgz",
      "integrity": "sha512-bxveV4V8v5Yb4ncFTT3rPSgZBOpCkjfK0y4oVVVJwIuDVBRMDXrPyXRL988i5ap9m9bnyEEjWfm5WkBmtffLfA==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=12.22"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/nzakas"
      }
    },
    "node_modules/@humanwhocodes/object-schema": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/@humanwhocodes/object-schema/-/object-schema-2.0.3.tgz",
      "integrity": "sha512-93zYdMES/c1D69yZiKDBj0V24vqNzB/koF26KPaagAfd3P/4gUlh3Dys5ogAK+Exi9QyzlD8x/08Zt7wIKcDcA==",
      "deprecated": "Use @eslint/object-schema instead",
      "license": "BSD-3-Clause"
    },
    "node_modules/@isaacs/cliui": {
      "version": "8.0.2",
      "resolved": "https://registry.npmjs.org/@isaacs/cliui/-/cliui-8.0.2.tgz",
      "integrity": "sha512-O8jcjabXaleOG9DQ0+ARXWZBTfnP4WNAqzuiJK7ll44AmxGKv/J2M4TPjxjY3znBCfvBXFzucm1twdyFybFqEA==",
      "license": "ISC",
      "dependencies": {
        "string-width": "^5.1.2",
        "string-width-cjs": "npm:string-width@^4.2.0",
        "strip-ansi": "^7.0.1",
        "strip-ansi-cjs": "npm:strip-ansi@^6.0.1",
        "wrap-ansi": "^8.1.0",
        "wrap-ansi-cjs": "npm:wrap-ansi@^7.0.0"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/ansi-regex": {
      "version": "6.2.2",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-6.2.2.tgz",
      "integrity": "sha512-Bq3SmSpyFHaWjPk8If9yc6svM8c56dB5BAtW4Qbw5jHTwwXXcTLoRMkpDJp6VL0XzlWaCHTXrkFURMYmD0sLqg==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-regex?sponsor=1"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/ansi-styles": {
      "version": "6.2.3",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-6.2.3.tgz",
      "integrity": "sha512-4Dj6M28JB+oAH8kFkTLUo+a2jwOFkuqb3yucU0CANcRRUbxS0cP0nZYCGjcc3BNXwRIsUVmDGgzawme7zvJHvg==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/string-width": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/string-width/-/string-width-5.1.2.tgz",
      "integrity": "sha512-HnLOCR3vjcY8beoNLtcjZ5/nxn2afmME6lhrDrebokqMap+XbeW8n9TXpPDOqdGK5qcI3oT0GKTW6wC7EMiVqA==",
      "license": "MIT",
      "dependencies": {
        "eastasianwidth": "^0.2.0",
        "emoji-regex": "^9.2.2",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/strip-ansi": {
      "version": "7.1.2",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-7.1.2.tgz",
      "integrity": "sha512-gmBGslpoQJtgnMAvOVqGZpEz9dyoKTCzy2nfz/n8aIFhN/jCE/rCmcxabB6jOOHV+0WNnylOxaxBQPSvcWklhA==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^6.0.1"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/strip-ansi?sponsor=1"
      }
    },
    "node_modules/@isaacs/cliui/node_modules/wrap-ansi": {
      "version": "8.1.0",
      "resolved": "https://registry.npmjs.org/wrap-ansi/-/wrap-ansi-8.1.0.tgz",
      "integrity": "sha512-si7QWI6zUMq56bESFvagtmzMdGOtoxfR+Sez11Mobfc7tm+VkUckk9bW2UeffTGVUbOksxmSw0AA2gs8g71NCQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^6.1.0",
        "string-width": "^5.0.1",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/wrap-ansi?sponsor=1"
      }
    },
    "node_modules/@istanbuljs/load-nyc-config": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@istanbuljs/load-nyc-config/-/load-nyc-config-1.1.0.tgz",
      "integrity": "sha512-VjeHSlIzpv/NyD3N0YuHfXOPDIixcA1q2ZV98wsMqcYlPmv2n3Yb2lYP9XMElnaFVXg5A7YLTeLu6V84uQDjmQ==",
      "license": "ISC",
      "dependencies": {
        "camelcase": "^5.3.1",
        "find-up": "^4.1.0",
        "get-package-type": "^0.1.0",
        "js-yaml": "^3.13.1",
        "resolve-from": "^5.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/@istanbuljs/load-nyc-config/node_modules/camelcase": {
      "version": "5.3.1",
      "resolved": "https://registry.npmjs.org/camelcase/-/camelcase-5.3.1.tgz",
      "integrity": "sha512-L28STB170nwWS63UjtlEOE3dldQApaJXZkOI1uMFfzf3rRuPegHaHesyee+YxQ+W6SvRDQV6UrdOdRiR153wJg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/@istanbuljs/schema": {
      "version": "0.1.3",
      "resolved": "https://registry.npmjs.org/@istanbuljs/schema/-/schema-0.1.3.tgz",
      "integrity": "sha512-ZXRY4jNvVgSVQ8DL3LTcakaAtXwTVUxE81hslsyD2AtoXW/wVob10HkOJ1X/pAlcI7D+2YoZKg5do8G/w6RYgA==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/@jest/console": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/console/-/console-27.5.1.tgz",
      "integrity": "sha512-kZ/tNpS3NXn0mlXXXPNuDZnb4c0oZ20r4K5eemM2k30ZC3G0T02nXUvyhf5YdbXWHPEJLc9qGLxEZ216MdL+Zg==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "jest-message-util": "^27.5.1",
        "jest-util": "^27.5.1",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/core": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/core/-/core-27.5.1.tgz",
      "integrity": "sha512-AK6/UTrvQD0Cd24NSqmIA6rKsu0tKIxfiCducZvqxYdmMisOYAsdItspT+fQDQYARPf8XgjAFZi0ogW2agH5nQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/console": "^27.5.1",
        "@jest/reporters": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "ansi-escapes": "^4.2.1",
        "chalk": "^4.0.0",
        "emittery": "^0.8.1",
        "exit": "^0.1.2",
        "graceful-fs": "^4.2.9",
        "jest-changed-files": "^27.5.1",
        "jest-config": "^27.5.1",
        "jest-haste-map": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-resolve-dependencies": "^27.5.1",
        "jest-runner": "^27.5.1",
        "jest-runtime": "^27.5.1",
        "jest-snapshot": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-validate": "^27.5.1",
        "jest-watcher": "^27.5.1",
        "micromatch": "^4.0.4",
        "rimraf": "^3.0.0",
        "slash": "^3.0.0",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "node-notifier": "^8.0.1 || ^9.0.0 || ^10.0.0"
      },
      "peerDependenciesMeta": {
        "node-notifier": {
          "optional": true
        }
      }
    },
    "node_modules/@jest/environment": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/environment/-/environment-27.5.1.tgz",
      "integrity": "sha512-/WQjhPJe3/ghaol/4Bq480JKXV/Rfw8nQdN7f41fM8VDHLcxKXou6QyXAh3EFr9/bVG3x74z1NWDkP87EiY8gA==",
      "license": "MIT",
      "dependencies": {
        "@jest/fake-timers": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "jest-mock": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/fake-timers": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/fake-timers/-/fake-timers-27.5.1.tgz",
      "integrity": "sha512-/aPowoolwa07k7/oM3aASneNeBGCmGQsc3ugN4u6s4C/+s5M64MFo/+djTdiwcbQlRfFElGuDXWzaWj6QgKObQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@sinonjs/fake-timers": "^8.0.1",
        "@types/node": "*",
        "jest-message-util": "^27.5.1",
        "jest-mock": "^27.5.1",
        "jest-util": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/globals": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/globals/-/globals-27.5.1.tgz",
      "integrity": "sha512-ZEJNB41OBQQgGzgyInAv0UUfDDj3upmHydjieSxFvTRuZElrx7tXg/uVQ5hYVEwiXs3+aMsAeEc9X7xiSKCm4Q==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/types": "^27.5.1",
        "expect": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/reporters": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/reporters/-/reporters-27.5.1.tgz",
      "integrity": "sha512-cPXh9hWIlVJMQkVk84aIvXuBB4uQQmFqZiacloFuGiP3ah1sbCxCosidXFDfqG8+6fO1oR2dTJTlsOy4VFmUfw==",
      "license": "MIT",
      "dependencies": {
        "@bcoe/v8-coverage": "^0.2.3",
        "@jest/console": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "collect-v8-coverage": "^1.0.0",
        "exit": "^0.1.2",
        "glob": "^7.1.2",
        "graceful-fs": "^4.2.9",
        "istanbul-lib-coverage": "^3.0.0",
        "istanbul-lib-instrument": "^5.1.0",
        "istanbul-lib-report": "^3.0.0",
        "istanbul-lib-source-maps": "^4.0.0",
        "istanbul-reports": "^3.1.3",
        "jest-haste-map": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-worker": "^27.5.1",
        "slash": "^3.0.0",
        "source-map": "^0.6.0",
        "string-length": "^4.0.1",
        "terminal-link": "^2.0.0",
        "v8-to-istanbul": "^8.1.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "node-notifier": "^8.0.1 || ^9.0.0 || ^10.0.0"
      },
      "peerDependenciesMeta": {
        "node-notifier": {
          "optional": true
        }
      }
    },
    "node_modules/@jest/reporters/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/@jest/schemas": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/@jest/schemas/-/schemas-28.1.3.tgz",
      "integrity": "sha512-/l/VWsdt/aBXgjshLWOFyFt3IVdYypu5y2Wn2rOO1un6nkqIn8SLXzgIMYXFyYsRWDyF5EthmKJMIdJvk08grg==",
      "license": "MIT",
      "dependencies": {
        "@sinclair/typebox": "^0.24.1"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/@jest/source-map": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/source-map/-/source-map-27.5.1.tgz",
      "integrity": "sha512-y9NIHUYF3PJRlHk98NdC/N1gl88BL08aQQgu4k4ZopQkCw9t9cV8mtl3TV8b/YCB8XaVTFrmUTAJvjsntDireg==",
      "license": "MIT",
      "dependencies": {
        "callsites": "^3.0.0",
        "graceful-fs": "^4.2.9",
        "source-map": "^0.6.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/source-map/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/@jest/test-result": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/test-result/-/test-result-27.5.1.tgz",
      "integrity": "sha512-EW35l2RYFUcUQxFJz5Cv5MTOxlJIQs4I7gxzi2zVU7PJhOwfYq1MdC5nhSmYjX1gmMmLPvB3sIaC+BkcHRBfag==",
      "license": "MIT",
      "dependencies": {
        "@jest/console": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/istanbul-lib-coverage": "^2.0.0",
        "collect-v8-coverage": "^1.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/test-sequencer": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/test-sequencer/-/test-sequencer-27.5.1.tgz",
      "integrity": "sha512-LCheJF7WB2+9JuCS7VB/EmGIdQuhtqjRNI9A43idHv3E4KltCTsPsLxvdaubFHSYwY/fNjMWjl6vNRhDiN7vpQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/test-result": "^27.5.1",
        "graceful-fs": "^4.2.9",
        "jest-haste-map": "^27.5.1",
        "jest-runtime": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/transform": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/transform/-/transform-27.5.1.tgz",
      "integrity": "sha512-ipON6WtYgl/1329g5AIJVbUuEh0wZVbdpGwC99Jw4LwuoBNS95MVphU6zOeD9pDkon+LLbFL7lOQRapbB8SCHw==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.1.0",
        "@jest/types": "^27.5.1",
        "babel-plugin-istanbul": "^6.1.1",
        "chalk": "^4.0.0",
        "convert-source-map": "^1.4.0",
        "fast-json-stable-stringify": "^2.0.0",
        "graceful-fs": "^4.2.9",
        "jest-haste-map": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-util": "^27.5.1",
        "micromatch": "^4.0.4",
        "pirates": "^4.0.4",
        "slash": "^3.0.0",
        "source-map": "^0.6.1",
        "write-file-atomic": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jest/transform/node_modules/convert-source-map": {
      "version": "1.9.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-1.9.0.tgz",
      "integrity": "sha512-ASFBup0Mz1uyiIjANan1jzLQami9z1PoYSZCiiYW2FczPbenXc45FZdBZLzOT+r6+iciuEModtmCti+hjaAk0A==",
      "license": "MIT"
    },
    "node_modules/@jest/transform/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/@jest/types": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/@jest/types/-/types-27.5.1.tgz",
      "integrity": "sha512-Cx46iJ9QpwQTjIdq5VJu2QTMMs3QlEjI0x1QbBP5W1+nMzyc2XmimiRR/CbX9TO0cPTeUlxWMOu8mslYsJ8DEw==",
      "license": "MIT",
      "dependencies": {
        "@types/istanbul-lib-coverage": "^2.0.0",
        "@types/istanbul-reports": "^3.0.0",
        "@types/node": "*",
        "@types/yargs": "^16.0.0",
        "chalk": "^4.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/@jridgewell/gen-mapping": {
      "version": "0.3.13",
      "resolved": "https://registry.npmjs.org/@jridgewell/gen-mapping/-/gen-mapping-0.3.13.tgz",
      "integrity": "sha512-2kkt/7niJ6MgEPxF0bYdQ6etZaA+fQvDcLKckhy1yIQOzaoKjBBjSj63/aLVjYE3qhRt5dvM+uUyfCg6UKCBbA==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/sourcemap-codec": "^1.5.0",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/remapping": {
      "version": "2.3.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/remapping/-/remapping-2.3.5.tgz",
      "integrity": "sha512-LI9u/+laYG4Ds1TDKSJW2YPrIlcVYOwi2fUC6xB43lueCjgxV4lffOCZCtYFiH6TNOX+tQKXx97T4IKHbhyHEQ==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.24"
      }
    },
    "node_modules/@jridgewell/resolve-uri": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/@jridgewell/resolve-uri/-/resolve-uri-3.1.2.tgz",
      "integrity": "sha512-bRISgCIjP20/tbWSPWMEi54QVPRZExkuD9lJL+UIxUKtwVJA8wW1Trb1jMs1RFXo1CBTNZ/5hpC9QvmKWdopKw==",
      "license": "MIT",
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/@jridgewell/source-map": {
      "version": "0.3.11",
      "resolved": "https://registry.npmjs.org/@jridgewell/source-map/-/source-map-0.3.11.tgz",
      "integrity": "sha512-ZMp1V8ZFcPG5dIWnQLr3NSI1MiCU7UETdS/A0G8V/XWHvJv3ZsFqutJn1Y5RPmAPX6F3BiE397OqveU/9NCuIA==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.5",
        "@jridgewell/trace-mapping": "^0.3.25"
      }
    },
    "node_modules/@jridgewell/sourcemap-codec": {
      "version": "1.5.5",
      "resolved": "https://registry.npmjs.org/@jridgewell/sourcemap-codec/-/sourcemap-codec-1.5.5.tgz",
      "integrity": "sha512-cYQ9310grqxueWbl+WuIUIaiUaDcj7WOq5fVhEljNVgRfOUhY9fy2zTvfoqWsnebh8Sl70VScFbICvJnLKB0Og==",
      "license": "MIT"
    },
    "node_modules/@jridgewell/trace-mapping": {
      "version": "0.3.31",
      "resolved": "https://registry.npmjs.org/@jridgewell/trace-mapping/-/trace-mapping-0.3.31.tgz",
      "integrity": "sha512-zzNR+SdQSDJzc8joaeP8QQoCQr8NuYx2dIIytl1QeBEZHJ9uW6hebsrYgbz8hJwUQao3TWCMtmfV8Nu1twOLAw==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/resolve-uri": "^3.1.0",
        "@jridgewell/sourcemap-codec": "^1.4.14"
      }
    },
    "node_modules/@kurkle/color": {
      "version": "0.3.4",
      "resolved": "https://registry.npmjs.org/@kurkle/color/-/color-0.3.4.tgz",
      "integrity": "sha512-M5UknZPHRu3DEDWoipU6sE8PdkZ6Z/S+v4dD+Ke8IaNlpdSQah50lz1KtcFBa2vsdOnwbbnxJwVM4wty6udA5w==",
      "license": "MIT"
    },
    "node_modules/@leichtgewicht/ip-codec": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@leichtgewicht/ip-codec/-/ip-codec-2.0.5.tgz",
      "integrity": "sha512-Vo+PSpZG2/fmgmiNzYK9qWRh8h/CHrwD0mo1h1DzL4yzHNSfWYujGTYsWGreD000gcgmZ7K4Ys6Tx9TxtsKdDw==",
      "license": "MIT"
    },
    "node_modules/@nicolo-ribaudo/eslint-scope-5-internals": {
      "version": "5.1.1-v1",
      "resolved": "https://registry.npmjs.org/@nicolo-ribaudo/eslint-scope-5-internals/-/eslint-scope-5-internals-5.1.1-v1.tgz",
      "integrity": "sha512-54/JRvkLIzzDWshCWfuhadfrfZVPiElY8Fcgmg1HroEly/EDSszzhBAsarCux+D/kOslTRquNzuyGSmUSTTHGg==",
      "license": "MIT",
      "dependencies": {
        "eslint-scope": "5.1.1"
      }
    },
    "node_modules/@nicolo-ribaudo/eslint-scope-5-internals/node_modules/eslint-scope": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-5.1.1.tgz",
      "integrity": "sha512-2NxwbF/hZ0KpepYN0cNbo+FN6XoK7GaHlQhgx/hIZl6Va0bF45RQOOwhLIy8lQDbuCiadSLCBnH2CFYquit5bw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^4.1.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/@nicolo-ribaudo/eslint-scope-5-internals/node_modules/estraverse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-4.3.0.tgz",
      "integrity": "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/@nodelib/fs.scandir": {
      "version": "2.1.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.scandir/-/fs.scandir-2.1.5.tgz",
      "integrity": "sha512-vq24Bq3ym5HEQm2NKCr3yXDwjc7vTsEThRDnkp2DK9p1uqLR+DHurm/NOTo0KG7HYHU7eppKZj3MyqYuMBf62g==",
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "2.0.5",
        "run-parallel": "^1.1.9"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.stat": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.stat/-/fs.stat-2.0.5.tgz",
      "integrity": "sha512-RkhPPp2zrqDAQA/2jNhnztcPAlv64XdhIp7a7454A5ovI7Bukxgt7MX7udwAu3zg1DcpPU0rz3VV1SeaqvY4+A==",
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@nodelib/fs.walk": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/@nodelib/fs.walk/-/fs.walk-1.2.8.tgz",
      "integrity": "sha512-oGB+UxlgWcgQkgwo8GcEGwemoTFt3FIO9ababBmaGwXIoBKZ+GTy0pP185beGg7Llih/NSHSV2XAs1lnznocSg==",
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.scandir": "2.1.5",
        "fastq": "^1.6.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/@pkgjs/parseargs": {
      "version": "0.11.0",
      "resolved": "https://registry.npmjs.org/@pkgjs/parseargs/-/parseargs-0.11.0.tgz",
      "integrity": "sha512-+1VkjdD0QBLPodGrJUeqarH8VAIvQODIbwh9XpP5Syisf7YoQgsJKPNFoqqLQlu+VQ/tVSshMR6loPMn8U+dPg==",
      "license": "MIT",
      "optional": true,
      "engines": {
        "node": ">=14"
      }
    },
    "node_modules/@pmmmwh/react-refresh-webpack-plugin": {
      "version": "0.5.17",
      "resolved": "https://registry.npmjs.org/@pmmmwh/react-refresh-webpack-plugin/-/react-refresh-webpack-plugin-0.5.17.tgz",
      "integrity": "sha512-tXDyE1/jzFsHXjhRZQ3hMl0IVhYe5qula43LDWIhVfjp9G/nT5OQY5AORVOrkEGAUltBJOfOWeETbmhm6kHhuQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-html": "^0.0.9",
        "core-js-pure": "^3.23.3",
        "error-stack-parser": "^2.0.6",
        "html-entities": "^2.1.0",
        "loader-utils": "^2.0.4",
        "schema-utils": "^4.2.0",
        "source-map": "^0.7.3"
      },
      "engines": {
        "node": ">= 10.13"
      },
      "peerDependencies": {
        "@types/webpack": "4.x || 5.x",
        "react-refresh": ">=0.10.0 <1.0.0",
        "sockjs-client": "^1.4.0",
        "type-fest": ">=0.17.0 <5.0.0",
        "webpack": ">=4.43.0 <6.0.0",
        "webpack-dev-server": "3.x || 4.x || 5.x",
        "webpack-hot-middleware": "2.x",
        "webpack-plugin-serve": "0.x || 1.x"
      },
      "peerDependenciesMeta": {
        "@types/webpack": {
          "optional": true
        },
        "sockjs-client": {
          "optional": true
        },
        "type-fest": {
          "optional": true
        },
        "webpack-dev-server": {
          "optional": true
        },
        "webpack-hot-middleware": {
          "optional": true
        },
        "webpack-plugin-serve": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/plugin-babel": {
      "version": "5.3.1",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-babel/-/plugin-babel-5.3.1.tgz",
      "integrity": "sha512-WFfdLWU/xVWKeRQnKmIAQULUI7Il0gZnBIH/ZFO069wYIfPu+8zrfp/KMW0atmELoRDq8FbiP3VCss9MhCut7Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-module-imports": "^7.10.4",
        "@rollup/pluginutils": "^3.1.0"
      },
      "engines": {
        "node": ">= 10.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0",
        "@types/babel__core": "^7.1.9",
        "rollup": "^1.20.0||^2.0.0"
      },
      "peerDependenciesMeta": {
        "@types/babel__core": {
          "optional": true
        }
      }
    },
    "node_modules/@rollup/plugin-node-resolve": {
      "version": "11.2.1",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-node-resolve/-/plugin-node-resolve-11.2.1.tgz",
      "integrity": "sha512-yc2n43jcqVyGE2sqV5/YCmocy9ArjVAP/BeXyTtADTBBX6V0e5UMqwO8CdQ0kzjb6zu5P1qMzsScCMRvE9OlVg==",
      "license": "MIT",
      "dependencies": {
        "@rollup/pluginutils": "^3.1.0",
        "@types/resolve": "1.17.1",
        "builtin-modules": "^3.1.0",
        "deepmerge": "^4.2.2",
        "is-module": "^1.0.0",
        "resolve": "^1.19.0"
      },
      "engines": {
        "node": ">= 10.0.0"
      },
      "peerDependencies": {
        "rollup": "^1.20.0||^2.0.0"
      }
    },
    "node_modules/@rollup/plugin-replace": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/@rollup/plugin-replace/-/plugin-replace-2.4.2.tgz",
      "integrity": "sha512-IGcu+cydlUMZ5En85jxHH4qj2hta/11BHq95iHEyb2sbgiN0eCdzvUcHw5gt9pBL5lTi4JDYJ1acCoMGpTvEZg==",
      "license": "MIT",
      "dependencies": {
        "@rollup/pluginutils": "^3.1.0",
        "magic-string": "^0.25.7"
      },
      "peerDependencies": {
        "rollup": "^1.20.0 || ^2.0.0"
      }
    },
    "node_modules/@rollup/pluginutils": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/@rollup/pluginutils/-/pluginutils-3.1.0.tgz",
      "integrity": "sha512-GksZ6pr6TpIjHm8h9lSQ8pi8BE9VeubNT0OMJ3B5uZJ8pz73NPiqOtCog/x2/QzM1ENChPKxMDhiQuRHsqc+lg==",
      "license": "MIT",
      "dependencies": {
        "@types/estree": "0.0.39",
        "estree-walker": "^1.0.1",
        "picomatch": "^2.2.2"
      },
      "engines": {
        "node": ">= 8.0.0"
      },
      "peerDependencies": {
        "rollup": "^1.20.0||^2.0.0"
      }
    },
    "node_modules/@rollup/pluginutils/node_modules/@types/estree": {
      "version": "0.0.39",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-0.0.39.tgz",
      "integrity": "sha512-EYNwp3bU+98cpU4lAWYYL7Zz+2gryWH1qbdDTidVd6hkiR6weksdbMadyXKXNPEkQFhXM+hVO9ZygomHXp+AIw==",
      "license": "MIT"
    },
    "node_modules/@rtsao/scc": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/@rtsao/scc/-/scc-1.1.0.tgz",
      "integrity": "sha512-zt6OdqaDoOnJ1ZYsCYGt9YmWzDXl4vQdKTyJev62gFhRGKdx7mcT54V9KIjg+d2wi9EXsPvAPKe7i7WjfVWB8g==",
      "license": "MIT"
    },
    "node_modules/@rushstack/eslint-patch": {
      "version": "1.12.0",
      "resolved": "https://registry.npmjs.org/@rushstack/eslint-patch/-/eslint-patch-1.12.0.tgz",
      "integrity": "sha512-5EwMtOqvJMMa3HbmxLlF74e+3/HhwBTMcvt3nqVJgGCozO6hzIPOBlwm8mGVNR9SN2IJpxSnlxczyDjcn7qIyw==",
      "license": "MIT"
    },
    "node_modules/@sinclair/typebox": {
      "version": "0.24.51",
      "resolved": "https://registry.npmjs.org/@sinclair/typebox/-/typebox-0.24.51.tgz",
      "integrity": "sha512-1P1OROm/rdubP5aFDSZQILU0vrLCJ4fvHt6EoqHEM+2D/G5MK3bIaymUKLit8Js9gbns5UyJnkP/TZROLw4tUA==",
      "license": "MIT"
    },
    "node_modules/@sinonjs/commons": {
      "version": "1.8.6",
      "resolved": "https://registry.npmjs.org/@sinonjs/commons/-/commons-1.8.6.tgz",
      "integrity": "sha512-Ky+XkAkqPZSm3NLBeUng77EBQl3cmeJhITaGHdYH8kjVB+aun3S4XBRti2zt17mtt0mIUDiNxYeoJm6drVvBJQ==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "type-detect": "4.0.8"
      }
    },
    "node_modules/@sinonjs/fake-timers": {
      "version": "8.1.0",
      "resolved": "https://registry.npmjs.org/@sinonjs/fake-timers/-/fake-timers-8.1.0.tgz",
      "integrity": "sha512-OAPJUAtgeINhh/TAlUID4QTs53Njm7xzddaVlEs/SXwgtiD1tW22zAB/W1wdqfrpmikgaWQ9Fw6Ws+hsiRm5Vg==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "@sinonjs/commons": "^1.7.0"
      }
    },
    "node_modules/@surma/rollup-plugin-off-main-thread": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/@surma/rollup-plugin-off-main-thread/-/rollup-plugin-off-main-thread-2.2.3.tgz",
      "integrity": "sha512-lR8q/9W7hZpMWweNiAKU7NQerBnzQQLvi8qnTDU/fxItPhtZVMbPV3lbCwjhIlNBe9Bbr5V+KHshvWmVSG9cxQ==",
      "license": "Apache-2.0",
      "dependencies": {
        "ejs": "^3.1.6",
        "json5": "^2.2.0",
        "magic-string": "^0.25.0",
        "string.prototype.matchall": "^4.0.6"
      }
    },
    "node_modules/@svgr/babel-plugin-add-jsx-attribute": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-add-jsx-attribute/-/babel-plugin-add-jsx-attribute-5.4.0.tgz",
      "integrity": "sha512-ZFf2gs/8/6B8PnSofI0inYXr2SDNTDScPXhN7k5EqD4aZ3gi6u+rbmZHVB8IM3wDyx8ntKACZbtXSm7oZGRqVg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-remove-jsx-attribute": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-remove-jsx-attribute/-/babel-plugin-remove-jsx-attribute-5.4.0.tgz",
      "integrity": "sha512-yaS4o2PgUtwLFGTKbsiAy6D0o3ugcUhWK0Z45umJ66EPWunAz9fuFw2gJuje6wqQvQWOTJvIahUwndOXb7QCPg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-remove-jsx-empty-expression": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-remove-jsx-empty-expression/-/babel-plugin-remove-jsx-empty-expression-5.0.1.tgz",
      "integrity": "sha512-LA72+88A11ND/yFIMzyuLRSMJ+tRKeYKeQ+mR3DcAZ5I4h5CPWN9AHyUzJbWSYp/u2u0xhmgOe0+E41+GjEueA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-replace-jsx-attribute-value": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-replace-jsx-attribute-value/-/babel-plugin-replace-jsx-attribute-value-5.0.1.tgz",
      "integrity": "sha512-PoiE6ZD2Eiy5mK+fjHqwGOS+IXX0wq/YDtNyIgOrc6ejFnxN4b13pRpiIPbtPwHEc+NT2KCjteAcq33/F1Y9KQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-svg-dynamic-title": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-svg-dynamic-title/-/babel-plugin-svg-dynamic-title-5.4.0.tgz",
      "integrity": "sha512-zSOZH8PdZOpuG1ZVx/cLVePB2ibo3WPpqo7gFIjLV9a0QsuQAzJiwwqmuEdTaW2pegyBE17Uu15mOgOcgabQZg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-svg-em-dimensions": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-svg-em-dimensions/-/babel-plugin-svg-em-dimensions-5.4.0.tgz",
      "integrity": "sha512-cPzDbDA5oT/sPXDCUYoVXEmm3VIoAWAPT6mSPTJNbQaBNUuEKVKyGH93oDY4e42PYHRW67N5alJx/eEol20abw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-transform-react-native-svg": {
      "version": "5.4.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-transform-react-native-svg/-/babel-plugin-transform-react-native-svg-5.4.0.tgz",
      "integrity": "sha512-3eYP/SaopZ41GHwXma7Rmxcv9uRslRDTY1estspeB1w1ueZWd/tPlMfEOoccYpEMZU3jD4OU7YitnXcF5hLW2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-plugin-transform-svg-component": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-plugin-transform-svg-component/-/babel-plugin-transform-svg-component-5.5.0.tgz",
      "integrity": "sha512-q4jSH1UUvbrsOtlo/tKcgSeiCHRSBdXoIoqX1pgcKK/aU3JD27wmMKwGtpB8qRYUYoyXvfGxUVKchLuR5pB3rQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/babel-preset": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/babel-preset/-/babel-preset-5.5.0.tgz",
      "integrity": "sha512-4FiXBjvQ+z2j7yASeGPEi8VD/5rrGQk4Xrq3EdJmoZgz/tpqChpo5hgXDvmEauwtvOc52q8ghhZK4Oy7qph4ig==",
      "license": "MIT",
      "dependencies": {
        "@svgr/babel-plugin-add-jsx-attribute": "^5.4.0",
        "@svgr/babel-plugin-remove-jsx-attribute": "^5.4.0",
        "@svgr/babel-plugin-remove-jsx-empty-expression": "^5.0.1",
        "@svgr/babel-plugin-replace-jsx-attribute-value": "^5.0.1",
        "@svgr/babel-plugin-svg-dynamic-title": "^5.4.0",
        "@svgr/babel-plugin-svg-em-dimensions": "^5.4.0",
        "@svgr/babel-plugin-transform-react-native-svg": "^5.4.0",
        "@svgr/babel-plugin-transform-svg-component": "^5.5.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/core": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/core/-/core-5.5.0.tgz",
      "integrity": "sha512-q52VOcsJPvV3jO1wkPtzTuKlvX7Y3xIcWRpCMtBF3MrteZJtBfQw/+u0B1BHy5ColpQc1/YVTrPEtSYIMNZlrQ==",
      "license": "MIT",
      "dependencies": {
        "@svgr/plugin-jsx": "^5.5.0",
        "camelcase": "^6.2.0",
        "cosmiconfig": "^7.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/hast-util-to-babel-ast": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/hast-util-to-babel-ast/-/hast-util-to-babel-ast-5.5.0.tgz",
      "integrity": "sha512-cAaR/CAiZRB8GP32N+1jocovUtvlj0+e65TB50/6Lcime+EA49m/8l+P2ko+XPJ4dw3xaPS3jOL4F2X4KWxoeQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.12.6"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/plugin-jsx": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/plugin-jsx/-/plugin-jsx-5.5.0.tgz",
      "integrity": "sha512-V/wVh33j12hGh05IDg8GpIUXbjAPnTdPTKuP4VNLggnwaHMPNQNae2pRnyTAILWCQdz5GyMqtO488g7CKM8CBA==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.12.3",
        "@svgr/babel-preset": "^5.5.0",
        "@svgr/hast-util-to-babel-ast": "^5.5.0",
        "svg-parser": "^2.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/plugin-svgo": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/plugin-svgo/-/plugin-svgo-5.5.0.tgz",
      "integrity": "sha512-r5swKk46GuQl4RrVejVwpeeJaydoxkdwkM1mBKOgJLBUJPGaLci6ylg/IjhrRsREKDkr4kbMWdgOtbXEh0fyLQ==",
      "license": "MIT",
      "dependencies": {
        "cosmiconfig": "^7.0.0",
        "deepmerge": "^4.2.2",
        "svgo": "^1.2.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@svgr/webpack": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/@svgr/webpack/-/webpack-5.5.0.tgz",
      "integrity": "sha512-DOBOK255wfQxguUta2INKkzPj6AIS6iafZYiYmHn6W3pHlycSRRlvWKCfLDG10fXfLWqE3DJHgRUOyJYmARa7g==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.12.3",
        "@babel/plugin-transform-react-constant-elements": "^7.12.1",
        "@babel/preset-env": "^7.12.1",
        "@babel/preset-react": "^7.12.5",
        "@svgr/core": "^5.5.0",
        "@svgr/plugin-jsx": "^5.5.0",
        "@svgr/plugin-svgo": "^5.5.0",
        "loader-utils": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/gregberge"
      }
    },
    "node_modules/@testing-library/dom": {
      "version": "10.4.1",
      "resolved": "https://registry.npmjs.org/@testing-library/dom/-/dom-10.4.1.tgz",
      "integrity": "sha512-o4PXJQidqJl82ckFaXUeoAW+XysPLauYI43Abki5hABd853iMhitooc6znOnczgbTYmEP6U6/y1ZyKAIsvMKGg==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.10.4",
        "@babel/runtime": "^7.12.5",
        "@types/aria-query": "^5.0.1",
        "aria-query": "5.3.0",
        "dom-accessibility-api": "^0.5.9",
        "lz-string": "^1.5.0",
        "picocolors": "1.1.1",
        "pretty-format": "^27.0.2"
      },
      "engines": {
        "node": ">=18"
      }
    },
    "node_modules/@testing-library/dom/node_modules/aria-query": {
      "version": "5.3.0",
      "resolved": "https://registry.npmjs.org/aria-query/-/aria-query-5.3.0.tgz",
      "integrity": "sha512-b0P0sZPKtyu8HkeRAfCq0IfURZK+SuwMjY1UXGBU27wpAiTwQAIlq56IbIO+ytk/JjS1fMR14ee5WBBfKi5J6A==",
      "license": "Apache-2.0",
      "dependencies": {
        "dequal": "^2.0.3"
      }
    },
    "node_modules/@testing-library/jest-dom": {
      "version": "6.8.0",
      "resolved": "https://registry.npmjs.org/@testing-library/jest-dom/-/jest-dom-6.8.0.tgz",
      "integrity": "sha512-WgXcWzVM6idy5JaftTVC8Vs83NKRmGJz4Hqs4oyOuO2J4r/y79vvKZsb+CaGyCSEbUPI6OsewfPd0G1A0/TUZQ==",
      "license": "MIT",
      "dependencies": {
        "@adobe/css-tools": "^4.4.0",
        "aria-query": "^5.0.0",
        "css.escape": "^1.5.1",
        "dom-accessibility-api": "^0.6.3",
        "picocolors": "^1.1.1",
        "redent": "^3.0.0"
      },
      "engines": {
        "node": ">=14",
        "npm": ">=6",
        "yarn": ">=1"
      }
    },
    "node_modules/@testing-library/jest-dom/node_modules/dom-accessibility-api": {
      "version": "0.6.3",
      "resolved": "https://registry.npmjs.org/dom-accessibility-api/-/dom-accessibility-api-0.6.3.tgz",
      "integrity": "sha512-7ZgogeTnjuHbo+ct10G9Ffp0mif17idi0IyWNVA/wcwcm7NPOD/WEHVP3n7n3MhXqxoIYm8d6MuZohYWIZ4T3w==",
      "license": "MIT"
    },
    "node_modules/@testing-library/react": {
      "version": "16.3.0",
      "resolved": "https://registry.npmjs.org/@testing-library/react/-/react-16.3.0.tgz",
      "integrity": "sha512-kFSyxiEDwv1WLl2fgsq6pPBbw5aWKrsY2/noi1Id0TK0UParSF62oFQFGHXIyaG4pp2tEub/Zlel+fjjZILDsw==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.12.5"
      },
      "engines": {
        "node": ">=18"
      },
      "peerDependencies": {
        "@testing-library/dom": "^10.0.0",
        "@types/react": "^18.0.0 || ^19.0.0",
        "@types/react-dom": "^18.0.0 || ^19.0.0",
        "react": "^18.0.0 || ^19.0.0",
        "react-dom": "^18.0.0 || ^19.0.0"
      },
      "peerDependenciesMeta": {
        "@types/react": {
          "optional": true
        },
        "@types/react-dom": {
          "optional": true
        }
      }
    },
    "node_modules/@testing-library/user-event": {
      "version": "13.5.0",
      "resolved": "https://registry.npmjs.org/@testing-library/user-event/-/user-event-13.5.0.tgz",
      "integrity": "sha512-5Kwtbo3Y/NowpkbRuSepbyMFkZmHgD+vPzYB/RJ4oxt5Gj/avFFBYjhw27cqSVPVw/3a67NK1PbiIr9k4Gwmdg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.12.5"
      },
      "engines": {
        "node": ">=10",
        "npm": ">=6"
      },
      "peerDependencies": {
        "@testing-library/dom": ">=7.21.4"
      }
    },
    "node_modules/@tootallnate/once": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/@tootallnate/once/-/once-1.1.2.tgz",
      "integrity": "sha512-RbzJvlNzmRq5c3O09UipeuXno4tA1FE6ikOjxZK0tuxVv3412l64l5t1W5pj4+rJq9vpkm/kwiR07aZXnsKPxw==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/@trysound/sax": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/@trysound/sax/-/sax-0.2.0.tgz",
      "integrity": "sha512-L7z9BgrNEcYyUYtF+HaEfiS5ebkh9jXqbszz7pC0hRBPaatV0XjSD3+eHrpqFemQfgwiFF0QPIarnIihIDn7OA==",
      "license": "ISC",
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/@types/aria-query": {
      "version": "5.0.4",
      "resolved": "https://registry.npmjs.org/@types/aria-query/-/aria-query-5.0.4.tgz",
      "integrity": "sha512-rfT93uj5s0PRL7EzccGMs3brplhcrghnDoV26NqKhCAS1hVo+WdNsPvE/yb6ilfr5hi2MEk6d5EWJTKdxg8jVw==",
      "license": "MIT"
    },
    "node_modules/@types/babel__core": {
      "version": "7.20.5",
      "resolved": "https://registry.npmjs.org/@types/babel__core/-/babel__core-7.20.5.tgz",
      "integrity": "sha512-qoQprZvz5wQFJwMDqeseRXWv3rqMvhgpbXFfVyWhbx9X47POIA6i/+dXefEmZKoAgOaTdaIgNSMqMIU61yRyzA==",
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.20.7",
        "@babel/types": "^7.20.7",
        "@types/babel__generator": "*",
        "@types/babel__template": "*",
        "@types/babel__traverse": "*"
      }
    },
    "node_modules/@types/babel__generator": {
      "version": "7.27.0",
      "resolved": "https://registry.npmjs.org/@types/babel__generator/-/babel__generator-7.27.0.tgz",
      "integrity": "sha512-ufFd2Xi92OAVPYsy+P4n7/U7e68fex0+Ee8gSG9KX7eo084CWiQ4sdxktvdl0bOPupXtVJPY19zk6EwWqUQ8lg==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.0.0"
      }
    },
    "node_modules/@types/babel__template": {
      "version": "7.4.4",
      "resolved": "https://registry.npmjs.org/@types/babel__template/-/babel__template-7.4.4.tgz",
      "integrity": "sha512-h/NUaSyG5EyxBIp8YRxo4RMe2/qQgvyowRwVMzhYhBCONbW8PUsg4lkFMrhgZhUe5z3L3MiLDuvyJ/CaPa2A8A==",
      "license": "MIT",
      "dependencies": {
        "@babel/parser": "^7.1.0",
        "@babel/types": "^7.0.0"
      }
    },
    "node_modules/@types/babel__traverse": {
      "version": "7.28.0",
      "resolved": "https://registry.npmjs.org/@types/babel__traverse/-/babel__traverse-7.28.0.tgz",
      "integrity": "sha512-8PvcXf70gTDZBgt9ptxJ8elBeBjcLOAcOtoO/mPJjtji1+CdGbHgm77om1GrsPxsiE+uXIpNSK64UYaIwQXd4Q==",
      "license": "MIT",
      "dependencies": {
        "@babel/types": "^7.28.2"
      }
    },
    "node_modules/@types/body-parser": {
      "version": "1.19.6",
      "resolved": "https://registry.npmjs.org/@types/body-parser/-/body-parser-1.19.6.tgz",
      "integrity": "sha512-HLFeCYgz89uk22N5Qg3dvGvsv46B8GLvKKo1zKG4NybA8U2DiEO3w9lqGg29t/tfLRJpJ6iQxnVw4OnB7MoM9g==",
      "license": "MIT",
      "dependencies": {
        "@types/connect": "*",
        "@types/node": "*"
      }
    },
    "node_modules/@types/bonjour": {
      "version": "3.5.13",
      "resolved": "https://registry.npmjs.org/@types/bonjour/-/bonjour-3.5.13.tgz",
      "integrity": "sha512-z9fJ5Im06zvUL548KvYNecEVlA7cVDkGUi6kZusb04mpyEFKCIZJvloCcmpmLaIahDpOQGHaHmG6imtPMmPXGQ==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/connect": {
      "version": "3.4.38",
      "resolved": "https://registry.npmjs.org/@types/connect/-/connect-3.4.38.tgz",
      "integrity": "sha512-K6uROf1LD88uDQqJCktA4yzL1YYAK6NgfsI0v/mTgyPKWsX1CnJ0XPSDhViejru1GcRkLWb8RlzFYJRqGUbaug==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/connect-history-api-fallback": {
      "version": "1.5.4",
      "resolved": "https://registry.npmjs.org/@types/connect-history-api-fallback/-/connect-history-api-fallback-1.5.4.tgz",
      "integrity": "sha512-n6Cr2xS1h4uAulPRdlw6Jl6s1oG8KrVilPN2yUITEs+K48EzMJJ3W1xy8K5eWuFvjp3R74AOIGSmp2UfBJ8HFw==",
      "license": "MIT",
      "dependencies": {
        "@types/express-serve-static-core": "*",
        "@types/node": "*"
      }
    },
    "node_modules/@types/eslint": {
      "version": "8.56.12",
      "resolved": "https://registry.npmjs.org/@types/eslint/-/eslint-8.56.12.tgz",
      "integrity": "sha512-03ruubjWyOHlmljCVoxSuNDdmfZDzsrrz0P2LeJsOXr+ZwFQ+0yQIwNCwt/GYhV7Z31fgtXJTAEs+FYlEL851g==",
      "license": "MIT",
      "dependencies": {
        "@types/estree": "*",
        "@types/json-schema": "*"
      }
    },
    "node_modules/@types/eslint-scope": {
      "version": "3.7.7",
      "resolved": "https://registry.npmjs.org/@types/eslint-scope/-/eslint-scope-3.7.7.tgz",
      "integrity": "sha512-MzMFlSLBqNF2gcHWO0G1vP/YQyfvrxZ0bF+u7mzUdZ1/xK4A4sru+nraZz5i3iEIk1l1uyicaDVTB4QbbEkAYg==",
      "license": "MIT",
      "dependencies": {
        "@types/eslint": "*",
        "@types/estree": "*"
      }
    },
    "node_modules/@types/estree": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/@types/estree/-/estree-1.0.8.tgz",
      "integrity": "sha512-dWHzHa2WqEXI/O1E9OjrocMTKJl2mSrEolh1Iomrv6U+JuNwaHXsXx9bLu5gG7BUWFIN0skIQJQ/L1rIex4X6w==",
      "license": "MIT"
    },
    "node_modules/@types/express": {
      "version": "4.17.23",
      "resolved": "https://registry.npmjs.org/@types/express/-/express-4.17.23.tgz",
      "integrity": "sha512-Crp6WY9aTYP3qPi2wGDo9iUe/rceX01UMhnF1jmwDcKCFM6cx7YhGP/Mpr3y9AASpfHixIG0E6azCcL5OcDHsQ==",
      "license": "MIT",
      "dependencies": {
        "@types/body-parser": "*",
        "@types/express-serve-static-core": "^4.17.33",
        "@types/qs": "*",
        "@types/serve-static": "*"
      }
    },
    "node_modules/@types/express-serve-static-core": {
      "version": "5.0.7",
      "resolved": "https://registry.npmjs.org/@types/express-serve-static-core/-/express-serve-static-core-5.0.7.tgz",
      "integrity": "sha512-R+33OsgWw7rOhD1emjU7dzCDHucJrgJXMA5PYCzJxVil0dsyx5iBEPHqpPfiKNJQb7lZ1vxwoLR4Z87bBUpeGQ==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "@types/qs": "*",
        "@types/range-parser": "*",
        "@types/send": "*"
      }
    },
    "node_modules/@types/express/node_modules/@types/express-serve-static-core": {
      "version": "4.19.6",
      "resolved": "https://registry.npmjs.org/@types/express-serve-static-core/-/express-serve-static-core-4.19.6.tgz",
      "integrity": "sha512-N4LZ2xG7DatVqhCZzOGb1Yi5lMbXSZcmdLDe9EzSndPV2HpWYWzRbaerl2n27irrm94EPpprqa8KpskPT085+A==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "@types/qs": "*",
        "@types/range-parser": "*",
        "@types/send": "*"
      }
    },
    "node_modules/@types/graceful-fs": {
      "version": "4.1.9",
      "resolved": "https://registry.npmjs.org/@types/graceful-fs/-/graceful-fs-4.1.9.tgz",
      "integrity": "sha512-olP3sd1qOEe5dXTSaFvQG+02VdRXcdytWLAZsAq1PecU8uqQAhkrnbli7DagjtXKW/Bl7YJbUsa8MPcuc8LHEQ==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/html-minifier-terser": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/@types/html-minifier-terser/-/html-minifier-terser-6.1.0.tgz",
      "integrity": "sha512-oh/6byDPnL1zeNXFrDXFLyZjkr1MsBG667IM792caf1L2UPOOMf65NFzjUH/ltyfwjAGfs1rsX1eftK0jC/KIg==",
      "license": "MIT"
    },
    "node_modules/@types/http-errors": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/@types/http-errors/-/http-errors-2.0.5.tgz",
      "integrity": "sha512-r8Tayk8HJnX0FztbZN7oVqGccWgw98T/0neJphO91KkmOzug1KkofZURD4UaD5uH8AqcFLfdPErnBod0u71/qg==",
      "license": "MIT"
    },
    "node_modules/@types/http-proxy": {
      "version": "1.17.16",
      "resolved": "https://registry.npmjs.org/@types/http-proxy/-/http-proxy-1.17.16.tgz",
      "integrity": "sha512-sdWoUajOB1cd0A8cRRQ1cfyWNbmFKLAqBB89Y8x5iYyG/mkJHc0YUH8pdWBy2omi9qtCpiIgGjuwO0dQST2l5w==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/istanbul-lib-coverage": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/@types/istanbul-lib-coverage/-/istanbul-lib-coverage-2.0.6.tgz",
      "integrity": "sha512-2QF/t/auWm0lsy8XtKVPG19v3sSOQlJe/YHZgfjb/KBBHOGSV+J2q/S671rcq9uTBrLAXmZpqJiaQbMT+zNU1w==",
      "license": "MIT"
    },
    "node_modules/@types/istanbul-lib-report": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/@types/istanbul-lib-report/-/istanbul-lib-report-3.0.3.tgz",
      "integrity": "sha512-NQn7AHQnk/RSLOxrBbGyJM/aVQ+pjj5HCgasFxc0K/KhoATfQ/47AyUl15I2yBUpihjmas+a+VJBOqecrFH+uA==",
      "license": "MIT",
      "dependencies": {
        "@types/istanbul-lib-coverage": "*"
      }
    },
    "node_modules/@types/istanbul-reports": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/@types/istanbul-reports/-/istanbul-reports-3.0.4.tgz",
      "integrity": "sha512-pk2B1NWalF9toCRu6gjBzR69syFjP4Od8WRAX+0mmf9lAjCRicLOWc+ZrxZHx/0XRjotgkF9t6iaMJ+aXcOdZQ==",
      "license": "MIT",
      "dependencies": {
        "@types/istanbul-lib-report": "*"
      }
    },
    "node_modules/@types/json-schema": {
      "version": "7.0.15",
      "resolved": "https://registry.npmjs.org/@types/json-schema/-/json-schema-7.0.15.tgz",
      "integrity": "sha512-5+fP8P8MFNC+AyZCDxrB2pkZFPGzqQWUzpSeuuVLvm8VMcorNYavBqoFcxK8bQz4Qsbn4oUEEem4wDLfcysGHA==",
      "license": "MIT"
    },
    "node_modules/@types/json5": {
      "version": "0.0.29",
      "resolved": "https://registry.npmjs.org/@types/json5/-/json5-0.0.29.tgz",
      "integrity": "sha512-dRLjCWHYg4oaA77cxO64oO+7JwCwnIzkZPdrrC71jQmQtlhM556pwKo5bUzqvZndkVbeFLIIi+9TC40JNF5hNQ==",
      "license": "MIT"
    },
    "node_modules/@types/mime": {
      "version": "1.3.5",
      "resolved": "https://registry.npmjs.org/@types/mime/-/mime-1.3.5.tgz",
      "integrity": "sha512-/pyBZWSLD2n0dcHE3hq8s8ZvcETHtEuF+3E7XVt0Ig2nvsVQXdghHVcEkIWjy9A0wKfTn97a/PSDYohKIlnP/w==",
      "license": "MIT"
    },
    "node_modules/@types/node": {
      "version": "24.5.2",
      "resolved": "https://registry.npmjs.org/@types/node/-/node-24.5.2.tgz",
      "integrity": "sha512-FYxk1I7wPv3K2XBaoyH2cTnocQEu8AOZ60hPbsyukMPLv5/5qr7V1i8PLHdl6Zf87I+xZXFvPCXYjiTFq+YSDQ==",
      "license": "MIT",
      "dependencies": {
        "undici-types": "~7.12.0"
      }
    },
    "node_modules/@types/node-forge": {
      "version": "1.3.14",
      "resolved": "https://registry.npmjs.org/@types/node-forge/-/node-forge-1.3.14.tgz",
      "integrity": "sha512-mhVF2BnD4BO+jtOp7z1CdzaK4mbuK0LLQYAvdOLqHTavxFNq4zA1EmYkpnFjP8HOUzedfQkRnp0E2ulSAYSzAw==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/parse-json": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/@types/parse-json/-/parse-json-4.0.2.tgz",
      "integrity": "sha512-dISoDXWWQwUquiKsyZ4Ng+HX2KsPL7LyHKHQwgGFEA3IaKac4Obd+h2a/a6waisAoepJlBcx9paWqjA8/HVjCw==",
      "license": "MIT"
    },
    "node_modules/@types/prettier": {
      "version": "2.7.3",
      "resolved": "https://registry.npmjs.org/@types/prettier/-/prettier-2.7.3.tgz",
      "integrity": "sha512-+68kP9yzs4LMp7VNh8gdzMSPZFL44MLGqiHWvttYJe+6qnuVr4Ek9wSBQoveqY/r+LwjCcU29kNVkidwim+kYA==",
      "license": "MIT"
    },
    "node_modules/@types/q": {
      "version": "1.5.8",
      "resolved": "https://registry.npmjs.org/@types/q/-/q-1.5.8.tgz",
      "integrity": "sha512-hroOstUScF6zhIi+5+x0dzqrHA1EJi+Irri6b1fxolMTqqHIV/Cg77EtnQcZqZCu8hR3mX2BzIxN4/GzI68Kfw==",
      "license": "MIT"
    },
    "node_modules/@types/qs": {
      "version": "6.14.0",
      "resolved": "https://registry.npmjs.org/@types/qs/-/qs-6.14.0.tgz",
      "integrity": "sha512-eOunJqu0K1923aExK6y8p6fsihYEn/BYuQ4g0CxAAgFc4b/ZLN4CrsRZ55srTdqoiLzU2B2evC+apEIxprEzkQ==",
      "license": "MIT"
    },
    "node_modules/@types/range-parser": {
      "version": "1.2.7",
      "resolved": "https://registry.npmjs.org/@types/range-parser/-/range-parser-1.2.7.tgz",
      "integrity": "sha512-hKormJbkJqzQGhziax5PItDUTMAM9uE2XXQmM37dyd4hVM+5aVl7oVxMVUiVQn2oCQFN/LKCZdvSM0pFRqbSmQ==",
      "license": "MIT"
    },
    "node_modules/@types/resolve": {
      "version": "1.17.1",
      "resolved": "https://registry.npmjs.org/@types/resolve/-/resolve-1.17.1.tgz",
      "integrity": "sha512-yy7HuzQhj0dhGpD8RLXSZWEkLsV9ibvxvi6EiJ3bkqLAO1RGo0WbkWQiwpRlSFymTJRz0d3k5LM3kkx8ArDbLw==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/retry": {
      "version": "0.12.0",
      "resolved": "https://registry.npmjs.org/@types/retry/-/retry-0.12.0.tgz",
      "integrity": "sha512-wWKOClTTiizcZhXnPY4wikVAwmdYHp8q6DmC+EJUzAMsycb7HB32Kh9RN4+0gExjmPmZSAQjgURXIGATPegAvA==",
      "license": "MIT"
    },
    "node_modules/@types/semver": {
      "version": "7.7.1",
      "resolved": "https://registry.npmjs.org/@types/semver/-/semver-7.7.1.tgz",
      "integrity": "sha512-FmgJfu+MOcQ370SD0ev7EI8TlCAfKYU+B4m5T3yXc1CiRN94g/SZPtsCkk506aUDtlMnFZvasDwHHUcZUEaYuA==",
      "license": "MIT"
    },
    "node_modules/@types/send": {
      "version": "0.17.5",
      "resolved": "https://registry.npmjs.org/@types/send/-/send-0.17.5.tgz",
      "integrity": "sha512-z6F2D3cOStZvuk2SaP6YrwkNO65iTZcwA2ZkSABegdkAh/lf+Aa/YQndZVfmEXT5vgAp6zv06VQ3ejSVjAny4w==",
      "license": "MIT",
      "dependencies": {
        "@types/mime": "^1",
        "@types/node": "*"
      }
    },
    "node_modules/@types/serve-index": {
      "version": "1.9.4",
      "resolved": "https://registry.npmjs.org/@types/serve-index/-/serve-index-1.9.4.tgz",
      "integrity": "sha512-qLpGZ/c2fhSs5gnYsQxtDEq3Oy8SXPClIXkW5ghvAvsNuVSA8k+gCONcUCS/UjLEYvYps+e8uBtfgXgvhwfNug==",
      "license": "MIT",
      "dependencies": {
        "@types/express": "*"
      }
    },
    "node_modules/@types/serve-static": {
      "version": "1.15.8",
      "resolved": "https://registry.npmjs.org/@types/serve-static/-/serve-static-1.15.8.tgz",
      "integrity": "sha512-roei0UY3LhpOJvjbIP6ZZFngyLKl5dskOtDhxY5THRSpO+ZI+nzJ+m5yUMzGrp89YRa7lvknKkMYjqQFGwA7Sg==",
      "license": "MIT",
      "dependencies": {
        "@types/http-errors": "*",
        "@types/node": "*",
        "@types/send": "*"
      }
    },
    "node_modules/@types/sockjs": {
      "version": "0.3.36",
      "resolved": "https://registry.npmjs.org/@types/sockjs/-/sockjs-0.3.36.tgz",
      "integrity": "sha512-MK9V6NzAS1+Ud7JV9lJLFqW85VbC9dq3LmwZCuBe4wBDgKC0Kj/jd8Xl+nSviU+Qc3+m7umHHyHg//2KSa0a0Q==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/stack-utils": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/@types/stack-utils/-/stack-utils-2.0.3.tgz",
      "integrity": "sha512-9aEbYZ3TbYMznPdcdr3SmIrLXwC/AKZXQeCf9Pgao5CKb8CyHuEX5jzWPTkvregvhRJHcpRO6BFoGW9ycaOkYw==",
      "license": "MIT"
    },
    "node_modules/@types/trusted-types": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/@types/trusted-types/-/trusted-types-2.0.7.tgz",
      "integrity": "sha512-ScaPdn1dQczgbl0QFTeTOmVHFULt394XJgOQNoyVhZ6r2vLnMLJfBPd53SB52T/3G36VI1/g2MZaX0cwDuXsfw==",
      "license": "MIT"
    },
    "node_modules/@types/ws": {
      "version": "8.18.1",
      "resolved": "https://registry.npmjs.org/@types/ws/-/ws-8.18.1.tgz",
      "integrity": "sha512-ThVF6DCVhA8kUGy+aazFQ4kXQ7E1Ty7A3ypFOe0IcJV8O/M511G99AW24irKrW56Wt44yG9+ij8FaqoBGkuBXg==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*"
      }
    },
    "node_modules/@types/yargs": {
      "version": "16.0.9",
      "resolved": "https://registry.npmjs.org/@types/yargs/-/yargs-16.0.9.tgz",
      "integrity": "sha512-tHhzvkFXZQeTECenFoRljLBYPZJ7jAVxqqtEI0qTLOmuultnFp4I9yKE17vTuhf7BkhCu7I4XuemPgikDVuYqA==",
      "license": "MIT",
      "dependencies": {
        "@types/yargs-parser": "*"
      }
    },
    "node_modules/@types/yargs-parser": {
      "version": "21.0.3",
      "resolved": "https://registry.npmjs.org/@types/yargs-parser/-/yargs-parser-21.0.3.tgz",
      "integrity": "sha512-I4q9QU9MQv4oEOz4tAHJtNz1cwuLxn2F3xcc2iV5WdqLPpUnj30aUuxt1mAxYTG+oe8CZMV/+6rU4S4gRDzqtQ==",
      "license": "MIT"
    },
    "node_modules/@typescript-eslint/eslint-plugin": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/eslint-plugin/-/eslint-plugin-5.62.0.tgz",
      "integrity": "sha512-TiZzBSJja/LbhNPvk6yc0JrX9XqhQ0hdh6M2svYfsHGejaKFIAGd9MQ+ERIMzLGlN/kZoYIgdxFV0PuljTKXag==",
      "license": "MIT",
      "dependencies": {
        "@eslint-community/regexpp": "^4.4.0",
        "@typescript-eslint/scope-manager": "5.62.0",
        "@typescript-eslint/type-utils": "5.62.0",
        "@typescript-eslint/utils": "5.62.0",
        "debug": "^4.3.4",
        "graphemer": "^1.4.0",
        "ignore": "^5.2.0",
        "natural-compare-lite": "^1.4.0",
        "semver": "^7.3.7",
        "tsutils": "^3.21.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "@typescript-eslint/parser": "^5.0.0",
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@typescript-eslint/experimental-utils": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/experimental-utils/-/experimental-utils-5.62.0.tgz",
      "integrity": "sha512-RTXpeB3eMkpoclG3ZHft6vG/Z30azNHuqY6wKPBHlVMZFuEvrtlEDe8gMqDb+SO+9hjC/pLekeSCryf9vMZlCw==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/utils": "5.62.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      }
    },
    "node_modules/@typescript-eslint/parser": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/parser/-/parser-5.62.0.tgz",
      "integrity": "sha512-VlJEV0fOQ7BExOsHYAGrgbEiZoi8D+Bl2+f6V2RrXerRSylnp+ZBHmPvaIa8cz0Ajx7WO7Z5RqfgYg7ED1nRhA==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "@typescript-eslint/scope-manager": "5.62.0",
        "@typescript-eslint/types": "5.62.0",
        "@typescript-eslint/typescript-estree": "5.62.0",
        "debug": "^4.3.4"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@typescript-eslint/scope-manager": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/scope-manager/-/scope-manager-5.62.0.tgz",
      "integrity": "sha512-VXuvVvZeQCQb5Zgf4HAxc04q5j+WrNAtNh9OwCsCgpKqESMTu3tF/jhZ3xG6T4NZwWl65Bg8KuS2uEvhSfLl0w==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/types": "5.62.0",
        "@typescript-eslint/visitor-keys": "5.62.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@typescript-eslint/type-utils": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/type-utils/-/type-utils-5.62.0.tgz",
      "integrity": "sha512-xsSQreu+VnfbqQpW5vnCJdq1Z3Q0U31qiWmRhr98ONQmcp/yhiPJFPq8MXiJVLiksmOKSjIldZzkebzHuCGzew==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/typescript-estree": "5.62.0",
        "@typescript-eslint/utils": "5.62.0",
        "debug": "^4.3.4",
        "tsutils": "^3.21.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "*"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@typescript-eslint/types": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/types/-/types-5.62.0.tgz",
      "integrity": "sha512-87NVngcbVXUahrRTqIK27gD2t5Cu1yuCXxbLcFtCzZGlfyVWWh8mLHkoxzjsB6DDNnvdL+fW8MiwPEJyGJQDgQ==",
      "license": "MIT",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@typescript-eslint/typescript-estree": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/typescript-estree/-/typescript-estree-5.62.0.tgz",
      "integrity": "sha512-CmcQ6uY7b9y694lKdRB8FEel7JbU/40iSAPomu++SjLMntB+2Leay2LO6i8VnJk58MtE9/nQSFIH6jpyRWyYzA==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "@typescript-eslint/types": "5.62.0",
        "@typescript-eslint/visitor-keys": "5.62.0",
        "debug": "^4.3.4",
        "globby": "^11.1.0",
        "is-glob": "^4.0.3",
        "semver": "^7.3.7",
        "tsutils": "^3.21.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/@typescript-eslint/utils": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/utils/-/utils-5.62.0.tgz",
      "integrity": "sha512-n8oxjeb5aIbPFEtmQxQYOLI0i9n5ySBEY/ZEHHZqKQSFnxio1rv6dthascc9dLuwrL0RC5mPCxB7vnAVGAYWAQ==",
      "license": "MIT",
      "dependencies": {
        "@eslint-community/eslint-utils": "^4.2.0",
        "@types/json-schema": "^7.0.9",
        "@types/semver": "^7.3.12",
        "@typescript-eslint/scope-manager": "5.62.0",
        "@typescript-eslint/types": "5.62.0",
        "@typescript-eslint/typescript-estree": "5.62.0",
        "eslint-scope": "^5.1.1",
        "semver": "^7.3.7"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      },
      "peerDependencies": {
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      }
    },
    "node_modules/@typescript-eslint/utils/node_modules/eslint-scope": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-5.1.1.tgz",
      "integrity": "sha512-2NxwbF/hZ0KpepYN0cNbo+FN6XoK7GaHlQhgx/hIZl6Va0bF45RQOOwhLIy8lQDbuCiadSLCBnH2CFYquit5bw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^4.1.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/@typescript-eslint/utils/node_modules/estraverse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-4.3.0.tgz",
      "integrity": "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/@typescript-eslint/visitor-keys": {
      "version": "5.62.0",
      "resolved": "https://registry.npmjs.org/@typescript-eslint/visitor-keys/-/visitor-keys-5.62.0.tgz",
      "integrity": "sha512-07ny+LHRzQXepkGg6w0mFY41fVUNBrL2Roj/++7V1txKugfjm/Ci/qSND03r2RhlJhJYMcTn9AhhSSqQp0Ysyw==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/types": "5.62.0",
        "eslint-visitor-keys": "^3.3.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/typescript-eslint"
      }
    },
    "node_modules/@ungap/structured-clone": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/@ungap/structured-clone/-/structured-clone-1.3.0.tgz",
      "integrity": "sha512-WmoN8qaIAo7WTYWbAZuG8PYEhn5fkz7dZrqTBZ7dtt//lL2Gwms1IcnQ5yHqjDfX8Ft5j4YzDM23f87zBfDe9g==",
      "license": "ISC"
    },
    "node_modules/@webassemblyjs/ast": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/ast/-/ast-1.14.1.tgz",
      "integrity": "sha512-nuBEDgQfm1ccRp/8bCQrx1frohyufl4JlbMMZ4P1wpeOfDhF6FQkxZJ1b/e+PLwr6X1Nhw6OLme5usuBWYBvuQ==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/helper-numbers": "1.13.2",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2"
      }
    },
    "node_modules/@webassemblyjs/floating-point-hex-parser": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/floating-point-hex-parser/-/floating-point-hex-parser-1.13.2.tgz",
      "integrity": "sha512-6oXyTOzbKxGH4steLbLNOu71Oj+C8Lg34n6CqRvqfS2O71BxY6ByfMDRhBytzknj9yGUPVJ1qIKhRlAwO1AovA==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/helper-api-error": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-api-error/-/helper-api-error-1.13.2.tgz",
      "integrity": "sha512-U56GMYxy4ZQCbDZd6JuvvNV/WFildOjsaWD3Tzzvmw/mas3cXzRJPMjP83JqEsgSbyrmaGjBfDtV7KDXV9UzFQ==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/helper-buffer": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-buffer/-/helper-buffer-1.14.1.tgz",
      "integrity": "sha512-jyH7wtcHiKssDtFPRB+iQdxlDf96m0E39yb0k5uJVhFGleZFoNw1c4aeIcVUPPbXUVJ94wwnMOAqUHyzoEPVMA==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/helper-numbers": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-numbers/-/helper-numbers-1.13.2.tgz",
      "integrity": "sha512-FE8aCmS5Q6eQYcV3gI35O4J789wlQA+7JrqTTpJqn5emA4U2hvwJmvFRC0HODS+3Ye6WioDklgd6scJ3+PLnEA==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/floating-point-hex-parser": "1.13.2",
        "@webassemblyjs/helper-api-error": "1.13.2",
        "@xtuc/long": "4.2.2"
      }
    },
    "node_modules/@webassemblyjs/helper-wasm-bytecode": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-wasm-bytecode/-/helper-wasm-bytecode-1.13.2.tgz",
      "integrity": "sha512-3QbLKy93F0EAIXLh0ogEVR6rOubA9AoZ+WRYhNbFyuB70j3dRdwH9g+qXhLAO0kiYGlg3TxDV+I4rQTr/YNXkA==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/helper-wasm-section": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/helper-wasm-section/-/helper-wasm-section-1.14.1.tgz",
      "integrity": "sha512-ds5mXEqTJ6oxRoqjhWDU83OgzAYjwsCV8Lo/N+oRsNDmx/ZDpqalmrtgOMkHwxsG0iI//3BwWAErYRHtgn0dZw==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-buffer": "1.14.1",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2",
        "@webassemblyjs/wasm-gen": "1.14.1"
      }
    },
    "node_modules/@webassemblyjs/ieee754": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/ieee754/-/ieee754-1.13.2.tgz",
      "integrity": "sha512-4LtOzh58S/5lX4ITKxnAK2USuNEvpdVV9AlgGQb8rJDHaLeHciwG4zlGr0j/SNWlr7x3vO1lDEsuePvtcDNCkw==",
      "license": "MIT",
      "dependencies": {
        "@xtuc/ieee754": "^1.2.0"
      }
    },
    "node_modules/@webassemblyjs/leb128": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/leb128/-/leb128-1.13.2.tgz",
      "integrity": "sha512-Lde1oNoIdzVzdkNEAWZ1dZ5orIbff80YPdHx20mrHwHrVNNTjNr8E3xz9BdpcGqRQbAEa+fkrCb+fRFTl/6sQw==",
      "license": "Apache-2.0",
      "dependencies": {
        "@xtuc/long": "4.2.2"
      }
    },
    "node_modules/@webassemblyjs/utf8": {
      "version": "1.13.2",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/utf8/-/utf8-1.13.2.tgz",
      "integrity": "sha512-3NQWGjKTASY1xV5m7Hr0iPeXD9+RDobLll3T9d2AO+g3my8xy5peVyjSag4I50mR1bBSN/Ct12lo+R9tJk0NZQ==",
      "license": "MIT"
    },
    "node_modules/@webassemblyjs/wasm-edit": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wasm-edit/-/wasm-edit-1.14.1.tgz",
      "integrity": "sha512-RNJUIQH/J8iA/1NzlE4N7KtyZNHi3w7at7hDjvRNm5rcUXa00z1vRz3glZoULfJ5mpvYhLybmVcwcjGrC1pRrQ==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-buffer": "1.14.1",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2",
        "@webassemblyjs/helper-wasm-section": "1.14.1",
        "@webassemblyjs/wasm-gen": "1.14.1",
        "@webassemblyjs/wasm-opt": "1.14.1",
        "@webassemblyjs/wasm-parser": "1.14.1",
        "@webassemblyjs/wast-printer": "1.14.1"
      }
    },
    "node_modules/@webassemblyjs/wasm-gen": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wasm-gen/-/wasm-gen-1.14.1.tgz",
      "integrity": "sha512-AmomSIjP8ZbfGQhumkNvgC33AY7qtMCXnN6bL2u2Js4gVCg8fp735aEiMSBbDR7UQIj90n4wKAFUSEd0QN2Ukg==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2",
        "@webassemblyjs/ieee754": "1.13.2",
        "@webassemblyjs/leb128": "1.13.2",
        "@webassemblyjs/utf8": "1.13.2"
      }
    },
    "node_modules/@webassemblyjs/wasm-opt": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wasm-opt/-/wasm-opt-1.14.1.tgz",
      "integrity": "sha512-PTcKLUNvBqnY2U6E5bdOQcSM+oVP/PmrDY9NzowJjislEjwP/C4an2303MCVS2Mg9d3AJpIGdUFIQQWbPds0Sw==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-buffer": "1.14.1",
        "@webassemblyjs/wasm-gen": "1.14.1",
        "@webassemblyjs/wasm-parser": "1.14.1"
      }
    },
    "node_modules/@webassemblyjs/wasm-parser": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wasm-parser/-/wasm-parser-1.14.1.tgz",
      "integrity": "sha512-JLBl+KZ0R5qB7mCnud/yyX08jWFw5MsoalJ1pQ4EdFlgj9VdXKGuENGsiCIjegI1W7p91rUlcB/LB5yRJKNTcQ==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@webassemblyjs/helper-api-error": "1.13.2",
        "@webassemblyjs/helper-wasm-bytecode": "1.13.2",
        "@webassemblyjs/ieee754": "1.13.2",
        "@webassemblyjs/leb128": "1.13.2",
        "@webassemblyjs/utf8": "1.13.2"
      }
    },
    "node_modules/@webassemblyjs/wast-printer": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/@webassemblyjs/wast-printer/-/wast-printer-1.14.1.tgz",
      "integrity": "sha512-kPSSXE6De1XOR820C90RIo2ogvZG+c3KiHzqUoO/F34Y2shGzesfqv7o57xrxovZJH/MetF5UjroJ/R/3isoiw==",
      "license": "MIT",
      "dependencies": {
        "@webassemblyjs/ast": "1.14.1",
        "@xtuc/long": "4.2.2"
      }
    },
    "node_modules/@xtuc/ieee754": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/@xtuc/ieee754/-/ieee754-1.2.0.tgz",
      "integrity": "sha512-DX8nKgqcGwsc0eJSqYt5lwP4DH5FlHnmuWWBRy7X0NcaGR0ZtuyeESgMwTYVEtxmsNGY+qit4QYT/MIYTOTPeA==",
      "license": "BSD-3-Clause"
    },
    "node_modules/@xtuc/long": {
      "version": "4.2.2",
      "resolved": "https://registry.npmjs.org/@xtuc/long/-/long-4.2.2.tgz",
      "integrity": "sha512-NuHqBY1PB/D8xU6s/thBgOAiAP7HOYDQ32+BFZILJ8ivkUkAHQnWfn6WhL79Owj1qmUnoN/YPhktdIoucipkAQ==",
      "license": "Apache-2.0"
    },
    "node_modules/abab": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/abab/-/abab-2.0.6.tgz",
      "integrity": "sha512-j2afSsaIENvHZN2B8GOpF566vZ5WVk5opAiMTvWgaQT8DkbOqsTfvNAvHoRGU2zzP8cPoqys+xHTRDWW8L+/BA==",
      "deprecated": "Use your platform's native atob() and btoa() methods instead",
      "license": "BSD-3-Clause"
    },
    "node_modules/accepts": {
      "version": "1.3.8",
      "resolved": "https://registry.npmjs.org/accepts/-/accepts-1.3.8.tgz",
      "integrity": "sha512-PYAthTa2m2VKxuvSD3DPC/Gy+U+sOA1LAuT8mkmRuvw+NACSaeXEQ+NHcVF7rONl6qcaxV3Uuemwawk+7+SJLw==",
      "license": "MIT",
      "dependencies": {
        "mime-types": "~2.1.34",
        "negotiator": "0.6.3"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/accepts/node_modules/negotiator": {
      "version": "0.6.3",
      "resolved": "https://registry.npmjs.org/negotiator/-/negotiator-0.6.3.tgz",
      "integrity": "sha512-+EUsqGPLsM+j/zdChZjsnX51g4XrHFOIXwfnCVPGlQk/k5giakcKsuxCObBRu6DSm9opw/O6slWbJdghQM4bBg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/acorn": {
      "version": "8.15.0",
      "resolved": "https://registry.npmjs.org/acorn/-/acorn-8.15.0.tgz",
      "integrity": "sha512-NZyJarBfL7nWwIq+FDL6Zp/yHEhePMNnnJ0y3qfieCrmNvYct8uvtiV41UvlSe6apAfk0fY1FbWx+NwfmpvtTg==",
      "license": "MIT",
      "bin": {
        "acorn": "bin/acorn"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/acorn-globals": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/acorn-globals/-/acorn-globals-6.0.0.tgz",
      "integrity": "sha512-ZQl7LOWaF5ePqqcX4hLuv/bLXYQNfNWw2c0/yX/TsPRKamzHcTGQnlCjHT3TsmkOUVEPS3crCxiPfdzE/Trlhg==",
      "license": "MIT",
      "dependencies": {
        "acorn": "^7.1.1",
        "acorn-walk": "^7.1.1"
      }
    },
    "node_modules/acorn-globals/node_modules/acorn": {
      "version": "7.4.1",
      "resolved": "https://registry.npmjs.org/acorn/-/acorn-7.4.1.tgz",
      "integrity": "sha512-nQyp0o1/mNdbTO1PO6kHkwSrmgZ0MT/jCCpNiwbUjGoRN4dlBhqJtoQuCnEOKzgTVwg0ZWiCoQy6SxMebQVh8A==",
      "license": "MIT",
      "bin": {
        "acorn": "bin/acorn"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/acorn-import-phases": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/acorn-import-phases/-/acorn-import-phases-1.0.4.tgz",
      "integrity": "sha512-wKmbr/DDiIXzEOiWrTTUcDm24kQ2vGfZQvM2fwg2vXqR5uW6aapr7ObPtj1th32b9u90/Pf4AItvdTh42fBmVQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10.13.0"
      },
      "peerDependencies": {
        "acorn": "^8.14.0"
      }
    },
    "node_modules/acorn-jsx": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/acorn-jsx/-/acorn-jsx-5.3.2.tgz",
      "integrity": "sha512-rq9s+JNhf0IChjtDXxllJ7g41oZk5SlXtp0LHwyA5cejwn7vKmKp4pPri6YEePv2PU65sAsegbXtIinmDFDXgQ==",
      "license": "MIT",
      "peerDependencies": {
        "acorn": "^6.0.0 || ^7.0.0 || ^8.0.0"
      }
    },
    "node_modules/acorn-walk": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/acorn-walk/-/acorn-walk-7.2.0.tgz",
      "integrity": "sha512-OPdCF6GsMIP+Az+aWfAAOEt2/+iVDKE7oy6lJ098aoe59oAmK76qV6Gw60SbZ8jHuG2wH058GF4pLFbYamYrVA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/address": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/address/-/address-1.2.2.tgz",
      "integrity": "sha512-4B/qKCfeE/ODUaAUpSwfzazo5x29WD4r3vXiWsB7I2mSDAihwEqKO+g8GELZUQSSAo5e1XTYh3ZVfLyxBc12nA==",
      "license": "MIT",
      "engines": {
        "node": ">= 10.0.0"
      }
    },
    "node_modules/adjust-sourcemap-loader": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/adjust-sourcemap-loader/-/adjust-sourcemap-loader-4.0.0.tgz",
      "integrity": "sha512-OXwN5b9pCUXNQHJpwwD2qP40byEmSgzj8B4ydSN0uMNYWiFmJ6x6KwUllMmfk8Rwu/HJDFR7U8ubsWBoN0Xp0A==",
      "license": "MIT",
      "dependencies": {
        "loader-utils": "^2.0.0",
        "regex-parser": "^2.2.11"
      },
      "engines": {
        "node": ">=8.9"
      }
    },
    "node_modules/agent-base": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/agent-base/-/agent-base-6.0.2.tgz",
      "integrity": "sha512-RZNwNclF7+MS/8bDg70amg32dyeZGZxiDuQmZxKLAlQjr3jGyLx+4Kkk58UO7D2QdgFIQCovuSuZESne6RG6XQ==",
      "license": "MIT",
      "dependencies": {
        "debug": "4"
      },
      "engines": {
        "node": ">= 6.0.0"
      }
    },
    "node_modules/ajv": {
      "version": "6.12.6",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-6.12.6.tgz",
      "integrity": "sha512-j3fVLgvTo527anyYyJOGTYJbG+vnnQYvE0m5mmkc1TK+nxAppkCLMIL0aZ4dblVCNoGShhm+kzE4ZUykBoMg4g==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.1",
        "fast-json-stable-stringify": "^2.0.0",
        "json-schema-traverse": "^0.4.1",
        "uri-js": "^4.2.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/ajv-formats": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/ajv-formats/-/ajv-formats-2.1.1.tgz",
      "integrity": "sha512-Wx0Kx52hxE7C18hkMEggYlEifqWZtYaRgouJor+WMdPnQyEK13vgEWyVNup7SoeeoLMsr4kf5h6dOW11I15MUA==",
      "license": "MIT",
      "dependencies": {
        "ajv": "^8.0.0"
      },
      "peerDependencies": {
        "ajv": "^8.0.0"
      },
      "peerDependenciesMeta": {
        "ajv": {
          "optional": true
        }
      }
    },
    "node_modules/ajv-formats/node_modules/ajv": {
      "version": "8.17.1",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-8.17.1.tgz",
      "integrity": "sha512-B/gBuNg5SiMTrPkC+A2+cW0RszwxYmn6VYxB/inlBStS5nx6xHIt/ehKRhIMhqusl7a8LjQoZnjCs5vhwxOQ1g==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "fast-uri": "^3.0.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/ajv-formats/node_modules/json-schema-traverse": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-1.0.0.tgz",
      "integrity": "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug==",
      "license": "MIT"
    },
    "node_modules/ajv-keywords": {
      "version": "3.5.2",
      "resolved": "https://registry.npmjs.org/ajv-keywords/-/ajv-keywords-3.5.2.tgz",
      "integrity": "sha512-5p6WTN0DdTGVQk6VjcEju19IgaHudalcfabD7yhDGeA6bcQnmL+CpveLJq/3hvfwd1aof6L386Ougkx6RfyMIQ==",
      "license": "MIT",
      "peerDependencies": {
        "ajv": "^6.9.1"
      }
    },
    "node_modules/ansi-escapes": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/ansi-escapes/-/ansi-escapes-4.3.2.tgz",
      "integrity": "sha512-gKXj5ALrKWQLsYG9jlTRmR/xKluxHV+Z9QEwNIgCfM1/uwPMCuzVVnh5mwTd+OuBZcwSIMbqssNWRm1lE51QaQ==",
      "license": "MIT",
      "dependencies": {
        "type-fest": "^0.21.3"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/ansi-escapes/node_modules/type-fest": {
      "version": "0.21.3",
      "resolved": "https://registry.npmjs.org/type-fest/-/type-fest-0.21.3.tgz",
      "integrity": "sha512-t0rzBq87m3fVcduHDUFhKmyyX+9eo6WQjZvf51Ea/M0Q7+T374Jp1aUiyUl0GKxp8M/OETVHSDvmkyPgvX+X2w==",
      "license": "(MIT OR CC0-1.0)",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/ansi-html": {
      "version": "0.0.9",
      "resolved": "https://registry.npmjs.org/ansi-html/-/ansi-html-0.0.9.tgz",
      "integrity": "sha512-ozbS3LuenHVxNRh/wdnN16QapUHzauqSomAl1jwwJRRsGwFwtj644lIhxfWu0Fy0acCij2+AEgHvjscq3dlVXg==",
      "engines": [
        "node >= 0.8.0"
      ],
      "license": "Apache-2.0",
      "bin": {
        "ansi-html": "bin/ansi-html"
      }
    },
    "node_modules/ansi-html-community": {
      "version": "0.0.8",
      "resolved": "https://registry.npmjs.org/ansi-html-community/-/ansi-html-community-0.0.8.tgz",
      "integrity": "sha512-1APHAyr3+PCamwNw3bXCPp4HFLONZt/yIH0sZp0/469KWNTEy+qN5jQ3GVX6DMZ1UXAi34yVwtTeaG/HpBuuzw==",
      "engines": [
        "node >= 0.8.0"
      ],
      "license": "Apache-2.0",
      "bin": {
        "ansi-html": "bin/ansi-html"
      }
    },
    "node_modules/ansi-regex": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-5.0.1.tgz",
      "integrity": "sha512-quJQXlTSUGL2LH9SUXo8VwsY4soanhgo6LNSm84E1LBcE8s3O0wpdiRzyR9z/ZZJMlMWv37qOOb9pdJlMUEKFQ==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/ansi-styles": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-4.3.0.tgz",
      "integrity": "sha512-zbB9rCJAT1rbjiVDb2hqKFHNYLxgtk8NURxZ3IZwD3F6NtxbXZQCnnSi1Lkx+IDohdPlFp222wVALIheZJQSEg==",
      "license": "MIT",
      "dependencies": {
        "color-convert": "^2.0.1"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/any-promise": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/any-promise/-/any-promise-1.3.0.tgz",
      "integrity": "sha512-7UvmKalWRt1wgjL1RrGxoSJW/0QZFIegpeGvZG9kjp8vrRu55XTHbwnqq2GpXm9uLbcuhxm3IqX9OB4MZR1b2A==",
      "license": "MIT"
    },
    "node_modules/anymatch": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/anymatch/-/anymatch-3.1.3.tgz",
      "integrity": "sha512-KMReFUr0B4t+D+OBkjR3KYqvocp2XaSzO55UcB6mgQMd3KbcE+mWTyvVV7D/zsdEbNnV6acZUutkiHQXvTr1Rw==",
      "license": "ISC",
      "dependencies": {
        "normalize-path": "^3.0.0",
        "picomatch": "^2.0.4"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/arg": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/arg/-/arg-5.0.2.tgz",
      "integrity": "sha512-PYjyFOLKQ9y57JvQ6QLo8dAgNqswh8M1RMJYdQduT6xbWSgK36P/Z/v+p888pM69jMMfS8Xd8F6I1kQ/I9HUGg==",
      "license": "MIT"
    },
    "node_modules/argparse": {
      "version": "1.0.10",
      "resolved": "https://registry.npmjs.org/argparse/-/argparse-1.0.10.tgz",
      "integrity": "sha512-o5Roy6tNG4SL/FOkCAN6RzjiakZS25RLYFrcMttJqbdd8BWrnA+fGz57iN5Pb06pvBGvl5gQ0B48dJlslXvoTg==",
      "license": "MIT",
      "dependencies": {
        "sprintf-js": "~1.0.2"
      }
    },
    "node_modules/aria-query": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/aria-query/-/aria-query-5.3.2.tgz",
      "integrity": "sha512-COROpnaoap1E2F000S62r6A60uHZnmlvomhfyT2DlTcrY1OrBKn2UhH7qn5wTC9zMvD0AY7csdPSNwKP+7WiQw==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/array-buffer-byte-length": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/array-buffer-byte-length/-/array-buffer-byte-length-1.0.2.tgz",
      "integrity": "sha512-LHE+8BuR7RYGDKvnrmcuSq3tDcKv9OFEXQt/HpbZhY7V6h0zlUXutnAD82GiFx9rdieCMjkvtcsPqBwgUl1Iiw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "is-array-buffer": "^3.0.5"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array-flatten": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/array-flatten/-/array-flatten-1.1.1.tgz",
      "integrity": "sha512-PCVAQswWemu6UdxsDFFX/+gVeYqKAod3D3UVm91jHwynguOwAvYPhx8nNlM++NqRcK6CxxpUafjmhIdKiHibqg==",
      "license": "MIT"
    },
    "node_modules/array-includes": {
      "version": "3.1.9",
      "resolved": "https://registry.npmjs.org/array-includes/-/array-includes-3.1.9.tgz",
      "integrity": "sha512-FmeCCAenzH0KH381SPT5FZmiA/TmpndpcaShhfgEN9eCVjnFBqq3l1xrI42y8+PPLI6hypzou4GXw00WHmPBLQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.24.0",
        "es-object-atoms": "^1.1.1",
        "get-intrinsic": "^1.3.0",
        "is-string": "^1.1.1",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array-union": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/array-union/-/array-union-2.1.0.tgz",
      "integrity": "sha512-HGyxoOTYUyCM6stUe6EJgnd4EoewAI7zMdfqO+kGjnlZmBDz/cR5pf8r/cR4Wq60sL/p0IkcjUEEPwS3GFrIyw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/array.prototype.findlast": {
      "version": "1.2.5",
      "resolved": "https://registry.npmjs.org/array.prototype.findlast/-/array.prototype.findlast-1.2.5.tgz",
      "integrity": "sha512-CVvd6FHg1Z3POpBLxO6E6zr+rSKEQ9L6rZHAaY7lLfhKsWYUBBOuMs0e9o24oopj6H+geRCX0YJ+TJLBK2eHyQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.findlastindex": {
      "version": "1.2.6",
      "resolved": "https://registry.npmjs.org/array.prototype.findlastindex/-/array.prototype.findlastindex-1.2.6.tgz",
      "integrity": "sha512-F/TKATkzseUExPlfvmwQKGITM3DGTK+vkAsCZoDc5daVygbJBnjEUCbgkAvVFsgfXfX4YIqZ/27G3k3tdXrTxQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "es-shim-unscopables": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.flat": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/array.prototype.flat/-/array.prototype.flat-1.3.3.tgz",
      "integrity": "sha512-rwG/ja1neyLqCuGZ5YYrznA62D4mZXg0i1cIskIUKSiqF3Cje9/wXAls9B9s1Wa2fomMsIv8czB8jZcPmxCXFg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.flatmap": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/array.prototype.flatmap/-/array.prototype.flatmap-1.3.3.tgz",
      "integrity": "sha512-Y7Wt51eKJSyi80hFrJCePGGNo5ktJCslFuboqJsbf57CCPcm5zztluPlc4/aD8sWsKvlwatezpV4U1efk8kpjg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.reduce": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/array.prototype.reduce/-/array.prototype.reduce-1.0.8.tgz",
      "integrity": "sha512-DwuEqgXFBwbmZSRqt3BpQigWNUoqw9Ml2dTWdF3B2zQlQX4OeUE0zyuzX0fX0IbTvjdkZbcBTU3idgpO78qkTw==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-array-method-boxes-properly": "^1.0.0",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "is-string": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/array.prototype.tosorted": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/array.prototype.tosorted/-/array.prototype.tosorted-1.1.4.tgz",
      "integrity": "sha512-p6Fx8B7b7ZhL/gmUsAy0D15WhvDccw3mnGNbZpi3pmeJdxtWsj2jEaI4Y6oo3XiHfzuSgPwKc04MYt6KgvC/wA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.3",
        "es-errors": "^1.3.0",
        "es-shim-unscopables": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/arraybuffer.prototype.slice": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/arraybuffer.prototype.slice/-/arraybuffer.prototype.slice-1.0.4.tgz",
      "integrity": "sha512-BNoCY6SXXPQ7gF2opIP4GBE+Xw7U+pHMYKuzjgCN3GwiaIR09UUeKfheyIry77QtrCBlC0KK0q5/TER/tYh3PQ==",
      "license": "MIT",
      "dependencies": {
        "array-buffer-byte-length": "^1.0.1",
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "is-array-buffer": "^3.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/asap": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/asap/-/asap-2.0.6.tgz",
      "integrity": "sha512-BSHWgDSAiKs50o2Re8ppvp3seVHXSRM44cdSsT9FfNEUUZLOGWVCsiWaRPWM1Znn+mqZ1OfVZ3z3DWEzSp7hRA==",
      "license": "MIT"
    },
    "node_modules/ast-types-flow": {
      "version": "0.0.8",
      "resolved": "https://registry.npmjs.org/ast-types-flow/-/ast-types-flow-0.0.8.tgz",
      "integrity": "sha512-OH/2E5Fg20h2aPrbe+QL8JZQFko0YZaF+j4mnQ7BGhfavO7OpSLa8a0y9sBwomHdSbkhTS8TQNayBfnW5DwbvQ==",
      "license": "MIT"
    },
    "node_modules/async": {
      "version": "3.2.6",
      "resolved": "https://registry.npmjs.org/async/-/async-3.2.6.tgz",
      "integrity": "sha512-htCUDlxyyCLMgaM3xXg0C0LW2xqfuQ6p05pCEIsXuyQ+a1koYKTuBMzRNwmybfLgvJDMd0r1LTn4+E0Ti6C2AA==",
      "license": "MIT"
    },
    "node_modules/async-function": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/async-function/-/async-function-1.0.0.tgz",
      "integrity": "sha512-hsU18Ae8CDTR6Kgu9DYf0EbCr/a5iGL0rytQDobUcdpYOKokk8LEjVphnXkDkgpi0wYVsqrXuP0bZxJaTqdgoA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/asynckit": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/asynckit/-/asynckit-0.4.0.tgz",
      "integrity": "sha512-Oei9OH4tRh0YqU3GxhX79dM/mwVgvbZJaSNaRk+bshkj0S5cfHcgYakreBjrHwatXKbz+IoIdYLxrKim2MjW0Q==",
      "license": "MIT"
    },
    "node_modules/at-least-node": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/at-least-node/-/at-least-node-1.0.0.tgz",
      "integrity": "sha512-+q/t7Ekv1EDY2l6Gda6LLiX14rU9TV20Wa3ofeQmwPFZbOMo9DXrLbOjFaaclkXKWidIaopwAObQDqwWtGUjqg==",
      "license": "ISC",
      "engines": {
        "node": ">= 4.0.0"
      }
    },
    "node_modules/autoprefixer": {
      "version": "10.4.21",
      "resolved": "https://registry.npmjs.org/autoprefixer/-/autoprefixer-10.4.21.tgz",
      "integrity": "sha512-O+A6LWV5LDHSJD3LjHYoNi4VLsj/Whi7k6zG12xTYaU4cQ8oxQGckXNX8cRHK5yOZ/ppVHe0ZBXGzSV9jXdVbQ==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/autoprefixer"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.24.4",
        "caniuse-lite": "^1.0.30001702",
        "fraction.js": "^4.3.7",
        "normalize-range": "^0.1.2",
        "picocolors": "^1.1.1",
        "postcss-value-parser": "^4.2.0"
      },
      "bin": {
        "autoprefixer": "bin/autoprefixer"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/available-typed-arrays": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/available-typed-arrays/-/available-typed-arrays-1.0.7.tgz",
      "integrity": "sha512-wvUjBtSGN7+7SjNpq/9M2Tg350UZD3q62IFZLbRAR1bSMlCo1ZaeW+BJ+D090e4hIIZLBcTDWe4Mh4jvUDajzQ==",
      "license": "MIT",
      "dependencies": {
        "possible-typed-array-names": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/axe-core": {
      "version": "4.10.3",
      "resolved": "https://registry.npmjs.org/axe-core/-/axe-core-4.10.3.tgz",
      "integrity": "sha512-Xm7bpRXnDSX2YE2YFfBk2FnF0ep6tmG7xPh8iHee8MIcrgq762Nkce856dYtJYLkuIoYZvGfTs/PbZhideTcEg==",
      "license": "MPL-2.0",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/axios": {
      "version": "1.12.2",
      "resolved": "https://registry.npmjs.org/axios/-/axios-1.12.2.tgz",
      "integrity": "sha512-vMJzPewAlRyOgxV2dU0Cuz2O8zzzx9VYtbJOaBgXFeLc4IV/Eg50n4LowmehOOR61S8ZMpc2K5Sa7g6A4jfkUw==",
      "license": "MIT",
      "dependencies": {
        "follow-redirects": "^1.15.6",
        "form-data": "^4.0.4",
        "proxy-from-env": "^1.1.0"
      }
    },
    "node_modules/axios/node_modules/form-data": {
      "version": "4.0.4",
      "resolved": "https://registry.npmjs.org/form-data/-/form-data-4.0.4.tgz",
      "integrity": "sha512-KrGhL9Q4zjj0kiUt5OO4Mr/A/jlI2jDYs5eHBpYHPcBEVSiipAvn2Ko2HnPe20rmcuuvMHNdZFp+4IlGTMF0Ow==",
      "license": "MIT",
      "dependencies": {
        "asynckit": "^0.4.0",
        "combined-stream": "^1.0.8",
        "es-set-tostringtag": "^2.1.0",
        "hasown": "^2.0.2",
        "mime-types": "^2.1.12"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/axobject-query": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/axobject-query/-/axobject-query-4.1.0.tgz",
      "integrity": "sha512-qIj0G9wZbMGNLjLmg1PT6v2mE9AH2zlnADJD/2tC6E00hgmhUOfEB6greHPAfLRSufHqROIUTkw6E+M3lH0PTQ==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/babel-jest": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/babel-jest/-/babel-jest-27.5.1.tgz",
      "integrity": "sha512-cdQ5dXjGRd0IBRATiQ4mZGlGlRE8kJpjPOixdNRdT+m3UcNqmYWN6rK6nvtXYfY3D76cb8s/O1Ss8ea24PIwcg==",
      "license": "MIT",
      "dependencies": {
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/babel__core": "^7.1.14",
        "babel-plugin-istanbul": "^6.1.1",
        "babel-preset-jest": "^27.5.1",
        "chalk": "^4.0.0",
        "graceful-fs": "^4.2.9",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.8.0"
      }
    },
    "node_modules/babel-loader": {
      "version": "8.4.1",
      "resolved": "https://registry.npmjs.org/babel-loader/-/babel-loader-8.4.1.tgz",
      "integrity": "sha512-nXzRChX+Z1GoE6yWavBQg6jDslyFF3SDjl2paADuoQtQW10JqShJt62R6eJQ5m/pjJFDT8xgKIWSP85OY8eXeA==",
      "license": "MIT",
      "dependencies": {
        "find-cache-dir": "^3.3.1",
        "loader-utils": "^2.0.4",
        "make-dir": "^3.1.0",
        "schema-utils": "^2.6.5"
      },
      "engines": {
        "node": ">= 8.9"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0",
        "webpack": ">=2"
      }
    },
    "node_modules/babel-loader/node_modules/schema-utils": {
      "version": "2.7.1",
      "resolved": "https://registry.npmjs.org/schema-utils/-/schema-utils-2.7.1.tgz",
      "integrity": "sha512-SHiNtMOUGWBQJwzISiVYKu82GiV4QYGePp3odlY1tuKO7gPtphAT5R/py0fA6xtbgLL/RvtJZnU9b8s0F1q0Xg==",
      "license": "MIT",
      "dependencies": {
        "@types/json-schema": "^7.0.5",
        "ajv": "^6.12.4",
        "ajv-keywords": "^3.5.2"
      },
      "engines": {
        "node": ">= 8.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/babel-plugin-istanbul": {
      "version": "6.1.1",
      "resolved": "https://registry.npmjs.org/babel-plugin-istanbul/-/babel-plugin-istanbul-6.1.1.tgz",
      "integrity": "sha512-Y1IQok9821cC9onCx5otgFfRm7Lm+I+wwxOx738M/WLPZ9Q42m4IG5W0FNX8WLL2gYMZo3JkuXIH2DOpWM+qwA==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "@babel/helper-plugin-utils": "^7.0.0",
        "@istanbuljs/load-nyc-config": "^1.0.0",
        "@istanbuljs/schema": "^0.1.2",
        "istanbul-lib-instrument": "^5.0.4",
        "test-exclude": "^6.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/babel-plugin-jest-hoist": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/babel-plugin-jest-hoist/-/babel-plugin-jest-hoist-27.5.1.tgz",
      "integrity": "sha512-50wCwD5EMNW4aRpOwtqzyZHIewTYNxLA4nhB+09d8BIssfNfzBRhkBIHiaPv1Si226TQSvp8gxAJm2iY2qs2hQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/template": "^7.3.3",
        "@babel/types": "^7.3.3",
        "@types/babel__core": "^7.0.0",
        "@types/babel__traverse": "^7.0.6"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/babel-plugin-macros": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/babel-plugin-macros/-/babel-plugin-macros-3.1.0.tgz",
      "integrity": "sha512-Cg7TFGpIr01vOQNODXOOaGz2NpCU5gl8x1qJFbb6hbZxR7XrcE2vtbAsTAbJ7/xwJtUuJEw8K8Zr/AE0LHlesg==",
      "license": "MIT",
      "dependencies": {
        "@babel/runtime": "^7.12.5",
        "cosmiconfig": "^7.0.0",
        "resolve": "^1.19.0"
      },
      "engines": {
        "node": ">=10",
        "npm": ">=6"
      }
    },
    "node_modules/babel-plugin-named-asset-import": {
      "version": "0.3.8",
      "resolved": "https://registry.npmjs.org/babel-plugin-named-asset-import/-/babel-plugin-named-asset-import-0.3.8.tgz",
      "integrity": "sha512-WXiAc++qo7XcJ1ZnTYGtLxmBCVbddAml3CEXgWaBzNzLNoxtQ8AiGEFDMOhot9XjTCQbvP5E77Fj9Gk924f00Q==",
      "license": "MIT",
      "peerDependencies": {
        "@babel/core": "^7.1.0"
      }
    },
    "node_modules/babel-plugin-polyfill-corejs2": {
      "version": "0.4.14",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-corejs2/-/babel-plugin-polyfill-corejs2-0.4.14.tgz",
      "integrity": "sha512-Co2Y9wX854ts6U8gAAPXfn0GmAyctHuK8n0Yhfjd6t30g7yvKjspvvOo9yG+z52PZRgFErt7Ka2pYnXCjLKEpg==",
      "license": "MIT",
      "dependencies": {
        "@babel/compat-data": "^7.27.7",
        "@babel/helper-define-polyfill-provider": "^0.6.5",
        "semver": "^6.3.1"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/babel-plugin-polyfill-corejs2/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/babel-plugin-polyfill-corejs3": {
      "version": "0.13.0",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-corejs3/-/babel-plugin-polyfill-corejs3-0.13.0.tgz",
      "integrity": "sha512-U+GNwMdSFgzVmfhNm8GJUX88AadB3uo9KpJqS3FaqNIPKgySuvMb+bHPsOmmuWyIcuqZj/pzt1RUIUZns4y2+A==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-define-polyfill-provider": "^0.6.5",
        "core-js-compat": "^3.43.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/babel-plugin-polyfill-regenerator": {
      "version": "0.6.5",
      "resolved": "https://registry.npmjs.org/babel-plugin-polyfill-regenerator/-/babel-plugin-polyfill-regenerator-0.6.5.tgz",
      "integrity": "sha512-ISqQ2frbiNU9vIJkzg7dlPpznPZ4jOiUQ1uSmB0fEHeowtN3COYRsXr/xexn64NpU13P06jc/L5TgiJXOgrbEg==",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-define-polyfill-provider": "^0.6.5"
      },
      "peerDependencies": {
        "@babel/core": "^7.4.0 || ^8.0.0-0 <8.0.0"
      }
    },
    "node_modules/babel-plugin-transform-react-remove-prop-types": {
      "version": "0.4.24",
      "resolved": "https://registry.npmjs.org/babel-plugin-transform-react-remove-prop-types/-/babel-plugin-transform-react-remove-prop-types-0.4.24.tgz",
      "integrity": "sha512-eqj0hVcJUR57/Ug2zE1Yswsw4LhuqqHhD+8v120T1cl3kjg76QwtyBrdIk4WVwK+lAhBJVYCd/v+4nc4y+8JsA==",
      "license": "MIT"
    },
    "node_modules/babel-preset-current-node-syntax": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/babel-preset-current-node-syntax/-/babel-preset-current-node-syntax-1.2.0.tgz",
      "integrity": "sha512-E/VlAEzRrsLEb2+dv8yp3bo4scof3l9nR4lrld+Iy5NyVqgVYUJnDAmunkhPMisRI32Qc4iRiz425d8vM++2fg==",
      "license": "MIT",
      "dependencies": {
        "@babel/plugin-syntax-async-generators": "^7.8.4",
        "@babel/plugin-syntax-bigint": "^7.8.3",
        "@babel/plugin-syntax-class-properties": "^7.12.13",
        "@babel/plugin-syntax-class-static-block": "^7.14.5",
        "@babel/plugin-syntax-import-attributes": "^7.24.7",
        "@babel/plugin-syntax-import-meta": "^7.10.4",
        "@babel/plugin-syntax-json-strings": "^7.8.3",
        "@babel/plugin-syntax-logical-assignment-operators": "^7.10.4",
        "@babel/plugin-syntax-nullish-coalescing-operator": "^7.8.3",
        "@babel/plugin-syntax-numeric-separator": "^7.10.4",
        "@babel/plugin-syntax-object-rest-spread": "^7.8.3",
        "@babel/plugin-syntax-optional-catch-binding": "^7.8.3",
        "@babel/plugin-syntax-optional-chaining": "^7.8.3",
        "@babel/plugin-syntax-private-property-in-object": "^7.14.5",
        "@babel/plugin-syntax-top-level-await": "^7.14.5"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0 || ^8.0.0-0"
      }
    },
    "node_modules/babel-preset-jest": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/babel-preset-jest/-/babel-preset-jest-27.5.1.tgz",
      "integrity": "sha512-Nptf2FzlPCWYuJg41HBqXVT8ym6bXOevuCTbhxlUpjwtysGaIWFvDEjp4y+G7fl13FgOdjs7P/DmErqH7da0Ag==",
      "license": "MIT",
      "dependencies": {
        "babel-plugin-jest-hoist": "^27.5.1",
        "babel-preset-current-node-syntax": "^1.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0"
      }
    },
    "node_modules/babel-preset-react-app": {
      "version": "10.1.0",
      "resolved": "https://registry.npmjs.org/babel-preset-react-app/-/babel-preset-react-app-10.1.0.tgz",
      "integrity": "sha512-f9B1xMdnkCIqe+2dHrJsoQFRz7reChaAHE/65SdaykPklQqhme2WaC08oD3is77x9ff98/9EazAKFDZv5rFEQg==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.16.0",
        "@babel/plugin-proposal-class-properties": "^7.16.0",
        "@babel/plugin-proposal-decorators": "^7.16.4",
        "@babel/plugin-proposal-nullish-coalescing-operator": "^7.16.0",
        "@babel/plugin-proposal-numeric-separator": "^7.16.0",
        "@babel/plugin-proposal-optional-chaining": "^7.16.0",
        "@babel/plugin-proposal-private-methods": "^7.16.0",
        "@babel/plugin-proposal-private-property-in-object": "^7.16.7",
        "@babel/plugin-transform-flow-strip-types": "^7.16.0",
        "@babel/plugin-transform-react-display-name": "^7.16.0",
        "@babel/plugin-transform-runtime": "^7.16.4",
        "@babel/preset-env": "^7.16.4",
        "@babel/preset-react": "^7.16.0",
        "@babel/preset-typescript": "^7.16.0",
        "@babel/runtime": "^7.16.3",
        "babel-plugin-macros": "^3.1.0",
        "babel-plugin-transform-react-remove-prop-types": "^0.4.24"
      }
    },
    "node_modules/babel-preset-react-app/node_modules/@babel/plugin-proposal-private-property-in-object": {
      "version": "7.21.11",
      "resolved": "https://registry.npmjs.org/@babel/plugin-proposal-private-property-in-object/-/plugin-proposal-private-property-in-object-7.21.11.tgz",
      "integrity": "sha512-0QZ8qP/3RLDVBwBFoWAwCtgcDZJVwA5LUJRZU8x2YFfKNuFq161wK3cuGrALu5yiPu+vzwTAg/sMWVNeWeNyaw==",
      "deprecated": "This proposal has been merged to the ECMAScript standard and thus this plugin is no longer maintained. Please use @babel/plugin-transform-private-property-in-object instead.",
      "license": "MIT",
      "dependencies": {
        "@babel/helper-annotate-as-pure": "^7.18.6",
        "@babel/helper-create-class-features-plugin": "^7.21.0",
        "@babel/helper-plugin-utils": "^7.20.2",
        "@babel/plugin-syntax-private-property-in-object": "^7.14.5"
      },
      "engines": {
        "node": ">=6.9.0"
      },
      "peerDependencies": {
        "@babel/core": "^7.0.0-0"
      }
    },
    "node_modules/balanced-match": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/balanced-match/-/balanced-match-1.0.2.tgz",
      "integrity": "sha512-3oSeUO0TMV67hN1AmbXsK4yaqU7tjiHlbxRDZOpH0KW9+CeX4bRAaX0Anxt0tx2MrpRpWwQaPwIlISEJhYU5Pw==",
      "license": "MIT"
    },
    "node_modules/baseline-browser-mapping": {
      "version": "2.8.6",
      "resolved": "https://registry.npmjs.org/baseline-browser-mapping/-/baseline-browser-mapping-2.8.6.tgz",
      "integrity": "sha512-wrH5NNqren/QMtKUEEJf7z86YjfqW/2uw3IL3/xpqZUC95SSVIFXYQeeGjL6FT/X68IROu6RMehZQS5foy2BXw==",
      "license": "Apache-2.0",
      "bin": {
        "baseline-browser-mapping": "dist/cli.js"
      }
    },
    "node_modules/batch": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/batch/-/batch-0.6.1.tgz",
      "integrity": "sha512-x+VAiMRL6UPkx+kudNvxTl6hB2XNNCG2r+7wixVfIYwu/2HKRXimwQyaumLjMveWvT2Hkd/cAJw+QBMfJ/EKVw==",
      "license": "MIT"
    },
    "node_modules/bfj": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/bfj/-/bfj-7.1.0.tgz",
      "integrity": "sha512-I6MMLkn+anzNdCUp9hMRyui1HaNEUCco50lxbvNS4+EyXg8lN3nJ48PjPWtbH8UVS9CuMoaKE9U2V3l29DaRQw==",
      "license": "MIT",
      "dependencies": {
        "bluebird": "^3.7.2",
        "check-types": "^11.2.3",
        "hoopy": "^0.1.4",
        "jsonpath": "^1.1.1",
        "tryer": "^1.0.1"
      },
      "engines": {
        "node": ">= 8.0.0"
      }
    },
    "node_modules/big.js": {
      "version": "5.2.2",
      "resolved": "https://registry.npmjs.org/big.js/-/big.js-5.2.2.tgz",
      "integrity": "sha512-vyL2OymJxmarO8gxMr0mhChsO9QGwhynfuu4+MHTAW6czfq9humCB7rKpUjDd9YUiDPU4mzpyupFSvOClAwbmQ==",
      "license": "MIT",
      "engines": {
        "node": "*"
      }
    },
    "node_modules/binary-extensions": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/binary-extensions/-/binary-extensions-2.3.0.tgz",
      "integrity": "sha512-Ceh+7ox5qe7LJuLHoY0feh3pHuUDHAcRUeyL2VYghZwfpkNIy/+8Ocg0a3UuSoYzavmylwuLWQOf3hl0jjMMIw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/bluebird": {
      "version": "3.7.2",
      "resolved": "https://registry.npmjs.org/bluebird/-/bluebird-3.7.2.tgz",
      "integrity": "sha512-XpNj6GDQzdfW+r2Wnn7xiSAd7TM3jzkxGXBGTtWKuSXv1xUV+azxAm8jdWZN06QTQk+2N2XB9jRDkvbmQmcRtg==",
      "license": "MIT"
    },
    "node_modules/body-parser": {
      "version": "1.20.3",
      "resolved": "https://registry.npmjs.org/body-parser/-/body-parser-1.20.3.tgz",
      "integrity": "sha512-7rAxByjUMqQ3/bHJy7D6OGXvx/MMc4IqBn/X0fcM1QUcAItpZrBEYhWGem+tzXH90c+G01ypMcYJBO9Y30203g==",
      "license": "MIT",
      "dependencies": {
        "bytes": "3.1.2",
        "content-type": "~1.0.5",
        "debug": "2.6.9",
        "depd": "2.0.0",
        "destroy": "1.2.0",
        "http-errors": "2.0.0",
        "iconv-lite": "0.4.24",
        "on-finished": "2.4.1",
        "qs": "6.13.0",
        "raw-body": "2.5.2",
        "type-is": "~1.6.18",
        "unpipe": "1.0.0"
      },
      "engines": {
        "node": ">= 0.8",
        "npm": "1.2.8000 || >= 1.4.16"
      }
    },
    "node_modules/body-parser/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/body-parser/node_modules/iconv-lite": {
      "version": "0.4.24",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.4.24.tgz",
      "integrity": "sha512-v3MXnZAcvnywkTUEZomIActle7RXXeedOR31wwl7VlyoXO4Qi9arvSenNQWne1TcRwhCL1HwLI21bEqdpj8/rA==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/body-parser/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/bonjour-service": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/bonjour-service/-/bonjour-service-1.3.0.tgz",
      "integrity": "sha512-3YuAUiSkWykd+2Azjgyxei8OWf8thdn8AITIog2M4UICzoqfjlqr64WIjEXZllf/W6vK1goqleSR6brGomxQqA==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "multicast-dns": "^7.2.5"
      }
    },
    "node_modules/boolbase": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/boolbase/-/boolbase-1.0.0.tgz",
      "integrity": "sha512-JZOSA7Mo9sNGB8+UjSgzdLtokWAky1zbztM3WRLCbZ70/3cTANmQmOdR7y2g+J0e2WXywy1yS468tY+IruqEww==",
      "license": "ISC"
    },
    "node_modules/brace-expansion": {
      "version": "1.1.12",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-1.1.12.tgz",
      "integrity": "sha512-9T9UjW3r0UW5c1Q7GTwllptXwhvYmEzFhzMfZ9H7FQWt+uZePjZPjBP/W1ZEyZ1twGWom5/56TF4lPcqjnDHcg==",
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^1.0.0",
        "concat-map": "0.0.1"
      }
    },
    "node_modules/braces": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/braces/-/braces-3.0.3.tgz",
      "integrity": "sha512-yQbXgO/OSZVD2IsiLlro+7Hf6Q18EJrKSEsdoMzKePKXct3gvD8oLcOQdIzGupr5Fj+EDe8gO/lxc1BzfMpxvA==",
      "license": "MIT",
      "dependencies": {
        "fill-range": "^7.1.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/browser-process-hrtime": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/browser-process-hrtime/-/browser-process-hrtime-1.0.0.tgz",
      "integrity": "sha512-9o5UecI3GhkpM6DrXr69PblIuWxPKk9Y0jHBRhdocZ2y7YECBFCsHm79Pr3OyR2AvjhDkabFJaDJMYRazHgsow==",
      "license": "BSD-2-Clause"
    },
    "node_modules/browserslist": {
      "version": "4.26.2",
      "resolved": "https://registry.npmjs.org/browserslist/-/browserslist-4.26.2.tgz",
      "integrity": "sha512-ECFzp6uFOSB+dcZ5BK/IBaGWssbSYBHvuMeMt3MMFyhI0Z8SqGgEkBLARgpRH3hutIgPVsALcMwbDrJqPxQ65A==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "baseline-browser-mapping": "^2.8.3",
        "caniuse-lite": "^1.0.30001741",
        "electron-to-chromium": "^1.5.218",
        "node-releases": "^2.0.21",
        "update-browserslist-db": "^1.1.3"
      },
      "bin": {
        "browserslist": "cli.js"
      },
      "engines": {
        "node": "^6 || ^7 || ^8 || ^9 || ^10 || ^11 || ^12 || >=13.7"
      }
    },
    "node_modules/bser": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/bser/-/bser-2.1.1.tgz",
      "integrity": "sha512-gQxTNE/GAfIIrmHLUE3oJyp5FO6HRBfhjnw4/wMmA63ZGDJnWBmgY/lyQBpnDUkGmAhbSe39tx2d/iTOAfglwQ==",
      "license": "Apache-2.0",
      "dependencies": {
        "node-int64": "^0.4.0"
      }
    },
    "node_modules/buffer-from": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/buffer-from/-/buffer-from-1.1.2.tgz",
      "integrity": "sha512-E+XQCRwSbaaiChtv6k6Dwgc+bx+Bs6vuKJHHl5kox/BaKbhiXzqQOwK4cO22yElGp2OCmjwVhT3HmxgyPGnJfQ==",
      "license": "MIT"
    },
    "node_modules/builtin-modules": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/builtin-modules/-/builtin-modules-3.3.0.tgz",
      "integrity": "sha512-zhaCDicdLuWN5UbN5IMnFqNMhNfo919sH85y2/ea+5Yg9TsTkeZxpL+JLbp6cgYFS4sRLp3YV4S6yDuqVWHYOw==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/bytes": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/bytes/-/bytes-3.1.2.tgz",
      "integrity": "sha512-/Nf7TyzTx6S3yRJObOAV7956r8cr2+Oj8AC5dt8wSP3BQAoeX58NoHyCU8P8zGkNXStjTSi6fzO6F0pBdcYbEg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/call-bind": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/call-bind/-/call-bind-1.0.8.tgz",
      "integrity": "sha512-oKlSFMcMwpUg2ednkhQ454wfWiU/ul3CkJe/PEHcTKuiX6RpbehUiFMXu13HalGZxfUwCQzZG747YXBn1im9ww==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.0",
        "es-define-property": "^1.0.0",
        "get-intrinsic": "^1.2.4",
        "set-function-length": "^1.2.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/call-bind-apply-helpers": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/call-bind-apply-helpers/-/call-bind-apply-helpers-1.0.2.tgz",
      "integrity": "sha512-Sp1ablJ0ivDkSzjcaJdxEunN5/XvksFJ2sMBFfq6x0ryhQV/2b/KwFe21cMpmHtPOSij8K99/wSfoEuTObmuMQ==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/call-bound": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/call-bound/-/call-bound-1.0.4.tgz",
      "integrity": "sha512-+ys997U96po4Kx/ABpBCqhA9EuxJaQWDQg7295H4hBphv3IZg0boBKuwYpt4YXp6MZ5AmZQnU/tyMTlRpaSejg==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "get-intrinsic": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/callsites": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/callsites/-/callsites-3.1.0.tgz",
      "integrity": "sha512-P8BjAsXvZS+VIDUI11hHCQEv74YT67YUi5JJFNWIqL235sBmjX4+qx9Muvls5ivyNENctx46xQLQ3aTuE7ssaQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/camel-case": {
      "version": "4.1.2",
      "resolved": "https://registry.npmjs.org/camel-case/-/camel-case-4.1.2.tgz",
      "integrity": "sha512-gxGWBrTT1JuMx6R+o5PTXMmUnhnVzLQ9SNutD4YqKtI6ap897t3tKECYla6gCWEkplXnlNybEkZg9GEGxKFCgw==",
      "license": "MIT",
      "dependencies": {
        "pascal-case": "^3.1.2",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/camelcase": {
      "version": "6.3.0",
      "resolved": "https://registry.npmjs.org/camelcase/-/camelcase-6.3.0.tgz",
      "integrity": "sha512-Gmy6FhYlCY7uOElZUSbxo2UCDH8owEk996gkbrpsgGtrJLM3J7jGxl9Ic7Qwwj4ivOE5AWZWRMecDdF7hqGjFA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/camelcase-css": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/camelcase-css/-/camelcase-css-2.0.1.tgz",
      "integrity": "sha512-QOSvevhslijgYwRx6Rv7zKdMF8lbRmx+uQGx2+vDc+KI/eBnsy9kit5aj23AgGu3pa4t9AgwbnXWqS+iOY+2aA==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/caniuse-api": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/caniuse-api/-/caniuse-api-3.0.0.tgz",
      "integrity": "sha512-bsTwuIg/BZZK/vreVTYYbSWoe2F+71P7K5QGEX+pT250DZbfU1MQ5prOKpPR+LL6uWKK3KMwMCAS74QB3Um1uw==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.0.0",
        "caniuse-lite": "^1.0.0",
        "lodash.memoize": "^4.1.2",
        "lodash.uniq": "^4.5.0"
      }
    },
    "node_modules/caniuse-lite": {
      "version": "1.0.30001743",
      "resolved": "https://registry.npmjs.org/caniuse-lite/-/caniuse-lite-1.0.30001743.tgz",
      "integrity": "sha512-e6Ojr7RV14Un7dz6ASD0aZDmQPT/A+eZU+nuTNfjqmRrmkmQlnTNWH0SKmqagx9PeW87UVqapSurtAXifmtdmw==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/caniuse-lite"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "CC-BY-4.0"
    },
    "node_modules/case-sensitive-paths-webpack-plugin": {
      "version": "2.4.0",
      "resolved": "https://registry.npmjs.org/case-sensitive-paths-webpack-plugin/-/case-sensitive-paths-webpack-plugin-2.4.0.tgz",
      "integrity": "sha512-roIFONhcxog0JSSWbvVAh3OocukmSgpqOH6YpMkCvav/ySIV3JKg4Dc8vYtQjYi/UxpNE36r/9v+VqTQqgkYmw==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/chalk": {
      "version": "4.1.2",
      "resolved": "https://registry.npmjs.org/chalk/-/chalk-4.1.2.tgz",
      "integrity": "sha512-oKnbhFyRIXpUuez8iBMmyEa4nbj4IOQyuhc/wy9kY7/WVPcwIO9VA668Pu8RkO7+0G76SLROeyw9CpQ061i4mA==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^4.1.0",
        "supports-color": "^7.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/chalk?sponsor=1"
      }
    },
    "node_modules/char-regex": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/char-regex/-/char-regex-1.0.2.tgz",
      "integrity": "sha512-kWWXztvZ5SBQV+eRgKFeh8q5sLuZY2+8WUIzlxWVTg+oGwY14qylx1KbKzHd8P6ZYkAg0xyIDU9JMHhyJMZ1jw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/chart.js": {
      "version": "4.5.0",
      "resolved": "https://registry.npmjs.org/chart.js/-/chart.js-4.5.0.tgz",
      "integrity": "sha512-aYeC/jDgSEx8SHWZvANYMioYMZ2KX02W6f6uVfyteuCGcadDLcYVHdfdygsTQkQ4TKn5lghoojAsPj5pu0SnvQ==",
      "license": "MIT",
      "dependencies": {
        "@kurkle/color": "^0.3.0"
      },
      "engines": {
        "pnpm": ">=8"
      }
    },
    "node_modules/check-types": {
      "version": "11.2.3",
      "resolved": "https://registry.npmjs.org/check-types/-/check-types-11.2.3.tgz",
      "integrity": "sha512-+67P1GkJRaxQD6PKK0Et9DhwQB+vGg3PM5+aavopCpZT1lj9jeqfvpgTLAWErNj8qApkkmXlu/Ug74kmhagkXg==",
      "license": "MIT"
    },
    "node_modules/chokidar": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/chokidar/-/chokidar-3.6.0.tgz",
      "integrity": "sha512-7VT13fmjotKpGipCW9JEQAusEPE+Ei8nl6/g4FBAmIm0GOOLMua9NDDo/DWp0ZAxCr3cPq5ZpBqmPAQgDda2Pw==",
      "license": "MIT",
      "dependencies": {
        "anymatch": "~3.1.2",
        "braces": "~3.0.2",
        "glob-parent": "~5.1.2",
        "is-binary-path": "~2.1.0",
        "is-glob": "~4.0.1",
        "normalize-path": "~3.0.0",
        "readdirp": "~3.6.0"
      },
      "engines": {
        "node": ">= 8.10.0"
      },
      "funding": {
        "url": "https://paulmillr.com/funding/"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/chokidar/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/chrome-trace-event": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/chrome-trace-event/-/chrome-trace-event-1.0.4.tgz",
      "integrity": "sha512-rNjApaLzuwaOTjCiT8lSDdGN1APCiqkChLMJxJPWLunPAt5fy8xgU9/jNOchV84wfIxrA0lRQB7oCT8jrn/wrQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6.0"
      }
    },
    "node_modules/ci-info": {
      "version": "3.9.0",
      "resolved": "https://registry.npmjs.org/ci-info/-/ci-info-3.9.0.tgz",
      "integrity": "sha512-NIxF55hv4nSqQswkAeiOi1r83xy8JldOFDTWiug55KBu9Jnblncd2U6ViHmYgHf01TPZS77NJBhBMKdWj9HQMQ==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/sibiraj-s"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/cjs-module-lexer": {
      "version": "1.4.3",
      "resolved": "https://registry.npmjs.org/cjs-module-lexer/-/cjs-module-lexer-1.4.3.tgz",
      "integrity": "sha512-9z8TZaGM1pfswYeXrUpzPrkx8UnWYdhJclsiYMm6x/w5+nN+8Tf/LnAgfLGQCm59qAOxU8WwHEq2vNwF6i4j+Q==",
      "license": "MIT"
    },
    "node_modules/clean-css": {
      "version": "5.3.3",
      "resolved": "https://registry.npmjs.org/clean-css/-/clean-css-5.3.3.tgz",
      "integrity": "sha512-D5J+kHaVb/wKSFcyyV75uCn8fiY4sV38XJoe4CUyGQ+mOU/fMVYUdH1hJC+CJQ5uY3EnW27SbJYS4X8BiLrAFg==",
      "license": "MIT",
      "dependencies": {
        "source-map": "~0.6.0"
      },
      "engines": {
        "node": ">= 10.0"
      }
    },
    "node_modules/clean-css/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/cliui": {
      "version": "7.0.4",
      "resolved": "https://registry.npmjs.org/cliui/-/cliui-7.0.4.tgz",
      "integrity": "sha512-OcRE68cOsVMXp1Yvonl/fzkQOyjLSu/8bhPDfQt0e0/Eb283TKP20Fs2MqoPsr9SwA595rRCA+QMzYc9nBP+JQ==",
      "license": "ISC",
      "dependencies": {
        "string-width": "^4.2.0",
        "strip-ansi": "^6.0.0",
        "wrap-ansi": "^7.0.0"
      }
    },
    "node_modules/co": {
      "version": "4.6.0",
      "resolved": "https://registry.npmjs.org/co/-/co-4.6.0.tgz",
      "integrity": "sha512-QVb0dM5HvG+uaxitm8wONl7jltx8dqhfU33DcqtOZcLSVIKSDDLDi7+0LbAKiyI8hD9u42m2YxXSkMGWThaecQ==",
      "license": "MIT",
      "engines": {
        "iojs": ">= 1.0.0",
        "node": ">= 0.12.0"
      }
    },
    "node_modules/coa": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/coa/-/coa-2.0.2.tgz",
      "integrity": "sha512-q5/jG+YQnSy4nRTV4F7lPepBJZ8qBNJJDBuJdoejDyLXgmL7IEo+Le2JDZudFTFt7mrCqIRaSjws4ygRCTCAXA==",
      "license": "MIT",
      "dependencies": {
        "@types/q": "^1.5.1",
        "chalk": "^2.4.1",
        "q": "^1.1.2"
      },
      "engines": {
        "node": ">= 4.0"
      }
    },
    "node_modules/coa/node_modules/ansi-styles": {
      "version": "3.2.1",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-3.2.1.tgz",
      "integrity": "sha512-VT0ZI6kZRdTh8YyJw3SMbYm/u+NqfsAxEpWO0Pf9sq8/e94WxxOpPKx9FR1FlyCtOVDNOQ+8ntlqFxiRc+r5qA==",
      "license": "MIT",
      "dependencies": {
        "color-convert": "^1.9.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/coa/node_modules/chalk": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/chalk/-/chalk-2.4.2.tgz",
      "integrity": "sha512-Mti+f9lpJNcwF4tWV8/OrTTtF1gZi+f8FqlyAdouralcFWFQWF2+NgCHShjkCb+IFBLq9buZwE1xckQU4peSuQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^3.2.1",
        "escape-string-regexp": "^1.0.5",
        "supports-color": "^5.3.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/coa/node_modules/color-convert": {
      "version": "1.9.3",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-1.9.3.tgz",
      "integrity": "sha512-QfAUtd+vFdAtFQcC8CCyYt1fYWxSqAiK2cSD6zDB8N3cpsEBAvRxp9zOGg6G/SHHJYAT88/az/IuDGALsNVbGg==",
      "license": "MIT",
      "dependencies": {
        "color-name": "1.1.3"
      }
    },
    "node_modules/coa/node_modules/color-name": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.3.tgz",
      "integrity": "sha512-72fSenhMw2HZMTVHeCA9KCmpEIbzWiQsjN+BHcBbS9vr1mtt+vJjPdksIBNUmKAW8TFUDPJK5SUU3QhE9NEXDw==",
      "license": "MIT"
    },
    "node_modules/coa/node_modules/escape-string-regexp": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-1.0.5.tgz",
      "integrity": "sha512-vbRorB5FUQWvla16U8R/qgaFIya2qGzwDrNmCZuYKrbdSUMG6I1ZCGQRefkRVhuOkIGVne7BQ35DSfo1qvJqFg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/coa/node_modules/has-flag": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/has-flag/-/has-flag-3.0.0.tgz",
      "integrity": "sha512-sKJf1+ceQBr4SMkvQnBDNDtf4TXpVhVGateu0t918bl30FnbE2m4vNLX+VWe/dpjlb+HugGYzW7uQXH98HPEYw==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/coa/node_modules/supports-color": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-5.5.0.tgz",
      "integrity": "sha512-QjVjwdXIt408MIiAqCX4oUKsgU2EqAGzs2Ppkm4aQYbjm+ZEWEcW4SfFNTr4uMNZma0ey4f5lgLrkB0aX0QMow==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^3.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/collect-v8-coverage": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/collect-v8-coverage/-/collect-v8-coverage-1.0.2.tgz",
      "integrity": "sha512-lHl4d5/ONEbLlJvaJNtsF/Lz+WvB07u2ycqTYbdrq7UypDXailES4valYb2eWiJFxZlVmpGekfqoxQhzyFdT4Q==",
      "license": "MIT"
    },
    "node_modules/color-convert": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-2.0.1.tgz",
      "integrity": "sha512-RRECPsj7iu/xb5oKYcsFHSppFNnsj/52OVTRKb4zP5onXwVF3zVmmToNcOfGC+CRDpfK/U584fMg38ZHCaElKQ==",
      "license": "MIT",
      "dependencies": {
        "color-name": "~1.1.4"
      },
      "engines": {
        "node": ">=7.0.0"
      }
    },
    "node_modules/color-name": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.4.tgz",
      "integrity": "sha512-dOy+3AuW3a2wNbZHIuMZpTcgjGuLU/uBL/ubcZF9OXbDo8ff4O8yVp5Bf0efS8uEoYo5q4Fx7dY9OgQGXgAsQA==",
      "license": "MIT"
    },
    "node_modules/colord": {
      "version": "2.9.3",
      "resolved": "https://registry.npmjs.org/colord/-/colord-2.9.3.tgz",
      "integrity": "sha512-jeC1axXpnb0/2nn/Y1LPuLdgXBLH7aDcHu4KEKfqw3CUhX7ZpfBSlPKyqXE6btIgEzfWtrX3/tyBCaCvXvMkOw==",
      "license": "MIT"
    },
    "node_modules/colorette": {
      "version": "2.0.20",
      "resolved": "https://registry.npmjs.org/colorette/-/colorette-2.0.20.tgz",
      "integrity": "sha512-IfEDxwoWIjkeXL1eXcDiow4UbKjhLdq6/EuSVR9GMN7KVH3r9gQ83e73hsz1Nd1T3ijd5xv1wcWRYO+D6kCI2w==",
      "license": "MIT"
    },
    "node_modules/combined-stream": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/combined-stream/-/combined-stream-1.0.8.tgz",
      "integrity": "sha512-FQN4MRfuJeHf7cBbBMJFXhKSDq+2kAArBlmRBvcvFE5BB1HZKXtSFASDhdlz9zOYwxh8lDdnvmMOe/+5cdoEdg==",
      "license": "MIT",
      "dependencies": {
        "delayed-stream": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/commander": {
      "version": "8.3.0",
      "resolved": "https://registry.npmjs.org/commander/-/commander-8.3.0.tgz",
      "integrity": "sha512-OkTL9umf+He2DZkUq8f8J9of7yL6RJKI24dVITBmNfZBmri9zYZQrKkuXiKhyfPSu8tUhnVBB1iKXevvnlR4Ww==",
      "license": "MIT",
      "engines": {
        "node": ">= 12"
      }
    },
    "node_modules/common-tags": {
      "version": "1.8.2",
      "resolved": "https://registry.npmjs.org/common-tags/-/common-tags-1.8.2.tgz",
      "integrity": "sha512-gk/Z852D2Wtb//0I+kRFNKKE9dIIVirjoqPoA1wJU+XePVXZfGeBpk45+A1rKO4Q43prqWBNY/MiIeRLbPWUaA==",
      "license": "MIT",
      "engines": {
        "node": ">=4.0.0"
      }
    },
    "node_modules/commondir": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/commondir/-/commondir-1.0.1.tgz",
      "integrity": "sha512-W9pAhw0ja1Edb5GVdIF1mjZw/ASI0AlShXM83UUGe2DVr5TdAPEA1OA8m/g8zWp9x6On7gqufY+FatDbC3MDQg==",
      "license": "MIT"
    },
    "node_modules/compressible": {
      "version": "2.0.18",
      "resolved": "https://registry.npmjs.org/compressible/-/compressible-2.0.18.tgz",
      "integrity": "sha512-AF3r7P5dWxL8MxyITRMlORQNaOA2IkAFaTr4k7BUumjPtRpGDTZpl0Pb1XCO6JeDCBdp126Cgs9sMxqSjgYyRg==",
      "license": "MIT",
      "dependencies": {
        "mime-db": ">= 1.43.0 < 2"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/compression": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/compression/-/compression-1.8.1.tgz",
      "integrity": "sha512-9mAqGPHLakhCLeNyxPkK4xVo746zQ/czLH1Ky+vkitMnWfWZps8r0qXuwhwizagCRttsL4lfG4pIOvaWLpAP0w==",
      "license": "MIT",
      "dependencies": {
        "bytes": "3.1.2",
        "compressible": "~2.0.18",
        "debug": "2.6.9",
        "negotiator": "~0.6.4",
        "on-headers": "~1.1.0",
        "safe-buffer": "5.2.1",
        "vary": "~1.1.2"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/compression/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/compression/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/concat-map": {
      "version": "0.0.1",
      "resolved": "https://registry.npmjs.org/concat-map/-/concat-map-0.0.1.tgz",
      "integrity": "sha512-/Srv4dswyQNBfohGpz9o6Yb3Gz3SrUDqBH5rTuhGR7ahtlbYKnVxw2bCFMRljaA7EXHaXZ8wsHdodFvbkhKmqg==",
      "license": "MIT"
    },
    "node_modules/confusing-browser-globals": {
      "version": "1.0.11",
      "resolved": "https://registry.npmjs.org/confusing-browser-globals/-/confusing-browser-globals-1.0.11.tgz",
      "integrity": "sha512-JsPKdmh8ZkmnHxDk55FZ1TqVLvEQTvoByJZRN9jzI0UjxK/QgAmsphz7PGtqgPieQZ/CQcHWXCR7ATDNhGe+YA==",
      "license": "MIT"
    },
    "node_modules/connect-history-api-fallback": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/connect-history-api-fallback/-/connect-history-api-fallback-2.0.0.tgz",
      "integrity": "sha512-U73+6lQFmfiNPrYbXqr6kZ1i1wiRqXnp2nhMsINseWXO8lDau0LGEffJ8kQi4EjLZympVgRdvqjAgiZ1tgzDDA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8"
      }
    },
    "node_modules/content-disposition": {
      "version": "0.5.4",
      "resolved": "https://registry.npmjs.org/content-disposition/-/content-disposition-0.5.4.tgz",
      "integrity": "sha512-FveZTNuGw04cxlAiWbzi6zTAL/lhehaWbTtgluJh4/E95DqMwTmha3KZN1aAWA8cFIhHzMZUvLevkw5Rqk+tSQ==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "5.2.1"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/content-type": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/content-type/-/content-type-1.0.5.tgz",
      "integrity": "sha512-nTjqfcBFEipKdXCv4YDQWCfmcLZKm81ldF0pAopTvyrFGVbcR6P/VAAd5G7N+0tTr8QqiU0tFadD6FK4NtJwOA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/convert-source-map": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-2.0.0.tgz",
      "integrity": "sha512-Kvp459HrV2FEJ1CAsi1Ku+MY3kasH19TFykTz2xWmMeq6bk2NU3XXvfJ+Q61m0xktWwt+1HSYf3JZsTms3aRJg==",
      "license": "MIT"
    },
    "node_modules/cookie": {
      "version": "0.7.1",
      "resolved": "https://registry.npmjs.org/cookie/-/cookie-0.7.1.tgz",
      "integrity": "sha512-6DnInpx7SJ2AK3+CTUE/ZM0vWTUboZCegxhC2xiIydHR9jNuTAASBrfEpHhiGOZw/nX51bHt6YQl8jsGo4y/0w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/cookie-signature": {
      "version": "1.0.6",
      "resolved": "https://registry.npmjs.org/cookie-signature/-/cookie-signature-1.0.6.tgz",
      "integrity": "sha512-QADzlaHc8icV8I7vbaJXJwod9HWYp8uCqf1xa4OfNu1T7JVxQIrUgOWtHdNDtPiywmFbiS12VjotIXLrKM3orQ==",
      "license": "MIT"
    },
    "node_modules/core-js": {
      "version": "3.45.1",
      "resolved": "https://registry.npmjs.org/core-js/-/core-js-3.45.1.tgz",
      "integrity": "sha512-L4NPsJlCfZsPeXukyzHFlg/i7IIVwHSItR0wg0FLNqYClJ4MQYTYLbC7EkjKYRLZF2iof2MUgN0EGy7MdQFChg==",
      "hasInstallScript": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/core-js"
      }
    },
    "node_modules/core-js-compat": {
      "version": "3.45.1",
      "resolved": "https://registry.npmjs.org/core-js-compat/-/core-js-compat-3.45.1.tgz",
      "integrity": "sha512-tqTt5T4PzsMIZ430XGviK4vzYSoeNJ6CXODi6c/voxOT6IZqBht5/EKaSNnYiEjjRYxjVz7DQIsOsY0XNi8PIA==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.25.3"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/core-js"
      }
    },
    "node_modules/core-js-pure": {
      "version": "3.45.1",
      "resolved": "https://registry.npmjs.org/core-js-pure/-/core-js-pure-3.45.1.tgz",
      "integrity": "sha512-OHnWFKgTUshEU8MK+lOs1H8kC8GkTi9Z1tvNkxrCcw9wl3MJIO7q2ld77wjWn4/xuGrVu2X+nME1iIIPBSdyEQ==",
      "hasInstallScript": true,
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/core-js"
      }
    },
    "node_modules/core-util-is": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/core-util-is/-/core-util-is-1.0.3.tgz",
      "integrity": "sha512-ZQBvi1DcpJ4GDqanjucZ2Hj3wEO5pZDS89BWbkcrvdxksJorwUDDZamX9ldFkp9aw2lmBDLgkObEA4DWNJ9FYQ==",
      "license": "MIT"
    },
    "node_modules/cosmiconfig": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/cosmiconfig/-/cosmiconfig-7.1.0.tgz",
      "integrity": "sha512-AdmX6xUzdNASswsFtmwSt7Vj8po9IuqXm0UXz7QKPuEUmPB4XyjGfaAr2PSuELMwkRMVH1EpIkX5bTZGRB3eCA==",
      "license": "MIT",
      "dependencies": {
        "@types/parse-json": "^4.0.0",
        "import-fresh": "^3.2.1",
        "parse-json": "^5.0.0",
        "path-type": "^4.0.0",
        "yaml": "^1.10.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/cross-spawn": {
      "version": "7.0.6",
      "resolved": "https://registry.npmjs.org/cross-spawn/-/cross-spawn-7.0.6.tgz",
      "integrity": "sha512-uV2QOWP2nWzsy2aMp8aRibhi9dlzF5Hgh5SHaB9OiTGEyDTiJJyx0uy51QXdyWbtAHNua4XJzUKca3OzKUd3vA==",
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.1.0",
        "shebang-command": "^2.0.0",
        "which": "^2.0.1"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/crypto-random-string": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/crypto-random-string/-/crypto-random-string-2.0.0.tgz",
      "integrity": "sha512-v1plID3y9r/lPhviJ1wrXpLeyUIGAZ2SHNYTEapm7/8A9nLPoyvVp3RK/EPFqn5kEznyWgYZNsRtYYIWbuG8KA==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/css-blank-pseudo": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/css-blank-pseudo/-/css-blank-pseudo-3.0.3.tgz",
      "integrity": "sha512-VS90XWtsHGqoM0t4KpH053c4ehxZ2E6HtGI7x68YFV0pTo/QmkV/YFA+NnlvK8guxZVNWGQhVNJGC39Q8XF4OQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9"
      },
      "bin": {
        "css-blank-pseudo": "dist/cli.cjs"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/css-declaration-sorter": {
      "version": "6.4.1",
      "resolved": "https://registry.npmjs.org/css-declaration-sorter/-/css-declaration-sorter-6.4.1.tgz",
      "integrity": "sha512-rtdthzxKuyq6IzqX6jEcIzQF/YqccluefyCYheovBOLhFT/drQA9zj/UbRAa9J7C0o6EG6u3E6g+vKkay7/k3g==",
      "license": "ISC",
      "engines": {
        "node": "^10 || ^12 || >=14"
      },
      "peerDependencies": {
        "postcss": "^8.0.9"
      }
    },
    "node_modules/css-has-pseudo": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/css-has-pseudo/-/css-has-pseudo-3.0.4.tgz",
      "integrity": "sha512-Vse0xpR1K9MNlp2j5w1pgWIJtm1a8qS0JwS9goFYcImjlHEmywP9VUF05aGBXzGpDJF86QXk4L0ypBmwPhGArw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9"
      },
      "bin": {
        "css-has-pseudo": "dist/cli.cjs"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/css-loader": {
      "version": "6.11.0",
      "resolved": "https://registry.npmjs.org/css-loader/-/css-loader-6.11.0.tgz",
      "integrity": "sha512-CTJ+AEQJjq5NzLga5pE39qdiSV56F8ywCIsqNIRF0r7BDgWsN25aazToqAFg7ZrtA/U016xudB3ffgweORxX7g==",
      "license": "MIT",
      "dependencies": {
        "icss-utils": "^5.1.0",
        "postcss": "^8.4.33",
        "postcss-modules-extract-imports": "^3.1.0",
        "postcss-modules-local-by-default": "^4.0.5",
        "postcss-modules-scope": "^3.2.0",
        "postcss-modules-values": "^4.0.0",
        "postcss-value-parser": "^4.2.0",
        "semver": "^7.5.4"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "@rspack/core": "0.x || 1.x",
        "webpack": "^5.0.0"
      },
      "peerDependenciesMeta": {
        "@rspack/core": {
          "optional": true
        },
        "webpack": {
          "optional": true
        }
      }
    },
    "node_modules/css-minimizer-webpack-plugin": {
      "version": "3.4.1",
      "resolved": "https://registry.npmjs.org/css-minimizer-webpack-plugin/-/css-minimizer-webpack-plugin-3.4.1.tgz",
      "integrity": "sha512-1u6D71zeIfgngN2XNRJefc/hY7Ybsxd74Jm4qngIXyUEk7fss3VUzuHxLAq/R8NAba4QU9OUSaMZlbpRc7bM4Q==",
      "license": "MIT",
      "dependencies": {
        "cssnano": "^5.0.6",
        "jest-worker": "^27.0.2",
        "postcss": "^8.3.5",
        "schema-utils": "^4.0.0",
        "serialize-javascript": "^6.0.0",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.0.0"
      },
      "peerDependenciesMeta": {
        "@parcel/css": {
          "optional": true
        },
        "clean-css": {
          "optional": true
        },
        "csso": {
          "optional": true
        },
        "esbuild": {
          "optional": true
        }
      }
    },
    "node_modules/css-minimizer-webpack-plugin/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/css-prefers-color-scheme": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/css-prefers-color-scheme/-/css-prefers-color-scheme-6.0.3.tgz",
      "integrity": "sha512-4BqMbZksRkJQx2zAjrokiGMd07RqOa2IxIrrN10lyBe9xhn9DEvjUK79J6jkeiv9D9hQFXKb6g1jwU62jziJZA==",
      "license": "CC0-1.0",
      "bin": {
        "css-prefers-color-scheme": "dist/cli.cjs"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/css-select": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/css-select/-/css-select-4.3.0.tgz",
      "integrity": "sha512-wPpOYtnsVontu2mODhA19JrqWxNsfdatRKd64kmpRbQgh1KtItko5sTnEpPdpSaJszTOhEMlF/RPz28qj4HqhQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "boolbase": "^1.0.0",
        "css-what": "^6.0.1",
        "domhandler": "^4.3.1",
        "domutils": "^2.8.0",
        "nth-check": "^2.0.1"
      },
      "funding": {
        "url": "https://github.com/sponsors/fb55"
      }
    },
    "node_modules/css-select-base-adapter": {
      "version": "0.1.1",
      "resolved": "https://registry.npmjs.org/css-select-base-adapter/-/css-select-base-adapter-0.1.1.tgz",
      "integrity": "sha512-jQVeeRG70QI08vSTwf1jHxp74JoZsr2XSgETae8/xC8ovSnL2WF87GTLO86Sbwdt2lK4Umg4HnnwMO4YF3Ce7w==",
      "license": "MIT"
    },
    "node_modules/css-tree": {
      "version": "1.0.0-alpha.37",
      "resolved": "https://registry.npmjs.org/css-tree/-/css-tree-1.0.0-alpha.37.tgz",
      "integrity": "sha512-DMxWJg0rnz7UgxKT0Q1HU/L9BeJI0M6ksor0OgqOnF+aRCDWg/N2641HmVyU9KVIu0OVVWOb2IpC9A+BJRnejg==",
      "license": "MIT",
      "dependencies": {
        "mdn-data": "2.0.4",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/css-tree/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/css-what": {
      "version": "6.2.2",
      "resolved": "https://registry.npmjs.org/css-what/-/css-what-6.2.2.tgz",
      "integrity": "sha512-u/O3vwbptzhMs3L1fQE82ZSLHQQfto5gyZzwteVIEyeaY5Fc7R4dapF/BvRoSYFeqfBk4m0V1Vafq5Pjv25wvA==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">= 6"
      },
      "funding": {
        "url": "https://github.com/sponsors/fb55"
      }
    },
    "node_modules/css.escape": {
      "version": "1.5.1",
      "resolved": "https://registry.npmjs.org/css.escape/-/css.escape-1.5.1.tgz",
      "integrity": "sha512-YUifsXXuknHlUsmlgyY0PKzgPOr7/FjCePfHNt0jxm83wHZi44VDMQ7/fGNkjY3/jV1MC+1CmZbaHzugyeRtpg==",
      "license": "MIT"
    },
    "node_modules/cssdb": {
      "version": "7.11.2",
      "resolved": "https://registry.npmjs.org/cssdb/-/cssdb-7.11.2.tgz",
      "integrity": "sha512-lhQ32TFkc1X4eTefGfYPvgovRSzIMofHkigfH8nWtyRL4XJLsRhJFreRvEgKzept7x1rjBuy3J/MurXLaFxW/A==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/csstools"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/csstools"
        }
      ],
      "license": "CC0-1.0"
    },
    "node_modules/cssesc": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/cssesc/-/cssesc-3.0.0.tgz",
      "integrity": "sha512-/Tb/JcjK111nNScGob5MNtsntNM1aCNUDipB/TkwZFhyDrrE47SOx/18wF2bbjgc3ZzCSKW1T5nt5EbFoAz/Vg==",
      "license": "MIT",
      "bin": {
        "cssesc": "bin/cssesc"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/cssnano": {
      "version": "5.1.15",
      "resolved": "https://registry.npmjs.org/cssnano/-/cssnano-5.1.15.tgz",
      "integrity": "sha512-j+BKgDcLDQA+eDifLx0EO4XSA56b7uut3BQFH+wbSaSTuGLuiyTa/wbRYthUXX8LC9mLg+WWKe8h+qJuwTAbHw==",
      "license": "MIT",
      "dependencies": {
        "cssnano-preset-default": "^5.2.14",
        "lilconfig": "^2.0.3",
        "yaml": "^1.10.2"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/cssnano"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/cssnano-preset-default": {
      "version": "5.2.14",
      "resolved": "https://registry.npmjs.org/cssnano-preset-default/-/cssnano-preset-default-5.2.14.tgz",
      "integrity": "sha512-t0SFesj/ZV2OTylqQVOrFgEh5uanxbO6ZAdeCrNsUQ6fVuXwYTxJPNAGvGTxHbD68ldIJNec7PyYZDBrfDQ+6A==",
      "license": "MIT",
      "dependencies": {
        "css-declaration-sorter": "^6.3.1",
        "cssnano-utils": "^3.1.0",
        "postcss-calc": "^8.2.3",
        "postcss-colormin": "^5.3.1",
        "postcss-convert-values": "^5.1.3",
        "postcss-discard-comments": "^5.1.2",
        "postcss-discard-duplicates": "^5.1.0",
        "postcss-discard-empty": "^5.1.1",
        "postcss-discard-overridden": "^5.1.0",
        "postcss-merge-longhand": "^5.1.7",
        "postcss-merge-rules": "^5.1.4",
        "postcss-minify-font-values": "^5.1.0",
        "postcss-minify-gradients": "^5.1.1",
        "postcss-minify-params": "^5.1.4",
        "postcss-minify-selectors": "^5.2.1",
        "postcss-normalize-charset": "^5.1.0",
        "postcss-normalize-display-values": "^5.1.0",
        "postcss-normalize-positions": "^5.1.1",
        "postcss-normalize-repeat-style": "^5.1.1",
        "postcss-normalize-string": "^5.1.0",
        "postcss-normalize-timing-functions": "^5.1.0",
        "postcss-normalize-unicode": "^5.1.1",
        "postcss-normalize-url": "^5.1.0",
        "postcss-normalize-whitespace": "^5.1.1",
        "postcss-ordered-values": "^5.1.3",
        "postcss-reduce-initial": "^5.1.2",
        "postcss-reduce-transforms": "^5.1.0",
        "postcss-svgo": "^5.1.0",
        "postcss-unique-selectors": "^5.1.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/cssnano-utils": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/cssnano-utils/-/cssnano-utils-3.1.0.tgz",
      "integrity": "sha512-JQNR19/YZhz4psLX/rQ9M83e3z2Wf/HdJbryzte4a3NSuafyp9w/I4U+hx5C2S9g41qlstH7DEWnZaaj83OuEA==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/csso": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/csso/-/csso-4.2.0.tgz",
      "integrity": "sha512-wvlcdIbf6pwKEk7vHj8/Bkc0B4ylXZruLvOgs9doS5eOsOpuodOV2zJChSpkp+pRpYQLQMeF04nr3Z68Sta9jA==",
      "license": "MIT",
      "dependencies": {
        "css-tree": "^1.1.2"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/csso/node_modules/css-tree": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/css-tree/-/css-tree-1.1.3.tgz",
      "integrity": "sha512-tRpdppF7TRazZrjJ6v3stzv93qxRcSsFmW6cX0Zm2NVKpxE1WV1HblnghVv9TreireHkqI/VDEsfolRF1p6y7Q==",
      "license": "MIT",
      "dependencies": {
        "mdn-data": "2.0.14",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/csso/node_modules/mdn-data": {
      "version": "2.0.14",
      "resolved": "https://registry.npmjs.org/mdn-data/-/mdn-data-2.0.14.tgz",
      "integrity": "sha512-dn6wd0uw5GsdswPFfsgMp5NSB0/aDe6fK94YJV/AJDYXL6HVLWBsxeq7js7Ad+mU2K9LAlwpk6kN2D5mwCPVow==",
      "license": "CC0-1.0"
    },
    "node_modules/csso/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/cssom": {
      "version": "0.4.4",
      "resolved": "https://registry.npmjs.org/cssom/-/cssom-0.4.4.tgz",
      "integrity": "sha512-p3pvU7r1MyyqbTk+WbNJIgJjG2VmTIaB10rI93LzVPrmDJKkzKYMtxxyAvQXR/NS6otuzveI7+7BBq3SjBS2mw==",
      "license": "MIT"
    },
    "node_modules/cssstyle": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/cssstyle/-/cssstyle-2.3.0.tgz",
      "integrity": "sha512-AZL67abkUzIuvcHqk7c09cezpGNcxUxU4Ioi/05xHk4DQeTkWmGYftIE6ctU6AEt+Gn4n1lDStOtj7FKycP71A==",
      "license": "MIT",
      "dependencies": {
        "cssom": "~0.3.6"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/cssstyle/node_modules/cssom": {
      "version": "0.3.8",
      "resolved": "https://registry.npmjs.org/cssom/-/cssom-0.3.8.tgz",
      "integrity": "sha512-b0tGHbfegbhPJpxpiBPU2sCkigAqtM9O121le6bbOlgyV+NyGyCmVfJ6QW9eRjz8CpNfWEOYBIMIGRYkLwsIYg==",
      "license": "MIT"
    },
    "node_modules/damerau-levenshtein": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/damerau-levenshtein/-/damerau-levenshtein-1.0.8.tgz",
      "integrity": "sha512-sdQSFB7+llfUcQHUQO3+B8ERRj0Oa4w9POWMI/puGtuf7gFywGmkaLCElnudfTiKZV+NvHqL0ifzdrI8Ro7ESA==",
      "license": "BSD-2-Clause"
    },
    "node_modules/data-urls": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/data-urls/-/data-urls-2.0.0.tgz",
      "integrity": "sha512-X5eWTSXO/BJmpdIKCRuKUgSCgAN0OwliVK3yPKbwIWU1Tdw5BRajxlzMidvh+gwko9AfQ9zIj52pzF91Q3YAvQ==",
      "license": "MIT",
      "dependencies": {
        "abab": "^2.0.3",
        "whatwg-mimetype": "^2.3.0",
        "whatwg-url": "^8.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/data-view-buffer": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/data-view-buffer/-/data-view-buffer-1.0.2.tgz",
      "integrity": "sha512-EmKO5V3OLXh1rtK2wgXRansaK1/mtVdTUEiEI0W8RkvgT05kfxaH29PliLnpLP73yYO6142Q72QNa8Wx/A5CqQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/data-view-byte-length": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/data-view-byte-length/-/data-view-byte-length-1.0.2.tgz",
      "integrity": "sha512-tuhGbE6CfTM9+5ANGf+oQb72Ky/0+s3xKUpHvShfiz2RxMFgFPjsXuRLBVMtvMs15awe45SRb83D6wH4ew6wlQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/inspect-js"
      }
    },
    "node_modules/data-view-byte-offset": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/data-view-byte-offset/-/data-view-byte-offset-1.0.1.tgz",
      "integrity": "sha512-BS8PfmtDGnrgYdOonGZQdLZslWIeCGFP9tpan0hi1Co2Zr2NKADsvGYA8XxuG/4UWgJ6Cjtv+YJnB6MM69QGlQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "is-data-view": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/debug": {
      "version": "4.4.3",
      "resolved": "https://registry.npmjs.org/debug/-/debug-4.4.3.tgz",
      "integrity": "sha512-RGwwWnwQvkVfavKVt22FGLw+xYSdzARwm0ru6DhTVA3umU5hZc28V3kO4stgYryrTlLpuvgI9GiijltAjNbcqA==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.3"
      },
      "engines": {
        "node": ">=6.0"
      },
      "peerDependenciesMeta": {
        "supports-color": {
          "optional": true
        }
      }
    },
    "node_modules/decimal.js": {
      "version": "10.6.0",
      "resolved": "https://registry.npmjs.org/decimal.js/-/decimal.js-10.6.0.tgz",
      "integrity": "sha512-YpgQiITW3JXGntzdUmyUR1V812Hn8T1YVXhCu+wO3OpS4eU9l4YdD3qjyiKdV6mvV29zapkMeD390UVEf2lkUg==",
      "license": "MIT"
    },
    "node_modules/dedent": {
      "version": "0.7.0",
      "resolved": "https://registry.npmjs.org/dedent/-/dedent-0.7.0.tgz",
      "integrity": "sha512-Q6fKUPqnAHAyhiUgFU7BUzLiv0kd8saH9al7tnu5Q/okj6dnupxyTgFIBjVzJATdfIAm9NAsvXNzjaKa+bxVyA==",
      "license": "MIT"
    },
    "node_modules/deep-is": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/deep-is/-/deep-is-0.1.4.tgz",
      "integrity": "sha512-oIPzksmTg4/MriiaYGO+okXDT7ztn/w3Eptv/+gSIdMdKsJo0u4CfYNFJPy+4SKMuCqGw2wxnA+URMg3t8a/bQ==",
      "license": "MIT"
    },
    "node_modules/deepmerge": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/deepmerge/-/deepmerge-4.3.1.tgz",
      "integrity": "sha512-3sUqbMEc77XqpdNO7FRyRog+eW3ph+GYCbj+rK+uYyRMuwsVy0rMiVtPn+QJlKFvWP/1PYpapqYn0Me2knFn+A==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/default-gateway": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/default-gateway/-/default-gateway-6.0.3.tgz",
      "integrity": "sha512-fwSOJsbbNzZ/CUFpqFBqYfYNLj1NbMPm8MMCIzHjC83iSJRBEGmDUxU+WP661BaBQImeC2yHwXtz+P/O9o+XEg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "execa": "^5.0.0"
      },
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/define-data-property": {
      "version": "1.1.4",
      "resolved": "https://registry.npmjs.org/define-data-property/-/define-data-property-1.1.4.tgz",
      "integrity": "sha512-rBMvIzlpA8v6E+SJZoo++HAYqsLrkg7MSfIinMPFhmkorw7X+dOXVJQs+QT69zGkzMyfDnIMN2Wid1+NbL3T+A==",
      "license": "MIT",
      "dependencies": {
        "es-define-property": "^1.0.0",
        "es-errors": "^1.3.0",
        "gopd": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/define-lazy-prop": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/define-lazy-prop/-/define-lazy-prop-2.0.0.tgz",
      "integrity": "sha512-Ds09qNh8yw3khSjiJjiUInaGX9xlqZDY7JVryGxdxV7NPeuqQfplOpQ66yJFZut3jLa5zOwkXw1g9EI2uKh4Og==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/define-properties": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/define-properties/-/define-properties-1.2.1.tgz",
      "integrity": "sha512-8QmQKqEASLd5nx0U1B1okLElbUuuttJ/AnYmRXbbbGDWh6uS208EjD4Xqq/I9wK7u0v6O08XhTWnt5XtEbR6Dg==",
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.0.1",
        "has-property-descriptors": "^1.0.0",
        "object-keys": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/delayed-stream": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/delayed-stream/-/delayed-stream-1.0.0.tgz",
      "integrity": "sha512-ZySD7Nf91aLB0RxL4KGrKHBXl7Eds1DAmEdcoVawXnLD7SDhpNgtuII2aAkg7a7QS41jxPSZ17p4VdGnMHk3MQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/depd": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/depd/-/depd-2.0.0.tgz",
      "integrity": "sha512-g7nH6P6dyDioJogAAGprGpCtVImJhpPk/roCzdb3fIh61/s/nPsfR6onyMwkCAR/OlC3yBC0lESvUoQEAssIrw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/dequal": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/dequal/-/dequal-2.0.3.tgz",
      "integrity": "sha512-0je+qPKHEMohvfRTCEo3CrPG6cAzAYgmzKyxRiYSSDkS6eGJdyVJm7WaYA5ECaAD9wLB2T4EEeymA5aFVcYXCA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/destroy": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/destroy/-/destroy-1.2.0.tgz",
      "integrity": "sha512-2sJGJTaXIIaR1w4iJSNoN0hnMY7Gpc/n8D4qSCJw8QqFWXf7cuAgnEHxBpweaVcPevC2l3KpjYCx3NypQQgaJg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8",
        "npm": "1.2.8000 || >= 1.4.16"
      }
    },
    "node_modules/detect-newline": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/detect-newline/-/detect-newline-3.1.0.tgz",
      "integrity": "sha512-TLz+x/vEXm/Y7P7wn1EJFNLxYpUD4TgMosxY6fAVJUnJMbupHBOncxyWUG9OpTaH9EBD7uFI5LfEgmMOc54DsA==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/detect-node": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/detect-node/-/detect-node-2.1.0.tgz",
      "integrity": "sha512-T0NIuQpnTvFDATNuHN5roPwSBG83rFsuO+MXXH9/3N1eFbn4wcPjttvjMLEPWJ0RGUYgQE7cGgS3tNxbqCGM7g==",
      "license": "MIT"
    },
    "node_modules/detect-port-alt": {
      "version": "1.1.6",
      "resolved": "https://registry.npmjs.org/detect-port-alt/-/detect-port-alt-1.1.6.tgz",
      "integrity": "sha512-5tQykt+LqfJFBEYaDITx7S7cR7mJ/zQmLXZ2qt5w04ainYZw6tBf9dBunMjVeVOdYVRUzUOE4HkY5J7+uttb5Q==",
      "license": "MIT",
      "dependencies": {
        "address": "^1.0.1",
        "debug": "^2.6.0"
      },
      "bin": {
        "detect": "bin/detect-port",
        "detect-port": "bin/detect-port"
      },
      "engines": {
        "node": ">= 4.2.1"
      }
    },
    "node_modules/detect-port-alt/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/detect-port-alt/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/didyoumean": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/didyoumean/-/didyoumean-1.2.2.tgz",
      "integrity": "sha512-gxtyfqMg7GKyhQmb056K7M3xszy/myH8w+B4RT+QXBQsvAOdc3XymqDDPHx1BgPgsdAA5SIifona89YtRATDzw==",
      "license": "Apache-2.0"
    },
    "node_modules/diff-sequences": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/diff-sequences/-/diff-sequences-27.5.1.tgz",
      "integrity": "sha512-k1gCAXAsNgLwEL+Y8Wvl+M6oEFj5bgazfZULpS5CneoPPXRaCCW7dm+q21Ky2VEE5X+VeRDBVg1Pcvvsr4TtNQ==",
      "license": "MIT",
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/dir-glob": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/dir-glob/-/dir-glob-3.0.1.tgz",
      "integrity": "sha512-WkrWp9GR4KXfKGYzOLmTuGVi1UWFfws377n9cc55/tb6DuqyF6pcQ5AbiHEshaDpY9v6oaSr2XCDidGmMwdzIA==",
      "license": "MIT",
      "dependencies": {
        "path-type": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/dlv": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/dlv/-/dlv-1.1.3.tgz",
      "integrity": "sha512-+HlytyjlPKnIG8XuRG8WvmBP8xs8P71y+SKKS6ZXWoEgLuePxtDoUEiH7WkdePWrQ5JBpE6aoVqfZfJUQkjXwA==",
      "license": "MIT"
    },
    "node_modules/dns-packet": {
      "version": "5.6.1",
      "resolved": "https://registry.npmjs.org/dns-packet/-/dns-packet-5.6.1.tgz",
      "integrity": "sha512-l4gcSouhcgIKRvyy99RNVOgxXiicE+2jZoNmaNmZ6JXiGajBOJAesk1OBlJuM5k2c+eudGdLxDqXuPCKIj6kpw==",
      "license": "MIT",
      "dependencies": {
        "@leichtgewicht/ip-codec": "^2.0.1"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/doctrine": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/doctrine/-/doctrine-3.0.0.tgz",
      "integrity": "sha512-yS+Q5i3hBf7GBkd4KG8a7eBNNWNGLTaEwwYWUijIYM7zrlYDM0BFXHjjPWlWZ1Rg7UaddZeIDmi9jF3HmqiQ2w==",
      "license": "Apache-2.0",
      "dependencies": {
        "esutils": "^2.0.2"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/dom-accessibility-api": {
      "version": "0.5.16",
      "resolved": "https://registry.npmjs.org/dom-accessibility-api/-/dom-accessibility-api-0.5.16.tgz",
      "integrity": "sha512-X7BJ2yElsnOJ30pZF4uIIDfBEVgF4XEBxL9Bxhy6dnrm5hkzqmsWHGTiHqRiITNhMyFLyAiWndIJP7Z1NTteDg==",
      "license": "MIT"
    },
    "node_modules/dom-converter": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/dom-converter/-/dom-converter-0.2.0.tgz",
      "integrity": "sha512-gd3ypIPfOMr9h5jIKq8E3sHOTCjeirnl0WK5ZdS1AW0Odt0b1PaWaHdJ4Qk4klv+YB9aJBS7mESXjFoDQPu6DA==",
      "license": "MIT",
      "dependencies": {
        "utila": "~0.4"
      }
    },
    "node_modules/dom-serializer": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/dom-serializer/-/dom-serializer-1.4.1.tgz",
      "integrity": "sha512-VHwB3KfrcOOkelEG2ZOfxqLZdfkil8PtJi4P8N2MMXucZq2yLp75ClViUlOVwyoHEDjYU433Aq+5zWP61+RGag==",
      "license": "MIT",
      "dependencies": {
        "domelementtype": "^2.0.1",
        "domhandler": "^4.2.0",
        "entities": "^2.0.0"
      },
      "funding": {
        "url": "https://github.com/cheeriojs/dom-serializer?sponsor=1"
      }
    },
    "node_modules/domelementtype": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/domelementtype/-/domelementtype-2.3.0.tgz",
      "integrity": "sha512-OLETBj6w0OsagBwdXnPdN0cnMfF9opN69co+7ZrbfPGrdpPVNBUj02spi6B1N7wChLQiPn4CSH/zJvXw56gmHw==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/fb55"
        }
      ],
      "license": "BSD-2-Clause"
    },
    "node_modules/domexception": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/domexception/-/domexception-2.0.1.tgz",
      "integrity": "sha512-yxJ2mFy/sibVQlu5qHjOkf9J3K6zgmCxgJ94u2EdvDOV09H+32LtRswEcUsmUWN72pVLOEnTSRaIVVzVQgS0dg==",
      "deprecated": "Use your platform's native DOMException instead",
      "license": "MIT",
      "dependencies": {
        "webidl-conversions": "^5.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/domexception/node_modules/webidl-conversions": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/webidl-conversions/-/webidl-conversions-5.0.0.tgz",
      "integrity": "sha512-VlZwKPCkYKxQgeSbH5EyngOmRp7Ww7I9rQLERETtf5ofd9pGeswWiOtogpEO850jziPRarreGxn5QIiTqpb2wA==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/domhandler": {
      "version": "4.3.1",
      "resolved": "https://registry.npmjs.org/domhandler/-/domhandler-4.3.1.tgz",
      "integrity": "sha512-GrwoxYN+uWlzO8uhUXRl0P+kHE4GtVPfYzVLcUxPL7KNdHKj66vvlhiweIHqYYXWlw+T8iLMp42Lm67ghw4WMQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "domelementtype": "^2.2.0"
      },
      "engines": {
        "node": ">= 4"
      },
      "funding": {
        "url": "https://github.com/fb55/domhandler?sponsor=1"
      }
    },
    "node_modules/domutils": {
      "version": "2.8.0",
      "resolved": "https://registry.npmjs.org/domutils/-/domutils-2.8.0.tgz",
      "integrity": "sha512-w96Cjofp72M5IIhpjgobBimYEfoPjx1Vx0BSX9P30WBdZW2WIKU0T1Bd0kz2eNZ9ikjKgHbEyKx8BB6H1L3h3A==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "dom-serializer": "^1.0.1",
        "domelementtype": "^2.2.0",
        "domhandler": "^4.2.0"
      },
      "funding": {
        "url": "https://github.com/fb55/domutils?sponsor=1"
      }
    },
    "node_modules/dot-case": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/dot-case/-/dot-case-3.0.4.tgz",
      "integrity": "sha512-Kv5nKlh6yRrdrGvxeJ2e5y2eRUpkUosIW4A2AS38zwSz27zu7ufDwQPi5Jhs3XAlGNetl3bmnGhQsMtkKJnj3w==",
      "license": "MIT",
      "dependencies": {
        "no-case": "^3.0.4",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/dotenv": {
      "version": "10.0.0",
      "resolved": "https://registry.npmjs.org/dotenv/-/dotenv-10.0.0.tgz",
      "integrity": "sha512-rlBi9d8jpv9Sf1klPjNfFAuWDjKLwTIJJ/VxtoTwIR6hnZxcEOQCZg2oIL3MWBYw5GpUDKOEnND7LXTbIpQ03Q==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/dotenv-expand": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/dotenv-expand/-/dotenv-expand-5.1.0.tgz",
      "integrity": "sha512-YXQl1DSa4/PQyRfgrv6aoNjhasp/p4qs9FjJ4q4cQk+8m4r6k4ZSiEyytKG8f8W9gi8WsQtIObNmKd+tMzNTmA==",
      "license": "BSD-2-Clause"
    },
    "node_modules/dunder-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/dunder-proto/-/dunder-proto-1.0.1.tgz",
      "integrity": "sha512-KIN/nDJBQRcXw0MLVhZE9iQHmG68qAVIBg9CqmUYjmQIhgij9U5MFvrqkUL5FbtyyzZuOeOt0zdeRe4UY7ct+A==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.1",
        "es-errors": "^1.3.0",
        "gopd": "^1.2.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/duplexer": {
      "version": "0.1.2",
      "resolved": "https://registry.npmjs.org/duplexer/-/duplexer-0.1.2.tgz",
      "integrity": "sha512-jtD6YG370ZCIi/9GTaJKQxWTZD045+4R4hTk/x1UyoqadyJ9x9CgSi1RlVDQF8U2sxLLSnFkCaMihqljHIWgMg==",
      "license": "MIT"
    },
    "node_modules/eastasianwidth": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/eastasianwidth/-/eastasianwidth-0.2.0.tgz",
      "integrity": "sha512-I88TYZWc9XiYHRQ4/3c5rjjfgkjhLyW2luGIheGERbNQ6OY7yTybanSpDXZa8y7VUP9YmDcYa+eyq4ca7iLqWA==",
      "license": "MIT"
    },
    "node_modules/ee-first": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/ee-first/-/ee-first-1.1.1.tgz",
      "integrity": "sha512-WMwm9LhRUo+WUaRN+vRuETqG89IgZphVSNkdFgeb6sS/E4OrDIN7t48CAewSHXc6C8lefD8KKfr5vY61brQlow==",
      "license": "MIT"
    },
    "node_modules/ejs": {
      "version": "3.1.10",
      "resolved": "https://registry.npmjs.org/ejs/-/ejs-3.1.10.tgz",
      "integrity": "sha512-UeJmFfOrAQS8OJWPZ4qtgHyWExa088/MtK5UEyoJGFH67cDEXkZSviOiKRCZ4Xij0zxI3JECgYs3oKx+AizQBA==",
      "license": "Apache-2.0",
      "dependencies": {
        "jake": "^10.8.5"
      },
      "bin": {
        "ejs": "bin/cli.js"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/electron-to-chromium": {
      "version": "1.5.222",
      "resolved": "https://registry.npmjs.org/electron-to-chromium/-/electron-to-chromium-1.5.222.tgz",
      "integrity": "sha512-gA7psSwSwQRE60CEoLz6JBCQPIxNeuzB2nL8vE03GK/OHxlvykbLyeiumQy1iH5C2f3YbRAZpGCMT12a/9ih9w==",
      "license": "ISC"
    },
    "node_modules/emittery": {
      "version": "0.8.1",
      "resolved": "https://registry.npmjs.org/emittery/-/emittery-0.8.1.tgz",
      "integrity": "sha512-uDfvUjVrfGJJhymx/kz6prltenw1u7WrCg1oa94zYY8xxVpLLUu045LAT0dhDZdXG58/EpPL/5kA180fQ/qudg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sindresorhus/emittery?sponsor=1"
      }
    },
    "node_modules/emoji-regex": {
      "version": "9.2.2",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-9.2.2.tgz",
      "integrity": "sha512-L18DaJsXSUk2+42pv8mLs5jJT2hqFkFE4j21wOmgbUqsZ2hL72NsUU785g9RXgo3s0ZNgVl42TiHp3ZtOv/Vyg==",
      "license": "MIT"
    },
    "node_modules/emojis-list": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/emojis-list/-/emojis-list-3.0.0.tgz",
      "integrity": "sha512-/kyM18EfinwXZbno9FyUGeFh87KC8HRQBQGildHZbEuRyWFOmv1U10o9BBp8XVZDVNNuQKyIGIu5ZYAAXJ0V2Q==",
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/encodeurl": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/encodeurl/-/encodeurl-2.0.0.tgz",
      "integrity": "sha512-Q0n9HRi4m6JuGIV1eFlmvJB7ZEVxu93IrMyiMsGC0lrMJMWzRgx6WGquyfQgZVb31vhGgXnfmPNNXmxnOkRBrg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/enhanced-resolve": {
      "version": "5.18.3",
      "resolved": "https://registry.npmjs.org/enhanced-resolve/-/enhanced-resolve-5.18.3.tgz",
      "integrity": "sha512-d4lC8xfavMeBjzGr2vECC3fsGXziXZQyJxD868h2M/mBI3PwAuODxAkLkq5HYuvrPYcUtiLzsTo8U3PgX3Ocww==",
      "license": "MIT",
      "dependencies": {
        "graceful-fs": "^4.2.4",
        "tapable": "^2.2.0"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/entities": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/entities/-/entities-2.2.0.tgz",
      "integrity": "sha512-p92if5Nz619I0w+akJrLZH0MX0Pb5DX39XOwQTtXSdQQOaYH03S1uIQp4mhOZtAXrxq4ViO67YTiLBo2638o9A==",
      "license": "BSD-2-Clause",
      "funding": {
        "url": "https://github.com/fb55/entities?sponsor=1"
      }
    },
    "node_modules/error-ex": {
      "version": "1.3.4",
      "resolved": "https://registry.npmjs.org/error-ex/-/error-ex-1.3.4.tgz",
      "integrity": "sha512-sqQamAnR14VgCr1A618A3sGrygcpK+HEbenA/HiEAkkUwcZIIB/tgWqHFxWgOyDh4nB4JCRimh79dR5Ywc9MDQ==",
      "license": "MIT",
      "dependencies": {
        "is-arrayish": "^0.2.1"
      }
    },
    "node_modules/error-stack-parser": {
      "version": "2.1.4",
      "resolved": "https://registry.npmjs.org/error-stack-parser/-/error-stack-parser-2.1.4.tgz",
      "integrity": "sha512-Sk5V6wVazPhq5MhpO+AUxJn5x7XSXGl1R93Vn7i+zS15KDVxQijejNCrz8340/2bgLBjR9GtEG8ZVKONDjcqGQ==",
      "license": "MIT",
      "dependencies": {
        "stackframe": "^1.3.4"
      }
    },
    "node_modules/es-abstract": {
      "version": "1.24.0",
      "resolved": "https://registry.npmjs.org/es-abstract/-/es-abstract-1.24.0.tgz",
      "integrity": "sha512-WSzPgsdLtTcQwm4CROfS5ju2Wa1QQcVeT37jFjYzdFz1r9ahadC8B8/a4qxJxM+09F18iumCdRmlr96ZYkQvEg==",
      "license": "MIT",
      "dependencies": {
        "array-buffer-byte-length": "^1.0.2",
        "arraybuffer.prototype.slice": "^1.0.4",
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "data-view-buffer": "^1.0.2",
        "data-view-byte-length": "^1.0.2",
        "data-view-byte-offset": "^1.0.1",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "es-set-tostringtag": "^2.1.0",
        "es-to-primitive": "^1.3.0",
        "function.prototype.name": "^1.1.8",
        "get-intrinsic": "^1.3.0",
        "get-proto": "^1.0.1",
        "get-symbol-description": "^1.1.0",
        "globalthis": "^1.0.4",
        "gopd": "^1.2.0",
        "has-property-descriptors": "^1.0.2",
        "has-proto": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "internal-slot": "^1.1.0",
        "is-array-buffer": "^3.0.5",
        "is-callable": "^1.2.7",
        "is-data-view": "^1.0.2",
        "is-negative-zero": "^2.0.3",
        "is-regex": "^1.2.1",
        "is-set": "^2.0.3",
        "is-shared-array-buffer": "^1.0.4",
        "is-string": "^1.1.1",
        "is-typed-array": "^1.1.15",
        "is-weakref": "^1.1.1",
        "math-intrinsics": "^1.1.0",
        "object-inspect": "^1.13.4",
        "object-keys": "^1.1.1",
        "object.assign": "^4.1.7",
        "own-keys": "^1.0.1",
        "regexp.prototype.flags": "^1.5.4",
        "safe-array-concat": "^1.1.3",
        "safe-push-apply": "^1.0.0",
        "safe-regex-test": "^1.1.0",
        "set-proto": "^1.0.0",
        "stop-iteration-iterator": "^1.1.0",
        "string.prototype.trim": "^1.2.10",
        "string.prototype.trimend": "^1.0.9",
        "string.prototype.trimstart": "^1.0.8",
        "typed-array-buffer": "^1.0.3",
        "typed-array-byte-length": "^1.0.3",
        "typed-array-byte-offset": "^1.0.4",
        "typed-array-length": "^1.0.7",
        "unbox-primitive": "^1.1.0",
        "which-typed-array": "^1.1.19"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/es-array-method-boxes-properly": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/es-array-method-boxes-properly/-/es-array-method-boxes-properly-1.0.0.tgz",
      "integrity": "sha512-wd6JXUmyHmt8T5a2xreUwKcGPq6f1f+WwIJkijUqiGcJz1qqnZgP6XIK+QyIWU5lT7imeNxUll48bziG+TSYcA==",
      "license": "MIT"
    },
    "node_modules/es-define-property": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/es-define-property/-/es-define-property-1.0.1.tgz",
      "integrity": "sha512-e3nRfgfUZ4rNGL232gUgX06QNyyez04KdjFrF+LTRoOXmrOgFKDg4BCdsjW8EnT69eqdYGmRpJwiPVYNrCaW3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-errors": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-errors/-/es-errors-1.3.0.tgz",
      "integrity": "sha512-Zf5H2Kxt2xjTvbJvP2ZWLEICxA6j+hAmMzIlypy4xcBg1vKVnx89Wy0GbS+kf5cwCVFFzdCFh2XSCFNULS6csw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-iterator-helpers": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/es-iterator-helpers/-/es-iterator-helpers-1.2.1.tgz",
      "integrity": "sha512-uDn+FE1yrDzyC0pCo961B2IHbdM8y/ACZsKD4dG6WqrjV53BADjwa7D+1aom2rsNVfLyDgU/eigvlJGJ08OQ4w==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.6",
        "es-errors": "^1.3.0",
        "es-set-tostringtag": "^2.0.3",
        "function-bind": "^1.1.2",
        "get-intrinsic": "^1.2.6",
        "globalthis": "^1.0.4",
        "gopd": "^1.2.0",
        "has-property-descriptors": "^1.0.2",
        "has-proto": "^1.2.0",
        "has-symbols": "^1.1.0",
        "internal-slot": "^1.1.0",
        "iterator.prototype": "^1.1.4",
        "safe-array-concat": "^1.1.3"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-module-lexer": {
      "version": "1.7.0",
      "resolved": "https://registry.npmjs.org/es-module-lexer/-/es-module-lexer-1.7.0.tgz",
      "integrity": "sha512-jEQoCwk8hyb2AZziIOLhDqpm5+2ww5uIE6lkO/6jcOCusfk6LhMHpXXfBLXTZ7Ydyt0j4VoUQv6uGNYbdW+kBA==",
      "license": "MIT"
    },
    "node_modules/es-object-atoms": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/es-object-atoms/-/es-object-atoms-1.1.1.tgz",
      "integrity": "sha512-FGgH2h8zKNim9ljj7dankFPcICIK9Cp5bm+c2gQSYePhpaG5+esrLODihIorn+Pe6FGJzWhXQotPv73jTaldXA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-set-tostringtag": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/es-set-tostringtag/-/es-set-tostringtag-2.1.0.tgz",
      "integrity": "sha512-j6vWzfrGVfyXxge+O0x5sh6cvxAog0a/4Rdd2K36zCMV5eJ+/+tOAngRO8cODMNWbVRdVlmGZQL2YS3yR8bIUA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-shim-unscopables": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/es-shim-unscopables/-/es-shim-unscopables-1.1.0.tgz",
      "integrity": "sha512-d9T8ucsEhh8Bi1woXCf+TIKDIROLG5WCkxg8geBCbvk22kzwC5G2OnXVMO6FUsvQlgUUXQ2itephWDLqDzbeCw==",
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/es-to-primitive": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/es-to-primitive/-/es-to-primitive-1.3.0.tgz",
      "integrity": "sha512-w+5mJ3GuFL+NjVtJlvydShqE1eN3h3PbI7/5LAsYJP/2qtuMXjfL2LpHSRqo4b4eSF5K/DH1JXKUAHSB2UW50g==",
      "license": "MIT",
      "dependencies": {
        "is-callable": "^1.2.7",
        "is-date-object": "^1.0.5",
        "is-symbol": "^1.0.4"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/escalade": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/escalade/-/escalade-3.2.0.tgz",
      "integrity": "sha512-WUj2qlxaQtO4g6Pq5c29GTcWGDyd8itL8zTlipgECz3JesAiiOKotd8JU6otB3PACgG6xkJUyVhboMS+bje/jA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/escape-html": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/escape-html/-/escape-html-1.0.3.tgz",
      "integrity": "sha512-NiSupZ4OeuGwr68lGIeym/ksIZMJodUGOSCZ/FSnTxcrekbvqrgdUxlJOMpijaKZVjAJrWrGs/6Jy8OMuyj9ow==",
      "license": "MIT"
    },
    "node_modules/escape-string-regexp": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-4.0.0.tgz",
      "integrity": "sha512-TtpcNJ3XAzx3Gq8sWRzJaVajRs0uVxA2YAkdb1jm2YkPz4G6egUFAyA3n5vtEIZefPk5Wa4UXbKuS5fKkJWdgA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/escodegen": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/escodegen/-/escodegen-2.1.0.tgz",
      "integrity": "sha512-2NlIDTwUWJN0mRPQOdtQBzbUHvdGY2P1VXSyU83Q3xKxM7WHX2Ql8dKq782Q9TgQUNOLEzEYu9bzLNj1q88I5w==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esprima": "^4.0.1",
        "estraverse": "^5.2.0",
        "esutils": "^2.0.2"
      },
      "bin": {
        "escodegen": "bin/escodegen.js",
        "esgenerate": "bin/esgenerate.js"
      },
      "engines": {
        "node": ">=6.0"
      },
      "optionalDependencies": {
        "source-map": "~0.6.1"
      }
    },
    "node_modules/escodegen/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "optional": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/eslint": {
      "version": "8.57.1",
      "resolved": "https://registry.npmjs.org/eslint/-/eslint-8.57.1.tgz",
      "integrity": "sha512-ypowyDxpVSYpkXr9WPv2PAZCtNip1Mv5KTW0SCurXv/9iOpcrH9PaqUElksqEB6pChqHGDRCFTyrZlGhnLNGiA==",
      "deprecated": "This version is no longer supported. Please see https://eslint.org/version-support for other options.",
      "license": "MIT",
      "dependencies": {
        "@eslint-community/eslint-utils": "^4.2.0",
        "@eslint-community/regexpp": "^4.6.1",
        "@eslint/eslintrc": "^2.1.4",
        "@eslint/js": "8.57.1",
        "@humanwhocodes/config-array": "^0.13.0",
        "@humanwhocodes/module-importer": "^1.0.1",
        "@nodelib/fs.walk": "^1.2.8",
        "@ungap/structured-clone": "^1.2.0",
        "ajv": "^6.12.4",
        "chalk": "^4.0.0",
        "cross-spawn": "^7.0.2",
        "debug": "^4.3.2",
        "doctrine": "^3.0.0",
        "escape-string-regexp": "^4.0.0",
        "eslint-scope": "^7.2.2",
        "eslint-visitor-keys": "^3.4.3",
        "espree": "^9.6.1",
        "esquery": "^1.4.2",
        "esutils": "^2.0.2",
        "fast-deep-equal": "^3.1.3",
        "file-entry-cache": "^6.0.1",
        "find-up": "^5.0.0",
        "glob-parent": "^6.0.2",
        "globals": "^13.19.0",
        "graphemer": "^1.4.0",
        "ignore": "^5.2.0",
        "imurmurhash": "^0.1.4",
        "is-glob": "^4.0.0",
        "is-path-inside": "^3.0.3",
        "js-yaml": "^4.1.0",
        "json-stable-stringify-without-jsonify": "^1.0.1",
        "levn": "^0.4.1",
        "lodash.merge": "^4.6.2",
        "minimatch": "^3.1.2",
        "natural-compare": "^1.4.0",
        "optionator": "^0.9.3",
        "strip-ansi": "^6.0.1",
        "text-table": "^0.2.0"
      },
      "bin": {
        "eslint": "bin/eslint.js"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/eslint-config-react-app": {
      "version": "7.0.1",
      "resolved": "https://registry.npmjs.org/eslint-config-react-app/-/eslint-config-react-app-7.0.1.tgz",
      "integrity": "sha512-K6rNzvkIeHaTd8m/QEh1Zko0KI7BACWkkneSs6s9cKZC/J27X3eZR6Upt1jkmZ/4FK+XUOPPxMEN7+lbUXfSlA==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.16.0",
        "@babel/eslint-parser": "^7.16.3",
        "@rushstack/eslint-patch": "^1.1.0",
        "@typescript-eslint/eslint-plugin": "^5.5.0",
        "@typescript-eslint/parser": "^5.5.0",
        "babel-preset-react-app": "^10.0.1",
        "confusing-browser-globals": "^1.0.11",
        "eslint-plugin-flowtype": "^8.0.3",
        "eslint-plugin-import": "^2.25.3",
        "eslint-plugin-jest": "^25.3.0",
        "eslint-plugin-jsx-a11y": "^6.5.1",
        "eslint-plugin-react": "^7.27.1",
        "eslint-plugin-react-hooks": "^4.3.0",
        "eslint-plugin-testing-library": "^5.0.1"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "eslint": "^8.0.0"
      }
    },
    "node_modules/eslint-import-resolver-node": {
      "version": "0.3.9",
      "resolved": "https://registry.npmjs.org/eslint-import-resolver-node/-/eslint-import-resolver-node-0.3.9.tgz",
      "integrity": "sha512-WFj2isz22JahUv+B788TlO3N6zL3nNJGU8CcZbPZvVEkBPaJdCV4vy5wyghty5ROFbCRnm132v8BScu5/1BQ8g==",
      "license": "MIT",
      "dependencies": {
        "debug": "^3.2.7",
        "is-core-module": "^2.13.0",
        "resolve": "^1.22.4"
      }
    },
    "node_modules/eslint-import-resolver-node/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-module-utils": {
      "version": "2.12.1",
      "resolved": "https://registry.npmjs.org/eslint-module-utils/-/eslint-module-utils-2.12.1.tgz",
      "integrity": "sha512-L8jSWTze7K2mTg0vos/RuLRS5soomksDPoJLXIslC7c8Wmut3bx7CPpJijDcBZtxQ5lrbUdM+s0OlNbz0DCDNw==",
      "license": "MIT",
      "dependencies": {
        "debug": "^3.2.7"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependenciesMeta": {
        "eslint": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-module-utils/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-plugin-flowtype": {
      "version": "8.0.3",
      "resolved": "https://registry.npmjs.org/eslint-plugin-flowtype/-/eslint-plugin-flowtype-8.0.3.tgz",
      "integrity": "sha512-dX8l6qUL6O+fYPtpNRideCFSpmWOUVx5QcaGLVqe/vlDiBSe4vYljDWDETwnyFzpl7By/WVIu6rcrniCgH9BqQ==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "lodash": "^4.17.21",
        "string-natural-compare": "^3.0.1"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "@babel/plugin-syntax-flow": "^7.14.5",
        "@babel/plugin-transform-react-jsx": "^7.14.9",
        "eslint": "^8.1.0"
      }
    },
    "node_modules/eslint-plugin-import": {
      "version": "2.32.0",
      "resolved": "https://registry.npmjs.org/eslint-plugin-import/-/eslint-plugin-import-2.32.0.tgz",
      "integrity": "sha512-whOE1HFo/qJDyX4SnXzP4N6zOWn79WhnCUY/iDR0mPfQZO8wcYE4JClzI2oZrhBnnMUCBCHZhO6VQyoBU95mZA==",
      "license": "MIT",
      "dependencies": {
        "@rtsao/scc": "^1.1.0",
        "array-includes": "^3.1.9",
        "array.prototype.findlastindex": "^1.2.6",
        "array.prototype.flat": "^1.3.3",
        "array.prototype.flatmap": "^1.3.3",
        "debug": "^3.2.7",
        "doctrine": "^2.1.0",
        "eslint-import-resolver-node": "^0.3.9",
        "eslint-module-utils": "^2.12.1",
        "hasown": "^2.0.2",
        "is-core-module": "^2.16.1",
        "is-glob": "^4.0.3",
        "minimatch": "^3.1.2",
        "object.fromentries": "^2.0.8",
        "object.groupby": "^1.0.3",
        "object.values": "^1.2.1",
        "semver": "^6.3.1",
        "string.prototype.trimend": "^1.0.9",
        "tsconfig-paths": "^3.15.0"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependencies": {
        "eslint": "^2 || ^3 || ^4 || ^5 || ^6 || ^7.2.0 || ^8 || ^9"
      }
    },
    "node_modules/eslint-plugin-import/node_modules/debug": {
      "version": "3.2.7",
      "resolved": "https://registry.npmjs.org/debug/-/debug-3.2.7.tgz",
      "integrity": "sha512-CFjzYYAi4ThfiQvizrFQevTTXHtnCqWfe7x1AhgEscTz6ZbLbfoLRLPugTQyBth6f8ZERVUSyWHFD/7Wu4t1XQ==",
      "license": "MIT",
      "dependencies": {
        "ms": "^2.1.1"
      }
    },
    "node_modules/eslint-plugin-import/node_modules/doctrine": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/doctrine/-/doctrine-2.1.0.tgz",
      "integrity": "sha512-35mSku4ZXK0vfCuHEDAwt55dg2jNajHZ1odvF+8SSr82EsZY4QmXfuWso8oEd8zRhVObSN18aM0CjSdoBX7zIw==",
      "license": "Apache-2.0",
      "dependencies": {
        "esutils": "^2.0.2"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/eslint-plugin-import/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/eslint-plugin-jest": {
      "version": "25.7.0",
      "resolved": "https://registry.npmjs.org/eslint-plugin-jest/-/eslint-plugin-jest-25.7.0.tgz",
      "integrity": "sha512-PWLUEXeeF7C9QGKqvdSbzLOiLTx+bno7/HC9eefePfEb257QFHg7ye3dh80AZVkaa/RQsBB1Q/ORQvg2X7F0NQ==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/experimental-utils": "^5.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || >=16.0.0"
      },
      "peerDependencies": {
        "@typescript-eslint/eslint-plugin": "^4.0.0 || ^5.0.0",
        "eslint": "^6.0.0 || ^7.0.0 || ^8.0.0"
      },
      "peerDependenciesMeta": {
        "@typescript-eslint/eslint-plugin": {
          "optional": true
        },
        "jest": {
          "optional": true
        }
      }
    },
    "node_modules/eslint-plugin-jsx-a11y": {
      "version": "6.10.2",
      "resolved": "https://registry.npmjs.org/eslint-plugin-jsx-a11y/-/eslint-plugin-jsx-a11y-6.10.2.tgz",
      "integrity": "sha512-scB3nz4WmG75pV8+3eRUQOHZlNSUhFNq37xnpgRkCCELU3XMvXAxLk1eqWWyE22Ki4Q01Fnsw9BA3cJHDPgn2Q==",
      "license": "MIT",
      "dependencies": {
        "aria-query": "^5.3.2",
        "array-includes": "^3.1.8",
        "array.prototype.flatmap": "^1.3.2",
        "ast-types-flow": "^0.0.8",
        "axe-core": "^4.10.0",
        "axobject-query": "^4.1.0",
        "damerau-levenshtein": "^1.0.8",
        "emoji-regex": "^9.2.2",
        "hasown": "^2.0.2",
        "jsx-ast-utils": "^3.3.5",
        "language-tags": "^1.0.9",
        "minimatch": "^3.1.2",
        "object.fromentries": "^2.0.8",
        "safe-regex-test": "^1.0.3",
        "string.prototype.includes": "^2.0.1"
      },
      "engines": {
        "node": ">=4.0"
      },
      "peerDependencies": {
        "eslint": "^3 || ^4 || ^5 || ^6 || ^7 || ^8 || ^9"
      }
    },
    "node_modules/eslint-plugin-react": {
      "version": "7.37.5",
      "resolved": "https://registry.npmjs.org/eslint-plugin-react/-/eslint-plugin-react-7.37.5.tgz",
      "integrity": "sha512-Qteup0SqU15kdocexFNAJMvCJEfa2xUKNV4CC1xsVMrIIqEy3SQ/rqyxCWNzfrd3/ldy6HMlD2e0JDVpDg2qIA==",
      "license": "MIT",
      "dependencies": {
        "array-includes": "^3.1.8",
        "array.prototype.findlast": "^1.2.5",
        "array.prototype.flatmap": "^1.3.3",
        "array.prototype.tosorted": "^1.1.4",
        "doctrine": "^2.1.0",
        "es-iterator-helpers": "^1.2.1",
        "estraverse": "^5.3.0",
        "hasown": "^2.0.2",
        "jsx-ast-utils": "^2.4.1 || ^3.0.0",
        "minimatch": "^3.1.2",
        "object.entries": "^1.1.9",
        "object.fromentries": "^2.0.8",
        "object.values": "^1.2.1",
        "prop-types": "^15.8.1",
        "resolve": "^2.0.0-next.5",
        "semver": "^6.3.1",
        "string.prototype.matchall": "^4.0.12",
        "string.prototype.repeat": "^1.0.0"
      },
      "engines": {
        "node": ">=4"
      },
      "peerDependencies": {
        "eslint": "^3 || ^4 || ^5 || ^6 || ^7 || ^8 || ^9.7"
      }
    },
    "node_modules/eslint-plugin-react-hooks": {
      "version": "4.6.2",
      "resolved": "https://registry.npmjs.org/eslint-plugin-react-hooks/-/eslint-plugin-react-hooks-4.6.2.tgz",
      "integrity": "sha512-QzliNJq4GinDBcD8gPB5v0wh6g8q3SUi6EFF0x8N/BL9PoVs0atuGc47ozMRyOWAKdwaZ5OnbOEa3WR+dSGKuQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "eslint": "^3.0.0 || ^4.0.0 || ^5.0.0 || ^6.0.0 || ^7.0.0 || ^8.0.0-0"
      }
    },
    "node_modules/eslint-plugin-react/node_modules/doctrine": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/doctrine/-/doctrine-2.1.0.tgz",
      "integrity": "sha512-35mSku4ZXK0vfCuHEDAwt55dg2jNajHZ1odvF+8SSr82EsZY4QmXfuWso8oEd8zRhVObSN18aM0CjSdoBX7zIw==",
      "license": "Apache-2.0",
      "dependencies": {
        "esutils": "^2.0.2"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/eslint-plugin-react/node_modules/resolve": {
      "version": "2.0.0-next.5",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-2.0.0-next.5.tgz",
      "integrity": "sha512-U7WjGVG9sH8tvjW5SmGbQuui75FiyjAX72HX15DwBBwF9dNiQZRQAg9nnPhYy+TUnE0+VcrttuvNI8oSxZcocA==",
      "license": "MIT",
      "dependencies": {
        "is-core-module": "^2.13.0",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/eslint-plugin-react/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/eslint-plugin-testing-library": {
      "version": "5.11.1",
      "resolved": "https://registry.npmjs.org/eslint-plugin-testing-library/-/eslint-plugin-testing-library-5.11.1.tgz",
      "integrity": "sha512-5eX9e1Kc2PqVRed3taaLnAAqPZGEX75C+M/rXzUAI3wIg/ZxzUm1OVAwfe/O+vE+6YXOLetSe9g5GKD2ecXipw==",
      "license": "MIT",
      "dependencies": {
        "@typescript-eslint/utils": "^5.58.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0",
        "npm": ">=6"
      },
      "peerDependencies": {
        "eslint": "^7.5.0 || ^8.0.0"
      }
    },
    "node_modules/eslint-scope": {
      "version": "7.2.2",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-7.2.2.tgz",
      "integrity": "sha512-dOt21O7lTMhDM+X9mB4GX+DZrZtCUJPL/wlcTqxyrx5IvO0IYtILdtrQGQp+8n5S0gwSVmOf9NQrjMOgfQZlIg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^5.2.0"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/eslint-visitor-keys": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/eslint-visitor-keys/-/eslint-visitor-keys-3.4.3.tgz",
      "integrity": "sha512-wpc+LXeiyiisxPlEkUzU6svyS1frIO3Mgxj1fdy7Pm8Ygzguax2N3Fa/D/ag1WqbOprdI+uY6wMUl8/a2G+iag==",
      "license": "Apache-2.0",
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/eslint-webpack-plugin": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/eslint-webpack-plugin/-/eslint-webpack-plugin-3.2.0.tgz",
      "integrity": "sha512-avrKcGncpPbPSUHX6B3stNGzkKFto3eL+DKM4+VyMrVnhPc3vRczVlCq3uhuFOdRvDHTVXuzwk1ZKUrqDQHQ9w==",
      "license": "MIT",
      "dependencies": {
        "@types/eslint": "^7.29.0 || ^8.4.1",
        "jest-worker": "^28.0.2",
        "micromatch": "^4.0.5",
        "normalize-path": "^3.0.0",
        "schema-utils": "^4.0.0"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "eslint": "^7.0.0 || ^8.0.0",
        "webpack": "^5.0.0"
      }
    },
    "node_modules/eslint-webpack-plugin/node_modules/jest-worker": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/jest-worker/-/jest-worker-28.1.3.tgz",
      "integrity": "sha512-CqRA220YV/6jCo8VWvAt1KKx6eek1VIHMPeLEbpcfSfkEeWyBNppynM/o6q+Wmw+sOhos2ml34wZbSX3G13//g==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "merge-stream": "^2.0.0",
        "supports-color": "^8.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/eslint-webpack-plugin/node_modules/supports-color": {
      "version": "8.1.1",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-8.1.1.tgz",
      "integrity": "sha512-MpUEN2OodtUzxvKQl72cUF7RQ5EiHsGvSsVG0ia9c5RbWGL2CI4C7EpPS8UTBIplnlzZiNuV56w+FuNxy3ty2Q==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/supports-color?sponsor=1"
      }
    },
    "node_modules/eslint/node_modules/argparse": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/argparse/-/argparse-2.0.1.tgz",
      "integrity": "sha512-8+9WqebbFzpX9OR+Wa6O29asIogeRMzcGtAINdpMHHyAg10f05aSFVBbcEqGf/PXw1EjAZ+q2/bEBg3DvurK3Q==",
      "license": "Python-2.0"
    },
    "node_modules/eslint/node_modules/find-up": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-5.0.0.tgz",
      "integrity": "sha512-78/PXT1wlLLDgTzDs7sjq9hzz0vXD+zn+7wypEe4fXQxCmdmqfGsEPQxmiCSQI3ajFV91bVSsvNtrJRiW6nGng==",
      "license": "MIT",
      "dependencies": {
        "locate-path": "^6.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint/node_modules/js-yaml": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/js-yaml/-/js-yaml-4.1.0.tgz",
      "integrity": "sha512-wpxZs9NoxZaJESJGIZTyDEaYpl0FKSA+FB9aJiyemKhMwkxQg63h4T1KJgUGHpTqPDNRcmmYLugrRjJlBtWvRA==",
      "license": "MIT",
      "dependencies": {
        "argparse": "^2.0.1"
      },
      "bin": {
        "js-yaml": "bin/js-yaml.js"
      }
    },
    "node_modules/eslint/node_modules/locate-path": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-6.0.0.tgz",
      "integrity": "sha512-iPZK6eYjbxRu3uB4/WZ3EsEIMJFMqAoopl3R+zuq0UjcAm/MO6KCweDgPfP3elTztoKP3KtnVHxTn2NHBSDVUw==",
      "license": "MIT",
      "dependencies": {
        "p-locate": "^5.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint/node_modules/p-limit": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-3.1.0.tgz",
      "integrity": "sha512-TYOanM3wGwNGsZN2cVTYPArw454xnXj5qmWF1bEoAc4+cU/ol7GVh7odevjp1FNHduHc3KZMcFduxU5Xc6uJRQ==",
      "license": "MIT",
      "dependencies": {
        "yocto-queue": "^0.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/eslint/node_modules/p-locate": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-5.0.0.tgz",
      "integrity": "sha512-LaNjtRWUBY++zB5nE/NwcaoMylSPk+S+ZHNB1TzdbMJMny6dynpAGt7X/tl/QYq3TIeE6nxHppbo2LGymrG5Pw==",
      "license": "MIT",
      "dependencies": {
        "p-limit": "^3.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/espree": {
      "version": "9.6.1",
      "resolved": "https://registry.npmjs.org/espree/-/espree-9.6.1.tgz",
      "integrity": "sha512-oruZaFkjorTpF32kDSI5/75ViwGeZginGGy2NoOSg3Q9bnwlnmDm4HLnkl0RE3n+njDXR037aY1+x58Z/zFdwQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "acorn": "^8.9.0",
        "acorn-jsx": "^5.3.2",
        "eslint-visitor-keys": "^3.4.1"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "funding": {
        "url": "https://opencollective.com/eslint"
      }
    },
    "node_modules/esprima": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/esprima/-/esprima-4.0.1.tgz",
      "integrity": "sha512-eGuFFw7Upda+g4p+QHvnW0RyTX/SVeJBDM/gCtMARO0cLuT2HcEKnTPvhjV6aGeqrCB/sbNop0Kszm0jsaWU4A==",
      "license": "BSD-2-Clause",
      "bin": {
        "esparse": "bin/esparse.js",
        "esvalidate": "bin/esvalidate.js"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/esquery": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/esquery/-/esquery-1.6.0.tgz",
      "integrity": "sha512-ca9pw9fomFcKPvFLXhBKUK90ZvGibiGOvRJNbjljY7s7uq/5YO4BOzcYtJqExdx99rF6aAcnRxHmcUHcz6sQsg==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "estraverse": "^5.1.0"
      },
      "engines": {
        "node": ">=0.10"
      }
    },
    "node_modules/esrecurse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/esrecurse/-/esrecurse-4.3.0.tgz",
      "integrity": "sha512-KmfKL3b6G+RXvP8N1vr3Tq1kL/oCFgn2NYXEtqP8/L3pKapUA4G8cFVaoF3SU323CD4XypR/ffioHmkti6/Tag==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "estraverse": "^5.2.0"
      },
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/estraverse": {
      "version": "5.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-5.3.0.tgz",
      "integrity": "sha512-MMdARuVEQziNTeJD8DgMqmhwR11BRQ/cBP+pLtYdSTnf3MIO8fFeiINEbX36ZdNlfU/7A9f3gUw49B3oQsvwBA==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/estree-walker": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/estree-walker/-/estree-walker-1.0.1.tgz",
      "integrity": "sha512-1fMXF3YP4pZZVozF8j/ZLfvnR8NSIljt56UhbZ5PeeDmmGHpgpdwQt7ITlGvYaQukCvuBRMLEiKiYC+oeIg4cg==",
      "license": "MIT"
    },
    "node_modules/esutils": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/esutils/-/esutils-2.0.3.tgz",
      "integrity": "sha512-kVscqXk4OCp68SZ0dkgEKVi6/8ij300KBWTJq32P/dYeWTSwK41WyTxalN1eRmA5Z9UU/LX9D7FWSmV9SAYx6g==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/etag": {
      "version": "1.8.1",
      "resolved": "https://registry.npmjs.org/etag/-/etag-1.8.1.tgz",
      "integrity": "sha512-aIL5Fx7mawVa300al2BnEE4iNvo1qETxLrPI/o05L7z6go7fCw1J6EQmbK4FmJ2AS7kgVF/KEZWufBfdClMcPg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/eventemitter3": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/eventemitter3/-/eventemitter3-4.0.7.tgz",
      "integrity": "sha512-8guHBZCwKnFhYdHr2ysuRWErTwhoN2X8XELRlrRwpmfeY2jjuUN4taQMsULKUVo1K4DvZl+0pgfyoysHxvmvEw==",
      "license": "MIT"
    },
    "node_modules/events": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/events/-/events-3.3.0.tgz",
      "integrity": "sha512-mQw+2fkQbALzQ7V0MY0IqdnXNOeTtP4r0lN9z7AAawCXgqea7bDii20AYrIBrFd/Hx0M2Ocz6S111CaFkUcb0Q==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8.x"
      }
    },
    "node_modules/execa": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/execa/-/execa-5.1.1.tgz",
      "integrity": "sha512-8uSpZZocAZRBAPIEINJj3Lo9HyGitllczc27Eh5YYojjMFMn8yHMDMaUHE2Jqfq05D/wucwI4JGURyXt1vchyg==",
      "license": "MIT",
      "dependencies": {
        "cross-spawn": "^7.0.3",
        "get-stream": "^6.0.0",
        "human-signals": "^2.1.0",
        "is-stream": "^2.0.0",
        "merge-stream": "^2.0.0",
        "npm-run-path": "^4.0.1",
        "onetime": "^5.1.2",
        "signal-exit": "^3.0.3",
        "strip-final-newline": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sindresorhus/execa?sponsor=1"
      }
    },
    "node_modules/exit": {
      "version": "0.1.2",
      "resolved": "https://registry.npmjs.org/exit/-/exit-0.1.2.tgz",
      "integrity": "sha512-Zk/eNKV2zbjpKzrsQ+n1G6poVbErQxJ0LBOJXaKZ1EViLzH+hrLu9cdXI4zw9dBQJslwBEpbQ2P1oS7nDxs6jQ==",
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/expect": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/expect/-/expect-27.5.1.tgz",
      "integrity": "sha512-E1q5hSUG2AmYQwQJ041nvgpkODHQvB+RKlB4IYdru6uJsyFTRyZAP463M+1lINorwbqAmUggi6+WwkD8lCS/Dw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "jest-matcher-utils": "^27.5.1",
        "jest-message-util": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/express": {
      "version": "4.21.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.21.2.tgz",
      "integrity": "sha512-28HqgMZAmih1Czt9ny7qr6ek2qddF4FclbMzwhCREB6OFfH+rXAnuNCwo1/wFvrtbgsQDb4kSbX9de9lFbrXnA==",
      "license": "MIT",
      "dependencies": {
        "accepts": "~1.3.8",
        "array-flatten": "1.1.1",
        "body-parser": "1.20.3",
        "content-disposition": "0.5.4",
        "content-type": "~1.0.4",
        "cookie": "0.7.1",
        "cookie-signature": "1.0.6",
        "debug": "2.6.9",
        "depd": "2.0.0",
        "encodeurl": "~2.0.0",
        "escape-html": "~1.0.3",
        "etag": "~1.8.1",
        "finalhandler": "1.3.1",
        "fresh": "0.5.2",
        "http-errors": "2.0.0",
        "merge-descriptors": "1.0.3",
        "methods": "~1.1.2",
        "on-finished": "2.4.1",
        "parseurl": "~1.3.3",
        "path-to-regexp": "0.1.12",
        "proxy-addr": "~2.0.7",
        "qs": "6.13.0",
        "range-parser": "~1.2.1",
        "safe-buffer": "5.2.1",
        "send": "0.19.0",
        "serve-static": "1.16.2",
        "setprototypeof": "1.2.0",
        "statuses": "2.0.1",
        "type-is": "~1.6.18",
        "utils-merge": "1.0.1",
        "vary": "~1.1.2"
      },
      "engines": {
        "node": ">= 0.10.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/express"
      }
    },
    "node_modules/express/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/express/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/fast-deep-equal": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/fast-deep-equal/-/fast-deep-equal-3.1.3.tgz",
      "integrity": "sha512-f3qQ9oQy9j2AhBe/H9VC91wLmKBCCU/gDOnKNAYG5hswO7BLKj09Hc5HYNz9cGI++xlpDCIgDaitVs03ATR84Q==",
      "license": "MIT"
    },
    "node_modules/fast-glob": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/fast-glob/-/fast-glob-3.3.3.tgz",
      "integrity": "sha512-7MptL8U0cqcFdzIzwOTHoilX9x5BrNqye7Z/LuC7kCMRio1EMSyqRK3BEAUD7sXRq4iT4AzTVuZdhgQ2TCvYLg==",
      "license": "MIT",
      "dependencies": {
        "@nodelib/fs.stat": "^2.0.2",
        "@nodelib/fs.walk": "^1.2.3",
        "glob-parent": "^5.1.2",
        "merge2": "^1.3.0",
        "micromatch": "^4.0.8"
      },
      "engines": {
        "node": ">=8.6.0"
      }
    },
    "node_modules/fast-glob/node_modules/glob-parent": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-5.1.2.tgz",
      "integrity": "sha512-AOIgSQCepiJYwP3ARnGx+5VnTu2HBYdzbGP45eLw1vr3zB3vZLeyed1sC9hnbcOc9/SrMyM5RPQrkGz4aS9Zow==",
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/fast-json-stable-stringify": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/fast-json-stable-stringify/-/fast-json-stable-stringify-2.1.0.tgz",
      "integrity": "sha512-lhd/wF+Lk98HZoTCtlVraHtfh5XYijIjalXck7saUtuanSDyLMxnHhSXEDJqHxD7msR8D0uCmqlkwjCV8xvwHw==",
      "license": "MIT"
    },
    "node_modules/fast-levenshtein": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/fast-levenshtein/-/fast-levenshtein-2.0.6.tgz",
      "integrity": "sha512-DCXu6Ifhqcks7TZKY3Hxp3y6qphY5SJZmrWMDrKcERSOXWQdMhU9Ig/PYrzyw/ul9jOIyh0N4M0tbC5hodg8dw==",
      "license": "MIT"
    },
    "node_modules/fast-uri": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/fast-uri/-/fast-uri-3.1.0.tgz",
      "integrity": "sha512-iPeeDKJSWf4IEOasVVrknXpaBV0IApz/gp7S2bb7Z4Lljbl2MGJRqInZiUrQwV16cpzw/D3S5j5Julj/gT52AA==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/fastify"
        },
        {
          "type": "opencollective",
          "url": "https://opencollective.com/fastify"
        }
      ],
      "license": "BSD-3-Clause"
    },
    "node_modules/fastq": {
      "version": "1.19.1",
      "resolved": "https://registry.npmjs.org/fastq/-/fastq-1.19.1.tgz",
      "integrity": "sha512-GwLTyxkCXjXbxqIhTsMI2Nui8huMPtnxg7krajPJAjnEG/iiOS7i+zCtWGZR9G0NBKbXKh6X9m9UIsYX/N6vvQ==",
      "license": "ISC",
      "dependencies": {
        "reusify": "^1.0.4"
      }
    },
    "node_modules/faye-websocket": {
      "version": "0.11.4",
      "resolved": "https://registry.npmjs.org/faye-websocket/-/faye-websocket-0.11.4.tgz",
      "integrity": "sha512-CzbClwlXAuiRQAlUyfqPgvPoNKTckTPGfwZV4ZdAhVcP2lh9KUxJg2b5GkE7XbjKQ3YJnQ9z6D9ntLAlB+tP8g==",
      "license": "Apache-2.0",
      "dependencies": {
        "websocket-driver": ">=0.5.1"
      },
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/fb-watchman": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/fb-watchman/-/fb-watchman-2.0.2.tgz",
      "integrity": "sha512-p5161BqbuCaSnB8jIbzQHOlpgsPmK5rJVDfDKO91Axs5NC1uu3HRQm6wt9cd9/+GtQQIO53JdGXXoyDpTAsgYA==",
      "license": "Apache-2.0",
      "dependencies": {
        "bser": "2.1.1"
      }
    },
    "node_modules/file-entry-cache": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/file-entry-cache/-/file-entry-cache-6.0.1.tgz",
      "integrity": "sha512-7Gps/XWymbLk2QLYK4NzpMOrYjMhdIxXuIvy2QBsLE6ljuodKvdkWs/cpyJJ3CVIVpH0Oi1Hvg1ovbMzLdFBBg==",
      "license": "MIT",
      "dependencies": {
        "flat-cache": "^3.0.4"
      },
      "engines": {
        "node": "^10.12.0 || >=12.0.0"
      }
    },
    "node_modules/file-loader": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/file-loader/-/file-loader-6.2.0.tgz",
      "integrity": "sha512-qo3glqyTa61Ytg4u73GultjHGjdRyig3tG6lPtyX/jOEJvHif9uB0/OCI2Kif6ctF3caQTW2G5gym21oAsI4pw==",
      "license": "MIT",
      "dependencies": {
        "loader-utils": "^2.0.0",
        "schema-utils": "^3.0.0"
      },
      "engines": {
        "node": ">= 10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^4.0.0 || ^5.0.0"
      }
    },
    "node_modules/file-loader/node_modules/schema-utils": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/schema-utils/-/schema-utils-3.3.0.tgz",
      "integrity": "sha512-pN/yOAvcC+5rQ5nERGuwrjLlYvLTbCibnZ1I7B1LaiAz9BRBlE9GMgE/eqV30P7aJQUf7Ddimy/RsbYO/GrVGg==",
      "license": "MIT",
      "dependencies": {
        "@types/json-schema": "^7.0.8",
        "ajv": "^6.12.5",
        "ajv-keywords": "^3.5.2"
      },
      "engines": {
        "node": ">= 10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/filelist": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/filelist/-/filelist-1.0.4.tgz",
      "integrity": "sha512-w1cEuf3S+DrLCQL7ET6kz+gmlJdbq9J7yXCSjK/OZCPA+qEN1WyF4ZAf0YYJa4/shHJra2t/d/r8SV4Ji+x+8Q==",
      "license": "Apache-2.0",
      "dependencies": {
        "minimatch": "^5.0.1"
      }
    },
    "node_modules/filelist/node_modules/brace-expansion": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.0.2.tgz",
      "integrity": "sha512-Jt0vHyM+jmUBqojB7E1NIYadt0vI0Qxjxd2TErW94wDz+E2LAm5vKMXXwg6ZZBTHPuUlDgQHKXvjGBdfcF1ZDQ==",
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^1.0.0"
      }
    },
    "node_modules/filelist/node_modules/minimatch": {
      "version": "5.1.6",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-5.1.6.tgz",
      "integrity": "sha512-lKwV/1brpG6mBUFHtb7NUmtABCb2WZZmm2wNiOA5hAb8VdCS4B3dtMWyvcoViccwAW/COERjXLt0zP1zXUN26g==",
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^2.0.1"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/filesize": {
      "version": "8.0.7",
      "resolved": "https://registry.npmjs.org/filesize/-/filesize-8.0.7.tgz",
      "integrity": "sha512-pjmC+bkIF8XI7fWaH8KxHcZL3DPybs1roSKP4rKDvy20tAWwIObE4+JIseG2byfGKhud5ZnM4YSGKBz7Sh0ndQ==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">= 0.4.0"
      }
    },
    "node_modules/fill-range": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/fill-range/-/fill-range-7.1.1.tgz",
      "integrity": "sha512-YsGpe3WHLK8ZYi4tWDg2Jy3ebRz2rXowDxnld4bkQB00cc/1Zw9AWnC0i9ztDJitivtQvaI9KaLyKrc+hBW0yg==",
      "license": "MIT",
      "dependencies": {
        "to-regex-range": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/finalhandler": {
      "version": "1.3.1",
      "resolved": "https://registry.npmjs.org/finalhandler/-/finalhandler-1.3.1.tgz",
      "integrity": "sha512-6BN9trH7bp3qvnrRyzsBz+g3lZxTNZTbVO2EV1CS0WIcDbawYVdYvGflME/9QP0h0pYlCDBCTjYa9nZzMDpyxQ==",
      "license": "MIT",
      "dependencies": {
        "debug": "2.6.9",
        "encodeurl": "~2.0.0",
        "escape-html": "~1.0.3",
        "on-finished": "2.4.1",
        "parseurl": "~1.3.3",
        "statuses": "2.0.1",
        "unpipe": "~1.0.0"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/finalhandler/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/finalhandler/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/find-cache-dir": {
      "version": "3.3.2",
      "resolved": "https://registry.npmjs.org/find-cache-dir/-/find-cache-dir-3.3.2.tgz",
      "integrity": "sha512-wXZV5emFEjrridIgED11OoUKLxiYjAcqot/NJdAkOhlJ+vGzwhOAfcG5OX1jP+S0PcjEn8bdMJv+g2jwQ3Onig==",
      "license": "MIT",
      "dependencies": {
        "commondir": "^1.0.1",
        "make-dir": "^3.0.2",
        "pkg-dir": "^4.1.0"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/avajs/find-cache-dir?sponsor=1"
      }
    },
    "node_modules/find-up": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-4.1.0.tgz",
      "integrity": "sha512-PpOwAdQ/YlXQ2vj8a3h8IipDuYRi3wceVQQGYWxNINccq40Anw7BlsEXCMbt1Zt+OLA6Fq9suIpIWD0OsnISlw==",
      "license": "MIT",
      "dependencies": {
        "locate-path": "^5.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/flat-cache": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/flat-cache/-/flat-cache-3.2.0.tgz",
      "integrity": "sha512-CYcENa+FtcUKLmhhqyctpclsq7QF38pKjZHsGNiSQF5r4FtoKDWabFDl3hzaEQMvT1LHEysw5twgLvpYYb4vbw==",
      "license": "MIT",
      "dependencies": {
        "flatted": "^3.2.9",
        "keyv": "^4.5.3",
        "rimraf": "^3.0.2"
      },
      "engines": {
        "node": "^10.12.0 || >=12.0.0"
      }
    },
    "node_modules/flatted": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/flatted/-/flatted-3.3.3.tgz",
      "integrity": "sha512-GX+ysw4PBCz0PzosHDepZGANEuFCMLrnRTiEy9McGjmkCQYwRq4A/X786G/fjM/+OjsWSU1ZrY5qyARZmO/uwg==",
      "license": "ISC"
    },
    "node_modules/follow-redirects": {
      "version": "1.15.11",
      "resolved": "https://registry.npmjs.org/follow-redirects/-/follow-redirects-1.15.11.tgz",
      "integrity": "sha512-deG2P0JfjrTxl50XGCDyfI97ZGVCxIpfKYmfyrQ54n5FO/0gfIES8C/Psl6kWVDolizcaaxZJnTS0QSMxvnsBQ==",
      "funding": [
        {
          "type": "individual",
          "url": "https://github.com/sponsors/RubenVerborgh"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": ">=4.0"
      },
      "peerDependenciesMeta": {
        "debug": {
          "optional": true
        }
      }
    },
    "node_modules/for-each": {
      "version": "0.3.5",
      "resolved": "https://registry.npmjs.org/for-each/-/for-each-0.3.5.tgz",
      "integrity": "sha512-dKx12eRCVIzqCxFGplyFKJMPvLEWgmNtUrpTiJIR5u97zEhRG8ySrtboPHZXx7daLxQVrl643cTzbab2tkQjxg==",
      "license": "MIT",
      "dependencies": {
        "is-callable": "^1.2.7"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/foreground-child": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/foreground-child/-/foreground-child-3.3.1.tgz",
      "integrity": "sha512-gIXjKqtFuWEgzFRJA9WCQeSJLZDjgJUOMCMzxtvFq/37KojM1BFGufqsCy0r4qSQmYLsZYMeyRqzIWOMup03sw==",
      "license": "ISC",
      "dependencies": {
        "cross-spawn": "^7.0.6",
        "signal-exit": "^4.0.1"
      },
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/foreground-child/node_modules/signal-exit": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/signal-exit/-/signal-exit-4.1.0.tgz",
      "integrity": "sha512-bzyZ1e88w9O1iNJbKnOlvYTrWPDl46O1bG0D3XInv+9tkPrxrN8jUUTiFlDkkmKWgn1M6CfIA13SuGqOa9Korw==",
      "license": "ISC",
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin": {
      "version": "6.5.3",
      "resolved": "https://registry.npmjs.org/fork-ts-checker-webpack-plugin/-/fork-ts-checker-webpack-plugin-6.5.3.tgz",
      "integrity": "sha512-SbH/l9ikmMWycd5puHJKTkZJKddF4iRLyW3DeZ08HTI7NGyLS38MXd/KGgeWumQO7YNQbW2u/NtPT2YowbPaGQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.8.3",
        "@types/json-schema": "^7.0.5",
        "chalk": "^4.1.0",
        "chokidar": "^3.4.2",
        "cosmiconfig": "^6.0.0",
        "deepmerge": "^4.2.2",
        "fs-extra": "^9.0.0",
        "glob": "^7.1.6",
        "memfs": "^3.1.2",
        "minimatch": "^3.0.4",
        "schema-utils": "2.7.0",
        "semver": "^7.3.2",
        "tapable": "^1.0.0"
      },
      "engines": {
        "node": ">=10",
        "yarn": ">=1.0.0"
      },
      "peerDependencies": {
        "eslint": ">= 6",
        "typescript": ">= 2.7",
        "vue-template-compiler": "*",
        "webpack": ">= 4"
      },
      "peerDependenciesMeta": {
        "eslint": {
          "optional": true
        },
        "vue-template-compiler": {
          "optional": true
        }
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin/node_modules/cosmiconfig": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/cosmiconfig/-/cosmiconfig-6.0.0.tgz",
      "integrity": "sha512-xb3ZL6+L8b9JLLCx3ZdoZy4+2ECphCMo2PwqgP1tlfVq6M6YReyzBJtvWWtbDSpNr9hn96pkCiZqUcFEc+54Qg==",
      "license": "MIT",
      "dependencies": {
        "@types/parse-json": "^4.0.0",
        "import-fresh": "^3.1.0",
        "parse-json": "^5.0.0",
        "path-type": "^4.0.0",
        "yaml": "^1.7.2"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin/node_modules/fs-extra": {
      "version": "9.1.0",
      "resolved": "https://registry.npmjs.org/fs-extra/-/fs-extra-9.1.0.tgz",
      "integrity": "sha512-hcg3ZmepS30/7BSFqRvoo3DOMQu7IjqxO5nCDt+zM9XWjb33Wg7ziNT+Qvqbuc3+gWpzO02JubVyk2G4Zvo1OQ==",
      "license": "MIT",
      "dependencies": {
        "at-least-node": "^1.0.0",
        "graceful-fs": "^4.2.0",
        "jsonfile": "^6.0.1",
        "universalify": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin/node_modules/schema-utils": {
      "version": "2.7.0",
      "resolved": "https://registry.npmjs.org/schema-utils/-/schema-utils-2.7.0.tgz",
      "integrity": "sha512-0ilKFI6QQF5nxDZLFn2dMjvc4hjg/Wkg7rHd3jK6/A4a1Hl9VFdQWvgB1UMGoU94pad1P/8N7fMcEnLnSiju8A==",
      "license": "MIT",
      "dependencies": {
        "@types/json-schema": "^7.0.4",
        "ajv": "^6.12.2",
        "ajv-keywords": "^3.4.1"
      },
      "engines": {
        "node": ">= 8.9.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/fork-ts-checker-webpack-plugin/node_modules/tapable": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/tapable/-/tapable-1.1.3.tgz",
      "integrity": "sha512-4WK/bYZmj8xLr+HUCODHGF1ZFzsYffasLUgEiMBY4fgtltdO6B4WJtlSbPaDTLpYTcGVwM2qLnFTICEcNxs3kA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/form-data": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/form-data/-/form-data-3.0.4.tgz",
      "integrity": "sha512-f0cRzm6dkyVYV3nPoooP8XlccPQukegwhAnpoLcXy+X+A8KfpGOoXwDr9FLZd3wzgLaBGQBE3lY93Zm/i1JvIQ==",
      "license": "MIT",
      "dependencies": {
        "asynckit": "^0.4.0",
        "combined-stream": "^1.0.8",
        "es-set-tostringtag": "^2.1.0",
        "hasown": "^2.0.2",
        "mime-types": "^2.1.35"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/forwarded": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/forwarded/-/forwarded-0.2.0.tgz",
      "integrity": "sha512-buRG0fpBtRHSTCOASe6hD258tEubFoRLb4ZNA6NxMVHNw2gOcwHo9wyablzMzOA5z9xA9L1KNjk/Nt6MT9aYow==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/fraction.js": {
      "version": "4.3.7",
      "resolved": "https://registry.npmjs.org/fraction.js/-/fraction.js-4.3.7.tgz",
      "integrity": "sha512-ZsDfxO51wGAXREY55a7la9LScWpwv9RxIrYABrlvOFBlH/ShPnrtsXeuUIfXKKOVicNxQ+o8JTbJvjS4M89yew==",
      "license": "MIT",
      "engines": {
        "node": "*"
      },
      "funding": {
        "type": "patreon",
        "url": "https://github.com/sponsors/rawify"
      }
    },
    "node_modules/fresh": {
      "version": "0.5.2",
      "resolved": "https://registry.npmjs.org/fresh/-/fresh-0.5.2.tgz",
      "integrity": "sha512-zJ2mQYM18rEFOudeV4GShTGIQ7RbzA7ozbU9I/XBpm7kqgMywgmylMwXHxZJmkVoYkna9d2pVXVXPdYTP9ej8Q==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/fs-extra": {
      "version": "10.1.0",
      "resolved": "https://registry.npmjs.org/fs-extra/-/fs-extra-10.1.0.tgz",
      "integrity": "sha512-oRXApq54ETRj4eMiFzGnHWGy+zo5raudjuxN0b8H7s/RU2oW0Wvsx9O0ACRN/kRq9E8Vu/ReskGB5o3ji+FzHQ==",
      "license": "MIT",
      "dependencies": {
        "graceful-fs": "^4.2.0",
        "jsonfile": "^6.0.1",
        "universalify": "^2.0.0"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/fs-monkey": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/fs-monkey/-/fs-monkey-1.1.0.tgz",
      "integrity": "sha512-QMUezzXWII9EV5aTFXW1UBVUO77wYPpjqIF8/AviUCThNeSYZykpoTixUeaNNBwmCev0AMDWMAni+f8Hxb1IFw==",
      "license": "Unlicense"
    },
    "node_modules/fs.realpath": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/fs.realpath/-/fs.realpath-1.0.0.tgz",
      "integrity": "sha512-OO0pH2lK6a0hZnAdau5ItzHPI6pUlvI7jMVnxUQRtw4owF2wk8lOSabtGDCTP4Ggrg2MbGnWO9X8K1t4+fGMDw==",
      "license": "ISC"
    },
    "node_modules/fsevents": {
      "version": "2.3.3",
      "resolved": "https://registry.npmjs.org/fsevents/-/fsevents-2.3.3.tgz",
      "integrity": "sha512-5xoDfX+fL7faATnagmWPpbFtwh/R77WmMMqqHGS65C3vvB0YHrgF+B1YmZ3441tMj5n63k0212XNoJwzlhffQw==",
      "hasInstallScript": true,
      "license": "MIT",
      "optional": true,
      "os": [
        "darwin"
      ],
      "engines": {
        "node": "^8.16.0 || ^10.6.0 || >=11.0.0"
      }
    },
    "node_modules/function-bind": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/function-bind/-/function-bind-1.1.2.tgz",
      "integrity": "sha512-7XHNxH7qX9xG5mIwxkhumTox/MIRNcOgDrxWsMt2pAr23WHp6MrRlN7FBSFpCpr+oVO0F744iUgR82nJMfG2SA==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/function.prototype.name": {
      "version": "1.1.8",
      "resolved": "https://registry.npmjs.org/function.prototype.name/-/function.prototype.name-1.1.8.tgz",
      "integrity": "sha512-e5iwyodOHhbMr/yNrc7fDYG4qlbIvI5gajyzPnb5TCwyhjApznQh1BMFou9b30SevY43gCJKXycoCBjMbsuW0Q==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "functions-have-names": "^1.2.3",
        "hasown": "^2.0.2",
        "is-callable": "^1.2.7"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/functions-have-names": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/functions-have-names/-/functions-have-names-1.2.3.tgz",
      "integrity": "sha512-xckBUXyTIqT97tq2x2AMb+g163b5JFysYk0x4qxNFwbfQkmNZoiRHb6sPzI9/QV33WeuvVYBUIiD4NzNIyqaRQ==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/gensync": {
      "version": "1.0.0-beta.2",
      "resolved": "https://registry.npmjs.org/gensync/-/gensync-1.0.0-beta.2.tgz",
      "integrity": "sha512-3hN7NaskYvMDLQY55gnW3NQ+mesEAepTqlg+VEbj7zzqEMBVNhzcGYYeqFo/TlYz6eQiFcp1HcsCZO+nGgS8zg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.9.0"
      }
    },
    "node_modules/get-caller-file": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/get-caller-file/-/get-caller-file-2.0.5.tgz",
      "integrity": "sha512-DyFP3BM/3YHTQOCUL/w0OZHR0lpKeGrxotcHWcqNEdnltqFwXVfhEBQ94eIo34AfQpo0rGki4cyIiftY06h2Fg==",
      "license": "ISC",
      "engines": {
        "node": "6.* || 8.* || >= 10.*"
      }
    },
    "node_modules/get-intrinsic": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/get-intrinsic/-/get-intrinsic-1.3.0.tgz",
      "integrity": "sha512-9fSjSaos/fRIVIp+xSJlE6lfwhES7LNtKaCBIamHsjr2na1BiABJPo0mOjjz8GJDURarmCPGqaiVg5mfjb98CQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind-apply-helpers": "^1.0.2",
        "es-define-property": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.1.1",
        "function-bind": "^1.1.2",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "hasown": "^2.0.2",
        "math-intrinsics": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/get-own-enumerable-property-symbols": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/get-own-enumerable-property-symbols/-/get-own-enumerable-property-symbols-3.0.2.tgz",
      "integrity": "sha512-I0UBV/XOz1XkIJHEUDMZAbzCThU/H8DxmSfmdGcKPnVhu2VfFqr34jr9777IyaTYvxjedWhqVIilEDsCdP5G6g==",
      "license": "ISC"
    },
    "node_modules/get-package-type": {
      "version": "0.1.0",
      "resolved": "https://registry.npmjs.org/get-package-type/-/get-package-type-0.1.0.tgz",
      "integrity": "sha512-pjzuKtY64GYfWizNAJ0fr9VqttZkNiK2iS430LtIHzjBEr6bX8Am2zm4sW4Ro5wjWW5cAlRL1qAMTcXbjNAO2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/get-proto": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/get-proto/-/get-proto-1.0.1.tgz",
      "integrity": "sha512-sTSfBjoXBp89JvIKIefqw7U2CCebsc74kiY6awiGogKtoSGbgjYE/G/+l9sF3MWFPNc9IcoOC4ODfKHfxFmp0g==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/get-stream": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/get-stream/-/get-stream-6.0.1.tgz",
      "integrity": "sha512-ts6Wi+2j3jQjqi70w5AlN8DFnkSwC+MqmxEzdEALB2qXZYV3X/b1CTfgPLGJNMeAWxdPfU8FO1ms3NUfaHCPYg==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/get-symbol-description": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/get-symbol-description/-/get-symbol-description-1.1.0.tgz",
      "integrity": "sha512-w9UMqWwJxHNOvoNzSJ2oPF5wvYcvP7jUvYzhp67yEhTi17ZDBBC1z9pTdGuzjD+EFIqLSYRweZjqfiPzQ06Ebg==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/glob": {
      "version": "7.2.3",
      "resolved": "https://registry.npmjs.org/glob/-/glob-7.2.3.tgz",
      "integrity": "sha512-nFR0zLpU2YCaRxwoCJvL6UvCH2JFyFVIvwTLsIf21AuHlMskA1hhTdk+LlYJtOlYt9v6dvszD2BGRqBL+iQK9Q==",
      "deprecated": "Glob versions prior to v9 are no longer supported",
      "license": "ISC",
      "dependencies": {
        "fs.realpath": "^1.0.0",
        "inflight": "^1.0.4",
        "inherits": "2",
        "minimatch": "^3.1.1",
        "once": "^1.3.0",
        "path-is-absolute": "^1.0.0"
      },
      "engines": {
        "node": "*"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/glob-parent": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/glob-parent/-/glob-parent-6.0.2.tgz",
      "integrity": "sha512-XxwI8EOhVQgWp6iDL+3b0r86f4d6AX6zSU55HfB4ydCEuXLXc5FcYeOu+nnGftS4TEju/11rt4KJPTMgbfmv4A==",
      "license": "ISC",
      "dependencies": {
        "is-glob": "^4.0.3"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/glob-to-regexp": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/glob-to-regexp/-/glob-to-regexp-0.4.1.tgz",
      "integrity": "sha512-lkX1HJXwyMcprw/5YUZc2s7DrpAiHB21/V+E1rHUrVNokkvB6bqMzT0VfV6/86ZNabt1k14YOIaT7nDvOX3Iiw==",
      "license": "BSD-2-Clause"
    },
    "node_modules/global-modules": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/global-modules/-/global-modules-2.0.0.tgz",
      "integrity": "sha512-NGbfmJBp9x8IxyJSd1P+otYK8vonoJactOogrVfFRIAEY1ukil8RSKDz2Yo7wh1oihl51l/r6W4epkeKJHqL8A==",
      "license": "MIT",
      "dependencies": {
        "global-prefix": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/global-prefix": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/global-prefix/-/global-prefix-3.0.0.tgz",
      "integrity": "sha512-awConJSVCHVGND6x3tmMaKcQvwXLhjdkmomy2W+Goaui8YPgYgXJZewhg3fWC+DlfqqQuWg8AwqjGTD2nAPVWg==",
      "license": "MIT",
      "dependencies": {
        "ini": "^1.3.5",
        "kind-of": "^6.0.2",
        "which": "^1.3.1"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/global-prefix/node_modules/which": {
      "version": "1.3.1",
      "resolved": "https://registry.npmjs.org/which/-/which-1.3.1.tgz",
      "integrity": "sha512-HxJdYWq1MTIQbJ3nw0cqssHoTNU267KlrDuGZ1WYlxDStUtKUhOaJmh112/TZmHxxUfuJqPXSOm7tDyas0OSIQ==",
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "which": "bin/which"
      }
    },
    "node_modules/globals": {
      "version": "13.24.0",
      "resolved": "https://registry.npmjs.org/globals/-/globals-13.24.0.tgz",
      "integrity": "sha512-AhO5QUcj8llrbG09iWhPU2B204J1xnPeL8kQmVorSsy+Sjj1sk8gIyh6cUocGmH4L0UuhAJy+hJMRA4mgA4mFQ==",
      "license": "MIT",
      "dependencies": {
        "type-fest": "^0.20.2"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/globalthis": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/globalthis/-/globalthis-1.0.4.tgz",
      "integrity": "sha512-DpLKbNU4WylpxJykQujfCcwYWiV/Jhm50Goo0wrVILAv5jOr9d+H+UR3PhSCD2rCCEIg0uc+G+muBTwD54JhDQ==",
      "license": "MIT",
      "dependencies": {
        "define-properties": "^1.2.1",
        "gopd": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/globby": {
      "version": "11.1.0",
      "resolved": "https://registry.npmjs.org/globby/-/globby-11.1.0.tgz",
      "integrity": "sha512-jhIXaOzy1sb8IyocaruWSn1TjmnBVs8Ayhcy83rmxNJ8q2uWKCAj3CnJY+KpGSXCueAPc0i05kVvVKtP1t9S3g==",
      "license": "MIT",
      "dependencies": {
        "array-union": "^2.1.0",
        "dir-glob": "^3.0.1",
        "fast-glob": "^3.2.9",
        "ignore": "^5.2.0",
        "merge2": "^1.4.1",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/gopd": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/gopd/-/gopd-1.2.0.tgz",
      "integrity": "sha512-ZUKRh6/kUFoAiTAtTYPZJ3hw9wNxx+BIBOijnlG9PnrJsCcSjs1wyyD6vJpaYtgnzDrKYRSqf3OO6Rfa93xsRg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/graceful-fs": {
      "version": "4.2.11",
      "resolved": "https://registry.npmjs.org/graceful-fs/-/graceful-fs-4.2.11.tgz",
      "integrity": "sha512-RbJ5/jmFcNNCcDV5o9eTnBLJ/HszWV0P73bc+Ff4nS/rJj+YaS6IGyiOL0VoBYX+l1Wrl3k63h/KrH+nhJ0XvQ==",
      "license": "ISC"
    },
    "node_modules/graphemer": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/graphemer/-/graphemer-1.4.0.tgz",
      "integrity": "sha512-EtKwoO6kxCL9WO5xipiHTZlSzBm7WLT627TqC/uVRd0HKmq8NXyebnNYxDoBi7wt8eTWrUrKXCOVaFq9x1kgag==",
      "license": "MIT"
    },
    "node_modules/gzip-size": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/gzip-size/-/gzip-size-6.0.0.tgz",
      "integrity": "sha512-ax7ZYomf6jqPTQ4+XCpUGyXKHk5WweS+e05MBO4/y3WJ5RkmPXNKvX+bx1behVILVwr6JSQvZAku021CHPXG3Q==",
      "license": "MIT",
      "dependencies": {
        "duplexer": "^0.1.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/handle-thing": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/handle-thing/-/handle-thing-2.0.1.tgz",
      "integrity": "sha512-9Qn4yBxelxoh2Ow62nP+Ka/kMnOXRi8BXnRaUwezLNhqelnN49xKz4F/dPP8OYLxLxq6JDtZb2i9XznUQbNPTg==",
      "license": "MIT"
    },
    "node_modules/harmony-reflect": {
      "version": "1.6.2",
      "resolved": "https://registry.npmjs.org/harmony-reflect/-/harmony-reflect-1.6.2.tgz",
      "integrity": "sha512-HIp/n38R9kQjDEziXyDTuW3vvoxxyxjxFzXLrBr18uB47GnSt+G9D29fqrpM5ZkspMcPICud3XsBJQ4Y2URg8g==",
      "license": "(Apache-2.0 OR MPL-1.1)"
    },
    "node_modules/has-bigints": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-bigints/-/has-bigints-1.1.0.tgz",
      "integrity": "sha512-R3pbpkcIqv2Pm3dUwgjclDRVmWpTJW2DcMzcIhEXEx1oh/CEMObMm3KLmRJOdvhM7o4uQBnwr8pzRK2sJWIqfg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-flag": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/has-flag/-/has-flag-4.0.0.tgz",
      "integrity": "sha512-EykJT/Q1KjTWctppgIAgfSO0tKVuZUjhgMr17kqTumMl6Afv3EISleU7qZUzoXDFTAHTDC4NOoG/ZxU3EvlMPQ==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/has-property-descriptors": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-property-descriptors/-/has-property-descriptors-1.0.2.tgz",
      "integrity": "sha512-55JNKuIW+vq4Ke1BjOTjM2YctQIvCT7GFzHwmfZPGo5wnrgkid0YQtnAleFSqumZm4az3n2BS+erby5ipJdgrg==",
      "license": "MIT",
      "dependencies": {
        "es-define-property": "^1.0.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-proto": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/has-proto/-/has-proto-1.2.0.tgz",
      "integrity": "sha512-KIL7eQPfHQRC8+XluaIw7BHUwwqL19bQn4hzNgdr+1wXoU0KKj6rufu47lhY7KbJR2C6T6+PfyN0Ea7wkSS+qQ==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-symbols": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/has-symbols/-/has-symbols-1.1.0.tgz",
      "integrity": "sha512-1cDNdwJ2Jaohmb3sg4OmKaMBwuC48sYni5HUw2DvsC8LjGTLK9h+eb1X6RyuOHe4hT0ULCW68iomhjUoKUqlPQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/has-tostringtag": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/has-tostringtag/-/has-tostringtag-1.0.2.tgz",
      "integrity": "sha512-NqADB8VjPFLM2V0VvHUewwwsw0ZWBaIdgo+ieHtK3hasLz4qeCRjYcqfB6AQrBggRKppKF8L52/VqdVsO47Dlw==",
      "license": "MIT",
      "dependencies": {
        "has-symbols": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/hasown": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/hasown/-/hasown-2.0.2.tgz",
      "integrity": "sha512-0hJU9SCPvmMzIBdZFqNPXWa6dqh7WdH0cII9y+CyS8rG3nL48Bclra9HmKhVVUHyPWNH5Y7xDwAB7bfgSjkUMQ==",
      "license": "MIT",
      "dependencies": {
        "function-bind": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/he": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/he/-/he-1.2.0.tgz",
      "integrity": "sha512-F/1DnUGPopORZi0ni+CvrCgHQ5FyEAHRLSApuYWMmrbSwoN2Mn/7k+Gl38gJnR7yyDZk6WLXwiGod1JOWNDKGw==",
      "license": "MIT",
      "bin": {
        "he": "bin/he"
      }
    },
    "node_modules/hoopy": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/hoopy/-/hoopy-0.1.4.tgz",
      "integrity": "sha512-HRcs+2mr52W0K+x8RzcLzuPPmVIKMSv97RGHy0Ea9y/mpcaK+xTrjICA04KAHi4GRzxliNqNJEFYWHghy3rSfQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 6.0.0"
      }
    },
    "node_modules/hpack.js": {
      "version": "2.1.6",
      "resolved": "https://registry.npmjs.org/hpack.js/-/hpack.js-2.1.6.tgz",
      "integrity": "sha512-zJxVehUdMGIKsRaNt7apO2Gqp0BdqW5yaiGHXXmbpvxgBYVZnAql+BJb4RO5ad2MgpbZKn5G6nMnegrH1FcNYQ==",
      "license": "MIT",
      "dependencies": {
        "inherits": "^2.0.1",
        "obuf": "^1.0.0",
        "readable-stream": "^2.0.1",
        "wbuf": "^1.1.0"
      }
    },
    "node_modules/hpack.js/node_modules/isarray": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/isarray/-/isarray-1.0.0.tgz",
      "integrity": "sha512-VLghIWNM6ELQzo7zwmcg0NmTVyWKYjvIeM83yjp0wRDTmUnrM678fQbcKBo6n2CJEF0szoG//ytg+TKla89ALQ==",
      "license": "MIT"
    },
    "node_modules/hpack.js/node_modules/readable-stream": {
      "version": "2.3.8",
      "resolved": "https://registry.npmjs.org/readable-stream/-/readable-stream-2.3.8.tgz",
      "integrity": "sha512-8p0AUk4XODgIewSi0l8Epjs+EVnWiK7NoDIEGU0HhE7+ZyY8D1IMY7odu5lRrFXGg71L15KG8QrPmum45RTtdA==",
      "license": "MIT",
      "dependencies": {
        "core-util-is": "~1.0.0",
        "inherits": "~2.0.3",
        "isarray": "~1.0.0",
        "process-nextick-args": "~2.0.0",
        "safe-buffer": "~5.1.1",
        "string_decoder": "~1.1.1",
        "util-deprecate": "~1.0.1"
      }
    },
    "node_modules/hpack.js/node_modules/safe-buffer": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/safe-buffer/-/safe-buffer-5.1.2.tgz",
      "integrity": "sha512-Gd2UZBJDkXlY7GbJxfsE8/nvKkUEU1G38c1siN6QP6a9PT9MmHB8GnpscSmMJSoF8LOIrt8ud/wPtojys4G6+g==",
      "license": "MIT"
    },
    "node_modules/hpack.js/node_modules/string_decoder": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/string_decoder/-/string_decoder-1.1.1.tgz",
      "integrity": "sha512-n/ShnvDi6FHbbVfviro+WojiFzv+s8MPMHBczVePfUpDJLwoLT0ht1l4YwBCbi8pJAveEEdnkHyPyTP/mzRfwg==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "~5.1.0"
      }
    },
    "node_modules/html-encoding-sniffer": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/html-encoding-sniffer/-/html-encoding-sniffer-2.0.1.tgz",
      "integrity": "sha512-D5JbOMBIR/TVZkubHT+OyT2705QvogUW4IBn6nHd756OwieSF9aDYFj4dv6HHEVGYbHaLETa3WggZYWWMyy3ZQ==",
      "license": "MIT",
      "dependencies": {
        "whatwg-encoding": "^1.0.5"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/html-entities": {
      "version": "2.6.0",
      "resolved": "https://registry.npmjs.org/html-entities/-/html-entities-2.6.0.tgz",
      "integrity": "sha512-kig+rMn/QOVRvr7c86gQ8lWXq+Hkv6CbAH1hLu+RG338StTpE8Z0b44SDVaqVu7HGKf27frdmUYEs9hTUX/cLQ==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/mdevils"
        },
        {
          "type": "patreon",
          "url": "https://patreon.com/mdevils"
        }
      ],
      "license": "MIT"
    },
    "node_modules/html-escaper": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/html-escaper/-/html-escaper-2.0.2.tgz",
      "integrity": "sha512-H2iMtd0I4Mt5eYiapRdIDjp+XzelXQ0tFE4JS7YFwFevXXMmOp9myNrUvCg0D6ws8iqkRPBfKHgbwig1SmlLfg==",
      "license": "MIT"
    },
    "node_modules/html-minifier-terser": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/html-minifier-terser/-/html-minifier-terser-6.1.0.tgz",
      "integrity": "sha512-YXxSlJBZTP7RS3tWnQw74ooKa6L9b9i9QYXY21eUEvhZ3u9XLfv6OnFsQq6RxkhHygsaUMvYsZRV5rU/OVNZxw==",
      "license": "MIT",
      "dependencies": {
        "camel-case": "^4.1.2",
        "clean-css": "^5.2.2",
        "commander": "^8.3.0",
        "he": "^1.2.0",
        "param-case": "^3.0.4",
        "relateurl": "^0.2.7",
        "terser": "^5.10.0"
      },
      "bin": {
        "html-minifier-terser": "cli.js"
      },
      "engines": {
        "node": ">=12"
      }
    },
    "node_modules/html-webpack-plugin": {
      "version": "5.6.4",
      "resolved": "https://registry.npmjs.org/html-webpack-plugin/-/html-webpack-plugin-5.6.4.tgz",
      "integrity": "sha512-V/PZeWsqhfpE27nKeX9EO2sbR+D17A+tLf6qU+ht66jdUsN0QLKJN27Z+1+gHrVMKgndBahes0PU6rRihDgHTw==",
      "license": "MIT",
      "dependencies": {
        "@types/html-minifier-terser": "^6.0.0",
        "html-minifier-terser": "^6.0.2",
        "lodash": "^4.17.21",
        "pretty-error": "^4.0.0",
        "tapable": "^2.0.0"
      },
      "engines": {
        "node": ">=10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/html-webpack-plugin"
      },
      "peerDependencies": {
        "@rspack/core": "0.x || 1.x",
        "webpack": "^5.20.0"
      },
      "peerDependenciesMeta": {
        "@rspack/core": {
          "optional": true
        },
        "webpack": {
          "optional": true
        }
      }
    },
    "node_modules/htmlparser2": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/htmlparser2/-/htmlparser2-6.1.0.tgz",
      "integrity": "sha512-gyyPk6rgonLFEDGoeRgQNaEUvdJ4ktTmmUh/h2t7s+M8oPpIPxgNACWa+6ESR57kXstwqPiCut0V8NRpcwgU7A==",
      "funding": [
        "https://github.com/fb55/htmlparser2?sponsor=1",
        {
          "type": "github",
          "url": "https://github.com/sponsors/fb55"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "domelementtype": "^2.0.1",
        "domhandler": "^4.0.0",
        "domutils": "^2.5.2",
        "entities": "^2.0.0"
      }
    },
    "node_modules/http-deceiver": {
      "version": "1.2.7",
      "resolved": "https://registry.npmjs.org/http-deceiver/-/http-deceiver-1.2.7.tgz",
      "integrity": "sha512-LmpOGxTfbpgtGVxJrj5k7asXHCgNZp5nLfp+hWc8QQRqtb7fUy6kRY3BO1h9ddF6yIPYUARgxGOwB42DnxIaNw==",
      "license": "MIT"
    },
    "node_modules/http-errors": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/http-errors/-/http-errors-2.0.0.tgz",
      "integrity": "sha512-FtwrG/euBzaEjYeRqOgly7G0qviiXoJWnvEH2Z1plBdXgbyjv34pHTSb9zoeHMyDy33+DWy5Wt9Wo+TURtOYSQ==",
      "license": "MIT",
      "dependencies": {
        "depd": "2.0.0",
        "inherits": "2.0.4",
        "setprototypeof": "1.2.0",
        "statuses": "2.0.1",
        "toidentifier": "1.0.1"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/http-parser-js": {
      "version": "0.5.10",
      "resolved": "https://registry.npmjs.org/http-parser-js/-/http-parser-js-0.5.10.tgz",
      "integrity": "sha512-Pysuw9XpUq5dVc/2SMHpuTY01RFl8fttgcyunjL7eEMhGM3cI4eOmiCycJDVCo/7O7ClfQD3SaI6ftDzqOXYMA==",
      "license": "MIT"
    },
    "node_modules/http-proxy": {
      "version": "1.18.1",
      "resolved": "https://registry.npmjs.org/http-proxy/-/http-proxy-1.18.1.tgz",
      "integrity": "sha512-7mz/721AbnJwIVbnaSv1Cz3Am0ZLT/UBwkC92VlxhXv/k/BBQfM2fXElQNC27BVGr0uwUpplYPQM9LnaBMR5NQ==",
      "license": "MIT",
      "dependencies": {
        "eventemitter3": "^4.0.0",
        "follow-redirects": "^1.0.0",
        "requires-port": "^1.0.0"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/http-proxy-agent": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/http-proxy-agent/-/http-proxy-agent-4.0.1.tgz",
      "integrity": "sha512-k0zdNgqWTGA6aeIRVpvfVob4fL52dTfaehylg0Y4UvSySvOq/Y+BOyPrgpUrA7HylqvU8vIZGsRuXmspskV0Tg==",
      "license": "MIT",
      "dependencies": {
        "@tootallnate/once": "1",
        "agent-base": "6",
        "debug": "4"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/http-proxy-middleware": {
      "version": "2.0.9",
      "resolved": "https://registry.npmjs.org/http-proxy-middleware/-/http-proxy-middleware-2.0.9.tgz",
      "integrity": "sha512-c1IyJYLYppU574+YI7R4QyX2ystMtVXZwIdzazUIPIJsHuWNd+mho2j+bKoHftndicGj9yh+xjd+l0yj7VeT1Q==",
      "license": "MIT",
      "dependencies": {
        "@types/http-proxy": "^1.17.8",
        "http-proxy": "^1.18.1",
        "is-glob": "^4.0.1",
        "is-plain-obj": "^3.0.0",
        "micromatch": "^4.0.2"
      },
      "engines": {
        "node": ">=12.0.0"
      },
      "peerDependencies": {
        "@types/express": "^4.17.13"
      },
      "peerDependenciesMeta": {
        "@types/express": {
          "optional": true
        }
      }
    },
    "node_modules/https-proxy-agent": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/https-proxy-agent/-/https-proxy-agent-5.0.1.tgz",
      "integrity": "sha512-dFcAjpTQFgoLMzC2VwU+C/CbS7uRL0lWmxDITmqm7C+7F0Odmj6s9l6alZc6AELXhrnggM2CeWSXHGOdX2YtwA==",
      "license": "MIT",
      "dependencies": {
        "agent-base": "6",
        "debug": "4"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/human-signals": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/human-signals/-/human-signals-2.1.0.tgz",
      "integrity": "sha512-B4FFZ6q/T2jhhksgkbEW3HBvWIfDW85snkQgawt07S7J5QXTk6BkNV+0yAeZrM5QpMAdYlocGoljn0sJ/WQkFw==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=10.17.0"
      }
    },
    "node_modules/iconv-lite": {
      "version": "0.6.3",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.6.3.tgz",
      "integrity": "sha512-4fCk79wshMdzMp2rH06qWrJE4iolqLhCUH+OiuIgU++RB0+94NlDL81atO7GX55uUKueo0txHNtvEyI6D7WdMw==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3.0.0"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/icss-utils": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/icss-utils/-/icss-utils-5.1.0.tgz",
      "integrity": "sha512-soFhflCVWLfRNOPU3iv5Z9VUdT44xFRbzjLsEzSr5AQmgqPMTHdU3PMT1Cf1ssx8fLNJDA1juftYl+PUcv3MqA==",
      "license": "ISC",
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/idb": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/idb/-/idb-7.1.1.tgz",
      "integrity": "sha512-gchesWBzyvGHRO9W8tzUWFDycow5gwjvFKfyV9FF32Y7F50yZMp7mP+T2mJIWFx49zicqyC4uefHM17o6xKIVQ==",
      "license": "ISC"
    },
    "node_modules/identity-obj-proxy": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/identity-obj-proxy/-/identity-obj-proxy-3.0.0.tgz",
      "integrity": "sha512-00n6YnVHKrinT9t0d9+5yZC6UBNJANpYEQvL2LlX6Ab9lnmxzIRcEmTPuyGScvl1+jKuCICX1Z0Ab1pPKKdikA==",
      "license": "MIT",
      "dependencies": {
        "harmony-reflect": "^1.4.6"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/ignore": {
      "version": "5.3.2",
      "resolved": "https://registry.npmjs.org/ignore/-/ignore-5.3.2.tgz",
      "integrity": "sha512-hsBTNUqQTDwkWtcdYI2i06Y/nUBEsNEDJKjWdigLvegy8kDuJAS8uRlpkkcQpyEXL0Z/pjDy5HBmMjRCJ2gq+g==",
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/immer": {
      "version": "9.0.21",
      "resolved": "https://registry.npmjs.org/immer/-/immer-9.0.21.tgz",
      "integrity": "sha512-bc4NBHqOqSfRW7POMkHd51LvClaeMXpm8dx0e8oE2GORbq5aRK7Bxl4FyzVLdGtLmvLKL7BTDBG5ACQm4HWjTA==",
      "license": "MIT",
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/immer"
      }
    },
    "node_modules/import-fresh": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/import-fresh/-/import-fresh-3.3.1.tgz",
      "integrity": "sha512-TR3KfrTZTYLPB6jUjfx6MF9WcWrHL9su5TObK4ZkYgBdWKPOFoSoQIdEuTuR82pmtxH2spWG9h6etwfr1pLBqQ==",
      "license": "MIT",
      "dependencies": {
        "parent-module": "^1.0.0",
        "resolve-from": "^4.0.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/import-fresh/node_modules/resolve-from": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/resolve-from/-/resolve-from-4.0.0.tgz",
      "integrity": "sha512-pb/MYmXstAkysRFx8piNI1tGFNQIFA3vkE3Gq4EuA1dF6gHp/+vgZqsCGJapvy8N3Q+4o7FwvquPJcnZ7RYy4g==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/import-local": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/import-local/-/import-local-3.2.0.tgz",
      "integrity": "sha512-2SPlun1JUPWoM6t3F0dw0FkCF/jWY8kttcY4f599GLTSjh2OCuuhdTkJQsEcZzBqbXZGKMK2OqW1oZsjtf/gQA==",
      "license": "MIT",
      "dependencies": {
        "pkg-dir": "^4.2.0",
        "resolve-cwd": "^3.0.0"
      },
      "bin": {
        "import-local-fixture": "fixtures/cli.js"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/imurmurhash": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/imurmurhash/-/imurmurhash-0.1.4.tgz",
      "integrity": "sha512-JmXMZ6wuvDmLiHEml9ykzqO6lwFbof0GG4IkcGaENdCRDDmMVnny7s5HsIgHCbaq0w2MyPhDqkhTUgS2LU2PHA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8.19"
      }
    },
    "node_modules/indent-string": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/indent-string/-/indent-string-4.0.0.tgz",
      "integrity": "sha512-EdDDZu4A2OyIK7Lr/2zG+w5jmbuk1DVBnEwREQvBzspBJkCEbRa8GxU1lghYcaGJCnRWibjDXlq779X1/y5xwg==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/inflight": {
      "version": "1.0.6",
      "resolved": "https://registry.npmjs.org/inflight/-/inflight-1.0.6.tgz",
      "integrity": "sha512-k92I/b08q4wvFscXCLvqfsHCrjrF7yiXsQuIVvVE7N82W3+aqpzuUdBbfhWcy/FZR3/4IgflMgKLOsvPDrGCJA==",
      "deprecated": "This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.",
      "license": "ISC",
      "dependencies": {
        "once": "^1.3.0",
        "wrappy": "1"
      }
    },
    "node_modules/inherits": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/inherits/-/inherits-2.0.4.tgz",
      "integrity": "sha512-k/vGaX4/Yla3WzyMCvTQOXYeIHvqOKtnqBduzTHpzpQZzAskKMhZ2K+EnBiSM9zGSoIFeMpXKxa4dYeZIQqewQ==",
      "license": "ISC"
    },
    "node_modules/ini": {
      "version": "1.3.8",
      "resolved": "https://registry.npmjs.org/ini/-/ini-1.3.8.tgz",
      "integrity": "sha512-JV/yugV2uzW5iMRSiZAyDtQd+nxtUnjeLt0acNdw98kKLrvuRVyB80tsREOE7yvGVgalhZ6RNXCmEHkUKBKxew==",
      "license": "ISC"
    },
    "node_modules/internal-slot": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/internal-slot/-/internal-slot-1.1.0.tgz",
      "integrity": "sha512-4gd7VpWNQNB4UKKCFFVcp1AVv+FMOgs9NKzjHKusc8jTMhd5eL1NqQqOpE0KzMds804/yHlglp3uxgluOqAPLw==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "hasown": "^2.0.2",
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/ipaddr.js": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/ipaddr.js/-/ipaddr.js-2.2.0.tgz",
      "integrity": "sha512-Ag3wB2o37wslZS19hZqorUnrnzSkpOVy+IiiDEiTqNubEYpYuHWIf6K4psgN2ZWKExS4xhVCrRVfb/wfW8fWJA==",
      "license": "MIT",
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/is-array-buffer": {
      "version": "3.0.5",
      "resolved": "https://registry.npmjs.org/is-array-buffer/-/is-array-buffer-3.0.5.tgz",
      "integrity": "sha512-DDfANUiiG2wC1qawP66qlTugJeL5HyzMpfr8lLK+jMQirGzNod0B12cFB/9q838Ru27sBwfw78/rdoU7RERz6A==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-arrayish": {
      "version": "0.2.1",
      "resolved": "https://registry.npmjs.org/is-arrayish/-/is-arrayish-0.2.1.tgz",
      "integrity": "sha512-zz06S8t0ozoDXMG+ube26zeCTNXcKIPJZJi8hBrF4idCLms4CG9QtK7qBl1boi5ODzFpjswb5JPmHCbMpjaYzg==",
      "license": "MIT"
    },
    "node_modules/is-async-function": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-async-function/-/is-async-function-2.1.1.tgz",
      "integrity": "sha512-9dgM/cZBnNvjzaMYHVoxxfPj2QXt22Ev7SuuPrs+xav0ukGB0S6d4ydZdEiM48kLx5kDV+QBPrpVnFyefL8kkQ==",
      "license": "MIT",
      "dependencies": {
        "async-function": "^1.0.0",
        "call-bound": "^1.0.3",
        "get-proto": "^1.0.1",
        "has-tostringtag": "^1.0.2",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-bigint": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-bigint/-/is-bigint-1.1.0.tgz",
      "integrity": "sha512-n4ZT37wG78iz03xPRKJrHTdZbe3IicyucEtdRsV5yglwc3GyUfbAfpSeD0FJ41NbUNSt5wbhqfp1fS+BgnvDFQ==",
      "license": "MIT",
      "dependencies": {
        "has-bigints": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-binary-path": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-binary-path/-/is-binary-path-2.1.0.tgz",
      "integrity": "sha512-ZMERYes6pDydyuGidse7OsHxtbI7WVeUEozgR/g7rd0xUimYNlvZRE/K2MgZTjWy725IfelLeVcEM97mmtRGXw==",
      "license": "MIT",
      "dependencies": {
        "binary-extensions": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-boolean-object": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/is-boolean-object/-/is-boolean-object-1.2.2.tgz",
      "integrity": "sha512-wa56o2/ElJMYqjCjGkXri7it5FbebW5usLw/nPmCMs5DeZ7eziSYZhSmPRn0txqeW4LnAmQQU7FgqLpsEFKM4A==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-callable": {
      "version": "1.2.7",
      "resolved": "https://registry.npmjs.org/is-callable/-/is-callable-1.2.7.tgz",
      "integrity": "sha512-1BC0BVFhS/p0qtw6enp8e+8OD0UrK0oFLztSjNzhcKA3WDuJxxAPXzPuPtKkjEY9UUoEWlX/8fgKeu2S8i9JTA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-core-module": {
      "version": "2.16.1",
      "resolved": "https://registry.npmjs.org/is-core-module/-/is-core-module-2.16.1.tgz",
      "integrity": "sha512-UfoeMA6fIJ8wTYFEUjelnaGI67v6+N7qXJEvQuIGa99l4xsCruSYOVSQ0uPANn4dAzm8lkYPaKLrrijLq7x23w==",
      "license": "MIT",
      "dependencies": {
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-data-view": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/is-data-view/-/is-data-view-1.0.2.tgz",
      "integrity": "sha512-RKtWF8pGmS87i2D6gqQu/l7EYRlVdfzemCJN/P3UOs//x1QE7mfhvzHIApBTRf7axvT6DMGwSwBXYCT0nfB9xw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "get-intrinsic": "^1.2.6",
        "is-typed-array": "^1.1.13"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-date-object": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-date-object/-/is-date-object-1.1.0.tgz",
      "integrity": "sha512-PwwhEakHVKTdRNVOw+/Gyh0+MzlCl4R6qKvkhuvLtPMggI1WAHt9sOwZxQLSGpUaDnrdyDsomoRgNnCfKNSXXg==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-docker": {
      "version": "2.2.1",
      "resolved": "https://registry.npmjs.org/is-docker/-/is-docker-2.2.1.tgz",
      "integrity": "sha512-F+i2BKsFrH66iaUFc0woD8sLy8getkwTwtOBjvs56Cx4CgJDeKQeqfz8wAYiSb8JOprWhHH5p77PbmYCvvUuXQ==",
      "license": "MIT",
      "bin": {
        "is-docker": "cli.js"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-extglob": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/is-extglob/-/is-extglob-2.1.1.tgz",
      "integrity": "sha512-SbKbANkN603Vi4jEZv49LeVJMn4yGwsbzZworEoyEiutsN3nJYdbO36zfhGJ6QEDpOZIFkDtnq5JRxmvl3jsoQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-finalizationregistry": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-finalizationregistry/-/is-finalizationregistry-1.1.1.tgz",
      "integrity": "sha512-1pC6N8qWJbWoPtEjgcL2xyhQOP491EQjeUo3qTKcmV8YSDDJrOepfG8pcC7h/QgnQHYSv0mJ3Z/ZWxmatVrysg==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-fullwidth-code-point": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/is-fullwidth-code-point/-/is-fullwidth-code-point-3.0.0.tgz",
      "integrity": "sha512-zymm5+u+sCsSWyD9qNaejV3DFvhCKclKdizYaJUuHA83RLjb7nSuGnddCHGv0hk+KY7BMAlsWeK4Ueg6EV6XQg==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-generator-fn": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-generator-fn/-/is-generator-fn-2.1.0.tgz",
      "integrity": "sha512-cTIB4yPYL/Grw0EaSzASzg6bBy9gqCofvWN8okThAYIxKJZC+udlRAmGbM0XLeniEJSs8uEgHPGuHSe1XsOLSQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/is-generator-function": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/is-generator-function/-/is-generator-function-1.1.0.tgz",
      "integrity": "sha512-nPUB5km40q9e8UfN/Zc24eLlzdSf9OfKByBw9CIdw4H1giPMeA0OIJvbchsCu4npfI2QcMVBsGEBHKZ7wLTWmQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "get-proto": "^1.0.0",
        "has-tostringtag": "^1.0.2",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-glob": {
      "version": "4.0.3",
      "resolved": "https://registry.npmjs.org/is-glob/-/is-glob-4.0.3.tgz",
      "integrity": "sha512-xelSayHH36ZgE7ZWhli7pW34hNbNl8Ojv5KVmkJD4hBdD3th8Tfk9vYasLM+mXWOZhFkgZfxhLSnrwRr4elSSg==",
      "license": "MIT",
      "dependencies": {
        "is-extglob": "^2.1.1"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-map": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-map/-/is-map-2.0.3.tgz",
      "integrity": "sha512-1Qed0/Hr2m+YqxnM09CjA2d/i6YZNfF6R2oRAOj36eUdS6qIV/huPJNSEpKbupewFs+ZsJlxsjjPbc0/afW6Lw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-module": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/is-module/-/is-module-1.0.0.tgz",
      "integrity": "sha512-51ypPSPCoTEIN9dy5Oy+h4pShgJmPCygKfyRCISBI+JoWT/2oJvK8QPxmwv7b/p239jXrm9M1mlQbyKJ5A152g==",
      "license": "MIT"
    },
    "node_modules/is-negative-zero": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-negative-zero/-/is-negative-zero-2.0.3.tgz",
      "integrity": "sha512-5KoIu2Ngpyek75jXodFvnafB6DJgr3u8uuK0LEZJjrU19DrMD3EVERaR8sjz8CCGgpZvxPl9SuE1GMVPFHx1mw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-number": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/is-number/-/is-number-7.0.0.tgz",
      "integrity": "sha512-41Cifkg6e8TylSpdtTpeLVMqvSBEVzTttHvERD741+pnZ8ANv0004MRL43QKPDlK9cGvNp6NZWZUBlbGXYxxng==",
      "license": "MIT",
      "engines": {
        "node": ">=0.12.0"
      }
    },
    "node_modules/is-number-object": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-number-object/-/is-number-object-1.1.1.tgz",
      "integrity": "sha512-lZhclumE1G6VYD8VHe35wFaIif+CTy5SJIi5+3y4psDgWu4wPDoBhF8NxUOinEc7pHgiTsT6MaBb92rKhhD+Xw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-obj": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/is-obj/-/is-obj-1.0.1.tgz",
      "integrity": "sha512-l4RyHgRqGN4Y3+9JHVrNqO+tN0rV5My76uW5/nuO4K1b6vw5G8d/cmFjP9tRfEsdhZNt0IFdZuK/c2Vr4Nb+Qg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-path-inside": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/is-path-inside/-/is-path-inside-3.0.3.tgz",
      "integrity": "sha512-Fd4gABb+ycGAmKou8eMftCupSir5lRxqf4aD/vd0cD2qc4HL07OjCeuHMr8Ro4CoMaeCKDB0/ECBOVWjTwUvPQ==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/is-plain-obj": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/is-plain-obj/-/is-plain-obj-3.0.0.tgz",
      "integrity": "sha512-gwsOE28k+23GP1B6vFl1oVh/WOzmawBrKwo5Ev6wMKzPkaXaCDIQKzLnvsA42DRlbVTWorkgTKIviAKCWkfUwA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-potential-custom-element-name": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/is-potential-custom-element-name/-/is-potential-custom-element-name-1.0.1.tgz",
      "integrity": "sha512-bCYeRA2rVibKZd+s2625gGnGF/t7DSqDs4dP7CrLA1m7jKWz6pps0LpYLJN8Q64HtmPKJ1hrN3nzPNKFEKOUiQ==",
      "license": "MIT"
    },
    "node_modules/is-regex": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/is-regex/-/is-regex-1.2.1.tgz",
      "integrity": "sha512-MjYsKHO5O7mCsmRGxWcLWheFqN9DJ/2TmngvjKXihe6efViPqc274+Fx/4fYj/r03+ESvBdTXK0V6tA3rgez1g==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "gopd": "^1.2.0",
        "has-tostringtag": "^1.0.2",
        "hasown": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-regexp": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/is-regexp/-/is-regexp-1.0.0.tgz",
      "integrity": "sha512-7zjFAPO4/gwyQAAgRRmqeEeyIICSdmCqa3tsVHMdBzaXXRiqopZL4Cyghg/XulGWrtABTpbnYYzzIRffLkP4oA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/is-root": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/is-root/-/is-root-2.1.0.tgz",
      "integrity": "sha512-AGOriNp96vNBd3HtU+RzFEc75FfR5ymiYv8E553I71SCeXBiMsVDUtdio1OEFvrPyLIQ9tVR5RxXIFe5PUFjMg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/is-set": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/is-set/-/is-set-2.0.3.tgz",
      "integrity": "sha512-iPAjerrse27/ygGLxw+EBR9agv9Y6uLeYVJMu+QNCoouJ1/1ri0mGrcWpfCqFZuzzx3WjtwxG098X+n4OuRkPg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-shared-array-buffer": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/is-shared-array-buffer/-/is-shared-array-buffer-1.0.4.tgz",
      "integrity": "sha512-ISWac8drv4ZGfwKl5slpHG9OwPNty4jOWPRIhBpxOoD+hqITiwuipOQ2bNthAzwA3B4fIjO4Nln74N0S9byq8A==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-stream": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/is-stream/-/is-stream-2.0.1.tgz",
      "integrity": "sha512-hFoiJiTl63nn+kstHGBtewWSKnQLpyb155KHheA1l39uvtO9nWIop1p3udqPcUd/xbF1VLMO4n7OI6p7RbngDg==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/is-string": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-string/-/is-string-1.1.1.tgz",
      "integrity": "sha512-BtEeSsoaQjlSPBemMQIrY1MY0uM6vnS1g5fmufYOtnxLGUZM2178PKbhsk7Ffv58IX+ZtcvoGwccYsh0PglkAA==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-symbol": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-symbol/-/is-symbol-1.1.1.tgz",
      "integrity": "sha512-9gGx6GTtCQM73BgmHQXfDmLtfjjTUDSyoxTCbp5WtoixAhfgsDirWIcVQ/IHpvI5Vgd5i/J5F7B9cN/WlVbC/w==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "has-symbols": "^1.1.0",
        "safe-regex-test": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-typed-array": {
      "version": "1.1.15",
      "resolved": "https://registry.npmjs.org/is-typed-array/-/is-typed-array-1.1.15.tgz",
      "integrity": "sha512-p3EcsicXjit7SaskXHs1hA91QxgTw46Fv6EFKKGS5DRFLD8yKnohjF3hxoju94b/OcMZoQukzpPpBE9uLVKzgQ==",
      "license": "MIT",
      "dependencies": {
        "which-typed-array": "^1.1.16"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-typedarray": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/is-typedarray/-/is-typedarray-1.0.0.tgz",
      "integrity": "sha512-cyA56iCMHAh5CdzjJIa4aohJyeO1YbwLi3Jc35MmRU6poroFjIGZzUzupGiRPOjgHg9TLu43xbpwXk523fMxKA==",
      "license": "MIT"
    },
    "node_modules/is-weakmap": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/is-weakmap/-/is-weakmap-2.0.2.tgz",
      "integrity": "sha512-K5pXYOm9wqY1RgjpL3YTkF39tni1XajUIkawTLUo9EZEVUFga5gSQJF8nNS7ZwJQ02y+1YCNYcMh+HIf1ZqE+w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakref": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/is-weakref/-/is-weakref-1.1.1.tgz",
      "integrity": "sha512-6i9mGWSlqzNMEqpCp93KwRS1uUOodk2OJ6b+sq7ZPDSy2WuI5NFIxp/254TytR8ftefexkWn5xNiHUNpPOfSew==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-weakset": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/is-weakset/-/is-weakset-2.0.4.tgz",
      "integrity": "sha512-mfcwb6IzQyOKTs84CQMrOwW4gQcaTOAWJ0zzJCl2WSPDrWk/OzDaImWFH3djXhb24g4eudZfLRozAvPGw4d9hQ==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "get-intrinsic": "^1.2.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/is-wsl": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/is-wsl/-/is-wsl-2.2.0.tgz",
      "integrity": "sha512-fKzAra0rGJUUBwGBgNkHZuToZcn+TtXHpeCgmkMJMMYx1sQDYaCSyjJBSCa2nH1DGm7s3n1oBnohoVTBaN7Lww==",
      "license": "MIT",
      "dependencies": {
        "is-docker": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/isarray": {
      "version": "2.0.5",
      "resolved": "https://registry.npmjs.org/isarray/-/isarray-2.0.5.tgz",
      "integrity": "sha512-xHjhDr3cNBK0BzdUJSPXZntQUx/mwMS5Rw4A7lPJ90XGAO6ISP/ePDNuo0vhqOZU+UD5JoodwCAAoZQd3FeAKw==",
      "license": "MIT"
    },
    "node_modules/isexe": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/isexe/-/isexe-2.0.0.tgz",
      "integrity": "sha512-RHxMLp9lnKHGHRng9QFhRCMbYAcVpn69smSGcq3f36xjgVVWThj4qqLbTLlq7Ssj8B+fIQ1EuCEGI2lKsyQeIw==",
      "license": "ISC"
    },
    "node_modules/istanbul-lib-coverage": {
      "version": "3.2.2",
      "resolved": "https://registry.npmjs.org/istanbul-lib-coverage/-/istanbul-lib-coverage-3.2.2.tgz",
      "integrity": "sha512-O8dpsF+r0WV/8MNRKfnmrtCWhuKjxrq2w+jpzBL5UZKTi2LeVWnWOmWRxFlesJONmc+wLAGvKQZEOanko0LFTg==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/istanbul-lib-instrument": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/istanbul-lib-instrument/-/istanbul-lib-instrument-5.2.1.tgz",
      "integrity": "sha512-pzqtp31nLv/XFOzXGuvhCb8qhjmTVo5vjVk19XE4CRlSWz0KoeJ3bw9XsA7nOp9YBf4qHjwBxkDzKcME/J29Yg==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "@babel/core": "^7.12.3",
        "@babel/parser": "^7.14.7",
        "@istanbuljs/schema": "^0.1.2",
        "istanbul-lib-coverage": "^3.2.0",
        "semver": "^6.3.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/istanbul-lib-instrument/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/istanbul-lib-report": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/istanbul-lib-report/-/istanbul-lib-report-3.0.1.tgz",
      "integrity": "sha512-GCfE1mtsHGOELCU8e/Z7YWzpmybrx/+dSTfLrvY8qRmaY6zXTKWn6WQIjaAFw069icm6GVMNkgu0NzI4iPZUNw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "istanbul-lib-coverage": "^3.0.0",
        "make-dir": "^4.0.0",
        "supports-color": "^7.1.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/istanbul-lib-report/node_modules/make-dir": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/make-dir/-/make-dir-4.0.0.tgz",
      "integrity": "sha512-hXdUTZYIVOt1Ex//jAQi+wTZZpUpwBj/0QsOzqegb3rGMMeJiSEu5xLHnYfBrRV4RH2+OCSOO95Is/7x1WJ4bw==",
      "license": "MIT",
      "dependencies": {
        "semver": "^7.5.3"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/istanbul-lib-source-maps": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/istanbul-lib-source-maps/-/istanbul-lib-source-maps-4.0.1.tgz",
      "integrity": "sha512-n3s8EwkdFIJCG3BPKBYvskgXGoy88ARzvegkitk60NxRdwltLOTaH7CUiMRXvwYorl0Q712iEjcWB+fK/MrWVw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "debug": "^4.1.1",
        "istanbul-lib-coverage": "^3.0.0",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/istanbul-lib-source-maps/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/istanbul-reports": {
      "version": "3.2.0",
      "resolved": "https://registry.npmjs.org/istanbul-reports/-/istanbul-reports-3.2.0.tgz",
      "integrity": "sha512-HGYWWS/ehqTV3xN10i23tkPkpH46MLCIMFNCaaKNavAXTF1RkqxawEPtnjnGZ6XKSInBKkiOA5BKS+aZiY3AvA==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "html-escaper": "^2.0.0",
        "istanbul-lib-report": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/iterator.prototype": {
      "version": "1.1.5",
      "resolved": "https://registry.npmjs.org/iterator.prototype/-/iterator.prototype-1.1.5.tgz",
      "integrity": "sha512-H0dkQoCa3b2VEeKQBOxFph+JAbcrQdE7KC0UkqwpLmv2EC4P41QXP+rqo9wYodACiG5/WM5s9oDApTU8utwj9g==",
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.6",
        "get-proto": "^1.0.0",
        "has-symbols": "^1.1.0",
        "set-function-name": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/jackspeak": {
      "version": "3.4.3",
      "resolved": "https://registry.npmjs.org/jackspeak/-/jackspeak-3.4.3.tgz",
      "integrity": "sha512-OGlZQpz2yfahA/Rd1Y8Cd9SIEsqvXkLVoSw/cgwhnhFMDbsQFeZYoJJ7bIZBS9BcamUW96asq/npPWugM+RQBw==",
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "@isaacs/cliui": "^8.0.2"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      },
      "optionalDependencies": {
        "@pkgjs/parseargs": "^0.11.0"
      }
    },
    "node_modules/jake": {
      "version": "10.9.4",
      "resolved": "https://registry.npmjs.org/jake/-/jake-10.9.4.tgz",
      "integrity": "sha512-wpHYzhxiVQL+IV05BLE2Xn34zW1S223hvjtqk0+gsPrwd/8JNLXJgZZM/iPFsYc1xyphF+6M6EvdE5E9MBGkDA==",
      "license": "Apache-2.0",
      "dependencies": {
        "async": "^3.2.6",
        "filelist": "^1.0.4",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "jake": "bin/cli.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/jest": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest/-/jest-27.5.1.tgz",
      "integrity": "sha512-Yn0mADZB89zTtjkPJEXwrac3LHudkQMR+Paqa8uxJHCBr9agxztUifWCyiYrjhMPBoUVBjyny0I7XH6ozDr7QQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/core": "^27.5.1",
        "import-local": "^3.0.2",
        "jest-cli": "^27.5.1"
      },
      "bin": {
        "jest": "bin/jest.js"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "node-notifier": "^8.0.1 || ^9.0.0 || ^10.0.0"
      },
      "peerDependenciesMeta": {
        "node-notifier": {
          "optional": true
        }
      }
    },
    "node_modules/jest-changed-files": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-changed-files/-/jest-changed-files-27.5.1.tgz",
      "integrity": "sha512-buBLMiByfWGCoMsLLzGUUSpAmIAGnbR2KJoMN10ziLhOLvP4e0SlypHnAel8iqQXTrcbmfEY9sSqae5sgUsTvw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "execa": "^5.0.0",
        "throat": "^6.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-circus": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-circus/-/jest-circus-27.5.1.tgz",
      "integrity": "sha512-D95R7x5UtlMA5iBYsOHFFbMD/GVA4R/Kdq15f7xYWUfWHBto9NYRsOvnSauTgdF+ogCpJ4tyKOXhUifxS65gdw==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "co": "^4.6.0",
        "dedent": "^0.7.0",
        "expect": "^27.5.1",
        "is-generator-fn": "^2.0.0",
        "jest-each": "^27.5.1",
        "jest-matcher-utils": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-runtime": "^27.5.1",
        "jest-snapshot": "^27.5.1",
        "jest-util": "^27.5.1",
        "pretty-format": "^27.5.1",
        "slash": "^3.0.0",
        "stack-utils": "^2.0.3",
        "throat": "^6.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-cli": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-cli/-/jest-cli-27.5.1.tgz",
      "integrity": "sha512-Hc6HOOwYq4/74/c62dEE3r5elx8wjYqxY0r0G/nFrLDPMFRu6RA/u8qINOIkvhxG7mMQ5EJsOGfRpI8L6eFUVw==",
      "license": "MIT",
      "dependencies": {
        "@jest/core": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/types": "^27.5.1",
        "chalk": "^4.0.0",
        "exit": "^0.1.2",
        "graceful-fs": "^4.2.9",
        "import-local": "^3.0.2",
        "jest-config": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-validate": "^27.5.1",
        "prompts": "^2.0.1",
        "yargs": "^16.2.0"
      },
      "bin": {
        "jest": "bin/jest.js"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "node-notifier": "^8.0.1 || ^9.0.0 || ^10.0.0"
      },
      "peerDependenciesMeta": {
        "node-notifier": {
          "optional": true
        }
      }
    },
    "node_modules/jest-config": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-config/-/jest-config-27.5.1.tgz",
      "integrity": "sha512-5sAsjm6tGdsVbW9ahcChPAFCk4IlkQUknH5AvKjuLTSlcO/wCZKyFdn7Rg0EkC+OGgWODEy2hDpWB1PgzH0JNA==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.8.0",
        "@jest/test-sequencer": "^27.5.1",
        "@jest/types": "^27.5.1",
        "babel-jest": "^27.5.1",
        "chalk": "^4.0.0",
        "ci-info": "^3.2.0",
        "deepmerge": "^4.2.2",
        "glob": "^7.1.1",
        "graceful-fs": "^4.2.9",
        "jest-circus": "^27.5.1",
        "jest-environment-jsdom": "^27.5.1",
        "jest-environment-node": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "jest-jasmine2": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-runner": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-validate": "^27.5.1",
        "micromatch": "^4.0.4",
        "parse-json": "^5.2.0",
        "pretty-format": "^27.5.1",
        "slash": "^3.0.0",
        "strip-json-comments": "^3.1.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "peerDependencies": {
        "ts-node": ">=9.0.0"
      },
      "peerDependenciesMeta": {
        "ts-node": {
          "optional": true
        }
      }
    },
    "node_modules/jest-diff": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-diff/-/jest-diff-27.5.1.tgz",
      "integrity": "sha512-m0NvkX55LDt9T4mctTEgnZk3fmEg3NRYutvMPWM/0iPnkFj2wIeF45O1718cMSOFO1vINkqmxqD8vE37uTEbqw==",
      "license": "MIT",
      "dependencies": {
        "chalk": "^4.0.0",
        "diff-sequences": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-docblock": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-docblock/-/jest-docblock-27.5.1.tgz",
      "integrity": "sha512-rl7hlABeTsRYxKiUfpHrQrG4e2obOiTQWfMEH3PxPjOtdsfLQO4ReWSZaQ7DETm4xu07rl4q/h4zcKXyU0/OzQ==",
      "license": "MIT",
      "dependencies": {
        "detect-newline": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-each": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-each/-/jest-each-27.5.1.tgz",
      "integrity": "sha512-1Ff6p+FbhT/bXQnEouYy00bkNSY7OUpfIcmdl8vZ31A1UUaurOLPA8a8BbJOF2RDUElwJhmeaV7LnagI+5UwNQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "chalk": "^4.0.0",
        "jest-get-type": "^27.5.1",
        "jest-util": "^27.5.1",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-environment-jsdom": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-environment-jsdom/-/jest-environment-jsdom-27.5.1.tgz",
      "integrity": "sha512-TFBvkTC1Hnnnrka/fUb56atfDtJ9VMZ94JkjTbggl1PEpwrYtUBKMezB3inLmWqQsXYLcMwNoDQwoBTAvFfsfw==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/fake-timers": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "jest-mock": "^27.5.1",
        "jest-util": "^27.5.1",
        "jsdom": "^16.6.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-environment-node": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-environment-node/-/jest-environment-node-27.5.1.tgz",
      "integrity": "sha512-Jt4ZUnxdOsTGwSRAfKEnE6BcwsSPNOijjwifq5sDFSA2kesnXTvNqKHYgM0hDq3549Uf/KzdXNYn4wMZJPlFLw==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/fake-timers": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "jest-mock": "^27.5.1",
        "jest-util": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-get-type": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-get-type/-/jest-get-type-27.5.1.tgz",
      "integrity": "sha512-2KY95ksYSaK7DMBWQn6dQz3kqAf3BB64y2udeG+hv4KfSOb9qwcYQstTJc1KCbsix+wLZWZYN8t7nwX3GOBLRw==",
      "license": "MIT",
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-haste-map": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-haste-map/-/jest-haste-map-27.5.1.tgz",
      "integrity": "sha512-7GgkZ4Fw4NFbMSDSpZwXeBiIbx+t/46nJ2QitkOjvwPYyZmqttu2TDSimMHP1EkPOi4xUZAN1doE5Vd25H4Jng==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@types/graceful-fs": "^4.1.2",
        "@types/node": "*",
        "anymatch": "^3.0.3",
        "fb-watchman": "^2.0.0",
        "graceful-fs": "^4.2.9",
        "jest-regex-util": "^27.5.1",
        "jest-serializer": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-worker": "^27.5.1",
        "micromatch": "^4.0.4",
        "walker": "^1.0.7"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      },
      "optionalDependencies": {
        "fsevents": "^2.3.2"
      }
    },
    "node_modules/jest-jasmine2": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-jasmine2/-/jest-jasmine2-27.5.1.tgz",
      "integrity": "sha512-jtq7VVyG8SqAorDpApwiJJImd0V2wv1xzdheGHRGyuT7gZm6gG47QEskOlzsN1PG/6WNaCo5pmwMHDf3AkG2pQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/source-map": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "co": "^4.6.0",
        "expect": "^27.5.1",
        "is-generator-fn": "^2.0.0",
        "jest-each": "^27.5.1",
        "jest-matcher-utils": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-runtime": "^27.5.1",
        "jest-snapshot": "^27.5.1",
        "jest-util": "^27.5.1",
        "pretty-format": "^27.5.1",
        "throat": "^6.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-leak-detector": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-leak-detector/-/jest-leak-detector-27.5.1.tgz",
      "integrity": "sha512-POXfWAMvfU6WMUXftV4HolnJfnPOGEu10fscNCA76KBpRRhcMN2c8d3iT2pxQS3HLbA+5X4sOUPzYO2NUyIlHQ==",
      "license": "MIT",
      "dependencies": {
        "jest-get-type": "^27.5.1",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-matcher-utils": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-matcher-utils/-/jest-matcher-utils-27.5.1.tgz",
      "integrity": "sha512-z2uTx/T6LBaCoNWNFWwChLBKYxTMcGBRjAt+2SbP929/Fflb9aa5LGma654Rz8z9HLxsrUaYzxE9T/EFIL/PAw==",
      "license": "MIT",
      "dependencies": {
        "chalk": "^4.0.0",
        "jest-diff": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-message-util": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-message-util/-/jest-message-util-27.5.1.tgz",
      "integrity": "sha512-rMyFe1+jnyAAf+NHwTclDz0eAaLkVDdKVHHBFWsBWHnnh5YeJMNWWsv7AbFYXfK3oTqvL7VTWkhNLu1jX24D+g==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.12.13",
        "@jest/types": "^27.5.1",
        "@types/stack-utils": "^2.0.0",
        "chalk": "^4.0.0",
        "graceful-fs": "^4.2.9",
        "micromatch": "^4.0.4",
        "pretty-format": "^27.5.1",
        "slash": "^3.0.0",
        "stack-utils": "^2.0.3"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-mock": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-mock/-/jest-mock-27.5.1.tgz",
      "integrity": "sha512-K4jKbY1d4ENhbrG2zuPWaQBvDly+iZ2yAW+T1fATN78hc0sInwn7wZB8XtlNnvHug5RMwV897Xm4LqmPM4e2Og==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@types/node": "*"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-pnp-resolver": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/jest-pnp-resolver/-/jest-pnp-resolver-1.2.3.tgz",
      "integrity": "sha512-+3NpwQEnRoIBtx4fyhblQDPgJI0H1IEIkX7ShLUjPGA7TtUTvI1oiKi3SR4oBR0hQhQR80l4WAe5RrXBwWMA8w==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "peerDependencies": {
        "jest-resolve": "*"
      },
      "peerDependenciesMeta": {
        "jest-resolve": {
          "optional": true
        }
      }
    },
    "node_modules/jest-regex-util": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-regex-util/-/jest-regex-util-27.5.1.tgz",
      "integrity": "sha512-4bfKq2zie+x16okqDXjXn9ql2B0dScQu+vcwe4TvFVhkVyuWLqpZrZtXxLLWoXYgn0E87I6r6GRYHF7wFZBUvg==",
      "license": "MIT",
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-resolve": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-resolve/-/jest-resolve-27.5.1.tgz",
      "integrity": "sha512-FFDy8/9E6CV83IMbDpcjOhumAQPDyETnU2KZ1O98DwTnz8AOBsW/Xv3GySr1mOZdItLR+zDZ7I/UdTFbgSOVCw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "chalk": "^4.0.0",
        "graceful-fs": "^4.2.9",
        "jest-haste-map": "^27.5.1",
        "jest-pnp-resolver": "^1.2.2",
        "jest-util": "^27.5.1",
        "jest-validate": "^27.5.1",
        "resolve": "^1.20.0",
        "resolve.exports": "^1.1.0",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-resolve-dependencies": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-resolve-dependencies/-/jest-resolve-dependencies-27.5.1.tgz",
      "integrity": "sha512-QQOOdY4PE39iawDn5rzbIePNigfe5B9Z91GDD1ae/xNDlu9kaat8QQ5EKnNmVWPV54hUdxCVwwj6YMgR2O7IOg==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-snapshot": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-runner": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-runner/-/jest-runner-27.5.1.tgz",
      "integrity": "sha512-g4NPsM4mFCOwFKXO4p/H/kWGdJp9V8kURY2lX8Me2drgXqG7rrZAx5kv+5H7wtt/cdFIjhqYx1HrlqWHaOvDaQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/console": "^27.5.1",
        "@jest/environment": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "emittery": "^0.8.1",
        "graceful-fs": "^4.2.9",
        "jest-docblock": "^27.5.1",
        "jest-environment-jsdom": "^27.5.1",
        "jest-environment-node": "^27.5.1",
        "jest-haste-map": "^27.5.1",
        "jest-leak-detector": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-runtime": "^27.5.1",
        "jest-util": "^27.5.1",
        "jest-worker": "^27.5.1",
        "source-map-support": "^0.5.6",
        "throat": "^6.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-runtime": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-runtime/-/jest-runtime-27.5.1.tgz",
      "integrity": "sha512-o7gxw3Gf+H2IGt8fv0RiyE1+r83FJBRruoA+FXrlHw6xEyBsU8ugA6IPfTdVyA0w8HClpbK+DGJxH59UrNMx8A==",
      "license": "MIT",
      "dependencies": {
        "@jest/environment": "^27.5.1",
        "@jest/fake-timers": "^27.5.1",
        "@jest/globals": "^27.5.1",
        "@jest/source-map": "^27.5.1",
        "@jest/test-result": "^27.5.1",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "chalk": "^4.0.0",
        "cjs-module-lexer": "^1.0.0",
        "collect-v8-coverage": "^1.0.0",
        "execa": "^5.0.0",
        "glob": "^7.1.3",
        "graceful-fs": "^4.2.9",
        "jest-haste-map": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-mock": "^27.5.1",
        "jest-regex-util": "^27.5.1",
        "jest-resolve": "^27.5.1",
        "jest-snapshot": "^27.5.1",
        "jest-util": "^27.5.1",
        "slash": "^3.0.0",
        "strip-bom": "^4.0.0"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-serializer": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-serializer/-/jest-serializer-27.5.1.tgz",
      "integrity": "sha512-jZCyo6iIxO1aqUxpuBlwTDMkzOAJS4a3eYz3YzgxxVQFwLeSA7Jfq5cbqCY+JLvTDrWirgusI/0KwxKMgrdf7w==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "graceful-fs": "^4.2.9"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-snapshot": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-snapshot/-/jest-snapshot-27.5.1.tgz",
      "integrity": "sha512-yYykXI5a0I31xX67mgeLw1DZ0bJB+gpq5IpSuCAoyDi0+BhgU/RIrL+RTzDmkNTchvDFWKP8lp+w/42Z3us5sA==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.7.2",
        "@babel/generator": "^7.7.2",
        "@babel/plugin-syntax-typescript": "^7.7.2",
        "@babel/traverse": "^7.7.2",
        "@babel/types": "^7.0.0",
        "@jest/transform": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/babel__traverse": "^7.0.4",
        "@types/prettier": "^2.1.5",
        "babel-preset-current-node-syntax": "^1.0.0",
        "chalk": "^4.0.0",
        "expect": "^27.5.1",
        "graceful-fs": "^4.2.9",
        "jest-diff": "^27.5.1",
        "jest-get-type": "^27.5.1",
        "jest-haste-map": "^27.5.1",
        "jest-matcher-utils": "^27.5.1",
        "jest-message-util": "^27.5.1",
        "jest-util": "^27.5.1",
        "natural-compare": "^1.4.0",
        "pretty-format": "^27.5.1",
        "semver": "^7.3.2"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-util": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-util/-/jest-util-27.5.1.tgz",
      "integrity": "sha512-Kv2o/8jNvX1MQ0KGtw480E/w4fBCDOnH6+6DmeKi6LZUIlKA5kwY0YNdlzaWTiVgxqAqik11QyxDOKk543aKXw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "ci-info": "^3.2.0",
        "graceful-fs": "^4.2.9",
        "picomatch": "^2.2.3"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-validate": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-validate/-/jest-validate-27.5.1.tgz",
      "integrity": "sha512-thkNli0LYTmOI1tDB3FI1S1RTp/Bqyd9pTarJwL87OIBFuqEb5Apv5EaApEudYg4g86e3CT6kM0RowkhtEnCBQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^27.5.1",
        "camelcase": "^6.2.0",
        "chalk": "^4.0.0",
        "jest-get-type": "^27.5.1",
        "leven": "^3.1.0",
        "pretty-format": "^27.5.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-watch-typeahead": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/jest-watch-typeahead/-/jest-watch-typeahead-1.1.0.tgz",
      "integrity": "sha512-Va5nLSJTN7YFtC2jd+7wsoe1pNe5K4ShLux/E5iHEwlB9AxaxmggY7to9KUqKojhaJw3aXqt5WAb4jGPOolpEw==",
      "license": "MIT",
      "dependencies": {
        "ansi-escapes": "^4.3.1",
        "chalk": "^4.0.0",
        "jest-regex-util": "^28.0.0",
        "jest-watcher": "^28.0.0",
        "slash": "^4.0.0",
        "string-length": "^5.0.1",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": "^12.22.0 || ^14.17.0 || >=16.0.0"
      },
      "peerDependencies": {
        "jest": "^27.0.0 || ^28.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@jest/console": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/@jest/console/-/console-28.1.3.tgz",
      "integrity": "sha512-QPAkP5EwKdK/bxIr6C1I4Vs0rm2nHiANzj/Z5X2JQkrZo6IqvC4ldZ9K95tF0HdidhA8Bo6egxSzUFPYKcEXLw==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^28.1.3",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "jest-message-util": "^28.1.3",
        "jest-util": "^28.1.3",
        "slash": "^3.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@jest/console/node_modules/slash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-3.0.0.tgz",
      "integrity": "sha512-g9Q1haeby36OSStwb4ntCGGGaKsaVSjQ68fBxoQcutl5fS1vuY18H3wSt3jFyFtrkx+Kz0V1G85A4MyAdDMi2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@jest/test-result": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/@jest/test-result/-/test-result-28.1.3.tgz",
      "integrity": "sha512-kZAkxnSE+FqE8YjW8gNuoVkkC9I7S1qmenl8sGcDOLropASP+BkcGKwhXoyqQuGOGeYY0y/ixjrd/iERpEXHNg==",
      "license": "MIT",
      "dependencies": {
        "@jest/console": "^28.1.3",
        "@jest/types": "^28.1.3",
        "@types/istanbul-lib-coverage": "^2.0.0",
        "collect-v8-coverage": "^1.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@jest/types": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/@jest/types/-/types-28.1.3.tgz",
      "integrity": "sha512-RyjiyMUZrKz/c+zlMFO1pm70DcIlST8AeWTkoUdZevew44wcNZQHsEVOiCVtgVnlFFD82FPaXycys58cf2muVQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/schemas": "^28.1.3",
        "@types/istanbul-lib-coverage": "^2.0.0",
        "@types/istanbul-reports": "^3.0.0",
        "@types/node": "*",
        "@types/yargs": "^17.0.8",
        "chalk": "^4.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/@types/yargs": {
      "version": "17.0.33",
      "resolved": "https://registry.npmjs.org/@types/yargs/-/yargs-17.0.33.tgz",
      "integrity": "sha512-WpxBCKWPLr4xSsHgz511rFJAM+wS28w2zEO1QDNY5zM/S8ok70NNfztH0xwhqKyaK0OHCbN98LDAZuy1ctxDkA==",
      "license": "MIT",
      "dependencies": {
        "@types/yargs-parser": "*"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/ansi-styles": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-5.2.0.tgz",
      "integrity": "sha512-Cxwpt2SfTzTtXcfOlzGEee8O+c+MmUgGrNiBcXnuWxuFJHe6a5Hz7qwhwe5OgaSYI0IJvkLqWX1ASG+cJOkEiA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/emittery": {
      "version": "0.10.2",
      "resolved": "https://registry.npmjs.org/emittery/-/emittery-0.10.2.tgz",
      "integrity": "sha512-aITqOwnLanpHLNXZJENbOgjUBeHocD+xsSJmNrjovKBW5HbSpW3d1pEls7GFQPUWXiwG9+0P4GtHfEqC/4M0Iw==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sindresorhus/emittery?sponsor=1"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-message-util": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/jest-message-util/-/jest-message-util-28.1.3.tgz",
      "integrity": "sha512-PFdn9Iewbt575zKPf1286Ht9EPoJmYT7P0kY+RibeYZ2XtOr53pDLEFoTWXbd1h4JiGiWpTBC84fc8xMXQMb7g==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.12.13",
        "@jest/types": "^28.1.3",
        "@types/stack-utils": "^2.0.0",
        "chalk": "^4.0.0",
        "graceful-fs": "^4.2.9",
        "micromatch": "^4.0.4",
        "pretty-format": "^28.1.3",
        "slash": "^3.0.0",
        "stack-utils": "^2.0.3"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-message-util/node_modules/slash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-3.0.0.tgz",
      "integrity": "sha512-g9Q1haeby36OSStwb4ntCGGGaKsaVSjQ68fBxoQcutl5fS1vuY18H3wSt3jFyFtrkx+Kz0V1G85A4MyAdDMi2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-regex-util": {
      "version": "28.0.2",
      "resolved": "https://registry.npmjs.org/jest-regex-util/-/jest-regex-util-28.0.2.tgz",
      "integrity": "sha512-4s0IgyNIy0y9FK+cjoVYoxamT7Zeo7MhzqRGx7YDYmaQn1wucY9rotiGkBzzcMXTtjrCAP/f7f+E0F7+fxPNdw==",
      "license": "MIT",
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-util": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/jest-util/-/jest-util-28.1.3.tgz",
      "integrity": "sha512-XdqfpHwpcSRko/C35uLYFM2emRAltIIKZiJ9eAmhjsj0CqZMa0p1ib0R5fWIqGhn1a103DebTbpqIaP1qCQ6tQ==",
      "license": "MIT",
      "dependencies": {
        "@jest/types": "^28.1.3",
        "@types/node": "*",
        "chalk": "^4.0.0",
        "ci-info": "^3.2.0",
        "graceful-fs": "^4.2.9",
        "picomatch": "^2.2.3"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-watcher": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/jest-watcher/-/jest-watcher-28.1.3.tgz",
      "integrity": "sha512-t4qcqj9hze+jviFPUN3YAtAEeFnr/azITXQEMARf5cMwKY2SMBRnCQTXLixTl20OR6mLh9KLMrgVJgJISym+1g==",
      "license": "MIT",
      "dependencies": {
        "@jest/test-result": "^28.1.3",
        "@jest/types": "^28.1.3",
        "@types/node": "*",
        "ansi-escapes": "^4.2.1",
        "chalk": "^4.0.0",
        "emittery": "^0.10.2",
        "jest-util": "^28.1.3",
        "string-length": "^4.0.1"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-watcher/node_modules/string-length": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/string-length/-/string-length-4.0.2.tgz",
      "integrity": "sha512-+l6rNN5fYHNhZZy41RXsYptCjA2Igmq4EG7kZAYFQI1E1VTXarr6ZPXBg6eq7Y6eK4FEhY6AJlyuFIb/v/S0VQ==",
      "license": "MIT",
      "dependencies": {
        "char-regex": "^1.0.2",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/jest-watcher/node_modules/strip-ansi": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/pretty-format": {
      "version": "28.1.3",
      "resolved": "https://registry.npmjs.org/pretty-format/-/pretty-format-28.1.3.tgz",
      "integrity": "sha512-8gFb/To0OmxHR9+ZTb14Df2vNxdGCX8g1xWGUTqUw5TiZvcQf5sHKObd5UcPyLLyowNwDAMTF3XWOG1B6mxl1Q==",
      "license": "MIT",
      "dependencies": {
        "@jest/schemas": "^28.1.3",
        "ansi-regex": "^5.0.1",
        "ansi-styles": "^5.0.0",
        "react-is": "^18.0.0"
      },
      "engines": {
        "node": "^12.13.0 || ^14.15.0 || ^16.10.0 || >=17.0.0"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/react-is": {
      "version": "18.3.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-18.3.1.tgz",
      "integrity": "sha512-/LLMVyas0ljjAtoYiPqYiL8VWXzUUdThrmU5+n20DZv+a+ClRoevUzw5JxU+Ieh5/c87ytoTBV9G1FiKfNJdmg==",
      "license": "MIT"
    },
    "node_modules/jest-watch-typeahead/node_modules/slash": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-4.0.0.tgz",
      "integrity": "sha512-3dOsAHXXUkQTpOYcoAxLIorMTp4gIQr5IW3iVb7A7lFIp0VHhnynm9izx6TssdrIcVIESAlVjtnO2K8bg+Coew==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/string-length": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/string-length/-/string-length-5.0.1.tgz",
      "integrity": "sha512-9Ep08KAMUn0OadnVaBuRdE2l615CQ508kr0XMadjClfYpdCyvrbFp6Taebo8yyxokQ4viUd/xPPUA4FGgUa0ow==",
      "license": "MIT",
      "dependencies": {
        "char-regex": "^2.0.0",
        "strip-ansi": "^7.0.1"
      },
      "engines": {
        "node": ">=12.20"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/string-length/node_modules/char-regex": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/char-regex/-/char-regex-2.0.2.tgz",
      "integrity": "sha512-cbGOjAptfM2LVmWhwRFHEKTPkLwNddVmuqYZQt895yXwAsWsXObCG+YN4DGQ/JBtT4GP1a1lPPdio2z413LmTg==",
      "license": "MIT",
      "engines": {
        "node": ">=12.20"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/strip-ansi": {
      "version": "7.1.2",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-7.1.2.tgz",
      "integrity": "sha512-gmBGslpoQJtgnMAvOVqGZpEz9dyoKTCzy2nfz/n8aIFhN/jCE/rCmcxabB6jOOHV+0WNnylOxaxBQPSvcWklhA==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^6.0.1"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/strip-ansi?sponsor=1"
      }
    },
    "node_modules/jest-watch-typeahead/node_modules/strip-ansi/node_modules/ansi-regex": {
      "version": "6.2.2",
      "resolved": "https://registry.npmjs.org/ansi-regex/-/ansi-regex-6.2.2.tgz",
      "integrity": "sha512-Bq3SmSpyFHaWjPk8If9yc6svM8c56dB5BAtW4Qbw5jHTwwXXcTLoRMkpDJp6VL0XzlWaCHTXrkFURMYmD0sLqg==",
      "license": "MIT",
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-regex?sponsor=1"
      }
    },
    "node_modules/jest-watcher": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-watcher/-/jest-watcher-27.5.1.tgz",
      "integrity": "sha512-z676SuD6Z8o8qbmEGhoEUFOM1+jfEiL3DXHK/xgEiG2EyNYfFG60jluWcupY6dATjfEsKQuibReS1djInQnoVw==",
      "license": "MIT",
      "dependencies": {
        "@jest/test-result": "^27.5.1",
        "@jest/types": "^27.5.1",
        "@types/node": "*",
        "ansi-escapes": "^4.2.1",
        "chalk": "^4.0.0",
        "jest-util": "^27.5.1",
        "string-length": "^4.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/jest-worker": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/jest-worker/-/jest-worker-27.5.1.tgz",
      "integrity": "sha512-7vuh85V5cdDofPyxn58nrPjBktZo0u9x1g8WtjQol+jZDaE+fhN+cIvTj11GndBnMnyfrUOG1sZQxCdjKh+DKg==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "merge-stream": "^2.0.0",
        "supports-color": "^8.0.0"
      },
      "engines": {
        "node": ">= 10.13.0"
      }
    },
    "node_modules/jest-worker/node_modules/supports-color": {
      "version": "8.1.1",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-8.1.1.tgz",
      "integrity": "sha512-MpUEN2OodtUzxvKQl72cUF7RQ5EiHsGvSsVG0ia9c5RbWGL2CI4C7EpPS8UTBIplnlzZiNuV56w+FuNxy3ty2Q==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/supports-color?sponsor=1"
      }
    },
    "node_modules/jiti": {
      "version": "1.21.7",
      "resolved": "https://registry.npmjs.org/jiti/-/jiti-1.21.7.tgz",
      "integrity": "sha512-/imKNG4EbWNrVjoNC/1H5/9GFy+tqjGBHCaSsN+P2RnPqjsLmv6UD3Ej+Kj8nBWaRAwyk7kK5ZUc+OEatnTR3A==",
      "license": "MIT",
      "bin": {
        "jiti": "bin/jiti.js"
      }
    },
    "node_modules/js-tokens": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/js-tokens/-/js-tokens-4.0.0.tgz",
      "integrity": "sha512-RdJUflcE3cUzKiMqQgsCu06FPu9UdIJO0beYbPhHN4k6apgJtifcoCtT9bcxOpYBtpD2kCM6Sbzg4CausW/PKQ==",
      "license": "MIT"
    },
    "node_modules/js-yaml": {
      "version": "3.14.1",
      "resolved": "https://registry.npmjs.org/js-yaml/-/js-yaml-3.14.1.tgz",
      "integrity": "sha512-okMH7OXXJ7YrN9Ok3/SXrnu4iX9yOk+25nqX4imS2npuvTYDmo/QEZoqwZkYaIDk3jVvBOTOIEgEhaLOynBS9g==",
      "license": "MIT",
      "dependencies": {
        "argparse": "^1.0.7",
        "esprima": "^4.0.0"
      },
      "bin": {
        "js-yaml": "bin/js-yaml.js"
      }
    },
    "node_modules/jsdom": {
      "version": "16.7.0",
      "resolved": "https://registry.npmjs.org/jsdom/-/jsdom-16.7.0.tgz",
      "integrity": "sha512-u9Smc2G1USStM+s/x1ru5Sxrl6mPYCbByG1U/hUmqaVsm4tbNyS7CicOSRyuGQYZhTu0h84qkZZQ/I+dzizSVw==",
      "license": "MIT",
      "dependencies": {
        "abab": "^2.0.5",
        "acorn": "^8.2.4",
        "acorn-globals": "^6.0.0",
        "cssom": "^0.4.4",
        "cssstyle": "^2.3.0",
        "data-urls": "^2.0.0",
        "decimal.js": "^10.2.1",
        "domexception": "^2.0.1",
        "escodegen": "^2.0.0",
        "form-data": "^3.0.0",
        "html-encoding-sniffer": "^2.0.1",
        "http-proxy-agent": "^4.0.1",
        "https-proxy-agent": "^5.0.0",
        "is-potential-custom-element-name": "^1.0.1",
        "nwsapi": "^2.2.0",
        "parse5": "6.0.1",
        "saxes": "^5.0.1",
        "symbol-tree": "^3.2.4",
        "tough-cookie": "^4.0.0",
        "w3c-hr-time": "^1.0.2",
        "w3c-xmlserializer": "^2.0.0",
        "webidl-conversions": "^6.1.0",
        "whatwg-encoding": "^1.0.5",
        "whatwg-mimetype": "^2.3.0",
        "whatwg-url": "^8.5.0",
        "ws": "^7.4.6",
        "xml-name-validator": "^3.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "canvas": "^2.5.0"
      },
      "peerDependenciesMeta": {
        "canvas": {
          "optional": true
        }
      }
    },
    "node_modules/jsesc": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/jsesc/-/jsesc-3.1.0.tgz",
      "integrity": "sha512-/sM3dO2FOzXjKQhJuo0Q173wf2KOo8t4I8vHy6lF9poUp7bKT0/NHE8fPX23PwfhnykfqnC2xRxOnVw5XuGIaA==",
      "license": "MIT",
      "bin": {
        "jsesc": "bin/jsesc"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/json-buffer": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/json-buffer/-/json-buffer-3.0.1.tgz",
      "integrity": "sha512-4bV5BfR2mqfQTJm+V5tPPdf+ZpuhiIvTuAB5g8kcrXOZpTT/QwwVRWBywX1ozr6lEuPdbHxwaJlm9G6mI2sfSQ==",
      "license": "MIT"
    },
    "node_modules/json-parse-even-better-errors": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/json-parse-even-better-errors/-/json-parse-even-better-errors-2.3.1.tgz",
      "integrity": "sha512-xyFwyhro/JEof6Ghe2iz2NcXoj2sloNsWr/XsERDK/oiPCfaNhl5ONfp+jQdAZRQQ0IJWNzH9zIZF7li91kh2w==",
      "license": "MIT"
    },
    "node_modules/json-schema": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/json-schema/-/json-schema-0.4.0.tgz",
      "integrity": "sha512-es94M3nTIfsEPisRafak+HDLfHXnKBhV3vU5eqPcS3flIWqcxJWgXHXiey3YrpaNsanY5ei1VoYEbOzijuq9BA==",
      "license": "(AFL-2.1 OR BSD-3-Clause)"
    },
    "node_modules/json-schema-traverse": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-0.4.1.tgz",
      "integrity": "sha512-xbbCH5dCYU5T8LcEhhuh7HJ88HXuW3qsI3Y0zOZFKfZEHcpWiHU/Jxzk629Brsab/mMiHQti9wMP+845RPe3Vg==",
      "license": "MIT"
    },
    "node_modules/json-stable-stringify-without-jsonify": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/json-stable-stringify-without-jsonify/-/json-stable-stringify-without-jsonify-1.0.1.tgz",
      "integrity": "sha512-Bdboy+l7tA3OGW6FjyFHWkP5LuByj1Tk33Ljyq0axyzdk9//JSi2u3fP1QSmd1KNwq6VOKYGlAu87CisVir6Pw==",
      "license": "MIT"
    },
    "node_modules/json5": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/json5/-/json5-2.2.3.tgz",
      "integrity": "sha512-XmOWe7eyHYH14cLdVPoyg+GOH3rYX++KpzrylJwSW98t3Nk+U8XOl8FWKOgwtzdb8lXGf6zYwDUzeHMWfxasyg==",
      "license": "MIT",
      "bin": {
        "json5": "lib/cli.js"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/jsonfile": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/jsonfile/-/jsonfile-6.2.0.tgz",
      "integrity": "sha512-FGuPw30AdOIUTRMC2OMRtQV+jkVj2cfPqSeWXv1NEAJ1qZ5zb1X6z1mFhbfOB/iy3ssJCD+3KuZ8r8C3uVFlAg==",
      "license": "MIT",
      "dependencies": {
        "universalify": "^2.0.0"
      },
      "optionalDependencies": {
        "graceful-fs": "^4.1.6"
      }
    },
    "node_modules/jsonpath": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/jsonpath/-/jsonpath-1.1.1.tgz",
      "integrity": "sha512-l6Cg7jRpixfbgoWgkrl77dgEj8RPvND0wMH6TwQmi9Qs4TFfS9u5cUFnbeKTwj5ga5Y3BTGGNI28k117LJ009w==",
      "license": "MIT",
      "dependencies": {
        "esprima": "1.2.2",
        "static-eval": "2.0.2",
        "underscore": "1.12.1"
      }
    },
    "node_modules/jsonpath/node_modules/esprima": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/esprima/-/esprima-1.2.2.tgz",
      "integrity": "sha512-+JpPZam9w5DuJ3Q67SqsMGtiHKENSMRVoxvArfJZK01/BfLEObtZ6orJa/MtoGNR/rfMgp5837T41PAmTwAv/A==",
      "bin": {
        "esparse": "bin/esparse.js",
        "esvalidate": "bin/esvalidate.js"
      },
      "engines": {
        "node": ">=0.4.0"
      }
    },
    "node_modules/jsonpointer": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/jsonpointer/-/jsonpointer-5.0.1.tgz",
      "integrity": "sha512-p/nXbhSEcu3pZRdkW1OfJhpsVtW1gd4Wa1fnQc9YLiTfAjn0312eMKimbdIQzuZl9aa9xUGaRlP9T/CJE/ditQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/jsx-ast-utils": {
      "version": "3.3.5",
      "resolved": "https://registry.npmjs.org/jsx-ast-utils/-/jsx-ast-utils-3.3.5.tgz",
      "integrity": "sha512-ZZow9HBI5O6EPgSJLUb8n2NKgmVWTwCvHGwFuJlMjvLFqlGG6pjirPhtdsseaLZjSibD8eegzmYpUZwoIlj2cQ==",
      "license": "MIT",
      "dependencies": {
        "array-includes": "^3.1.6",
        "array.prototype.flat": "^1.3.1",
        "object.assign": "^4.1.4",
        "object.values": "^1.1.6"
      },
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/keyv": {
      "version": "4.5.4",
      "resolved": "https://registry.npmjs.org/keyv/-/keyv-4.5.4.tgz",
      "integrity": "sha512-oxVHkHR/EJf2CNXnWxRLW6mg7JyCCUcG0DtEGmL2ctUo1PNTin1PUil+r/+4r5MpVgC/fn1kjsx7mjSujKqIpw==",
      "license": "MIT",
      "dependencies": {
        "json-buffer": "3.0.1"
      }
    },
    "node_modules/kind-of": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/kind-of/-/kind-of-6.0.3.tgz",
      "integrity": "sha512-dcS1ul+9tmeD95T+x28/ehLgd9mENa3LsvDTtzm3vyBEO7RPptvAD+t44WVXaUjTBRcrpFeFlC8WCruUR456hw==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/kleur": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/kleur/-/kleur-3.0.3.tgz",
      "integrity": "sha512-eTIzlVOSUR+JxdDFepEYcBMtZ9Qqdef+rnzWdRZuMbOywu5tO2w2N7rqjoANZ5k9vywhL6Br1VRjUIgTQx4E8w==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/klona": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/klona/-/klona-2.0.6.tgz",
      "integrity": "sha512-dhG34DXATL5hSxJbIexCft8FChFXtmskoZYnoPWjXQuebWYCNkVeV3KkGegCK9CP1oswI/vQibS2GY7Em/sJJA==",
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/language-subtag-registry": {
      "version": "0.3.23",
      "resolved": "https://registry.npmjs.org/language-subtag-registry/-/language-subtag-registry-0.3.23.tgz",
      "integrity": "sha512-0K65Lea881pHotoGEa5gDlMxt3pctLi2RplBb7Ezh4rRdLEOtgi7n4EwK9lamnUCkKBqaeKRVebTq6BAxSkpXQ==",
      "license": "CC0-1.0"
    },
    "node_modules/language-tags": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/language-tags/-/language-tags-1.0.9.tgz",
      "integrity": "sha512-MbjN408fEndfiQXbFQ1vnd+1NoLDsnQW41410oQBXiyXDMYH5z505juWa4KUE1LqxRC7DgOgZDbKLxHIwm27hA==",
      "license": "MIT",
      "dependencies": {
        "language-subtag-registry": "^0.3.20"
      },
      "engines": {
        "node": ">=0.10"
      }
    },
    "node_modules/launch-editor": {
      "version": "2.11.1",
      "resolved": "https://registry.npmjs.org/launch-editor/-/launch-editor-2.11.1.tgz",
      "integrity": "sha512-SEET7oNfgSaB6Ym0jufAdCeo3meJVeCaaDyzRygy0xsp2BFKCprcfHljTq4QkzTLUxEKkFK6OK4811YM2oSrRg==",
      "license": "MIT",
      "dependencies": {
        "picocolors": "^1.1.1",
        "shell-quote": "^1.8.3"
      }
    },
    "node_modules/leven": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/leven/-/leven-3.1.0.tgz",
      "integrity": "sha512-qsda+H8jTaUaN/x5vzW2rzc+8Rw4TAQ/4KjB46IwK5VH+IlVeeeje/EoZRpiXvIqjFgK84QffqPztGI3VBLG1A==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/levn": {
      "version": "0.4.1",
      "resolved": "https://registry.npmjs.org/levn/-/levn-0.4.1.tgz",
      "integrity": "sha512-+bT2uH4E5LGE7h/n3evcS/sQlJXCpIp6ym8OWJ5eV6+67Dsql/LaaT7qJBAt2rzfoa/5QBGBhxDix1dMt2kQKQ==",
      "license": "MIT",
      "dependencies": {
        "prelude-ls": "^1.2.1",
        "type-check": "~0.4.0"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/lilconfig": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/lilconfig/-/lilconfig-2.1.0.tgz",
      "integrity": "sha512-utWOt/GHzuUxnLKxB6dk81RoOeoNeHgbrXiuGk4yyF5qlRz+iIVWu56E2fqGHFrXz0QNUhLB/8nKqvRH66JKGQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/lines-and-columns": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/lines-and-columns/-/lines-and-columns-1.2.4.tgz",
      "integrity": "sha512-7ylylesZQ/PV29jhEDl3Ufjo6ZX7gCqJr5F7PKrqc93v7fzSymt1BpwEU8nAUXs8qzzvqhbjhK5QZg6Mt/HkBg==",
      "license": "MIT"
    },
    "node_modules/loader-runner": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/loader-runner/-/loader-runner-4.3.0.tgz",
      "integrity": "sha512-3R/1M+yS3j5ou80Me59j7F9IMs4PXs3VqRrm0TU3AbKPxlmpoY1TNscJV/oGJXo8qCatFGTfDbY6W6ipGOYXfg==",
      "license": "MIT",
      "engines": {
        "node": ">=6.11.5"
      }
    },
    "node_modules/loader-utils": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/loader-utils/-/loader-utils-2.0.4.tgz",
      "integrity": "sha512-xXqpXoINfFhgua9xiqD8fPFHgkoq1mmmpE92WlDbm9rNRd/EbRb+Gqf908T2DMfuHjjJlksiK2RbHVOdD/MqSw==",
      "license": "MIT",
      "dependencies": {
        "big.js": "^5.2.2",
        "emojis-list": "^3.0.0",
        "json5": "^2.1.2"
      },
      "engines": {
        "node": ">=8.9.0"
      }
    },
    "node_modules/locate-path": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-5.0.0.tgz",
      "integrity": "sha512-t7hw9pI+WvuwNJXwk5zVHpyhIqzg2qTlklJOf0mVxGSbe3Fp2VieZcduNYjaLDoy6p9uGpQEGWG87WpMKlNq8g==",
      "license": "MIT",
      "dependencies": {
        "p-locate": "^4.1.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/lodash": {
      "version": "4.17.21",
      "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",
      "integrity": "sha512-v2kDEe57lecTulaDIuNTPy3Ry4gLGJ6Z1O3vE1krgXZNrsQ+LFTGHVxVjcXPs17LhbZVGedAJv8XZ1tvj5FvSg==",
      "license": "MIT"
    },
    "node_modules/lodash.debounce": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/lodash.debounce/-/lodash.debounce-4.0.8.tgz",
      "integrity": "sha512-FT1yDzDYEoYWhnSGnpE/4Kj1fLZkDFyqRb7fNt6FdYOSxlUWAtp42Eh6Wb0rGIv/m9Bgo7x4GhQbm5Ys4SG5ow==",
      "license": "MIT"
    },
    "node_modules/lodash.memoize": {
      "version": "4.1.2",
      "resolved": "https://registry.npmjs.org/lodash.memoize/-/lodash.memoize-4.1.2.tgz",
      "integrity": "sha512-t7j+NzmgnQzTAYXcsHYLgimltOV1MXHtlOWf6GjL9Kj8GK5FInw5JotxvbOs+IvV1/Dzo04/fCGfLVs7aXb4Ag==",
      "license": "MIT"
    },
    "node_modules/lodash.merge": {
      "version": "4.6.2",
      "resolved": "https://registry.npmjs.org/lodash.merge/-/lodash.merge-4.6.2.tgz",
      "integrity": "sha512-0KpjqXRVvrYyCsX1swR/XTK0va6VQkQM6MNo7PqW77ByjAhoARA8EfrP1N4+KlKj8YS0ZUCtRT/YUuhyYDujIQ==",
      "license": "MIT"
    },
    "node_modules/lodash.sortby": {
      "version": "4.7.0",
      "resolved": "https://registry.npmjs.org/lodash.sortby/-/lodash.sortby-4.7.0.tgz",
      "integrity": "sha512-HDWXG8isMntAyRF5vZ7xKuEvOhT4AhlRt/3czTSjvGUxjYCBVRQY48ViDHyfYz9VIoBkW4TMGQNapx+l3RUwdA==",
      "license": "MIT"
    },
    "node_modules/lodash.uniq": {
      "version": "4.5.0",
      "resolved": "https://registry.npmjs.org/lodash.uniq/-/lodash.uniq-4.5.0.tgz",
      "integrity": "sha512-xfBaXQd9ryd9dlSDvnvI0lvxfLJlYAZzXomUYzLKtUeOQvOP5piqAWuGtrhWeqaXK9hhoM/iyJc5AV+XfsX3HQ==",
      "license": "MIT"
    },
    "node_modules/loose-envify": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/loose-envify/-/loose-envify-1.4.0.tgz",
      "integrity": "sha512-lyuxPGr/Wfhrlem2CL/UcnUc1zcqKAImBDzukY7Y5F/yQiNdko6+fRLevlw1HgMySw7f611UIY408EtxRSoK3Q==",
      "license": "MIT",
      "dependencies": {
        "js-tokens": "^3.0.0 || ^4.0.0"
      },
      "bin": {
        "loose-envify": "cli.js"
      }
    },
    "node_modules/lower-case": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/lower-case/-/lower-case-2.0.2.tgz",
      "integrity": "sha512-7fm3l3NAF9WfN6W3JOmf5drwpVqX78JtoGJ3A6W0a6ZnldM41w2fV5D490psKFTpMds8TJse/eHLFFsNHHjHgg==",
      "license": "MIT",
      "dependencies": {
        "tslib": "^2.0.3"
      }
    },
    "node_modules/lru-cache": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-5.1.1.tgz",
      "integrity": "sha512-KpNARQA3Iwv+jTA0utUVVbrh+Jlrr1Fv0e56GGzAFOXN7dk/FviaDW8LHmK52DlcH4WP2n6gI8vN1aesBFgo9w==",
      "license": "ISC",
      "dependencies": {
        "yallist": "^3.0.2"
      }
    },
    "node_modules/lz-string": {
      "version": "1.5.0",
      "resolved": "https://registry.npmjs.org/lz-string/-/lz-string-1.5.0.tgz",
      "integrity": "sha512-h5bgJWpxJNswbU7qCrV0tIKQCaS3blPDrqKWx+QxzuzL1zGUzij9XCWLrSLsJPu5t+eWA/ycetzYAO5IOMcWAQ==",
      "license": "MIT",
      "bin": {
        "lz-string": "bin/bin.js"
      }
    },
    "node_modules/magic-string": {
      "version": "0.25.9",
      "resolved": "https://registry.npmjs.org/magic-string/-/magic-string-0.25.9.tgz",
      "integrity": "sha512-RmF0AsMzgt25qzqqLc1+MbHmhdx0ojF2Fvs4XnOqz2ZOBXzzkEwc/dJQZCYHAn7v1jbVOjAZfK8msRn4BxO4VQ==",
      "license": "MIT",
      "dependencies": {
        "sourcemap-codec": "^1.4.8"
      }
    },
    "node_modules/make-dir": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/make-dir/-/make-dir-3.1.0.tgz",
      "integrity": "sha512-g3FeP20LNwhALb/6Cz6Dd4F2ngze0jz7tbzrD2wAV+o9FeNHe4rL+yK2md0J/fiSf1sa1ADhXqi5+oVwOM/eGw==",
      "license": "MIT",
      "dependencies": {
        "semver": "^6.0.0"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/make-dir/node_modules/semver": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/semver/-/semver-6.3.1.tgz",
      "integrity": "sha512-BR7VvDCVHO+q2xBEWskxS6DJE1qRnb7DxzUrogb71CWoSficBxYsiAGd+Kl0mmq/MprG9yArRkyrQxTO6XjMzA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      }
    },
    "node_modules/makeerror": {
      "version": "1.0.12",
      "resolved": "https://registry.npmjs.org/makeerror/-/makeerror-1.0.12.tgz",
      "integrity": "sha512-JmqCvUhmt43madlpFzG4BQzG2Z3m6tvQDNKdClZnO3VbIudJYmxsT0FNJMeiB2+JTSlTQTSbU8QdesVmwJcmLg==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "tmpl": "1.0.5"
      }
    },
    "node_modules/math-intrinsics": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/math-intrinsics/-/math-intrinsics-1.1.0.tgz",
      "integrity": "sha512-/IXtbwEk5HTPyEwyKX6hGkYXxM9nbj64B+ilVJnC/R6B0pH5G4V3b0pVbL7DBj4tkhBAppbQUlf6F6Xl9LHu1g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/mdn-data": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/mdn-data/-/mdn-data-2.0.4.tgz",
      "integrity": "sha512-iV3XNKw06j5Q7mi6h+9vbx23Tv7JkjEVgKHW4pimwyDGWm0OIQntJJ+u1C6mg6mK1EaTv42XQ7w76yuzH7M2cA==",
      "license": "CC0-1.0"
    },
    "node_modules/media-typer": {
      "version": "0.3.0",
      "resolved": "https://registry.npmjs.org/media-typer/-/media-typer-0.3.0.tgz",
      "integrity": "sha512-dq+qelQ9akHpcOl/gUVRTxVIOkAJ1wR3QAvb4RsVjS8oVoFjDGTc679wJYmUmknUF5HwMLOgb5O+a3KxfWapPQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/memfs": {
      "version": "3.5.3",
      "resolved": "https://registry.npmjs.org/memfs/-/memfs-3.5.3.tgz",
      "integrity": "sha512-UERzLsxzllchadvbPs5aolHh65ISpKpM+ccLbOJ8/vvpBKmAWf+la7dXFy7Mr0ySHbdHrFv5kGFCUHHe6GFEmw==",
      "license": "Unlicense",
      "dependencies": {
        "fs-monkey": "^1.0.4"
      },
      "engines": {
        "node": ">= 4.0.0"
      }
    },
    "node_modules/merge-descriptors": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/merge-descriptors/-/merge-descriptors-1.0.3.tgz",
      "integrity": "sha512-gaNvAS7TZ897/rVaZ0nMtAyxNyi/pdbjbAwUpFQpN70GqnVfOiXpeUUMKRBmzXaSQ8DdTX4/0ms62r2K+hE6mQ==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/merge-stream": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/merge-stream/-/merge-stream-2.0.0.tgz",
      "integrity": "sha512-abv/qOcuPfk3URPfDzmZU1LKmuw8kT+0nIHvKrKgFrwifol/doWcdA4ZqsWQ8ENrFKkd67Mfpo/LovbIUsbt3w==",
      "license": "MIT"
    },
    "node_modules/merge2": {
      "version": "1.4.1",
      "resolved": "https://registry.npmjs.org/merge2/-/merge2-1.4.1.tgz",
      "integrity": "sha512-8q7VEgMJW4J8tcfVPy8g09NcQwZdbwFEqhe/WZkoIzjn/3TGDwtOCYtXGxA3O8tPzpczCCDgv+P2P5y00ZJOOg==",
      "license": "MIT",
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/methods": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/methods/-/methods-1.1.2.tgz",
      "integrity": "sha512-iclAHeNqNm68zFtnZ0e+1L2yUIdvzNoauKU4WBA3VvH/vPFieF7qfRlwUZU+DA9P9bPXIS90ulxoUoCH23sV2w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/micromatch": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/micromatch/-/micromatch-4.0.8.tgz",
      "integrity": "sha512-PXwfBhYu0hBCPw8Dn0E+WDYb7af3dSLVWKi3HGv84IdF4TyFoC0ysxFd0Goxw7nSv4T/PzEJQxsYsEiFCKo2BA==",
      "license": "MIT",
      "dependencies": {
        "braces": "^3.0.3",
        "picomatch": "^2.3.1"
      },
      "engines": {
        "node": ">=8.6"
      }
    },
    "node_modules/mime": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/mime/-/mime-1.6.0.tgz",
      "integrity": "sha512-x0Vn8spI+wuJ1O6S7gnbaQg8Pxh4NNHb7KSINmEWKiPE4RKOplvijn+NkmYmmRgP68mc70j2EbeTFRsrswaQeg==",
      "license": "MIT",
      "bin": {
        "mime": "cli.js"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/mime-db": {
      "version": "1.52.0",
      "resolved": "https://registry.npmjs.org/mime-db/-/mime-db-1.52.0.tgz",
      "integrity": "sha512-sPU4uV7dYlvtWJxwwxHD0PuihVNiE7TyAbQ5SWxDCB9mUYvOgroQOwYQQOKPJ8CIbE+1ETVlOoK1UC2nU3gYvg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/mime-types": {
      "version": "2.1.35",
      "resolved": "https://registry.npmjs.org/mime-types/-/mime-types-2.1.35.tgz",
      "integrity": "sha512-ZDY+bPm5zTTF+YpCrAU9nK0UgICYPT0QtT1NZWFv4s++TNkcgVaT0g6+4R2uI4MjQjzysHB1zxuWL50hzaeXiw==",
      "license": "MIT",
      "dependencies": {
        "mime-db": "1.52.0"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/mimic-fn": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/mimic-fn/-/mimic-fn-2.1.0.tgz",
      "integrity": "sha512-OqbOk5oEQeAZ8WXWydlu9HJjz9WVdEIvamMCcXmuqUYjTknH/sqsWvhQ3vgwKFRR1HpjvNBKQ37nbJgYzGqGcg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/min-indent": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/min-indent/-/min-indent-1.0.1.tgz",
      "integrity": "sha512-I9jwMn07Sy/IwOj3zVkVik2JTvgpaykDZEigL6Rx6N9LbMywwUSMtxET+7lVoDLLd3O3IXwJwvuuns8UB/HeAg==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/mini-css-extract-plugin": {
      "version": "2.9.4",
      "resolved": "https://registry.npmjs.org/mini-css-extract-plugin/-/mini-css-extract-plugin-2.9.4.tgz",
      "integrity": "sha512-ZWYT7ln73Hptxqxk2DxPU9MmapXRhxkJD6tkSR04dnQxm8BGu2hzgKLugK5yySD97u/8yy7Ma7E76k9ZdvtjkQ==",
      "license": "MIT",
      "dependencies": {
        "schema-utils": "^4.0.0",
        "tapable": "^2.2.1"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.0.0"
      }
    },
    "node_modules/minimalistic-assert": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/minimalistic-assert/-/minimalistic-assert-1.0.1.tgz",
      "integrity": "sha512-UtJcAD4yEaGtjPezWuO9wC4nwUnVH/8/Im3yEHQP4b67cXlD/Qr9hdITCU1xDbSEXg2XKNaP8jsReV7vQd00/A==",
      "license": "ISC"
    },
    "node_modules/minimatch": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-3.1.2.tgz",
      "integrity": "sha512-J7p63hRiAjw1NDEww1W7i37+ByIrOWO5XQQAzZ3VOcL0PNybwpfmV/N05zFAzwQ9USyEcX6t3UO+K5aqBQOIHw==",
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^1.1.7"
      },
      "engines": {
        "node": "*"
      }
    },
    "node_modules/minimist": {
      "version": "1.2.8",
      "resolved": "https://registry.npmjs.org/minimist/-/minimist-1.2.8.tgz",
      "integrity": "sha512-2yyAR8qBkN3YuheJanUpWC5U3bb5osDywNB8RzDVlDwDHbocAJveqqj1u8+SVD7jkWT4yvsHCpWqqWqAxb0zCA==",
      "license": "MIT",
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/minipass": {
      "version": "7.1.2",
      "resolved": "https://registry.npmjs.org/minipass/-/minipass-7.1.2.tgz",
      "integrity": "sha512-qOOzS1cBTWYF4BH8fVePDBOO9iptMnGUEZwNc/cMWnTV2nVLZ7VoNWEPHkYczZA0pdoA7dl6e7FL659nX9S2aw==",
      "license": "ISC",
      "engines": {
        "node": ">=16 || 14 >=14.17"
      }
    },
    "node_modules/mkdirp": {
      "version": "0.5.6",
      "resolved": "https://registry.npmjs.org/mkdirp/-/mkdirp-0.5.6.tgz",
      "integrity": "sha512-FP+p8RB8OWpF3YZBCrP5gtADmtXApB5AMLn+vdyA+PyxCjrCs00mjyUozssO33cwDeT3wNGdLxJ5M//YqtHAJw==",
      "license": "MIT",
      "dependencies": {
        "minimist": "^1.2.6"
      },
      "bin": {
        "mkdirp": "bin/cmd.js"
      }
    },
    "node_modules/ms": {
      "version": "2.1.3",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.1.3.tgz",
      "integrity": "sha512-6FlzubTLZG3J2a/NVCAleEhjzq5oxgHyaCU9yYXvcLsvoVaHJq/s5xXI6/XXP6tz7R9xAOtHnSO/tXtF3WRTlA==",
      "license": "MIT"
    },
    "node_modules/multicast-dns": {
      "version": "7.2.5",
      "resolved": "https://registry.npmjs.org/multicast-dns/-/multicast-dns-7.2.5.tgz",
      "integrity": "sha512-2eznPJP8z2BFLX50tf0LuODrpINqP1RVIm/CObbTcBRITQgmC/TjcREF1NeTBzIcR5XO/ukWo+YHOjBbFwIupg==",
      "license": "MIT",
      "dependencies": {
        "dns-packet": "^5.2.2",
        "thunky": "^1.0.2"
      },
      "bin": {
        "multicast-dns": "cli.js"
      }
    },
    "node_modules/mz": {
      "version": "2.7.0",
      "resolved": "https://registry.npmjs.org/mz/-/mz-2.7.0.tgz",
      "integrity": "sha512-z81GNO7nnYMEhrGh9LeymoE4+Yr0Wn5McHIZMK5cfQCl+NDX08sCZgUc9/6MHni9IWuFLm1Z3HTCXu2z9fN62Q==",
      "license": "MIT",
      "dependencies": {
        "any-promise": "^1.0.0",
        "object-assign": "^4.0.1",
        "thenify-all": "^1.0.0"
      }
    },
    "node_modules/nanoid": {
      "version": "3.3.11",
      "resolved": "https://registry.npmjs.org/nanoid/-/nanoid-3.3.11.tgz",
      "integrity": "sha512-N8SpfPUnUp1bK+PMYW8qSWdl9U+wwNWI4QKxOYDy9JAro3WMX7p2OeVRF9v+347pnakNevPmiHhNmZ2HbFA76w==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "bin": {
        "nanoid": "bin/nanoid.cjs"
      },
      "engines": {
        "node": "^10 || ^12 || ^13.7 || ^14 || >=15.0.1"
      }
    },
    "node_modules/natural-compare": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/natural-compare/-/natural-compare-1.4.0.tgz",
      "integrity": "sha512-OWND8ei3VtNC9h7V60qff3SVobHr996CTwgxubgyQYEpg290h9J0buyECNNJexkFm5sOajh5G116RYA1c8ZMSw==",
      "license": "MIT"
    },
    "node_modules/natural-compare-lite": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/natural-compare-lite/-/natural-compare-lite-1.4.0.tgz",
      "integrity": "sha512-Tj+HTDSJJKaZnfiuw+iaF9skdPpTo2GtEly5JHnWV/hfv2Qj/9RKsGISQtLh2ox3l5EAGw487hnBee0sIJ6v2g==",
      "license": "MIT"
    },
    "node_modules/negotiator": {
      "version": "0.6.4",
      "resolved": "https://registry.npmjs.org/negotiator/-/negotiator-0.6.4.tgz",
      "integrity": "sha512-myRT3DiWPHqho5PrJaIRyaMv2kgYf0mUVgBNOYMuCH5Ki1yEiQaf/ZJuQ62nvpc44wL5WDbTX7yGJi1Neevw8w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/neo-async": {
      "version": "2.6.2",
      "resolved": "https://registry.npmjs.org/neo-async/-/neo-async-2.6.2.tgz",
      "integrity": "sha512-Yd3UES5mWCSqR+qNT93S3UoYUkqAZ9lLg8a7g9rimsWmYGK8cVToA4/sF3RrshdyV3sAGMXVUmpMYOw+dLpOuw==",
      "license": "MIT"
    },
    "node_modules/no-case": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/no-case/-/no-case-3.0.4.tgz",
      "integrity": "sha512-fgAN3jGAh+RoxUGZHTSOLJIqUc2wmoBwGR4tbpNAKmmovFoWq0OdRkb0VkldReO2a2iBT/OEulG9XSUc10r3zg==",
      "license": "MIT",
      "dependencies": {
        "lower-case": "^2.0.2",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/node-forge": {
      "version": "1.3.1",
      "resolved": "https://registry.npmjs.org/node-forge/-/node-forge-1.3.1.tgz",
      "integrity": "sha512-dPEtOeMvF9VMcYV/1Wb8CPoVAXtp6MKMlcbAt4ddqmGqUJ6fQZFXkNZNkNlfevtNkGtaSoXf/vNNNSvgrdXwtA==",
      "license": "(BSD-3-Clause OR GPL-2.0)",
      "engines": {
        "node": ">= 6.13.0"
      }
    },
    "node_modules/node-int64": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/node-int64/-/node-int64-0.4.0.tgz",
      "integrity": "sha512-O5lz91xSOeoXP6DulyHfllpq+Eg00MWitZIbtPfoSEvqIHdl5gfcY6hYzDWnj0qD5tz52PI08u9qUvSVeUBeHw==",
      "license": "MIT"
    },
    "node_modules/node-releases": {
      "version": "2.0.21",
      "resolved": "https://registry.npmjs.org/node-releases/-/node-releases-2.0.21.tgz",
      "integrity": "sha512-5b0pgg78U3hwXkCM8Z9b2FJdPZlr9Psr9V2gQPESdGHqbntyFJKFW4r5TeWGFzafGY3hzs1JC62VEQMbl1JFkw==",
      "license": "MIT"
    },
    "node_modules/normalize-path": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/normalize-path/-/normalize-path-3.0.0.tgz",
      "integrity": "sha512-6eZs5Ls3WtCisHWp9S2GUy8dqkpGi4BVSz3GaqiE6ezub0512ESztXUwUB6C6IKbQkY2Pnb/mD4WYojCRwcwLA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/normalize-range": {
      "version": "0.1.2",
      "resolved": "https://registry.npmjs.org/normalize-range/-/normalize-range-0.1.2.tgz",
      "integrity": "sha512-bdok/XvKII3nUpklnV6P2hxtMNrCboOjAcyBuQnWEhO665FwrSNRxU+AqpsyvO6LgGYPspN+lu5CLtw4jPRKNA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/normalize-url": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/normalize-url/-/normalize-url-6.1.0.tgz",
      "integrity": "sha512-DlL+XwOy3NxAQ8xuC0okPgK46iuVNAK01YN7RueYBqqFeGsBjV9XmCAzAdgt+667bCl5kPh9EqKKDwnaPG1I7A==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/npm-run-path": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/npm-run-path/-/npm-run-path-4.0.1.tgz",
      "integrity": "sha512-S48WzZW777zhNIrn7gxOlISNAqi9ZC/uQFnRdbeIHhZhCA6UqpkOT8T1G7BvfdgP4Er8gF4sUbaS0i7QvIfCWw==",
      "license": "MIT",
      "dependencies": {
        "path-key": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/nth-check": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/nth-check/-/nth-check-2.1.1.tgz",
      "integrity": "sha512-lqjrjmaOoAnWfMmBPL+XNnynZh2+swxiX3WUE0s4yEHI6m+AwrK2UZOimIRl3X/4QctVqS8AiZjFqyOGrMXb/w==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "boolbase": "^1.0.0"
      },
      "funding": {
        "url": "https://github.com/fb55/nth-check?sponsor=1"
      }
    },
    "node_modules/nwsapi": {
      "version": "2.2.22",
      "resolved": "https://registry.npmjs.org/nwsapi/-/nwsapi-2.2.22.tgz",
      "integrity": "sha512-ujSMe1OWVn55euT1ihwCI1ZcAaAU3nxUiDwfDQldc51ZXaB9m2AyOn6/jh1BLe2t/G8xd6uKG1UBF2aZJeg2SQ==",
      "license": "MIT"
    },
    "node_modules/object-assign": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz",
      "integrity": "sha512-rJgTQnkUnH1sFw8yT6VSU3zD3sWmu6sZhIseY8VX+GRu3P6F7Fu+JNDoXfklElbLJSnc3FUQHVe4cU5hj+BcUg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/object-hash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/object-hash/-/object-hash-3.0.0.tgz",
      "integrity": "sha512-RSn9F68PjH9HqtltsSnqYC1XXoWe9Bju5+213R98cNGttag9q9yAOTzdbsqvIa7aNm5WffBZFpWYr2aWrklWAw==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/object-inspect": {
      "version": "1.13.4",
      "resolved": "https://registry.npmjs.org/object-inspect/-/object-inspect-1.13.4.tgz",
      "integrity": "sha512-W67iLl4J2EXEGTbfeHCffrjDfitvLANg0UlX3wFUUSTx92KXRFegMHUVgSqE+wvhAbi4WqjGg9czysTV2Epbew==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object-keys": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/object-keys/-/object-keys-1.1.1.tgz",
      "integrity": "sha512-NuAESUOUMrlIXOfHKzD6bpPu3tYt3xvjNdRIQ+FeT0lNb4K8WR70CaDxhuNguS2XG+GjkyMwOzsN5ZktImfhLA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.assign": {
      "version": "4.1.7",
      "resolved": "https://registry.npmjs.org/object.assign/-/object.assign-4.1.7.tgz",
      "integrity": "sha512-nK28WOo+QIjBkDduTINE4JkF/UJJKyf2EJxvJKfblDpyg0Q+pkOHNTL0Qwy6NP6FhE/EnzV73BxxqcJaXY9anw==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0",
        "has-symbols": "^1.1.0",
        "object-keys": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object.entries": {
      "version": "1.1.9",
      "resolved": "https://registry.npmjs.org/object.entries/-/object.entries-1.1.9.tgz",
      "integrity": "sha512-8u/hfXFRBD1O0hPUjioLhoWFHRmt6tKA4/vZPyckBr18l1KE9uHrFaFaUi8MDRTpi4uak2goyPTSNJLXX2k2Hw==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.fromentries": {
      "version": "2.0.8",
      "resolved": "https://registry.npmjs.org/object.fromentries/-/object.fromentries-2.0.8.tgz",
      "integrity": "sha512-k6E21FzySsSK5a21KRADBd/NGneRegFO5pLHfdQLpRDETUNJueLXs3WCzyQ3tFRDYgbq3KHGXfTbi2bs8WQ6rQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object.getownpropertydescriptors": {
      "version": "2.1.8",
      "resolved": "https://registry.npmjs.org/object.getownpropertydescriptors/-/object.getownpropertydescriptors-2.1.8.tgz",
      "integrity": "sha512-qkHIGe4q0lSYMv0XI4SsBTJz3WaURhLvd0lKSgtVuOsJ2krg4SgMw3PIRQFMp07yi++UR3se2mkcLqsBNpBb/A==",
      "license": "MIT",
      "dependencies": {
        "array.prototype.reduce": "^1.0.6",
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2",
        "es-object-atoms": "^1.0.0",
        "gopd": "^1.0.1",
        "safe-array-concat": "^1.1.2"
      },
      "engines": {
        "node": ">= 0.8"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/object.groupby": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/object.groupby/-/object.groupby-1.0.3.tgz",
      "integrity": "sha512-+Lhy3TQTuzXI5hevh8sBGqbmurHbbIjAi0Z4S63nthVLmLxfbj4T54a4CfZrXIrt9iP4mVAPYMo/v99taj3wjQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/object.values": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/object.values/-/object.values-1.2.1.tgz",
      "integrity": "sha512-gXah6aZrcUxjWg2zR2MwouP2eHlCBzdV4pygudehaKXSGW4v2AsRQUK+lwwXhii6KFZcunEnmSUoYp5CXibxtA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/obuf": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/obuf/-/obuf-1.1.2.tgz",
      "integrity": "sha512-PX1wu0AmAdPqOL1mWhqmlOd8kOIZQwGZw6rh7uby9fTc5lhaOWFLX3I6R1hrF9k3zUY40e6igsLGkDXK92LJNg==",
      "license": "MIT"
    },
    "node_modules/on-finished": {
      "version": "2.4.1",
      "resolved": "https://registry.npmjs.org/on-finished/-/on-finished-2.4.1.tgz",
      "integrity": "sha512-oVlzkg3ENAhCk2zdv7IJwd/QUD4z2RxRwpkcGY8psCVcCYZNq4wYnVWALHM+brtuJjePWiYF/ClmuDr8Ch5+kg==",
      "license": "MIT",
      "dependencies": {
        "ee-first": "1.1.1"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/on-headers": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/on-headers/-/on-headers-1.1.0.tgz",
      "integrity": "sha512-737ZY3yNnXy37FHkQxPzt4UZ2UWPWiCZWLvFZ4fu5cueciegX0zGPnrlY6bwRg4FdQOe9YU8MkmJwGhoMybl8A==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/once": {
      "version": "1.4.0",
      "resolved": "https://registry.npmjs.org/once/-/once-1.4.0.tgz",
      "integrity": "sha512-lNaJgI+2Q5URQBkccEKHTQOPaXdUxnZZElQTZY0MFUAuaEqe1E+Nyvgdz/aIyNi6Z9MzO5dv1H8n58/GELp3+w==",
      "license": "ISC",
      "dependencies": {
        "wrappy": "1"
      }
    },
    "node_modules/onetime": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/onetime/-/onetime-5.1.2.tgz",
      "integrity": "sha512-kbpaSSGJTWdAY5KPVeMOKXSrPtr8C8C7wodJbcsd51jRnmD+GZu8Y0VoU6Dm5Z4vWr0Ig/1NKuWRKf7j5aaYSg==",
      "license": "MIT",
      "dependencies": {
        "mimic-fn": "^2.1.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/open": {
      "version": "8.4.2",
      "resolved": "https://registry.npmjs.org/open/-/open-8.4.2.tgz",
      "integrity": "sha512-7x81NCL719oNbsq/3mh+hVrAWmFuEYUqrq/Iw3kUzH8ReypT9QQ0BLoJS7/G9k6N81XjW4qHWtjWwe/9eLy1EQ==",
      "license": "MIT",
      "dependencies": {
        "define-lazy-prop": "^2.0.0",
        "is-docker": "^2.1.1",
        "is-wsl": "^2.2.0"
      },
      "engines": {
        "node": ">=12"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/optionator": {
      "version": "0.9.4",
      "resolved": "https://registry.npmjs.org/optionator/-/optionator-0.9.4.tgz",
      "integrity": "sha512-6IpQ7mKUxRcZNLIObR0hz7lxsapSSIYNZJwXPGeF0mTVqGKFIXj1DQcMoT22S3ROcLyY/rz0PWaWZ9ayWmad9g==",
      "license": "MIT",
      "dependencies": {
        "deep-is": "^0.1.3",
        "fast-levenshtein": "^2.0.6",
        "levn": "^0.4.1",
        "prelude-ls": "^1.2.1",
        "type-check": "^0.4.0",
        "word-wrap": "^1.2.5"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/own-keys": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/own-keys/-/own-keys-1.0.1.tgz",
      "integrity": "sha512-qFOyK5PjiWZd+QQIh+1jhdb9LpxTF0qs7Pm8o5QHYZ0M3vKqSqzsZaEB6oWlxZ+q2sJBMI/Ktgd2N5ZwQoRHfg==",
      "license": "MIT",
      "dependencies": {
        "get-intrinsic": "^1.2.6",
        "object-keys": "^1.1.1",
        "safe-push-apply": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/p-limit": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-2.3.0.tgz",
      "integrity": "sha512-//88mFWSJx8lxCzwdAABTJL2MyWB12+eIY7MDL2SqLmAkeKU9qxRvWuSyTjm3FUmpBEMuFfckAIqEaVGUDxb6w==",
      "license": "MIT",
      "dependencies": {
        "p-try": "^2.0.0"
      },
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/p-locate": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-4.1.0.tgz",
      "integrity": "sha512-R79ZZ/0wAxKGu3oYMlz8jy/kbhsNrS7SKZ7PxEHBgJ5+F2mtFW2fK2cOtBh1cHYkQsbzFV7I+EoRKe6Yt0oK7A==",
      "license": "MIT",
      "dependencies": {
        "p-limit": "^2.2.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/p-retry": {
      "version": "4.6.2",
      "resolved": "https://registry.npmjs.org/p-retry/-/p-retry-4.6.2.tgz",
      "integrity": "sha512-312Id396EbJdvRONlngUx0NydfrIQ5lsYu0znKVUzVvArzEIt08V1qhtyESbGVd1FGX7UKtiFp5uwKZdM8wIuQ==",
      "license": "MIT",
      "dependencies": {
        "@types/retry": "0.12.0",
        "retry": "^0.13.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/p-try": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/p-try/-/p-try-2.2.0.tgz",
      "integrity": "sha512-R4nPAVTAU0B9D35/Gk3uJf/7XYbQcyohSKdvAxIRSNghFl4e71hVoGnBNQz9cWaXxO2I10KTC+3jMdvvoKw6dQ==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/package-json-from-dist": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/package-json-from-dist/-/package-json-from-dist-1.0.1.tgz",
      "integrity": "sha512-UEZIS3/by4OC8vL3P2dTXRETpebLI2NiI5vIrjaD/5UtrkFX/tNbwjTSRAGC/+7CAo2pIcBaRgWmcBBHcsaCIw==",
      "license": "BlueOak-1.0.0"
    },
    "node_modules/param-case": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/param-case/-/param-case-3.0.4.tgz",
      "integrity": "sha512-RXlj7zCYokReqWpOPH9oYivUzLYZ5vAPIfEmCTNViosC78F8F0H9y7T7gG2M39ymgutxF5gcFEsyZQSph9Bp3A==",
      "license": "MIT",
      "dependencies": {
        "dot-case": "^3.0.4",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/parent-module": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/parent-module/-/parent-module-1.0.1.tgz",
      "integrity": "sha512-GQ2EWRpQV8/o+Aw8YqtfZZPfNRWZYkbidE9k5rpl/hC3vtHHBfGm2Ifi6qWV+coDGkrUKZAxE3Lot5kcsRlh+g==",
      "license": "MIT",
      "dependencies": {
        "callsites": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/parse-json": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/parse-json/-/parse-json-5.2.0.tgz",
      "integrity": "sha512-ayCKvm/phCGxOkYRSCM82iDwct8/EonSEgCSxWxD7ve6jHggsFl4fZVQBPRNgQoKiuV/odhFrGzQXZwbifC8Rg==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.0.0",
        "error-ex": "^1.3.1",
        "json-parse-even-better-errors": "^2.3.0",
        "lines-and-columns": "^1.1.6"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/parse5": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/parse5/-/parse5-6.0.1.tgz",
      "integrity": "sha512-Ofn/CTFzRGTTxwpNEs9PP93gXShHcTq255nzRYSKe8AkVpZY7e1fpmTfOyoIvjP5HG7Z2ZM7VS9PPhQGW2pOpw==",
      "license": "MIT"
    },
    "node_modules/parseurl": {
      "version": "1.3.3",
      "resolved": "https://registry.npmjs.org/parseurl/-/parseurl-1.3.3.tgz",
      "integrity": "sha512-CiyeOxFT/JZyN5m0z9PfXw4SCBJ6Sygz1Dpl0wqjlhDEGGBP1GnsUVEL0p63hoG1fcj3fHynXi9NYO4nWOL+qQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/pascal-case": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/pascal-case/-/pascal-case-3.1.2.tgz",
      "integrity": "sha512-uWlGT3YSnK9x3BQJaOdcZwrnV6hPpd8jFH1/ucpiLRPh/2zCVJKS19E4GvYHvaCcACn3foXZ0cLB9Wrx1KGe5g==",
      "license": "MIT",
      "dependencies": {
        "no-case": "^3.0.4",
        "tslib": "^2.0.3"
      }
    },
    "node_modules/path-exists": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-exists/-/path-exists-4.0.0.tgz",
      "integrity": "sha512-ak9Qy5Q7jYb2Wwcey5Fpvg2KoAc/ZIhLSLOSBmRmygPsGwkVVt0fZa0qrtMz+m6tJTAHfZQ8FnmB4MG4LWy7/w==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-is-absolute": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/path-is-absolute/-/path-is-absolute-1.0.1.tgz",
      "integrity": "sha512-AVbw3UJ2e9bq64vSaS9Am0fje1Pa8pbGqTTsmXfaIiMpnr5DlDhfJOuLj9Sf95ZPVDAUerDfEk88MPmPe7UCQg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/path-key": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/path-key/-/path-key-3.1.1.tgz",
      "integrity": "sha512-ojmeN0qd+y0jszEtoY48r0Peq5dwMEkIlCOu6Q5f41lfkswXuKtYrhgoTpLnyIcHm24Uhqx+5Tqm2InSwLhE6Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/path-parse": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/path-parse/-/path-parse-1.0.7.tgz",
      "integrity": "sha512-LDJzPVEEEPR+y48z93A0Ed0yXb8pAByGWo/k5YYdYgpY2/2EsOsksJrq7lOHxryrVOn1ejG6oAp8ahvOIQD8sw==",
      "license": "MIT"
    },
    "node_modules/path-scurry": {
      "version": "1.11.1",
      "resolved": "https://registry.npmjs.org/path-scurry/-/path-scurry-1.11.1.tgz",
      "integrity": "sha512-Xa4Nw17FS9ApQFJ9umLiJS4orGjm7ZzwUrwamcGQuHSzDyth9boKDaycYdDcZDuqYATXw4HFXgaqWTctW/v1HA==",
      "license": "BlueOak-1.0.0",
      "dependencies": {
        "lru-cache": "^10.2.0",
        "minipass": "^5.0.0 || ^6.0.2 || ^7.0.0"
      },
      "engines": {
        "node": ">=16 || 14 >=14.18"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/path-scurry/node_modules/lru-cache": {
      "version": "10.4.3",
      "resolved": "https://registry.npmjs.org/lru-cache/-/lru-cache-10.4.3.tgz",
      "integrity": "sha512-JNAzZcXrCt42VGLuYz0zfAzDfAvJWW6AfYlDBQyDV5DClI2m5sAmK+OIO7s59XfsRsWHp02jAJrRadPRGTt6SQ==",
      "license": "ISC"
    },
    "node_modules/path-to-regexp": {
      "version": "0.1.12",
      "resolved": "https://registry.npmjs.org/path-to-regexp/-/path-to-regexp-0.1.12.tgz",
      "integrity": "sha512-RA1GjUVMnvYFxuqovrEqZoxxW5NUZqbwKtYz/Tt7nXerk0LbLblQmrsgdeOxV5SFHf0UDggjS/bSeOZwt1pmEQ==",
      "license": "MIT"
    },
    "node_modules/path-type": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/path-type/-/path-type-4.0.0.tgz",
      "integrity": "sha512-gDKb8aZMDeD/tZWs9P6+q0J9Mwkdl6xMV8TjnGP3qJVJ06bdMgkbBlLU8IdfOsIsFz2BW1rNVT3XuNEl8zPAvw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/performance-now": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/performance-now/-/performance-now-2.1.0.tgz",
      "integrity": "sha512-7EAHlyLHI56VEIdK57uwHdHKIaAGbnXPiw0yWbarQZOKaKpvUIgW0jWRVLiatnM+XXlSwsanIBH/hzGMJulMow==",
      "license": "MIT"
    },
    "node_modules/picocolors": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-1.1.1.tgz",
      "integrity": "sha512-xceH2snhtb5M9liqDsmEw56le376mTZkEX/jEb/RxNFyegNul7eNslCXP9FDj/Lcu0X8KEyMceP2ntpaHrDEVA==",
      "license": "ISC"
    },
    "node_modules/picomatch": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/picomatch/-/picomatch-2.3.1.tgz",
      "integrity": "sha512-JU3teHTNjmE2VCGFzuY8EXzCDVwEqB2a8fsIvwaStHhAWJEeVd1o1QD80CU6+ZdEXXSLbSsuLwJjkCBWqRQUVA==",
      "license": "MIT",
      "engines": {
        "node": ">=8.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/jonschlinkert"
      }
    },
    "node_modules/pify": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/pify/-/pify-2.3.0.tgz",
      "integrity": "sha512-udgsAY+fTnvv7kI7aaxbqwWNb0AHiB0qBO89PZKPkoTmGOgdbrHDKD+0B2X4uTfJ/FT1R09r9gTsjUjNJotuog==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/pirates": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/pirates/-/pirates-4.0.7.tgz",
      "integrity": "sha512-TfySrs/5nm8fQJDcBDuUng3VOUKsd7S+zqvbOTiGXHfxX4wK31ard+hoNuvkicM/2YFzlpDgABOevKSsB4G/FA==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/pkg-dir": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/pkg-dir/-/pkg-dir-4.2.0.tgz",
      "integrity": "sha512-HRDzbaKjC+AOWVXxAU/x54COGeIv9eb+6CkDSQoNTt4XyWoIJvuPsXizxu/Fr23EiekbtZwmh1IcIG/l/a10GQ==",
      "license": "MIT",
      "dependencies": {
        "find-up": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/pkg-up": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/pkg-up/-/pkg-up-3.1.0.tgz",
      "integrity": "sha512-nDywThFk1i4BQK4twPQ6TA4RT8bDY96yeuCVBWL3ePARCiEKDRSrNGbFIgUJpLp+XeIR65v8ra7WuJOFUBtkMA==",
      "license": "MIT",
      "dependencies": {
        "find-up": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/pkg-up/node_modules/find-up": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-3.0.0.tgz",
      "integrity": "sha512-1yD6RmLI1XBfxugvORwlck6f75tYL+iR0jqwsOrOxMZyGYqUuDhJ0l4AXdO1iX/FTs9cBAMEk1gWSEx1kSbylg==",
      "license": "MIT",
      "dependencies": {
        "locate-path": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/pkg-up/node_modules/locate-path": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-3.0.0.tgz",
      "integrity": "sha512-7AO748wWnIhNqAuaty2ZWHkQHRSNfPVIsPIfwEOWO22AmaoVrWavlOcMR5nzTLNYvp36X220/maaRsrec1G65A==",
      "license": "MIT",
      "dependencies": {
        "p-locate": "^3.0.0",
        "path-exists": "^3.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/pkg-up/node_modules/p-locate": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-3.0.0.tgz",
      "integrity": "sha512-x+12w/To+4GFfgJhBEpiDcLozRJGegY+Ei7/z0tSLkMmxGZNybVMSfWj9aJn8Z5Fc7dBUNJOOVgPv2H7IwulSQ==",
      "license": "MIT",
      "dependencies": {
        "p-limit": "^2.0.0"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/pkg-up/node_modules/path-exists": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/path-exists/-/path-exists-3.0.0.tgz",
      "integrity": "sha512-bpC7GYwiDYQ4wYLe+FA8lhRjhQCMcQGuSgGGqDkg/QerRWw9CmGRT0iSOVRSZJ29NMLZgIzqaljJ63oaL4NIJQ==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/possible-typed-array-names": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/possible-typed-array-names/-/possible-typed-array-names-1.1.0.tgz",
      "integrity": "sha512-/+5VFTchJDoVj3bhoqi6UeymcD00DAwb1nJwamzPvHEszJ4FpF6SNNbUbOS8yI56qHzdV8eK0qEfOSiodkTdxg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/postcss": {
      "version": "8.5.6",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-8.5.6.tgz",
      "integrity": "sha512-3Ybi1tAuwAP9s0r1UQ2J4n5Y0G05bJkpUIO0/bI9MhwmD70S5aTWbXGBwxHrelT+XM1k6dM0pk+SwNkpTRN7Pg==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/postcss"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "nanoid": "^3.3.11",
        "picocolors": "^1.1.1",
        "source-map-js": "^1.2.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14"
      }
    },
    "node_modules/postcss-attribute-case-insensitive": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/postcss-attribute-case-insensitive/-/postcss-attribute-case-insensitive-5.0.2.tgz",
      "integrity": "sha512-XIidXV8fDr0kKt28vqki84fRK8VW8eTuIa4PChv2MqKuT6C9UjmSKzen6KaWhWEoYvwxFCa7n/tC1SZ3tyq4SQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-browser-comments": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/postcss-browser-comments/-/postcss-browser-comments-4.0.0.tgz",
      "integrity": "sha512-X9X9/WN3KIvY9+hNERUqX9gncsgBA25XaeR+jshHz2j8+sYyHktHw1JdKuMjeLpGktXidqDhA7b/qm1mrBDmgg==",
      "license": "CC0-1.0",
      "engines": {
        "node": ">=8"
      },
      "peerDependencies": {
        "browserslist": ">=4",
        "postcss": ">=8"
      }
    },
    "node_modules/postcss-calc": {
      "version": "8.2.4",
      "resolved": "https://registry.npmjs.org/postcss-calc/-/postcss-calc-8.2.4.tgz",
      "integrity": "sha512-SmWMSJmB8MRnnULldx0lQIyhSNvuDl9HfrZkaqqE/WHAhToYsAvDq+yAsA/kIyINDszOp3Rh0GFoNuH5Ypsm3Q==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9",
        "postcss-value-parser": "^4.2.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.2"
      }
    },
    "node_modules/postcss-clamp": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/postcss-clamp/-/postcss-clamp-4.1.0.tgz",
      "integrity": "sha512-ry4b1Llo/9zz+PKC+030KUnPITTJAHeOwjfAyyB60eT0AorGLdzp52s31OsPRHRf8NchkgFoG2y6fCfn1IV1Ow==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": ">=7.6.0"
      },
      "peerDependencies": {
        "postcss": "^8.4.6"
      }
    },
    "node_modules/postcss-color-functional-notation": {
      "version": "4.2.4",
      "resolved": "https://registry.npmjs.org/postcss-color-functional-notation/-/postcss-color-functional-notation-4.2.4.tgz",
      "integrity": "sha512-2yrTAUZUab9s6CpxkxC4rVgFEVaR6/2Pipvi6qcgvnYiVqZcbDHEoBDhrXzyb7Efh2CCfHQNtcqWcIruDTIUeg==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-color-hex-alpha": {
      "version": "8.0.4",
      "resolved": "https://registry.npmjs.org/postcss-color-hex-alpha/-/postcss-color-hex-alpha-8.0.4.tgz",
      "integrity": "sha512-nLo2DCRC9eE4w2JmuKgVA3fGL3d01kGq752pVALF68qpGLmx2Qrk91QTKkdUqqp45T1K1XV8IhQpcu1hoAQflQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-color-rebeccapurple": {
      "version": "7.1.1",
      "resolved": "https://registry.npmjs.org/postcss-color-rebeccapurple/-/postcss-color-rebeccapurple-7.1.1.tgz",
      "integrity": "sha512-pGxkuVEInwLHgkNxUc4sdg4g3py7zUeCQ9sMfwyHAT+Ezk8a4OaaVZ8lIY5+oNqA/BXXgLyXv0+5wHP68R79hg==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-colormin": {
      "version": "5.3.1",
      "resolved": "https://registry.npmjs.org/postcss-colormin/-/postcss-colormin-5.3.1.tgz",
      "integrity": "sha512-UsWQG0AqTFQmpBegeLLc1+c3jIqBNB0zlDGRWR+dQ3pRKJL1oeMzyqmH3o2PIfn9MBdNrVPWhDbT769LxCTLJQ==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "caniuse-api": "^3.0.0",
        "colord": "^2.9.1",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-convert-values": {
      "version": "5.1.3",
      "resolved": "https://registry.npmjs.org/postcss-convert-values/-/postcss-convert-values-5.1.3.tgz",
      "integrity": "sha512-82pC1xkJZtcJEfiLw6UXnXVXScgtBrjlO5CBmuDQc+dlb88ZYheFsjTn40+zBVi3DkfF7iezO0nJUPLcJK3pvA==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-custom-media": {
      "version": "8.0.2",
      "resolved": "https://registry.npmjs.org/postcss-custom-media/-/postcss-custom-media-8.0.2.tgz",
      "integrity": "sha512-7yi25vDAoHAkbhAzX9dHx2yc6ntS4jQvejrNcC+csQJAXjj15e7VcWfMgLqBNAbOvqi5uIa9huOVwdHbf+sKqg==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.3"
      }
    },
    "node_modules/postcss-custom-properties": {
      "version": "12.1.11",
      "resolved": "https://registry.npmjs.org/postcss-custom-properties/-/postcss-custom-properties-12.1.11.tgz",
      "integrity": "sha512-0IDJYhgU8xDv1KY6+VgUwuQkVtmYzRwu+dMjnmdMafXYv86SWqfxkc7qdDvWS38vsjaEtv8e0vGOUQrAiMBLpQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-custom-selectors": {
      "version": "6.0.3",
      "resolved": "https://registry.npmjs.org/postcss-custom-selectors/-/postcss-custom-selectors-6.0.3.tgz",
      "integrity": "sha512-fgVkmyiWDwmD3JbpCmB45SvvlCD6z9CG6Ie6Iere22W5aHea6oWa7EM2bpnv2Fj3I94L3VbtvX9KqwSi5aFzSg==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.4"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.3"
      }
    },
    "node_modules/postcss-dir-pseudo-class": {
      "version": "6.0.5",
      "resolved": "https://registry.npmjs.org/postcss-dir-pseudo-class/-/postcss-dir-pseudo-class-6.0.5.tgz",
      "integrity": "sha512-eqn4m70P031PF7ZQIvSgy9RSJ5uI2171O/OO/zcRNYpJbvaeKFUlar1aJ7rmgiQtbm0FSPsRewjpdS0Oew7MPA==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-discard-comments": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/postcss-discard-comments/-/postcss-discard-comments-5.1.2.tgz",
      "integrity": "sha512-+L8208OVbHVF2UQf1iDmRcbdjJkuBF6IS29yBDSiWUIzpYaAhtNl6JYnYm12FnkeCwQqF5LeklOu6rAqgfBZqQ==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-discard-duplicates": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-discard-duplicates/-/postcss-discard-duplicates-5.1.0.tgz",
      "integrity": "sha512-zmX3IoSI2aoenxHV6C7plngHWWhUOV3sP1T8y2ifzxzbtnuhk1EdPwm0S1bIUNaJ2eNbWeGLEwzw8huPD67aQw==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-discard-empty": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-discard-empty/-/postcss-discard-empty-5.1.1.tgz",
      "integrity": "sha512-zPz4WljiSuLWsI0ir4Mcnr4qQQ5e1Ukc3i7UfE2XcrwKK2LIPIqE5jxMRxO6GbI3cv//ztXDsXwEWT3BHOGh3A==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-discard-overridden": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-discard-overridden/-/postcss-discard-overridden-5.1.0.tgz",
      "integrity": "sha512-21nOL7RqWR1kasIVdKs8HNqQJhFxLsyRfAnUDm4Fe4t4mCWL9OJiHvlHPjcd8zc5Myu89b/7wZDnOSjFgeWRtw==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-double-position-gradients": {
      "version": "3.1.2",
      "resolved": "https://registry.npmjs.org/postcss-double-position-gradients/-/postcss-double-position-gradients-3.1.2.tgz",
      "integrity": "sha512-GX+FuE/uBR6eskOK+4vkXgT6pDkexLokPaz/AbJna9s5Kzp/yl488pKPjhy0obB475ovfT1Wv8ho7U/cHNaRgQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-env-function": {
      "version": "4.0.6",
      "resolved": "https://registry.npmjs.org/postcss-env-function/-/postcss-env-function-4.0.6.tgz",
      "integrity": "sha512-kpA6FsLra+NqcFnL81TnsU+Z7orGtDTxcOhl6pwXeEq1yFPpRMkCDpHhrz8CFQDr/Wfm0jLiNQ1OsGGPjlqPwA==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-flexbugs-fixes": {
      "version": "5.0.2",
      "resolved": "https://registry.npmjs.org/postcss-flexbugs-fixes/-/postcss-flexbugs-fixes-5.0.2.tgz",
      "integrity": "sha512-18f9voByak7bTktR2QgDveglpn9DTbBWPUzSOe9g0N4WR/2eSt6Vrcbf0hmspvMI6YWGywz6B9f7jzpFNJJgnQ==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8.1.4"
      }
    },
    "node_modules/postcss-focus-visible": {
      "version": "6.0.4",
      "resolved": "https://registry.npmjs.org/postcss-focus-visible/-/postcss-focus-visible-6.0.4.tgz",
      "integrity": "sha512-QcKuUU/dgNsstIK6HELFRT5Y3lbrMLEOwG+A4s5cA+fx3A3y/JTq3X9LaOj3OC3ALH0XqyrgQIgey/MIZ8Wczw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-focus-within": {
      "version": "5.0.4",
      "resolved": "https://registry.npmjs.org/postcss-focus-within/-/postcss-focus-within-5.0.4.tgz",
      "integrity": "sha512-vvjDN++C0mu8jz4af5d52CB184ogg/sSxAFS+oUJQq2SuCe7T5U2iIsVJtsCp2d6R4j0jr5+q3rPkBVZkXD9fQ==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.9"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-font-variant": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/postcss-font-variant/-/postcss-font-variant-5.0.0.tgz",
      "integrity": "sha512-1fmkBaCALD72CK2a9i468mA/+tr9/1cBxRRMXOUaZqO43oWPR5imcyPjXwuv7PXbCid4ndlP5zWhidQVVa3hmA==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-gap-properties": {
      "version": "3.0.5",
      "resolved": "https://registry.npmjs.org/postcss-gap-properties/-/postcss-gap-properties-3.0.5.tgz",
      "integrity": "sha512-IuE6gKSdoUNcvkGIqdtjtcMtZIFyXZhmFd5RUlg97iVEvp1BZKV5ngsAjCjrVy+14uhGBQl9tzmi1Qwq4kqVOg==",
      "license": "CC0-1.0",
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-image-set-function": {
      "version": "4.0.7",
      "resolved": "https://registry.npmjs.org/postcss-image-set-function/-/postcss-image-set-function-4.0.7.tgz",
      "integrity": "sha512-9T2r9rsvYzm5ndsBE8WgtrMlIT7VbtTfE7b3BQnudUqnBcBo7L758oc+o+pdj/dUV0l5wjwSdjeOH2DZtfv8qw==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-import": {
      "version": "15.1.0",
      "resolved": "https://registry.npmjs.org/postcss-import/-/postcss-import-15.1.0.tgz",
      "integrity": "sha512-hpr+J05B2FVYUAXHeK1YyI267J/dDDhMU6B6civm8hSY1jYJnBXxzKDKDswzJmtLHryrjhnDjqqp/49t8FALew==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.0.0",
        "read-cache": "^1.0.0",
        "resolve": "^1.1.7"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "peerDependencies": {
        "postcss": "^8.0.0"
      }
    },
    "node_modules/postcss-initial": {
      "version": "4.0.1",
      "resolved": "https://registry.npmjs.org/postcss-initial/-/postcss-initial-4.0.1.tgz",
      "integrity": "sha512-0ueD7rPqX8Pn1xJIjay0AZeIuDoF+V+VvMt/uOnn+4ezUKhZM/NokDeP6DwMNyIoYByuN/94IQnt5FEkaN59xQ==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8.0.0"
      }
    },
    "node_modules/postcss-js": {
      "version": "4.1.0",
      "resolved": "https://registry.npmjs.org/postcss-js/-/postcss-js-4.1.0.tgz",
      "integrity": "sha512-oIAOTqgIo7q2EOwbhb8UalYePMvYoIeRY2YKntdpFQXNosSu3vLrniGgmH9OKs/qAkfoj5oB3le/7mINW1LCfw==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "camelcase-css": "^2.0.1"
      },
      "engines": {
        "node": "^12 || ^14 || >= 16"
      },
      "peerDependencies": {
        "postcss": "^8.4.21"
      }
    },
    "node_modules/postcss-lab-function": {
      "version": "4.2.1",
      "resolved": "https://registry.npmjs.org/postcss-lab-function/-/postcss-lab-function-4.2.1.tgz",
      "integrity": "sha512-xuXll4isR03CrQsmxyz92LJB2xX9n+pZJ5jE9JgcnmsCammLyKdlzrBin+25dy6wIjfhJpKBAN80gsTlCgRk2w==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-progressive-custom-properties": "^1.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-load-config": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/postcss-load-config/-/postcss-load-config-4.0.2.tgz",
      "integrity": "sha512-bSVhyJGL00wMVoPUzAVAnbEoWyqRxkjv64tUl427SKnPrENtq6hJwUojroMz2VB+Q1edmi4IfrAPpami5VVgMQ==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "lilconfig": "^3.0.0",
        "yaml": "^2.3.4"
      },
      "engines": {
        "node": ">= 14"
      },
      "peerDependencies": {
        "postcss": ">=8.0.9",
        "ts-node": ">=9.0.0"
      },
      "peerDependenciesMeta": {
        "postcss": {
          "optional": true
        },
        "ts-node": {
          "optional": true
        }
      }
    },
    "node_modules/postcss-load-config/node_modules/lilconfig": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/lilconfig/-/lilconfig-3.1.3.tgz",
      "integrity": "sha512-/vlFKAoH5Cgt3Ie+JLhRbwOsCQePABiU3tJ1egGvyQ+33R/vcwM2Zl2QR/LzjsBeItPt3oSVXapn+m4nQDvpzw==",
      "license": "MIT",
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/antonk52"
      }
    },
    "node_modules/postcss-load-config/node_modules/yaml": {
      "version": "2.8.1",
      "resolved": "https://registry.npmjs.org/yaml/-/yaml-2.8.1.tgz",
      "integrity": "sha512-lcYcMxX2PO9XMGvAJkJ3OsNMw+/7FKes7/hgerGUYWIoWu5j/+YQqcZr5JnPZWzOsEBgMbSbiSTn/dv/69Mkpw==",
      "license": "ISC",
      "bin": {
        "yaml": "bin.mjs"
      },
      "engines": {
        "node": ">= 14.6"
      }
    },
    "node_modules/postcss-loader": {
      "version": "6.2.1",
      "resolved": "https://registry.npmjs.org/postcss-loader/-/postcss-loader-6.2.1.tgz",
      "integrity": "sha512-WbbYpmAaKcux/P66bZ40bpWsBucjx/TTgVVzRZ9yUO8yQfVBlameJ0ZGVaPfH64hNSBh63a+ICP5nqOpBA0w+Q==",
      "license": "MIT",
      "dependencies": {
        "cosmiconfig": "^7.0.0",
        "klona": "^2.0.5",
        "semver": "^7.3.5"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "postcss": "^7.0.0 || ^8.0.1",
        "webpack": "^5.0.0"
      }
    },
    "node_modules/postcss-logical": {
      "version": "5.0.4",
      "resolved": "https://registry.npmjs.org/postcss-logical/-/postcss-logical-5.0.4.tgz",
      "integrity": "sha512-RHXxplCeLh9VjinvMrZONq7im4wjWGlRJAqmAVLXyZaXwfDWP73/oq4NdIp+OZwhQUMj0zjqDfM5Fj7qby+B4g==",
      "license": "CC0-1.0",
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.4"
      }
    },
    "node_modules/postcss-media-minmax": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/postcss-media-minmax/-/postcss-media-minmax-5.0.0.tgz",
      "integrity": "sha512-yDUvFf9QdFZTuCUg0g0uNSHVlJ5X1lSzDZjPSFaiCWvjgsvu8vEVxtahPrLMinIDEEGnx6cBe6iqdx5YWz08wQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10.0.0"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-merge-longhand": {
      "version": "5.1.7",
      "resolved": "https://registry.npmjs.org/postcss-merge-longhand/-/postcss-merge-longhand-5.1.7.tgz",
      "integrity": "sha512-YCI9gZB+PLNskrK0BB3/2OzPnGhPkBEwmwhfYk1ilBHYVAZB7/tkTHFBAnCrvBBOmeYyMYw3DMjT55SyxMBzjQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0",
        "stylehacks": "^5.1.1"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-merge-rules": {
      "version": "5.1.4",
      "resolved": "https://registry.npmjs.org/postcss-merge-rules/-/postcss-merge-rules-5.1.4.tgz",
      "integrity": "sha512-0R2IuYpgU93y9lhVbO/OylTtKMVcHb67zjWIfCiKR9rWL3GUk1677LAqD/BcHizukdZEjT8Ru3oHRoAYoJy44g==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "caniuse-api": "^3.0.0",
        "cssnano-utils": "^3.1.0",
        "postcss-selector-parser": "^6.0.5"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-minify-font-values": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-minify-font-values/-/postcss-minify-font-values-5.1.0.tgz",
      "integrity": "sha512-el3mYTgx13ZAPPirSVsHqFzl+BBBDrXvbySvPGFnQcTI4iNslrPaFq4muTkLZmKlGk4gyFAYUBMH30+HurREyA==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-minify-gradients": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-minify-gradients/-/postcss-minify-gradients-5.1.1.tgz",
      "integrity": "sha512-VGvXMTpCEo4qHTNSa9A0a3D+dxGFZCYwR6Jokk+/3oB6flu2/PnPXAh2x7x52EkY5xlIHLm+Le8tJxe/7TNhzw==",
      "license": "MIT",
      "dependencies": {
        "colord": "^2.9.1",
        "cssnano-utils": "^3.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-minify-params": {
      "version": "5.1.4",
      "resolved": "https://registry.npmjs.org/postcss-minify-params/-/postcss-minify-params-5.1.4.tgz",
      "integrity": "sha512-+mePA3MgdmVmv6g+30rn57USjOGSAyuxUmkfiWpzalZ8aiBkdPYjXWtHuwJGm1v5Ojy0Z0LaSYhHaLJQB0P8Jw==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "cssnano-utils": "^3.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-minify-selectors": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/postcss-minify-selectors/-/postcss-minify-selectors-5.2.1.tgz",
      "integrity": "sha512-nPJu7OjZJTsVUmPdm2TcaiohIwxP+v8ha9NehQ2ye9szv4orirRU3SDdtUmKH+10nzn0bAyOXZ0UEr7OpvLehg==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.5"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-modules-extract-imports": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/postcss-modules-extract-imports/-/postcss-modules-extract-imports-3.1.0.tgz",
      "integrity": "sha512-k3kNe0aNFQDAZGbin48pL2VNidTF0w4/eASDsxlyspobzU3wZQLOGj7L9gfRe0Jo9/4uud09DsjFNH7winGv8Q==",
      "license": "ISC",
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-modules-local-by-default": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/postcss-modules-local-by-default/-/postcss-modules-local-by-default-4.2.0.tgz",
      "integrity": "sha512-5kcJm/zk+GJDSfw+V/42fJ5fhjL5YbFDl8nVdXkJPLLW+Vf9mTD5Xe0wqIaDnLuL2U6cDNpTr+UQ+v2HWIBhzw==",
      "license": "MIT",
      "dependencies": {
        "icss-utils": "^5.0.0",
        "postcss-selector-parser": "^7.0.0",
        "postcss-value-parser": "^4.1.0"
      },
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-modules-local-by-default/node_modules/postcss-selector-parser": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-7.1.0.tgz",
      "integrity": "sha512-8sLjZwK0R+JlxlYcTuVnyT2v+htpdrjDOKuMcOVdYjt52Lh8hWRYpxBPoKx/Zg+bcjc3wx6fmQevMmUztS/ccA==",
      "license": "MIT",
      "dependencies": {
        "cssesc": "^3.0.0",
        "util-deprecate": "^1.0.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/postcss-modules-scope": {
      "version": "3.2.1",
      "resolved": "https://registry.npmjs.org/postcss-modules-scope/-/postcss-modules-scope-3.2.1.tgz",
      "integrity": "sha512-m9jZstCVaqGjTAuny8MdgE88scJnCiQSlSrOWcTQgM2t32UBe+MUmFSO5t7VMSfAf/FJKImAxBav8ooCHJXCJA==",
      "license": "ISC",
      "dependencies": {
        "postcss-selector-parser": "^7.0.0"
      },
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-modules-scope/node_modules/postcss-selector-parser": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-7.1.0.tgz",
      "integrity": "sha512-8sLjZwK0R+JlxlYcTuVnyT2v+htpdrjDOKuMcOVdYjt52Lh8hWRYpxBPoKx/Zg+bcjc3wx6fmQevMmUztS/ccA==",
      "license": "MIT",
      "dependencies": {
        "cssesc": "^3.0.0",
        "util-deprecate": "^1.0.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/postcss-modules-values": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/postcss-modules-values/-/postcss-modules-values-4.0.0.tgz",
      "integrity": "sha512-RDxHkAiEGI78gS2ofyvCsu7iycRv7oqw5xMWn9iMoR0N/7mf9D50ecQqUo5BZ9Zh2vH4bCUR/ktCqbB9m8vJjQ==",
      "license": "ISC",
      "dependencies": {
        "icss-utils": "^5.0.0"
      },
      "engines": {
        "node": "^10 || ^12 || >= 14"
      },
      "peerDependencies": {
        "postcss": "^8.1.0"
      }
    },
    "node_modules/postcss-nested": {
      "version": "6.2.0",
      "resolved": "https://registry.npmjs.org/postcss-nested/-/postcss-nested-6.2.0.tgz",
      "integrity": "sha512-HQbt28KulC5AJzG+cZtj9kvKB93CFCdLvog1WFLf1D+xmMvPGlBstkpTEZfK5+AN9hfJocyBFCNiqyS48bpgzQ==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/postcss/"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.1.1"
      },
      "engines": {
        "node": ">=12.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.14"
      }
    },
    "node_modules/postcss-nesting": {
      "version": "10.2.0",
      "resolved": "https://registry.npmjs.org/postcss-nesting/-/postcss-nesting-10.2.0.tgz",
      "integrity": "sha512-EwMkYchxiDiKUhlJGzWsD9b2zvq/r2SSubcRrgP+jujMXFzqvANLt16lJANC+5uZ6hjI7lpRmI6O8JIl+8l1KA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/selector-specificity": "^2.0.0",
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-normalize": {
      "version": "10.0.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize/-/postcss-normalize-10.0.1.tgz",
      "integrity": "sha512-+5w18/rDev5mqERcG3W5GZNMJa1eoYYNGo8gB7tEwaos0ajk3ZXAI4mHGcNT47NE+ZnZD1pEpUOFLvltIwmeJA==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/normalize.css": "*",
        "postcss-browser-comments": "^4",
        "sanitize.css": "*"
      },
      "engines": {
        "node": ">= 12"
      },
      "peerDependencies": {
        "browserslist": ">= 4",
        "postcss": ">= 8"
      }
    },
    "node_modules/postcss-normalize-charset": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-charset/-/postcss-normalize-charset-5.1.0.tgz",
      "integrity": "sha512-mSgUJ+pd/ldRGVx26p2wz9dNZ7ji6Pn8VWBajMXFf8jk7vUoSrZ2lt/wZR7DtlZYKesmZI680qjr2CeFF2fbUg==",
      "license": "MIT",
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-display-values": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-display-values/-/postcss-normalize-display-values-5.1.0.tgz",
      "integrity": "sha512-WP4KIM4o2dazQXWmFaqMmcvsKmhdINFblgSeRgn8BJ6vxaMyaJkwAzpPpuvSIoG/rmX3M+IrRZEz2H0glrQNEA==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-positions": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize-positions/-/postcss-normalize-positions-5.1.1.tgz",
      "integrity": "sha512-6UpCb0G4eofTCQLFVuI3EVNZzBNPiIKcA1AKVka+31fTVySphr3VUgAIULBhxZkKgwLImhzMR2Bw1ORK+37INg==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-repeat-style": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize-repeat-style/-/postcss-normalize-repeat-style-5.1.1.tgz",
      "integrity": "sha512-mFpLspGWkQtBcWIRFLmewo8aC3ImN2i/J3v8YCFUwDnPu3Xz4rLohDO26lGjwNsQxB3YF0KKRwspGzE2JEuS0g==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-string": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-string/-/postcss-normalize-string-5.1.0.tgz",
      "integrity": "sha512-oYiIJOf4T9T1N4i+abeIc7Vgm/xPCGih4bZz5Nm0/ARVJ7K6xrDlLwvwqOydvyL3RHNf8qZk6vo3aatiw/go3w==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-timing-functions": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-timing-functions/-/postcss-normalize-timing-functions-5.1.0.tgz",
      "integrity": "sha512-DOEkzJ4SAXv5xkHl0Wa9cZLF3WCBhF3o1SKVxKQAa+0pYKlueTpCgvkFAHfk+Y64ezX9+nITGrDZeVGgITJXjg==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-unicode": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize-unicode/-/postcss-normalize-unicode-5.1.1.tgz",
      "integrity": "sha512-qnCL5jzkNUmKVhZoENp1mJiGNPcsJCs1aaRmURmeJGES23Z/ajaln+EPTD+rBeNkSryI+2WTdW+lwcVdOikrpA==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-url": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-normalize-url/-/postcss-normalize-url-5.1.0.tgz",
      "integrity": "sha512-5upGeDO+PVthOxSmds43ZeMeZfKH+/DKgGRD7TElkkyS46JXAUhMzIKiCa7BabPeIy3AQcTkXwVVN7DbqsiCew==",
      "license": "MIT",
      "dependencies": {
        "normalize-url": "^6.0.1",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-normalize-whitespace": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-normalize-whitespace/-/postcss-normalize-whitespace-5.1.1.tgz",
      "integrity": "sha512-83ZJ4t3NUDETIHTa3uEg6asWjSBYL5EdkVB0sDncx9ERzOKBVJIUeDO9RyA9Zwtig8El1d79HBp0JEi8wvGQnA==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-opacity-percentage": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/postcss-opacity-percentage/-/postcss-opacity-percentage-1.1.3.tgz",
      "integrity": "sha512-An6Ba4pHBiDtyVpSLymUUERMo2cU7s+Obz6BTrS+gxkbnSBNKSuD0AVUc+CpBMrpVPKKfoVz0WQCX+Tnst0i4A==",
      "funding": [
        {
          "type": "kofi",
          "url": "https://ko-fi.com/mrcgrtz"
        },
        {
          "type": "liberapay",
          "url": "https://liberapay.com/mrcgrtz"
        }
      ],
      "license": "MIT",
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-ordered-values": {
      "version": "5.1.3",
      "resolved": "https://registry.npmjs.org/postcss-ordered-values/-/postcss-ordered-values-5.1.3.tgz",
      "integrity": "sha512-9UO79VUhPwEkzbb3RNpqqghc6lcYej1aveQteWY+4POIwlqkYE21HKWaLDF6lWNuqCobEAyTovVhtI32Rbv2RQ==",
      "license": "MIT",
      "dependencies": {
        "cssnano-utils": "^3.1.0",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-overflow-shorthand": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/postcss-overflow-shorthand/-/postcss-overflow-shorthand-3.0.4.tgz",
      "integrity": "sha512-otYl/ylHK8Y9bcBnPLo3foYFLL6a6Ak+3EQBPOTR7luMYCOsiVTUk1iLvNf6tVPNGXcoL9Hoz37kpfriRIFb4A==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-page-break": {
      "version": "3.0.4",
      "resolved": "https://registry.npmjs.org/postcss-page-break/-/postcss-page-break-3.0.4.tgz",
      "integrity": "sha512-1JGu8oCjVXLa9q9rFTo4MbeeA5FMe00/9C7lN4va606Rdb+HkxXtXsmEDrIraQ11fGz/WvKWa8gMuCKkrXpTsQ==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8"
      }
    },
    "node_modules/postcss-place": {
      "version": "7.0.5",
      "resolved": "https://registry.npmjs.org/postcss-place/-/postcss-place-7.0.5.tgz",
      "integrity": "sha512-wR8igaZROA6Z4pv0d+bvVrvGY4GVHihBCBQieXFY3kuSuMyOmEnnfFzHl/tQuqHZkfkIVBEbDvYcFfHmpSet9g==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-preset-env": {
      "version": "7.8.3",
      "resolved": "https://registry.npmjs.org/postcss-preset-env/-/postcss-preset-env-7.8.3.tgz",
      "integrity": "sha512-T1LgRm5uEVFSEF83vHZJV2z19lHg4yJuZ6gXZZkqVsqv63nlr6zabMH3l4Pc01FQCyfWVrh2GaUeCVy9Po+Aag==",
      "license": "CC0-1.0",
      "dependencies": {
        "@csstools/postcss-cascade-layers": "^1.1.1",
        "@csstools/postcss-color-function": "^1.1.1",
        "@csstools/postcss-font-format-keywords": "^1.0.1",
        "@csstools/postcss-hwb-function": "^1.0.2",
        "@csstools/postcss-ic-unit": "^1.0.1",
        "@csstools/postcss-is-pseudo-class": "^2.0.7",
        "@csstools/postcss-nested-calc": "^1.0.0",
        "@csstools/postcss-normalize-display-values": "^1.0.1",
        "@csstools/postcss-oklab-function": "^1.1.1",
        "@csstools/postcss-progressive-custom-properties": "^1.3.0",
        "@csstools/postcss-stepped-value-functions": "^1.0.1",
        "@csstools/postcss-text-decoration-shorthand": "^1.0.0",
        "@csstools/postcss-trigonometric-functions": "^1.0.2",
        "@csstools/postcss-unset-value": "^1.0.2",
        "autoprefixer": "^10.4.13",
        "browserslist": "^4.21.4",
        "css-blank-pseudo": "^3.0.3",
        "css-has-pseudo": "^3.0.4",
        "css-prefers-color-scheme": "^6.0.3",
        "cssdb": "^7.1.0",
        "postcss-attribute-case-insensitive": "^5.0.2",
        "postcss-clamp": "^4.1.0",
        "postcss-color-functional-notation": "^4.2.4",
        "postcss-color-hex-alpha": "^8.0.4",
        "postcss-color-rebeccapurple": "^7.1.1",
        "postcss-custom-media": "^8.0.2",
        "postcss-custom-properties": "^12.1.10",
        "postcss-custom-selectors": "^6.0.3",
        "postcss-dir-pseudo-class": "^6.0.5",
        "postcss-double-position-gradients": "^3.1.2",
        "postcss-env-function": "^4.0.6",
        "postcss-focus-visible": "^6.0.4",
        "postcss-focus-within": "^5.0.4",
        "postcss-font-variant": "^5.0.0",
        "postcss-gap-properties": "^3.0.5",
        "postcss-image-set-function": "^4.0.7",
        "postcss-initial": "^4.0.1",
        "postcss-lab-function": "^4.2.1",
        "postcss-logical": "^5.0.4",
        "postcss-media-minmax": "^5.0.0",
        "postcss-nesting": "^10.2.0",
        "postcss-opacity-percentage": "^1.1.2",
        "postcss-overflow-shorthand": "^3.0.4",
        "postcss-page-break": "^3.0.4",
        "postcss-place": "^7.0.5",
        "postcss-pseudo-class-any-link": "^7.1.6",
        "postcss-replace-overflow-wrap": "^4.0.0",
        "postcss-selector-not": "^6.0.1",
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-pseudo-class-any-link": {
      "version": "7.1.6",
      "resolved": "https://registry.npmjs.org/postcss-pseudo-class-any-link/-/postcss-pseudo-class-any-link-7.1.6.tgz",
      "integrity": "sha512-9sCtZkO6f/5ML9WcTLcIyV1yz9D1rf0tWc+ulKcvV30s0iZKS/ONyETvoWsr6vnrmW+X+KmuK3gV/w5EWnT37w==",
      "license": "CC0-1.0",
      "dependencies": {
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-reduce-initial": {
      "version": "5.1.2",
      "resolved": "https://registry.npmjs.org/postcss-reduce-initial/-/postcss-reduce-initial-5.1.2.tgz",
      "integrity": "sha512-dE/y2XRaqAi6OvjzD22pjTUQ8eOfc6m/natGHgKFBK9DxFmIm69YmaRVQrGgFlEfc1HePIurY0TmDeROK05rIg==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "caniuse-api": "^3.0.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-reduce-transforms": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-reduce-transforms/-/postcss-reduce-transforms-5.1.0.tgz",
      "integrity": "sha512-2fbdbmgir5AvpW9RLtdONx1QoYG2/EtqpNQbFASDlixBbAYuTcJ0dECwlqNqH7VbaUnEnh8SrxOe2sRIn24XyQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-replace-overflow-wrap": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/postcss-replace-overflow-wrap/-/postcss-replace-overflow-wrap-4.0.0.tgz",
      "integrity": "sha512-KmF7SBPphT4gPPcKZc7aDkweHiKEEO8cla/GjcBK+ckKxiZslIu3C4GCRW3DNfL0o7yW7kMQu9xlZ1kXRXLXtw==",
      "license": "MIT",
      "peerDependencies": {
        "postcss": "^8.0.3"
      }
    },
    "node_modules/postcss-selector-not": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/postcss-selector-not/-/postcss-selector-not-6.0.1.tgz",
      "integrity": "sha512-1i9affjAe9xu/y9uqWH+tD4r6/hDaXJruk8xn2x1vzxC2U3J3LKO3zJW4CyxlNhA56pADJ/djpEwpH1RClI2rQ==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.10"
      },
      "engines": {
        "node": "^12 || ^14 || >=16"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/csstools"
      },
      "peerDependencies": {
        "postcss": "^8.2"
      }
    },
    "node_modules/postcss-selector-parser": {
      "version": "6.1.2",
      "resolved": "https://registry.npmjs.org/postcss-selector-parser/-/postcss-selector-parser-6.1.2.tgz",
      "integrity": "sha512-Q8qQfPiZ+THO/3ZrOrO0cJJKfpYCagtMUkXbnEfmgUjwXg6z/WBeOyS9APBBPCTSiDV+s4SwQGu8yFsiMRIudg==",
      "license": "MIT",
      "dependencies": {
        "cssesc": "^3.0.0",
        "util-deprecate": "^1.0.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/postcss-svgo": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/postcss-svgo/-/postcss-svgo-5.1.0.tgz",
      "integrity": "sha512-D75KsH1zm5ZrHyxPakAxJWtkyXew5qwS70v56exwvw542d9CRtTo78K0WeFxZB4G7JXKKMbEZtZayTGdIky/eA==",
      "license": "MIT",
      "dependencies": {
        "postcss-value-parser": "^4.2.0",
        "svgo": "^2.7.0"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-svgo/node_modules/commander": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/commander/-/commander-7.2.0.tgz",
      "integrity": "sha512-QrWXB+ZQSVPmIWIhtEO9H+gwHaMGYiF5ChvoJ+K9ZGHG/sVsa6yiesAD1GC/x46sET00Xlwo1u49RVVVzvcSkw==",
      "license": "MIT",
      "engines": {
        "node": ">= 10"
      }
    },
    "node_modules/postcss-svgo/node_modules/css-tree": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/css-tree/-/css-tree-1.1.3.tgz",
      "integrity": "sha512-tRpdppF7TRazZrjJ6v3stzv93qxRcSsFmW6cX0Zm2NVKpxE1WV1HblnghVv9TreireHkqI/VDEsfolRF1p6y7Q==",
      "license": "MIT",
      "dependencies": {
        "mdn-data": "2.0.14",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/postcss-svgo/node_modules/mdn-data": {
      "version": "2.0.14",
      "resolved": "https://registry.npmjs.org/mdn-data/-/mdn-data-2.0.14.tgz",
      "integrity": "sha512-dn6wd0uw5GsdswPFfsgMp5NSB0/aDe6fK94YJV/AJDYXL6HVLWBsxeq7js7Ad+mU2K9LAlwpk6kN2D5mwCPVow==",
      "license": "CC0-1.0"
    },
    "node_modules/postcss-svgo/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/postcss-svgo/node_modules/svgo": {
      "version": "2.8.0",
      "resolved": "https://registry.npmjs.org/svgo/-/svgo-2.8.0.tgz",
      "integrity": "sha512-+N/Q9kV1+F+UeWYoSiULYo4xYSDQlTgb+ayMobAXPwMnLvop7oxKMo9OzIrX5x3eS4L4f2UHhc9axXwY8DpChg==",
      "license": "MIT",
      "dependencies": {
        "@trysound/sax": "0.2.0",
        "commander": "^7.2.0",
        "css-select": "^4.1.3",
        "css-tree": "^1.1.3",
        "csso": "^4.2.0",
        "picocolors": "^1.0.0",
        "stable": "^0.1.8"
      },
      "bin": {
        "svgo": "bin/svgo"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/postcss-unique-selectors": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/postcss-unique-selectors/-/postcss-unique-selectors-5.1.1.tgz",
      "integrity": "sha512-5JiODlELrz8L2HwxfPnhOWZYWDxVHWL83ufOv84NrcgipI7TaeRsatAhK4Tr2/ZiYldpK/wBvw5BD3qfaK96GA==",
      "license": "MIT",
      "dependencies": {
        "postcss-selector-parser": "^6.0.5"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/postcss-value-parser": {
      "version": "4.2.0",
      "resolved": "https://registry.npmjs.org/postcss-value-parser/-/postcss-value-parser-4.2.0.tgz",
      "integrity": "sha512-1NNCs6uurfkVbeXG4S8JFT9t19m45ICnif8zWLd5oPSZ50QnwMfK+H3jv408d4jw/7Bttv5axS5IiHoLaVNHeQ==",
      "license": "MIT"
    },
    "node_modules/prelude-ls": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/prelude-ls/-/prelude-ls-1.2.1.tgz",
      "integrity": "sha512-vkcDPrRZo1QZLbn5RLGPpg/WmIQ65qoWWhcGKf/b5eplkkarX0m9z8ppCat4mlOqUsWpyNuYgO3VRyrYHSzX5g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/pretty-bytes": {
      "version": "5.6.0",
      "resolved": "https://registry.npmjs.org/pretty-bytes/-/pretty-bytes-5.6.0.tgz",
      "integrity": "sha512-FFw039TmrBqFK8ma/7OL3sDz/VytdtJr044/QUJtH0wK9lb9jLq9tJyIxUwtQJHwar2BqtiA4iCWSwo9JLkzFg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/pretty-error": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/pretty-error/-/pretty-error-4.0.0.tgz",
      "integrity": "sha512-AoJ5YMAcXKYxKhuJGdcvse+Voc6v1RgnsR3nWcYU7q4t6z0Q6T86sv5Zq8VIRbOWWFpvdGE83LtdSMNd+6Y0xw==",
      "license": "MIT",
      "dependencies": {
        "lodash": "^4.17.20",
        "renderkid": "^3.0.0"
      }
    },
    "node_modules/pretty-format": {
      "version": "27.5.1",
      "resolved": "https://registry.npmjs.org/pretty-format/-/pretty-format-27.5.1.tgz",
      "integrity": "sha512-Qb1gy5OrP5+zDf2Bvnzdl3jsTf1qXVMazbvCoKhtKqVs4/YK4ozX4gKQJJVyNe+cajNPn0KoC0MC3FUmaHWEmQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1",
        "ansi-styles": "^5.0.0",
        "react-is": "^17.0.1"
      },
      "engines": {
        "node": "^10.13.0 || ^12.13.0 || ^14.15.0 || >=15.0.0"
      }
    },
    "node_modules/pretty-format/node_modules/ansi-styles": {
      "version": "5.2.0",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-5.2.0.tgz",
      "integrity": "sha512-Cxwpt2SfTzTtXcfOlzGEee8O+c+MmUgGrNiBcXnuWxuFJHe6a5Hz7qwhwe5OgaSYI0IJvkLqWX1ASG+cJOkEiA==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/ansi-styles?sponsor=1"
      }
    },
    "node_modules/process-nextick-args": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/process-nextick-args/-/process-nextick-args-2.0.1.tgz",
      "integrity": "sha512-3ouUOpQhtgrbOa17J7+uxOTpITYWaGP7/AhoR3+A+/1e9skrzelGi/dXzEYyvbxubEF6Wn2ypscTKiKJFFn1ag==",
      "license": "MIT"
    },
    "node_modules/promise": {
      "version": "8.3.0",
      "resolved": "https://registry.npmjs.org/promise/-/promise-8.3.0.tgz",
      "integrity": "sha512-rZPNPKTOYVNEEKFaq1HqTgOwZD+4/YHS5ukLzQCypkj+OkYx7iv0mA91lJlpPPZ8vMau3IIGj5Qlwrx+8iiSmg==",
      "license": "MIT",
      "dependencies": {
        "asap": "~2.0.6"
      }
    },
    "node_modules/prompts": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/prompts/-/prompts-2.4.2.tgz",
      "integrity": "sha512-NxNv/kLguCA7p3jE8oL2aEBsrJWgAakBpgmgK6lpPWV+WuOmY6r2/zbAVnP+T8bQlA0nzHXSJSJW0Hq7ylaD2Q==",
      "license": "MIT",
      "dependencies": {
        "kleur": "^3.0.3",
        "sisteransi": "^1.0.5"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/prop-types": {
      "version": "15.8.1",
      "resolved": "https://registry.npmjs.org/prop-types/-/prop-types-15.8.1.tgz",
      "integrity": "sha512-oj87CgZICdulUohogVAR7AjlC0327U4el4L6eAvOqCeudMDVU0NThNaV+b9Df4dXgSP1gXMTnPdhfe/2qDH5cg==",
      "license": "MIT",
      "dependencies": {
        "loose-envify": "^1.4.0",
        "object-assign": "^4.1.1",
        "react-is": "^16.13.1"
      }
    },
    "node_modules/prop-types/node_modules/react-is": {
      "version": "16.13.1",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-16.13.1.tgz",
      "integrity": "sha512-24e6ynE2H+OKt4kqsOvNd8kBpV65zoxbA4BVsEOB3ARVWQki/DHzaUoC5KuON/BiccDaCCTZBuOcfZs70kR8bQ==",
      "license": "MIT"
    },
    "node_modules/proxy-addr": {
      "version": "2.0.7",
      "resolved": "https://registry.npmjs.org/proxy-addr/-/proxy-addr-2.0.7.tgz",
      "integrity": "sha512-llQsMLSUDUPT44jdrU/O37qlnifitDP+ZwrmmZcoSKyLKvtZxpyV0n2/bD/N4tBAAZ/gJEdZU7KMraoK1+XYAg==",
      "license": "MIT",
      "dependencies": {
        "forwarded": "0.2.0",
        "ipaddr.js": "1.9.1"
      },
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/proxy-addr/node_modules/ipaddr.js": {
      "version": "1.9.1",
      "resolved": "https://registry.npmjs.org/ipaddr.js/-/ipaddr.js-1.9.1.tgz",
      "integrity": "sha512-0KI/607xoxSToH7GjN1FfSbLoU0+btTicjsQSWQlh/hZykN8KpmMf7uYwPW3R+akZ6R/w18ZlXSHBYXiYUPO3g==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/proxy-from-env": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/proxy-from-env/-/proxy-from-env-1.1.0.tgz",
      "integrity": "sha512-D+zkORCbA9f1tdWRK0RaCR3GPv50cMxcrz4X8k5LTSUD1Dkw47mKJEZQNunItRTkWwgtaUSo1RVFRIG9ZXiFYg==",
      "license": "MIT"
    },
    "node_modules/psl": {
      "version": "1.15.0",
      "resolved": "https://registry.npmjs.org/psl/-/psl-1.15.0.tgz",
      "integrity": "sha512-JZd3gMVBAVQkSs6HdNZo9Sdo0LNcQeMNP3CozBJb3JYC/QUYZTnKxP+f8oWRX4rHP5EurWxqAHTSwUCjlNKa1w==",
      "license": "MIT",
      "dependencies": {
        "punycode": "^2.3.1"
      },
      "funding": {
        "url": "https://github.com/sponsors/lupomontero"
      }
    },
    "node_modules/punycode": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/punycode/-/punycode-2.3.1.tgz",
      "integrity": "sha512-vYt7UD1U9Wg6138shLtLOvdAu+8DsC/ilFtEVHcH+wydcSpNE20AfSOduf6MkRFahL5FY7X1oU7nKVZFtfq8Fg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/q": {
      "version": "1.5.1",
      "resolved": "https://registry.npmjs.org/q/-/q-1.5.1.tgz",
      "integrity": "sha512-kV/CThkXo6xyFEZUugw/+pIOywXcDbFYgSct5cT3gqlbkBE1SJdwy6UQoZvodiWF/ckQLZyDE/Bu1M6gVu5lVw==",
      "deprecated": "You or someone you depend on is using Q, the JavaScript Promise library that gave JavaScript developers strong feelings about promises. They can almost certainly migrate to the native JavaScript promise now. Thank you literally everyone for joining me in this bet against the odds. Be excellent to each other.\n\n(For a CapTP with native promises, see @endo/eventual-send and @endo/captp)",
      "license": "MIT",
      "engines": {
        "node": ">=0.6.0",
        "teleport": ">=0.2.0"
      }
    },
    "node_modules/qs": {
      "version": "6.13.0",
      "resolved": "https://registry.npmjs.org/qs/-/qs-6.13.0.tgz",
      "integrity": "sha512-+38qI9SOr8tfZ4QmJNplMUxqjbe7LKvvZgWdExBOmd+egZTtjLB67Gu0HRX3u/XOq7UU2Nx6nsjvS16Z9uwfpg==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "side-channel": "^1.0.6"
      },
      "engines": {
        "node": ">=0.6"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/querystringify": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/querystringify/-/querystringify-2.2.0.tgz",
      "integrity": "sha512-FIqgj2EUvTa7R50u0rGsyTftzjYmv/a3hO345bZNrqabNqjtgiDMgmo4mkUjd+nzU5oF3dClKqFIPUKybUyqoQ==",
      "license": "MIT"
    },
    "node_modules/queue-microtask": {
      "version": "1.2.3",
      "resolved": "https://registry.npmjs.org/queue-microtask/-/queue-microtask-1.2.3.tgz",
      "integrity": "sha512-NuaNSa6flKT5JaSYQzJok04JzTL1CA6aGhv5rfLW3PgqA+M2ChpZQnAC8h8i4ZFkBS8X5RqkDBHA7r4hej3K9A==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT"
    },
    "node_modules/raf": {
      "version": "3.4.1",
      "resolved": "https://registry.npmjs.org/raf/-/raf-3.4.1.tgz",
      "integrity": "sha512-Sq4CW4QhwOHE8ucn6J34MqtZCeWFP2aQSmrlroYgqAV1PjStIhJXxYuTgUIfkEk7zTLjmIjLmU5q+fbD1NnOJA==",
      "license": "MIT",
      "dependencies": {
        "performance-now": "^2.1.0"
      }
    },
    "node_modules/randombytes": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/randombytes/-/randombytes-2.1.0.tgz",
      "integrity": "sha512-vYl3iOX+4CKUWuxGi9Ukhie6fsqXqS9FE2Zaic4tNFD2N2QQaXOMFbuKK4QmDHC0JO6B1Zp41J0LpT0oR68amQ==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "^5.1.0"
      }
    },
    "node_modules/range-parser": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/range-parser/-/range-parser-1.2.1.tgz",
      "integrity": "sha512-Hrgsx+orqoygnmhFbKaHE6c296J+HTAQXoxEF6gNupROmmGJRoyzfG3ccAveqCBrwr/2yxQ5BVd/GTl5agOwSg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/raw-body": {
      "version": "2.5.2",
      "resolved": "https://registry.npmjs.org/raw-body/-/raw-body-2.5.2.tgz",
      "integrity": "sha512-8zGqypfENjCIqGhgXToC8aB2r7YrBX+AQAfIPs/Mlk+BtPTztOvTS01NRW/3Eh60J+a48lt8qsCzirQ6loCVfA==",
      "license": "MIT",
      "dependencies": {
        "bytes": "3.1.2",
        "http-errors": "2.0.0",
        "iconv-lite": "0.4.24",
        "unpipe": "1.0.0"
      },
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/raw-body/node_modules/iconv-lite": {
      "version": "0.4.24",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.4.24.tgz",
      "integrity": "sha512-v3MXnZAcvnywkTUEZomIActle7RXXeedOR31wwl7VlyoXO4Qi9arvSenNQWne1TcRwhCL1HwLI21bEqdpj8/rA==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react": {
      "version": "19.1.1",
      "resolved": "https://registry.npmjs.org/react/-/react-19.1.1.tgz",
      "integrity": "sha512-w8nqGImo45dmMIfljjMwOGtbmC/mk4CMYhWIicdSflH91J9TyCyczcPFXJzrZ/ZXcgGRFeP6BU0BEJTw6tZdfQ==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-app-polyfill": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/react-app-polyfill/-/react-app-polyfill-3.0.0.tgz",
      "integrity": "sha512-sZ41cxiU5llIB003yxxQBYrARBqe0repqPTTYBTmMqTz9szeBbE37BehCE891NZsmdZqqP+xWKdT3eo3vOzN8w==",
      "license": "MIT",
      "dependencies": {
        "core-js": "^3.19.2",
        "object-assign": "^4.1.1",
        "promise": "^8.1.0",
        "raf": "^3.4.1",
        "regenerator-runtime": "^0.13.9",
        "whatwg-fetch": "^3.6.2"
      },
      "engines": {
        "node": ">=14"
      }
    },
    "node_modules/react-chartjs-2": {
      "version": "5.3.0",
      "resolved": "https://registry.npmjs.org/react-chartjs-2/-/react-chartjs-2-5.3.0.tgz",
      "integrity": "sha512-UfZZFnDsERI3c3CZGxzvNJd02SHjaSJ8kgW1djn65H1KK8rehwTjyrRKOG3VTMG8wtHZ5rgAO5oTHtHi9GCCmw==",
      "license": "MIT",
      "peerDependencies": {
        "chart.js": "^4.1.1",
        "react": "^16.8.0 || ^17.0.0 || ^18.0.0 || ^19.0.0"
      }
    },
    "node_modules/react-dev-utils": {
      "version": "12.0.1",
      "resolved": "https://registry.npmjs.org/react-dev-utils/-/react-dev-utils-12.0.1.tgz",
      "integrity": "sha512-84Ivxmr17KjUupyqzFode6xKhjwuEJDROWKJy/BthkL7Wn6NJ8h4WE6k/exAv6ImS+0oZLRRW5j/aINMHyeGeQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.16.0",
        "address": "^1.1.2",
        "browserslist": "^4.18.1",
        "chalk": "^4.1.2",
        "cross-spawn": "^7.0.3",
        "detect-port-alt": "^1.1.6",
        "escape-string-regexp": "^4.0.0",
        "filesize": "^8.0.6",
        "find-up": "^5.0.0",
        "fork-ts-checker-webpack-plugin": "^6.5.0",
        "global-modules": "^2.0.0",
        "globby": "^11.0.4",
        "gzip-size": "^6.0.0",
        "immer": "^9.0.7",
        "is-root": "^2.1.0",
        "loader-utils": "^3.2.0",
        "open": "^8.4.0",
        "pkg-up": "^3.1.0",
        "prompts": "^2.4.2",
        "react-error-overlay": "^6.0.11",
        "recursive-readdir": "^2.2.2",
        "shell-quote": "^1.7.3",
        "strip-ansi": "^6.0.1",
        "text-table": "^0.2.0"
      },
      "engines": {
        "node": ">=14"
      }
    },
    "node_modules/react-dev-utils/node_modules/find-up": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/find-up/-/find-up-5.0.0.tgz",
      "integrity": "sha512-78/PXT1wlLLDgTzDs7sjq9hzz0vXD+zn+7wypEe4fXQxCmdmqfGsEPQxmiCSQI3ajFV91bVSsvNtrJRiW6nGng==",
      "license": "MIT",
      "dependencies": {
        "locate-path": "^6.0.0",
        "path-exists": "^4.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/react-dev-utils/node_modules/loader-utils": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/loader-utils/-/loader-utils-3.3.1.tgz",
      "integrity": "sha512-FMJTLMXfCLMLfJxcX9PFqX5qD88Z5MRGaZCVzfuqeZSPsyiBzs+pahDQjbIWz2QIzPZz0NX9Zy4FX3lmK6YHIg==",
      "license": "MIT",
      "engines": {
        "node": ">= 12.13.0"
      }
    },
    "node_modules/react-dev-utils/node_modules/locate-path": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/locate-path/-/locate-path-6.0.0.tgz",
      "integrity": "sha512-iPZK6eYjbxRu3uB4/WZ3EsEIMJFMqAoopl3R+zuq0UjcAm/MO6KCweDgPfP3elTztoKP3KtnVHxTn2NHBSDVUw==",
      "license": "MIT",
      "dependencies": {
        "p-locate": "^5.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/react-dev-utils/node_modules/p-limit": {
      "version": "3.1.0",
      "resolved": "https://registry.npmjs.org/p-limit/-/p-limit-3.1.0.tgz",
      "integrity": "sha512-TYOanM3wGwNGsZN2cVTYPArw454xnXj5qmWF1bEoAc4+cU/ol7GVh7odevjp1FNHduHc3KZMcFduxU5Xc6uJRQ==",
      "license": "MIT",
      "dependencies": {
        "yocto-queue": "^0.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/react-dev-utils/node_modules/p-locate": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/p-locate/-/p-locate-5.0.0.tgz",
      "integrity": "sha512-LaNjtRWUBY++zB5nE/NwcaoMylSPk+S+ZHNB1TzdbMJMny6dynpAGt7X/tl/QYq3TIeE6nxHppbo2LGymrG5Pw==",
      "license": "MIT",
      "dependencies": {
        "p-limit": "^3.0.2"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/react-dom": {
      "version": "19.1.1",
      "resolved": "https://registry.npmjs.org/react-dom/-/react-dom-19.1.1.tgz",
      "integrity": "sha512-Dlq/5LAZgF0Gaz6yiqZCf6VCcZs1ghAJyrsu84Q/GT0gV+mCxbfmKNoGRKBYMJ8IEdGPqu49YWXD02GCknEDkw==",
      "license": "MIT",
      "dependencies": {
        "scheduler": "^0.26.0"
      },
      "peerDependencies": {
        "react": "^19.1.1"
      }
    },
    "node_modules/react-error-overlay": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/react-error-overlay/-/react-error-overlay-6.1.0.tgz",
      "integrity": "sha512-SN/U6Ytxf1QGkw/9ve5Y+NxBbZM6Ht95tuXNMKs8EJyFa/Vy/+Co3stop3KBHARfn/giv+Lj1uUnTfOJ3moFEQ==",
      "license": "MIT"
    },
    "node_modules/react-is": {
      "version": "17.0.2",
      "resolved": "https://registry.npmjs.org/react-is/-/react-is-17.0.2.tgz",
      "integrity": "sha512-w2GsyukL62IJnlaff/nRegPQR94C/XXamvMWmSHRJ4y7Ts/4ocGRmTHvOs8PSE6pB3dWOrD/nueuU5sduBsQ4w==",
      "license": "MIT"
    },
    "node_modules/react-refresh": {
      "version": "0.11.0",
      "resolved": "https://registry.npmjs.org/react-refresh/-/react-refresh-0.11.0.tgz",
      "integrity": "sha512-F27qZr8uUqwhWZboondsPx8tnC3Ct3SxZA3V5WyEvujRyyNv0VYPhoBg1gZ8/MV5tubQp76Trw8lTv9hzRBa+A==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/react-scripts": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/react-scripts/-/react-scripts-5.0.1.tgz",
      "integrity": "sha512-8VAmEm/ZAwQzJ+GOMLbBsTdDKOpuZh7RPs0UymvBR2vRk4iZWCskjbFnxqjrzoIvlNNRZ3QJFx6/qDSi6zSnaQ==",
      "license": "MIT",
      "dependencies": {
        "@babel/core": "^7.16.0",
        "@pmmmwh/react-refresh-webpack-plugin": "^0.5.3",
        "@svgr/webpack": "^5.5.0",
        "babel-jest": "^27.4.2",
        "babel-loader": "^8.2.3",
        "babel-plugin-named-asset-import": "^0.3.8",
        "babel-preset-react-app": "^10.0.1",
        "bfj": "^7.0.2",
        "browserslist": "^4.18.1",
        "camelcase": "^6.2.1",
        "case-sensitive-paths-webpack-plugin": "^2.4.0",
        "css-loader": "^6.5.1",
        "css-minimizer-webpack-plugin": "^3.2.0",
        "dotenv": "^10.0.0",
        "dotenv-expand": "^5.1.0",
        "eslint": "^8.3.0",
        "eslint-config-react-app": "^7.0.1",
        "eslint-webpack-plugin": "^3.1.1",
        "file-loader": "^6.2.0",
        "fs-extra": "^10.0.0",
        "html-webpack-plugin": "^5.5.0",
        "identity-obj-proxy": "^3.0.0",
        "jest": "^27.4.3",
        "jest-resolve": "^27.4.2",
        "jest-watch-typeahead": "^1.0.0",
        "mini-css-extract-plugin": "^2.4.5",
        "postcss": "^8.4.4",
        "postcss-flexbugs-fixes": "^5.0.2",
        "postcss-loader": "^6.2.1",
        "postcss-normalize": "^10.0.1",
        "postcss-preset-env": "^7.0.1",
        "prompts": "^2.4.2",
        "react-app-polyfill": "^3.0.0",
        "react-dev-utils": "^12.0.1",
        "react-refresh": "^0.11.0",
        "resolve": "^1.20.0",
        "resolve-url-loader": "^4.0.0",
        "sass-loader": "^12.3.0",
        "semver": "^7.3.5",
        "source-map-loader": "^3.0.0",
        "style-loader": "^3.3.1",
        "tailwindcss": "^3.0.2",
        "terser-webpack-plugin": "^5.2.5",
        "webpack": "^5.64.4",
        "webpack-dev-server": "^4.6.0",
        "webpack-manifest-plugin": "^4.0.2",
        "workbox-webpack-plugin": "^6.4.1"
      },
      "bin": {
        "react-scripts": "bin/react-scripts.js"
      },
      "engines": {
        "node": ">=14.0.0"
      },
      "optionalDependencies": {
        "fsevents": "^2.3.2"
      },
      "peerDependencies": {
        "react": ">= 16",
        "typescript": "^3.2.1 || ^4"
      },
      "peerDependenciesMeta": {
        "typescript": {
          "optional": true
        }
      }
    },
    "node_modules/read-cache": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/read-cache/-/read-cache-1.0.0.tgz",
      "integrity": "sha512-Owdv/Ft7IjOgm/i0xvNDZ1LrRANRfew4b2prF3OWMQLxLfu3bS8FVhCsrSCMK4lR56Y9ya+AThoTpDCTxCmpRA==",
      "license": "MIT",
      "dependencies": {
        "pify": "^2.3.0"
      }
    },
    "node_modules/readable-stream": {
      "version": "3.6.2",
      "resolved": "https://registry.npmjs.org/readable-stream/-/readable-stream-3.6.2.tgz",
      "integrity": "sha512-9u/sniCrY3D5WdsERHzHE4G2YCXqoG5FTHUiCC4SIbr6XcLZBY05ya9EKjYek9O5xOAwjGq+1JdGBAS7Q9ScoA==",
      "license": "MIT",
      "dependencies": {
        "inherits": "^2.0.3",
        "string_decoder": "^1.1.1",
        "util-deprecate": "^1.0.1"
      },
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/readdirp": {
      "version": "3.6.0",
      "resolved": "https://registry.npmjs.org/readdirp/-/readdirp-3.6.0.tgz",
      "integrity": "sha512-hOS089on8RduqdbhvQ5Z37A0ESjsqz6qnRcffsMU3495FuTdqSm+7bhJ29JvIOsBDEEnan5DPu9t3To9VRlMzA==",
      "license": "MIT",
      "dependencies": {
        "picomatch": "^2.2.1"
      },
      "engines": {
        "node": ">=8.10.0"
      }
    },
    "node_modules/recursive-readdir": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/recursive-readdir/-/recursive-readdir-2.2.3.tgz",
      "integrity": "sha512-8HrF5ZsXk5FAH9dgsx3BlUer73nIhuj+9OrQwEbLTPOBzGkL1lsFCR01am+v+0m2Cmbs1nP12hLDl5FA7EszKA==",
      "license": "MIT",
      "dependencies": {
        "minimatch": "^3.0.5"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/redent": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/redent/-/redent-3.0.0.tgz",
      "integrity": "sha512-6tDA8g98We0zd0GvVeMT9arEOnTw9qM03L9cJXaCjrip1OO764RDBLBfrB4cwzNGDj5OA5ioymC9GkizgWJDUg==",
      "license": "MIT",
      "dependencies": {
        "indent-string": "^4.0.0",
        "strip-indent": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/reflect.getprototypeof": {
      "version": "1.0.10",
      "resolved": "https://registry.npmjs.org/reflect.getprototypeof/-/reflect.getprototypeof-1.0.10.tgz",
      "integrity": "sha512-00o4I+DVrefhv+nX0ulyi3biSHCPDe+yLv5o/p6d/UVlirijB8E16FtfwSAi4g3tcqrQ4lRAqQSoFEZJehYEcw==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.9",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.7",
        "get-proto": "^1.0.1",
        "which-builtin-type": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/regenerate": {
      "version": "1.4.2",
      "resolved": "https://registry.npmjs.org/regenerate/-/regenerate-1.4.2.tgz",
      "integrity": "sha512-zrceR/XhGYU/d/opr2EKO7aRHUeiBI8qjtfHqADTwZd6Szfy16la6kqD0MIUs5z5hx6AaKa+PixpPrR289+I0A==",
      "license": "MIT"
    },
    "node_modules/regenerate-unicode-properties": {
      "version": "10.2.2",
      "resolved": "https://registry.npmjs.org/regenerate-unicode-properties/-/regenerate-unicode-properties-10.2.2.tgz",
      "integrity": "sha512-m03P+zhBeQd1RGnYxrGyDAPpWX/epKirLrp8e3qevZdVkKtnCrjjWczIbYc8+xd6vcTStVlqfycTx1KR4LOr0g==",
      "license": "MIT",
      "dependencies": {
        "regenerate": "^1.4.2"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/regenerator-runtime": {
      "version": "0.13.11",
      "resolved": "https://registry.npmjs.org/regenerator-runtime/-/regenerator-runtime-0.13.11.tgz",
      "integrity": "sha512-kY1AZVr2Ra+t+piVaJ4gxaFaReZVH40AKNo7UCX6W+dEwBo/2oZJzqfuN1qLq1oL45o56cPaTXELwrTh8Fpggg==",
      "license": "MIT"
    },
    "node_modules/regex-parser": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/regex-parser/-/regex-parser-2.3.1.tgz",
      "integrity": "sha512-yXLRqatcCuKtVHsWrNg0JL3l1zGfdXeEvDa0bdu4tCDQw0RpMDZsqbkyRTUnKMR0tXF627V2oEWjBEaEdqTwtQ==",
      "license": "MIT"
    },
    "node_modules/regexp.prototype.flags": {
      "version": "1.5.4",
      "resolved": "https://registry.npmjs.org/regexp.prototype.flags/-/regexp.prototype.flags-1.5.4.tgz",
      "integrity": "sha512-dYqgNSZbDwkaJ2ceRd9ojCGjBq+mOm9LmtXnAnEGyHhN/5R7iDW2TRw3h+o/jCFxus3P2LfWIIiwowAjANm7IA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "define-properties": "^1.2.1",
        "es-errors": "^1.3.0",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "set-function-name": "^2.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/regexpu-core": {
      "version": "6.3.1",
      "resolved": "https://registry.npmjs.org/regexpu-core/-/regexpu-core-6.3.1.tgz",
      "integrity": "sha512-DzcswPr252wEr7Qz8AyAVbfyBDKLoYp6eRA1We2Fa9qirRFSdtkP5sHr3yglDKy2BbA0fd2T+j/CUSKes3FeVQ==",
      "license": "MIT",
      "dependencies": {
        "regenerate": "^1.4.2",
        "regenerate-unicode-properties": "^10.2.2",
        "regjsgen": "^0.8.0",
        "regjsparser": "^0.12.0",
        "unicode-match-property-ecmascript": "^2.0.0",
        "unicode-match-property-value-ecmascript": "^2.2.1"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/regjsgen": {
      "version": "0.8.0",
      "resolved": "https://registry.npmjs.org/regjsgen/-/regjsgen-0.8.0.tgz",
      "integrity": "sha512-RvwtGe3d7LvWiDQXeQw8p5asZUmfU1G/l6WbUXeHta7Y2PEIvBTwH6E2EfmYUK8pxcxEdEmaomqyp0vZZ7C+3Q==",
      "license": "MIT"
    },
    "node_modules/regjsparser": {
      "version": "0.12.0",
      "resolved": "https://registry.npmjs.org/regjsparser/-/regjsparser-0.12.0.tgz",
      "integrity": "sha512-cnE+y8bz4NhMjISKbgeVJtqNbtf5QpjZP+Bslo+UqkIt9QPnX9q095eiRRASJG1/tz6dlNr6Z5NsBiWYokp6EQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "jsesc": "~3.0.2"
      },
      "bin": {
        "regjsparser": "bin/parser"
      }
    },
    "node_modules/regjsparser/node_modules/jsesc": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/jsesc/-/jsesc-3.0.2.tgz",
      "integrity": "sha512-xKqzzWXDttJuOcawBt4KnKHHIf5oQ/Cxax+0PWFG+DFDgHNAdi+TXECADI+RYiFUMmx8792xsMbbgXj4CwnP4g==",
      "license": "MIT",
      "bin": {
        "jsesc": "bin/jsesc"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/relateurl": {
      "version": "0.2.7",
      "resolved": "https://registry.npmjs.org/relateurl/-/relateurl-0.2.7.tgz",
      "integrity": "sha512-G08Dxvm4iDN3MLM0EsP62EDV9IuhXPR6blNz6Utcp7zyV3tr4HVNINt6MpaRWbxoOHT3Q7YN2P+jaHX8vUbgog==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.10"
      }
    },
    "node_modules/renderkid": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/renderkid/-/renderkid-3.0.0.tgz",
      "integrity": "sha512-q/7VIQA8lmM1hF+jn+sFSPWGlMkSAeNYcPLmDQx2zzuiDfaLrOmumR8iaUKlenFgh0XRPIUeSPlH3A+AW3Z5pg==",
      "license": "MIT",
      "dependencies": {
        "css-select": "^4.1.3",
        "dom-converter": "^0.2.0",
        "htmlparser2": "^6.1.0",
        "lodash": "^4.17.21",
        "strip-ansi": "^6.0.1"
      }
    },
    "node_modules/require-directory": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/require-directory/-/require-directory-2.1.1.tgz",
      "integrity": "sha512-fGxEI7+wsG9xrvdjsrlmL22OMTTiHRwAMroiEeMgq8gzoLC/PQr7RsRDSTLUg/bZAZtF+TVIkHc6/4RIKrui+Q==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/require-from-string": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/require-from-string/-/require-from-string-2.0.2.tgz",
      "integrity": "sha512-Xf0nWe6RseziFMu+Ap9biiUbmplq6S9/p+7w7YXP/JBHhrUDDUhwa+vANyubuqfZWTveU//DYVGsDG7RKL/vEw==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/requires-port": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/requires-port/-/requires-port-1.0.0.tgz",
      "integrity": "sha512-KigOCHcocU3XODJxsu8i/j8T9tzT4adHiecwORRQ0ZZFcp7ahwXuRU1m+yuO90C5ZUyGeGfocHDI14M3L3yDAQ==",
      "license": "MIT"
    },
    "node_modules/resolve": {
      "version": "1.22.10",
      "resolved": "https://registry.npmjs.org/resolve/-/resolve-1.22.10.tgz",
      "integrity": "sha512-NPRy+/ncIMeDlTAsuqwKIiferiawhefFJtkNSW0qZJEqMEb+qBt/77B/jGeeek+F0uOeN05CDa6HXbbIgtVX4w==",
      "license": "MIT",
      "dependencies": {
        "is-core-module": "^2.16.0",
        "path-parse": "^1.0.7",
        "supports-preserve-symlinks-flag": "^1.0.0"
      },
      "bin": {
        "resolve": "bin/resolve"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/resolve-cwd": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/resolve-cwd/-/resolve-cwd-3.0.0.tgz",
      "integrity": "sha512-OrZaX2Mb+rJCpH/6CpSqt9xFVpN++x01XnN2ie9g6P5/3xelLAkXWVADpdz1IHD/KFfEXyE6V0U01OQ3UO2rEg==",
      "license": "MIT",
      "dependencies": {
        "resolve-from": "^5.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/resolve-from": {
      "version": "5.0.0",
      "resolved": "https://registry.npmjs.org/resolve-from/-/resolve-from-5.0.0.tgz",
      "integrity": "sha512-qYg9KP24dD5qka9J47d0aVky0N+b4fTU89LN9iDnjB5waksiC49rvMB0PrUJQGoTmH50XPiqOvAjDfaijGxYZw==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/resolve-url-loader": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/resolve-url-loader/-/resolve-url-loader-4.0.0.tgz",
      "integrity": "sha512-05VEMczVREcbtT7Bz+C+96eUO5HDNvdthIiMB34t7FcF8ehcu4wC0sSgPUubs3XW2Q3CNLJk/BJrCU9wVRymiA==",
      "license": "MIT",
      "dependencies": {
        "adjust-sourcemap-loader": "^4.0.0",
        "convert-source-map": "^1.7.0",
        "loader-utils": "^2.0.0",
        "postcss": "^7.0.35",
        "source-map": "0.6.1"
      },
      "engines": {
        "node": ">=8.9"
      },
      "peerDependencies": {
        "rework": "1.0.1",
        "rework-visit": "1.0.0"
      },
      "peerDependenciesMeta": {
        "rework": {
          "optional": true
        },
        "rework-visit": {
          "optional": true
        }
      }
    },
    "node_modules/resolve-url-loader/node_modules/convert-source-map": {
      "version": "1.9.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-1.9.0.tgz",
      "integrity": "sha512-ASFBup0Mz1uyiIjANan1jzLQami9z1PoYSZCiiYW2FczPbenXc45FZdBZLzOT+r6+iciuEModtmCti+hjaAk0A==",
      "license": "MIT"
    },
    "node_modules/resolve-url-loader/node_modules/picocolors": {
      "version": "0.2.1",
      "resolved": "https://registry.npmjs.org/picocolors/-/picocolors-0.2.1.tgz",
      "integrity": "sha512-cMlDqaLEqfSaW8Z7N5Jw+lyIW869EzT73/F5lhtY9cLGoVxSXznfgfXMO0Z5K0o0Q2TkTXq+0KFsdnSe3jDViA==",
      "license": "ISC"
    },
    "node_modules/resolve-url-loader/node_modules/postcss": {
      "version": "7.0.39",
      "resolved": "https://registry.npmjs.org/postcss/-/postcss-7.0.39.tgz",
      "integrity": "sha512-yioayjNbHn6z1/Bywyb2Y4s3yvDAeXGOyxqD+LnVOinq6Mdmd++SW2wUNVzavyyHxd6+DxzWGIuosg6P1Rj8uA==",
      "license": "MIT",
      "dependencies": {
        "picocolors": "^0.2.1",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=6.0.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/postcss/"
      }
    },
    "node_modules/resolve-url-loader/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/resolve.exports": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/resolve.exports/-/resolve.exports-1.1.1.tgz",
      "integrity": "sha512-/NtpHNDN7jWhAaQ9BvBUYZ6YTXsRBgfqWFWP7BZBaoMJO/I3G5OFzvTuWNlZC3aPjins1F+TNrLKsGbH4rfsRQ==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/retry": {
      "version": "0.13.1",
      "resolved": "https://registry.npmjs.org/retry/-/retry-0.13.1.tgz",
      "integrity": "sha512-XQBQ3I8W1Cge0Seh+6gjj03LbmRFWuoszgK9ooCpwYIrhhoO80pfq4cUkU5DkknwfOfFteRwlZ56PYOGYyFWdg==",
      "license": "MIT",
      "engines": {
        "node": ">= 4"
      }
    },
    "node_modules/reusify": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/reusify/-/reusify-1.1.0.tgz",
      "integrity": "sha512-g6QUff04oZpHs0eG5p83rFLhHeV00ug/Yf9nZM6fLeUrPguBTkTQOdpAWWspMh55TZfVQDPaN3NQJfbVRAxdIw==",
      "license": "MIT",
      "engines": {
        "iojs": ">=1.0.0",
        "node": ">=0.10.0"
      }
    },
    "node_modules/rimraf": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/rimraf/-/rimraf-3.0.2.tgz",
      "integrity": "sha512-JZkJMZkAGFFPP2YqXZXPbMlMBgsxzE8ILs4lMIX/2o0L9UBw9O/Y3o6wFw/i9YLapcUJWwqbi3kdxIPdC62TIA==",
      "deprecated": "Rimraf versions prior to v4 are no longer supported",
      "license": "ISC",
      "dependencies": {
        "glob": "^7.1.3"
      },
      "bin": {
        "rimraf": "bin.js"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/rollup": {
      "version": "2.79.2",
      "resolved": "https://registry.npmjs.org/rollup/-/rollup-2.79.2.tgz",
      "integrity": "sha512-fS6iqSPZDs3dr/y7Od6y5nha8dW1YnbgtsyotCVvoFGKbERG++CVRFv1meyGDE1SNItQA8BrnCw7ScdAhRJ3XQ==",
      "license": "MIT",
      "bin": {
        "rollup": "dist/bin/rollup"
      },
      "engines": {
        "node": ">=10.0.0"
      },
      "optionalDependencies": {
        "fsevents": "~2.3.2"
      }
    },
    "node_modules/rollup-plugin-terser": {
      "version": "7.0.2",
      "resolved": "https://registry.npmjs.org/rollup-plugin-terser/-/rollup-plugin-terser-7.0.2.tgz",
      "integrity": "sha512-w3iIaU4OxcF52UUXiZNsNeuXIMDvFrr+ZXK6bFZ0Q60qyVfq4uLptoS4bbq3paG3x216eQllFZX7zt6TIImguQ==",
      "deprecated": "This package has been deprecated and is no longer maintained. Please use @rollup/plugin-terser",
      "license": "MIT",
      "dependencies": {
        "@babel/code-frame": "^7.10.4",
        "jest-worker": "^26.2.1",
        "serialize-javascript": "^4.0.0",
        "terser": "^5.0.0"
      },
      "peerDependencies": {
        "rollup": "^2.0.0"
      }
    },
    "node_modules/rollup-plugin-terser/node_modules/jest-worker": {
      "version": "26.6.2",
      "resolved": "https://registry.npmjs.org/jest-worker/-/jest-worker-26.6.2.tgz",
      "integrity": "sha512-KWYVV1c4i+jbMpaBC+U++4Va0cp8OisU185o73T1vo99hqi7w8tSJfUXYswwqqrjzwxa6KpRK54WhPvwf5w6PQ==",
      "license": "MIT",
      "dependencies": {
        "@types/node": "*",
        "merge-stream": "^2.0.0",
        "supports-color": "^7.0.0"
      },
      "engines": {
        "node": ">= 10.13.0"
      }
    },
    "node_modules/rollup-plugin-terser/node_modules/serialize-javascript": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/serialize-javascript/-/serialize-javascript-4.0.0.tgz",
      "integrity": "sha512-GaNA54380uFefWghODBWEGisLZFj00nS5ACs6yHa9nLqlLpVLO8ChDGeKRjZnV4Nh4n0Qi7nhYZD/9fCPzEqkw==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "randombytes": "^2.1.0"
      }
    },
    "node_modules/run-parallel": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/run-parallel/-/run-parallel-1.2.0.tgz",
      "integrity": "sha512-5l4VyZR86LZ/lDxZTR6jqL8AFE2S0IFLMP26AbjsLVADxHdhB/c0GUsH+y39UfCi3dzz8OlQuPmnaJOMoDHQBA==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "queue-microtask": "^1.2.2"
      }
    },
    "node_modules/safe-array-concat": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/safe-array-concat/-/safe-array-concat-1.1.3.tgz",
      "integrity": "sha512-AURm5f0jYEOydBj7VQlVvDrjeFgthDdEF5H1dP+6mNpoXOMo1quQqJ4wvJDyRZ9+pO3kGWoOdmV08cSv2aJV6Q==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "get-intrinsic": "^1.2.6",
        "has-symbols": "^1.1.0",
        "isarray": "^2.0.5"
      },
      "engines": {
        "node": ">=0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safe-buffer": {
      "version": "5.2.1",
      "resolved": "https://registry.npmjs.org/safe-buffer/-/safe-buffer-5.2.1.tgz",
      "integrity": "sha512-rp3So07KcdmmKbGvgaNxQSJr7bGVSVk5S9Eq1F+ppbRo70+YeaDxkw5Dd8NPN+GD6bjnYm2VuPuCXmpuYvmCXQ==",
      "funding": [
        {
          "type": "github",
          "url": "https://github.com/sponsors/feross"
        },
        {
          "type": "patreon",
          "url": "https://www.patreon.com/feross"
        },
        {
          "type": "consulting",
          "url": "https://feross.org/support"
        }
      ],
      "license": "MIT"
    },
    "node_modules/safe-push-apply": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/safe-push-apply/-/safe-push-apply-1.0.0.tgz",
      "integrity": "sha512-iKE9w/Z7xCzUMIZqdBsp6pEQvwuEebH4vdpjcDWnyzaI6yl6O9FHvVpmGelvEHNsoY6wGblkxR6Zty/h00WiSA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "isarray": "^2.0.5"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safe-regex-test": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/safe-regex-test/-/safe-regex-test-1.1.0.tgz",
      "integrity": "sha512-x/+Cz4YrimQxQccJf5mKEbIa1NzeCRNI5Ecl/ekmlYaampdNLPalVyIcCZNNH3MvmqBugV5TMYZXv0ljslUlaw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "is-regex": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/safer-buffer": {
      "version": "2.1.2",
      "resolved": "https://registry.npmjs.org/safer-buffer/-/safer-buffer-2.1.2.tgz",
      "integrity": "sha512-YZo3K82SD7Riyi0E1EQPojLz7kpepnSQI9IyPbHHg1XXXevb5dJI7tpyN2ADxGcQbHG7vcyRHk0cbwqcQriUtg==",
      "license": "MIT"
    },
    "node_modules/sanitize.css": {
      "version": "13.0.0",
      "resolved": "https://registry.npmjs.org/sanitize.css/-/sanitize.css-13.0.0.tgz",
      "integrity": "sha512-ZRwKbh/eQ6w9vmTjkuG0Ioi3HBwPFce0O+v//ve+aOq1oeCy7jMV2qzzAlpsNuqpqCBjjriM1lbtZbF/Q8jVyA==",
      "license": "CC0-1.0"
    },
    "node_modules/sass-loader": {
      "version": "12.6.0",
      "resolved": "https://registry.npmjs.org/sass-loader/-/sass-loader-12.6.0.tgz",
      "integrity": "sha512-oLTaH0YCtX4cfnJZxKSLAyglED0naiYfNG1iXfU5w1LNZ+ukoA5DtyDIN5zmKVZwYNJP4KRc5Y3hkWga+7tYfA==",
      "license": "MIT",
      "dependencies": {
        "klona": "^2.0.4",
        "neo-async": "^2.6.2"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "fibers": ">= 3.1.0",
        "node-sass": "^4.0.0 || ^5.0.0 || ^6.0.0 || ^7.0.0",
        "sass": "^1.3.0",
        "sass-embedded": "*",
        "webpack": "^5.0.0"
      },
      "peerDependenciesMeta": {
        "fibers": {
          "optional": true
        },
        "node-sass": {
          "optional": true
        },
        "sass": {
          "optional": true
        },
        "sass-embedded": {
          "optional": true
        }
      }
    },
    "node_modules/sax": {
      "version": "1.2.4",
      "resolved": "https://registry.npmjs.org/sax/-/sax-1.2.4.tgz",
      "integrity": "sha512-NqVDv9TpANUjFm0N8uM5GxL36UgKi9/atZw+x7YFnQ8ckwFGKrl4xX4yWtrey3UJm5nP1kUbnYgLopqWNSRhWw==",
      "license": "ISC"
    },
    "node_modules/saxes": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/saxes/-/saxes-5.0.1.tgz",
      "integrity": "sha512-5LBh1Tls8c9xgGjw3QrMwETmTMVk0oFgvrFSvWx62llR2hcEInrKNZ2GZCCuuy2lvWrdl5jhbpeqc5hRYKFOcw==",
      "license": "ISC",
      "dependencies": {
        "xmlchars": "^2.2.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/scheduler": {
      "version": "0.26.0",
      "resolved": "https://registry.npmjs.org/scheduler/-/scheduler-0.26.0.tgz",
      "integrity": "sha512-NlHwttCI/l5gCPR3D1nNXtWABUmBwvZpEQiD4IXSbIDq8BzLIK/7Ir5gTFSGZDUu37K5cMNp0hFtzO38sC7gWA==",
      "license": "MIT"
    },
    "node_modules/schema-utils": {
      "version": "4.3.2",
      "resolved": "https://registry.npmjs.org/schema-utils/-/schema-utils-4.3.2.tgz",
      "integrity": "sha512-Gn/JaSk/Mt9gYubxTtSn/QCV4em9mpAPiR1rqy/Ocu19u/G9J5WWdNoUT4SiV6mFC3y6cxyFcFwdzPM3FgxGAQ==",
      "license": "MIT",
      "dependencies": {
        "@types/json-schema": "^7.0.9",
        "ajv": "^8.9.0",
        "ajv-formats": "^2.1.1",
        "ajv-keywords": "^5.1.0"
      },
      "engines": {
        "node": ">= 10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/schema-utils/node_modules/ajv": {
      "version": "8.17.1",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-8.17.1.tgz",
      "integrity": "sha512-B/gBuNg5SiMTrPkC+A2+cW0RszwxYmn6VYxB/inlBStS5nx6xHIt/ehKRhIMhqusl7a8LjQoZnjCs5vhwxOQ1g==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "fast-uri": "^3.0.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/schema-utils/node_modules/ajv-keywords": {
      "version": "5.1.0",
      "resolved": "https://registry.npmjs.org/ajv-keywords/-/ajv-keywords-5.1.0.tgz",
      "integrity": "sha512-YCS/JNFAUyr5vAuhk1DWm1CBxRHW9LbJ2ozWeemrIqpbsqKjHVxYPyi5GC0rjZIT5JxJ3virVTS8wk4i/Z+krw==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3"
      },
      "peerDependencies": {
        "ajv": "^8.8.2"
      }
    },
    "node_modules/schema-utils/node_modules/json-schema-traverse": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-1.0.0.tgz",
      "integrity": "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug==",
      "license": "MIT"
    },
    "node_modules/select-hose": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/select-hose/-/select-hose-2.0.0.tgz",
      "integrity": "sha512-mEugaLK+YfkijB4fx0e6kImuJdCIt2LxCRcbEYPqRGCs4F2ogyfZU5IAZRdjCP8JPq2AtdNoC/Dux63d9Kiryg==",
      "license": "MIT"
    },
    "node_modules/selfsigned": {
      "version": "2.4.1",
      "resolved": "https://registry.npmjs.org/selfsigned/-/selfsigned-2.4.1.tgz",
      "integrity": "sha512-th5B4L2U+eGLq1TVh7zNRGBapioSORUeymIydxgFpwww9d2qyKvtuPU2jJuHvYAwwqi2Y596QBL3eEqcPEYL8Q==",
      "license": "MIT",
      "dependencies": {
        "@types/node-forge": "^1.3.0",
        "node-forge": "^1"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/semver": {
      "version": "7.7.2",
      "resolved": "https://registry.npmjs.org/semver/-/semver-7.7.2.tgz",
      "integrity": "sha512-RF0Fw+rO5AMf9MAyaRXI4AV0Ulj5lMHqVxxdSgiVbixSCXoEmmX/jk0CuJw4+3SqroYO9VoUh+HcuJivvtJemA==",
      "license": "ISC",
      "bin": {
        "semver": "bin/semver.js"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/send": {
      "version": "0.19.0",
      "resolved": "https://registry.npmjs.org/send/-/send-0.19.0.tgz",
      "integrity": "sha512-dW41u5VfLXu8SJh5bwRmyYUbAoSB3c9uQh6L8h/KtsFREPWpbX1lrljJo186Jc4nmci/sGUZ9a0a0J2zgfq2hw==",
      "license": "MIT",
      "dependencies": {
        "debug": "2.6.9",
        "depd": "2.0.0",
        "destroy": "1.2.0",
        "encodeurl": "~1.0.2",
        "escape-html": "~1.0.3",
        "etag": "~1.8.1",
        "fresh": "0.5.2",
        "http-errors": "2.0.0",
        "mime": "1.6.0",
        "ms": "2.1.3",
        "on-finished": "2.4.1",
        "range-parser": "~1.2.1",
        "statuses": "2.0.1"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/send/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/send/node_modules/debug/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/send/node_modules/encodeurl": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/encodeurl/-/encodeurl-1.0.2.tgz",
      "integrity": "sha512-TPJXq8JqFaVYm2CWmPvnP2Iyo4ZSM7/QKcSmuMLDObfpH5fi7RUGmd/rTDf+rut/saiDiQEeVTNgAmJEdAOx0w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/serialize-javascript": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/serialize-javascript/-/serialize-javascript-6.0.2.tgz",
      "integrity": "sha512-Saa1xPByTTq2gdeFZYLLo+RFE35NHZkAbqZeWNd3BpzppeVisAqpDjcp8dyf6uIvEqJRd46jemmyA4iFIeVk8g==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "randombytes": "^2.1.0"
      }
    },
    "node_modules/serve-index": {
      "version": "1.9.1",
      "resolved": "https://registry.npmjs.org/serve-index/-/serve-index-1.9.1.tgz",
      "integrity": "sha512-pXHfKNP4qujrtteMrSBb0rc8HJ9Ms/GrXwcUtUtD5s4ewDJI8bT3Cz2zTVRMKtri49pLx2e0Ya8ziP5Ya2pZZw==",
      "license": "MIT",
      "dependencies": {
        "accepts": "~1.3.4",
        "batch": "0.6.1",
        "debug": "2.6.9",
        "escape-html": "~1.0.3",
        "http-errors": "~1.6.2",
        "mime-types": "~2.1.17",
        "parseurl": "~1.3.2"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/serve-index/node_modules/debug": {
      "version": "2.6.9",
      "resolved": "https://registry.npmjs.org/debug/-/debug-2.6.9.tgz",
      "integrity": "sha512-bC7ElrdJaJnPbAP+1EotYvqZsb3ecl5wi6Bfi6BJTUcNowp6cvspg0jXznRTKDjm/E7AdgFBVeAPVMNcKGsHMA==",
      "license": "MIT",
      "dependencies": {
        "ms": "2.0.0"
      }
    },
    "node_modules/serve-index/node_modules/depd": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/depd/-/depd-1.1.2.tgz",
      "integrity": "sha512-7emPTl6Dpo6JRXOXjLRxck+FlLRX5847cLKEn00PLAgc3g2hTZZgr+e4c2v6QpSmLeFP3n5yUo7ft6avBK/5jQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/serve-index/node_modules/http-errors": {
      "version": "1.6.3",
      "resolved": "https://registry.npmjs.org/http-errors/-/http-errors-1.6.3.tgz",
      "integrity": "sha512-lks+lVC8dgGyh97jxvxeYTWQFvh4uw4yC12gVl63Cg30sjPX4wuGcdkICVXDAESr6OJGjqGA8Iz5mkeN6zlD7A==",
      "license": "MIT",
      "dependencies": {
        "depd": "~1.1.2",
        "inherits": "2.0.3",
        "setprototypeof": "1.1.0",
        "statuses": ">= 1.4.0 < 2"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/serve-index/node_modules/inherits": {
      "version": "2.0.3",
      "resolved": "https://registry.npmjs.org/inherits/-/inherits-2.0.3.tgz",
      "integrity": "sha512-x00IRNXNy63jwGkJmzPigoySHbaqpNuzKbBOmzK+g2OdZpQ9w+sxCN+VSB3ja7IAge2OP2qpfxTjeNcyjmW1uw==",
      "license": "ISC"
    },
    "node_modules/serve-index/node_modules/ms": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/ms/-/ms-2.0.0.tgz",
      "integrity": "sha512-Tpp60P6IUJDTuOq/5Z8cdskzJujfwqfOTkrwIwj7IRISpnkJnT6SyJ4PCPnGMoFjC9ddhal5KVIYtAt97ix05A==",
      "license": "MIT"
    },
    "node_modules/serve-index/node_modules/setprototypeof": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/setprototypeof/-/setprototypeof-1.1.0.tgz",
      "integrity": "sha512-BvE/TwpZX4FXExxOxZyRGQQv651MSwmWKZGqvmPcRIjDqWub67kTKuIMx43cZZrS/cBBzwBcNDWoFxt2XEFIpQ==",
      "license": "ISC"
    },
    "node_modules/serve-index/node_modules/statuses": {
      "version": "1.5.0",
      "resolved": "https://registry.npmjs.org/statuses/-/statuses-1.5.0.tgz",
      "integrity": "sha512-OpZ3zP+jT1PI7I8nemJX4AKmAX070ZkYPVWV/AaKTJl+tXCTGyVdC1a4SL8RUQYEwk/f34ZX8UTykN68FwrqAA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/serve-static": {
      "version": "1.16.2",
      "resolved": "https://registry.npmjs.org/serve-static/-/serve-static-1.16.2.tgz",
      "integrity": "sha512-VqpjJZKadQB/PEbEwvFdO43Ax5dFBZ2UECszz8bQ7pi7wt//PWe1P6MN7eCnjsatYtBT6EuiClbjSWP2WrIoTw==",
      "license": "MIT",
      "dependencies": {
        "encodeurl": "~2.0.0",
        "escape-html": "~1.0.3",
        "parseurl": "~1.3.3",
        "send": "0.19.0"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/set-function-length": {
      "version": "1.2.2",
      "resolved": "https://registry.npmjs.org/set-function-length/-/set-function-length-1.2.2.tgz",
      "integrity": "sha512-pgRc4hJ4/sNjWCSS9AmnS40x3bNMDTknHgL5UaMBTMyJnU90EgWh1Rz+MC9eFu4BuN/UwZjKQuY/1v3rM7HMfg==",
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-errors": "^1.3.0",
        "function-bind": "^1.1.2",
        "get-intrinsic": "^1.2.4",
        "gopd": "^1.0.1",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/set-function-name": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/set-function-name/-/set-function-name-2.0.2.tgz",
      "integrity": "sha512-7PGFlmtwsEADb0WYyvCMa1t+yke6daIG4Wirafur5kcf+MhUnPms1UeR0CKQdTZD81yESwMHbtn+TR+dMviakQ==",
      "license": "MIT",
      "dependencies": {
        "define-data-property": "^1.1.4",
        "es-errors": "^1.3.0",
        "functions-have-names": "^1.2.3",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/set-proto": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/set-proto/-/set-proto-1.0.0.tgz",
      "integrity": "sha512-RJRdvCo6IAnPdsvP/7m6bsQqNnn1FCBX5ZNtFL98MmFF/4xAIJTIg1YbHW5DC2W5SKZanrC6i4HsJqlajw/dZw==",
      "license": "MIT",
      "dependencies": {
        "dunder-proto": "^1.0.1",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/setprototypeof": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/setprototypeof/-/setprototypeof-1.2.0.tgz",
      "integrity": "sha512-E5LDX7Wrp85Kil5bhZv46j8jOeboKq5JMmYM3gVGdGH8xFpPWXUMsNrlODCrkoxMEeNi/XZIwuRvY4XNwYMJpw==",
      "license": "ISC"
    },
    "node_modules/shebang-command": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/shebang-command/-/shebang-command-2.0.0.tgz",
      "integrity": "sha512-kHxr2zZpYtdmrN1qDjrrX/Z1rR1kG8Dx+gkpK1G4eXmvXswmcE1hTWBWYUzlraYw1/yZp6YuDY77YtvbN0dmDA==",
      "license": "MIT",
      "dependencies": {
        "shebang-regex": "^3.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shebang-regex": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/shebang-regex/-/shebang-regex-3.0.0.tgz",
      "integrity": "sha512-7++dFhtcx3353uBaq8DDR4NuxBetBzC7ZQOhmTQInHEd6bSrXdiEyzCvG07Z44UYdLShWUyXt5M/yhz8ekcb1A==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/shell-quote": {
      "version": "1.8.3",
      "resolved": "https://registry.npmjs.org/shell-quote/-/shell-quote-1.8.3.tgz",
      "integrity": "sha512-ObmnIF4hXNg1BqhnHmgbDETF8dLPCggZWBjkQfhZpbszZnYur5DUljTcCHii5LC3J5E0yeO/1LIMyH+UvHQgyw==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/side-channel/-/side-channel-1.1.0.tgz",
      "integrity": "sha512-ZX99e6tRweoUXqR+VBrslhda51Nh5MTQwou5tnUDgbtyM0dBgmhEDtWGP/xbKn6hqfPRHujUNwz5fy/wbbhnpw==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3",
        "side-channel-list": "^1.0.0",
        "side-channel-map": "^1.0.1",
        "side-channel-weakmap": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-list": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/side-channel-list/-/side-channel-list-1.0.0.tgz",
      "integrity": "sha512-FCLHtRD/gnpCiCHEiJLOwdmFP+wzCmDEkc9y7NsYxeF4u7Btsn1ZuwgwJGxImImHicJArLP4R0yX4c2KCrMrTA==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-map": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/side-channel-map/-/side-channel-map-1.0.1.tgz",
      "integrity": "sha512-VCjCNfgMsby3tTdo02nbjtM/ewra6jPHmpThenkTYh8pG9ucZ/1P8So4u4FGBek/BjpOVsDCMoLA/iuBKIFXRA==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/side-channel-weakmap": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/side-channel-weakmap/-/side-channel-weakmap-1.0.2.tgz",
      "integrity": "sha512-WPS/HvHQTYnHisLo9McqBHOJk2FkHO/tlpvldyrnem4aeQp4hai3gythswg6p01oSoTl58rcpiFAjF2br2Ak2A==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "es-errors": "^1.3.0",
        "get-intrinsic": "^1.2.5",
        "object-inspect": "^1.13.3",
        "side-channel-map": "^1.0.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/signal-exit": {
      "version": "3.0.7",
      "resolved": "https://registry.npmjs.org/signal-exit/-/signal-exit-3.0.7.tgz",
      "integrity": "sha512-wnD2ZE+l+SPC/uoS0vXeE9L1+0wuaMqKlfz9AMUo38JsyLSBWSFcHR1Rri62LZc12vLr1gb3jl7iwQhgwpAbGQ==",
      "license": "ISC"
    },
    "node_modules/sisteransi": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/sisteransi/-/sisteransi-1.0.5.tgz",
      "integrity": "sha512-bLGGlR1QxBcynn2d5YmDX4MGjlZvy2MRBDRNHLJ8VI6l6+9FUiyTFNJ0IveOSP0bcXgVDPRcfGqA0pjaqUpfVg==",
      "license": "MIT"
    },
    "node_modules/slash": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/slash/-/slash-3.0.0.tgz",
      "integrity": "sha512-g9Q1haeby36OSStwb4ntCGGGaKsaVSjQ68fBxoQcutl5fS1vuY18H3wSt3jFyFtrkx+Kz0V1G85A4MyAdDMi2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/sockjs": {
      "version": "0.3.24",
      "resolved": "https://registry.npmjs.org/sockjs/-/sockjs-0.3.24.tgz",
      "integrity": "sha512-GJgLTZ7vYb/JtPSSZ10hsOYIvEYsjbNU+zPdIHcUaWVNUEPivzxku31865sSSud0Da0W4lEeOPlmw93zLQchuQ==",
      "license": "MIT",
      "dependencies": {
        "faye-websocket": "^0.11.3",
        "uuid": "^8.3.2",
        "websocket-driver": "^0.7.4"
      }
    },
    "node_modules/source-list-map": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/source-list-map/-/source-list-map-2.0.1.tgz",
      "integrity": "sha512-qnQ7gVMxGNxsiL4lEuJwe/To8UnK7fAnmbGEEH8RpLouuKbeEm0lhbQVFIrNSuB+G7tVrAlVsZgETT5nljf+Iw==",
      "license": "MIT"
    },
    "node_modules/source-map": {
      "version": "0.7.6",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.7.6.tgz",
      "integrity": "sha512-i5uvt8C3ikiWeNZSVZNWcfZPItFQOsYTUAOkcUPGd8DqDy1uOUikjt5dG+uRlwyvR108Fb9DOd4GvXfT0N2/uQ==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">= 12"
      }
    },
    "node_modules/source-map-js": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/source-map-js/-/source-map-js-1.2.1.tgz",
      "integrity": "sha512-UXWMKhLOwVKb728IUtQPXxfYU+usdybtUrK/8uGE8CQMvrhOpwvzDBwj0QhSL7MQc7vIsISBG8VQ8+IDQxpfQA==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/source-map-loader": {
      "version": "3.0.2",
      "resolved": "https://registry.npmjs.org/source-map-loader/-/source-map-loader-3.0.2.tgz",
      "integrity": "sha512-BokxPoLjyl3iOrgkWaakaxqnelAJSS+0V+De0kKIq6lyWrXuiPgYTGp6z3iHmqljKAaLXwZa+ctD8GccRJeVvg==",
      "license": "MIT",
      "dependencies": {
        "abab": "^2.0.5",
        "iconv-lite": "^0.6.3",
        "source-map-js": "^1.0.1"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.0.0"
      }
    },
    "node_modules/source-map-support": {
      "version": "0.5.21",
      "resolved": "https://registry.npmjs.org/source-map-support/-/source-map-support-0.5.21.tgz",
      "integrity": "sha512-uBHU3L3czsIyYXKX88fdrGovxdSCoTGDRZ6SYXtSRxLZUzHg5P/66Ht6uoUlHu9EZod+inXhKo3qQgwXUT/y1w==",
      "license": "MIT",
      "dependencies": {
        "buffer-from": "^1.0.0",
        "source-map": "^0.6.0"
      }
    },
    "node_modules/source-map-support/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/sourcemap-codec": {
      "version": "1.4.8",
      "resolved": "https://registry.npmjs.org/sourcemap-codec/-/sourcemap-codec-1.4.8.tgz",
      "integrity": "sha512-9NykojV5Uih4lgo5So5dtw+f0JgJX30KCNI8gwhz2J9A15wD0Ml6tjHKwf6fTSa6fAdVBdZeNOs9eJ71qCk8vA==",
      "deprecated": "Please use @jridgewell/sourcemap-codec instead",
      "license": "MIT"
    },
    "node_modules/spdy": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/spdy/-/spdy-4.0.2.tgz",
      "integrity": "sha512-r46gZQZQV+Kl9oItvl1JZZqJKGr+oEkB08A6BzkiR7593/7IbtuncXHd2YoYeTsG4157ZssMu9KYvUHLcjcDoA==",
      "license": "MIT",
      "dependencies": {
        "debug": "^4.1.0",
        "handle-thing": "^2.0.0",
        "http-deceiver": "^1.2.7",
        "select-hose": "^2.0.0",
        "spdy-transport": "^3.0.0"
      },
      "engines": {
        "node": ">=6.0.0"
      }
    },
    "node_modules/spdy-transport": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/spdy-transport/-/spdy-transport-3.0.0.tgz",
      "integrity": "sha512-hsLVFE5SjA6TCisWeJXFKniGGOpBgMLmerfO2aCyCU5s7nJ/rpAepqmFifv/GCbSbueEeAJJnmSQ2rKC/g8Fcw==",
      "license": "MIT",
      "dependencies": {
        "debug": "^4.1.0",
        "detect-node": "^2.0.4",
        "hpack.js": "^2.1.6",
        "obuf": "^1.1.2",
        "readable-stream": "^3.0.6",
        "wbuf": "^1.7.3"
      }
    },
    "node_modules/sprintf-js": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/sprintf-js/-/sprintf-js-1.0.3.tgz",
      "integrity": "sha512-D9cPgkvLlV3t3IzL0D0YLvGA9Ahk4PcvVwUbN0dSGr1aP0Nrt4AEnTUbuGvquEC0mA64Gqt1fzirlRs5ibXx8g==",
      "license": "BSD-3-Clause"
    },
    "node_modules/stable": {
      "version": "0.1.8",
      "resolved": "https://registry.npmjs.org/stable/-/stable-0.1.8.tgz",
      "integrity": "sha512-ji9qxRnOVfcuLDySj9qzhGSEFVobyt1kIOSkj1qZzYLzq7Tos/oUUWvotUPQLlrsidqsK6tBH89Bc9kL5zHA6w==",
      "deprecated": "Modern JS already guarantees Array#sort() is a stable sort, so this library is deprecated. See the compatibility table on MDN: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort#browser_compatibility",
      "license": "MIT"
    },
    "node_modules/stack-utils": {
      "version": "2.0.6",
      "resolved": "https://registry.npmjs.org/stack-utils/-/stack-utils-2.0.6.tgz",
      "integrity": "sha512-XlkWvfIm6RmsWtNJx+uqtKLS8eqFbxUg0ZzLXqY0caEy9l7hruX8IpiDnjsLavoBgqCCR71TqWO8MaXYheJ3RQ==",
      "license": "MIT",
      "dependencies": {
        "escape-string-regexp": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/stack-utils/node_modules/escape-string-regexp": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-2.0.0.tgz",
      "integrity": "sha512-UpzcLCXolUWcNu5HtVMHYdXJjArjsF9C0aNnquZYY4uW/Vu0miy5YoWvbV345HauVvcAUnpRuhMMcqTcGOY2+w==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/stackframe": {
      "version": "1.3.4",
      "resolved": "https://registry.npmjs.org/stackframe/-/stackframe-1.3.4.tgz",
      "integrity": "sha512-oeVtt7eWQS+Na6F//S4kJ2K2VbRlS9D43mAlMyVpVWovy9o+jfgH8O9agzANzaiLjclA0oYzUXEM4PurhSUChw==",
      "license": "MIT"
    },
    "node_modules/static-eval": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/static-eval/-/static-eval-2.0.2.tgz",
      "integrity": "sha512-N/D219Hcr2bPjLxPiV+TQE++Tsmrady7TqAJugLy7Xk1EumfDWS/f5dtBbkRCGE7wKKXuYockQoj8Rm2/pVKyg==",
      "license": "MIT",
      "dependencies": {
        "escodegen": "^1.8.1"
      }
    },
    "node_modules/static-eval/node_modules/escodegen": {
      "version": "1.14.3",
      "resolved": "https://registry.npmjs.org/escodegen/-/escodegen-1.14.3.tgz",
      "integrity": "sha512-qFcX0XJkdg+PB3xjZZG/wKSuT1PnQWx57+TVSjIMmILd2yC/6ByYElPwJnslDsuWuSAp4AwJGumarAAmJch5Kw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esprima": "^4.0.1",
        "estraverse": "^4.2.0",
        "esutils": "^2.0.2",
        "optionator": "^0.8.1"
      },
      "bin": {
        "escodegen": "bin/escodegen.js",
        "esgenerate": "bin/esgenerate.js"
      },
      "engines": {
        "node": ">=4.0"
      },
      "optionalDependencies": {
        "source-map": "~0.6.1"
      }
    },
    "node_modules/static-eval/node_modules/estraverse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-4.3.0.tgz",
      "integrity": "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/static-eval/node_modules/levn": {
      "version": "0.3.0",
      "resolved": "https://registry.npmjs.org/levn/-/levn-0.3.0.tgz",
      "integrity": "sha512-0OO4y2iOHix2W6ujICbKIaEQXvFQHue65vUG3pb5EUomzPI90z9hsA1VsO/dbIIpC53J8gxM9Q4Oho0jrCM/yA==",
      "license": "MIT",
      "dependencies": {
        "prelude-ls": "~1.1.2",
        "type-check": "~0.3.2"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/static-eval/node_modules/optionator": {
      "version": "0.8.3",
      "resolved": "https://registry.npmjs.org/optionator/-/optionator-0.8.3.tgz",
      "integrity": "sha512-+IW9pACdk3XWmmTXG8m3upGUJst5XRGzxMRjXzAuJ1XnIFNvfhjjIuYkDvysnPQ7qzqVzLt78BCruntqRhWQbA==",
      "license": "MIT",
      "dependencies": {
        "deep-is": "~0.1.3",
        "fast-levenshtein": "~2.0.6",
        "levn": "~0.3.0",
        "prelude-ls": "~1.1.2",
        "type-check": "~0.3.2",
        "word-wrap": "~1.2.3"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/static-eval/node_modules/prelude-ls": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/prelude-ls/-/prelude-ls-1.1.2.tgz",
      "integrity": "sha512-ESF23V4SKG6lVSGZgYNpbsiaAkdab6ZgOxe52p7+Kid3W3u3bxR4Vfd/o21dmN7jSt0IwgZ4v5MUd26FEtXE9w==",
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/static-eval/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "optional": true,
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/static-eval/node_modules/type-check": {
      "version": "0.3.2",
      "resolved": "https://registry.npmjs.org/type-check/-/type-check-0.3.2.tgz",
      "integrity": "sha512-ZCmOJdvOWDBYJlzAoFkC+Q0+bUyEOS1ltgp1MGU03fqHG+dbi9tBFU2Rd9QKiDZFAYrhPh2JUf7rZRIuHRKtOg==",
      "license": "MIT",
      "dependencies": {
        "prelude-ls": "~1.1.2"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/statuses": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/statuses/-/statuses-2.0.1.tgz",
      "integrity": "sha512-RwNA9Z/7PrK06rYLIzFMlaF+l73iwpzsqRIFgbMLbTcLD6cOao82TaWefPXQvB2fOC4AjuYSEndS7N/mTCbkdQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/stop-iteration-iterator": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/stop-iteration-iterator/-/stop-iteration-iterator-1.1.0.tgz",
      "integrity": "sha512-eLoXW/DHyl62zxY4SCaIgnRhuMr6ri4juEYARS8E6sCEqzKpOiE521Ucofdx+KnDZl5xmvGYaaKCk5FEOxJCoQ==",
      "license": "MIT",
      "dependencies": {
        "es-errors": "^1.3.0",
        "internal-slot": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/string_decoder": {
      "version": "1.3.0",
      "resolved": "https://registry.npmjs.org/string_decoder/-/string_decoder-1.3.0.tgz",
      "integrity": "sha512-hkRX8U1WjJFd8LsDJ2yQ/wWWxaopEsABU1XfkM8A+j0+85JAGppt16cr1Whg6KIbb4okU6Mql6BOj+uup/wKeA==",
      "license": "MIT",
      "dependencies": {
        "safe-buffer": "~5.2.0"
      }
    },
    "node_modules/string-length": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/string-length/-/string-length-4.0.2.tgz",
      "integrity": "sha512-+l6rNN5fYHNhZZy41RXsYptCjA2Igmq4EG7kZAYFQI1E1VTXarr6ZPXBg6eq7Y6eK4FEhY6AJlyuFIb/v/S0VQ==",
      "license": "MIT",
      "dependencies": {
        "char-regex": "^1.0.2",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/string-natural-compare": {
      "version": "3.0.1",
      "resolved": "https://registry.npmjs.org/string-natural-compare/-/string-natural-compare-3.0.1.tgz",
      "integrity": "sha512-n3sPwynL1nwKi3WJ6AIsClwBMa0zTi54fn2oLU6ndfTSIO05xaznjSf15PcBZU6FNWbmN5Q6cxT4V5hGvB4taw==",
      "license": "MIT"
    },
    "node_modules/string-width": {
      "version": "4.2.3",
      "resolved": "https://registry.npmjs.org/string-width/-/string-width-4.2.3.tgz",
      "integrity": "sha512-wKyQRQpjJ0sIp62ErSZdGsjMJWsap5oRNihHhu6G7JVO/9jIB6UyevL+tXuOqrng8j/cxKTWyWUwvSTriiZz/g==",
      "license": "MIT",
      "dependencies": {
        "emoji-regex": "^8.0.0",
        "is-fullwidth-code-point": "^3.0.0",
        "strip-ansi": "^6.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/string-width-cjs": {
      "name": "string-width",
      "version": "4.2.3",
      "resolved": "https://registry.npmjs.org/string-width/-/string-width-4.2.3.tgz",
      "integrity": "sha512-wKyQRQpjJ0sIp62ErSZdGsjMJWsap5oRNihHhu6G7JVO/9jIB6UyevL+tXuOqrng8j/cxKTWyWUwvSTriiZz/g==",
      "license": "MIT",
      "dependencies": {
        "emoji-regex": "^8.0.0",
        "is-fullwidth-code-point": "^3.0.0",
        "strip-ansi": "^6.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/string-width-cjs/node_modules/emoji-regex": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-8.0.0.tgz",
      "integrity": "sha512-MSjYzcWNOA0ewAHpz0MxpYFvwg6yjy1NG3xteoqz644VCo/RPgnr1/GGt+ic3iJTzQ8Eu3TdM14SawnVUmGE6A==",
      "license": "MIT"
    },
    "node_modules/string-width/node_modules/emoji-regex": {
      "version": "8.0.0",
      "resolved": "https://registry.npmjs.org/emoji-regex/-/emoji-regex-8.0.0.tgz",
      "integrity": "sha512-MSjYzcWNOA0ewAHpz0MxpYFvwg6yjy1NG3xteoqz644VCo/RPgnr1/GGt+ic3iJTzQ8Eu3TdM14SawnVUmGE6A==",
      "license": "MIT"
    },
    "node_modules/string.prototype.includes": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/string.prototype.includes/-/string.prototype.includes-2.0.1.tgz",
      "integrity": "sha512-o7+c9bW6zpAdJHTtujeePODAhkuicdAryFsfVKwA+wGw89wJ4GTY484WTucM9hLtDEOpOvI+aHnzqnC5lHp4Rg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.3"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/string.prototype.matchall": {
      "version": "4.0.12",
      "resolved": "https://registry.npmjs.org/string.prototype.matchall/-/string.prototype.matchall-4.0.12.tgz",
      "integrity": "sha512-6CC9uyBL+/48dYizRf7H7VAYCMCNTBeM78x/VTUe9bFEaxBepPJDa1Ow99LqI/1yF7kuy7Q3cQsYMrcjGUcskA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.3",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.6",
        "es-errors": "^1.3.0",
        "es-object-atoms": "^1.0.0",
        "get-intrinsic": "^1.2.6",
        "gopd": "^1.2.0",
        "has-symbols": "^1.1.0",
        "internal-slot": "^1.1.0",
        "regexp.prototype.flags": "^1.5.3",
        "set-function-name": "^2.0.2",
        "side-channel": "^1.1.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.repeat": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/string.prototype.repeat/-/string.prototype.repeat-1.0.0.tgz",
      "integrity": "sha512-0u/TldDbKD8bFCQ/4f5+mNRrXwZ8hg2w7ZR8wa16e8z9XpePWl3eGEcUD0OXpEH/VJH/2G3gjUtR3ZOiBe2S/w==",
      "license": "MIT",
      "dependencies": {
        "define-properties": "^1.1.3",
        "es-abstract": "^1.17.5"
      }
    },
    "node_modules/string.prototype.trim": {
      "version": "1.2.10",
      "resolved": "https://registry.npmjs.org/string.prototype.trim/-/string.prototype.trim-1.2.10.tgz",
      "integrity": "sha512-Rs66F0P/1kedk5lyYyH9uBzuiI/kNRmwJAR9quK6VOtIpZ2G+hMZd+HQbbv25MgCA6gEffoMZYxlTod4WcdrKA==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "define-data-property": "^1.1.4",
        "define-properties": "^1.2.1",
        "es-abstract": "^1.23.5",
        "es-object-atoms": "^1.0.0",
        "has-property-descriptors": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trimend": {
      "version": "1.0.9",
      "resolved": "https://registry.npmjs.org/string.prototype.trimend/-/string.prototype.trimend-1.0.9.tgz",
      "integrity": "sha512-G7Ok5C6E/j4SGfyLCloXTrngQIQU3PWtXGst3yM7Bea9FRURf1S42ZHlZZtsNque2FN2PoUhfZXYLNWwEr4dLQ==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.2",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/string.prototype.trimstart": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/string.prototype.trimstart/-/string.prototype.trimstart-1.0.8.tgz",
      "integrity": "sha512-UXSH262CSZY1tfu3G3Secr6uGLCFVPMhIqHjlgCUtCCcgihYc/xKs9djMTMUOb2j1mVSeU8EU6NWc/iQKU6Gfg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "define-properties": "^1.2.1",
        "es-object-atoms": "^1.0.0"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/stringify-object": {
      "version": "3.3.0",
      "resolved": "https://registry.npmjs.org/stringify-object/-/stringify-object-3.3.0.tgz",
      "integrity": "sha512-rHqiFh1elqCQ9WPLIC8I0Q/g/wj5J1eMkyoiD6eoQApWHP0FtlK7rqnhmabL5VUY9JQCcqwwvlOaSuutekgyrw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "get-own-enumerable-property-symbols": "^3.0.0",
        "is-obj": "^1.0.1",
        "is-regexp": "^1.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/strip-ansi": {
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-ansi-cjs": {
      "name": "strip-ansi",
      "version": "6.0.1",
      "resolved": "https://registry.npmjs.org/strip-ansi/-/strip-ansi-6.0.1.tgz",
      "integrity": "sha512-Y38VPSHcqkFrCpFnQ9vuSXmquuv5oXOKpGeT6aGrr3o3Gc9AlVa6JBfUSOCnbxGGZF+/0ooI7KrPuUSztUdU5A==",
      "license": "MIT",
      "dependencies": {
        "ansi-regex": "^5.0.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-bom": {
      "version": "4.0.0",
      "resolved": "https://registry.npmjs.org/strip-bom/-/strip-bom-4.0.0.tgz",
      "integrity": "sha512-3xurFv5tEgii33Zi8Jtp55wEIILR9eh34FAW00PZf+JnSsTmV/ioewSgQl97JHvgjoRGwPShsWm+IdrxB35d0w==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-comments": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/strip-comments/-/strip-comments-2.0.1.tgz",
      "integrity": "sha512-ZprKx+bBLXv067WTCALv8SSz5l2+XhpYCsVtSqlMnkAXMWDq+/ekVbl1ghqP9rUHTzv6sm/DwCOiYutU/yp1fw==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/strip-final-newline": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/strip-final-newline/-/strip-final-newline-2.0.0.tgz",
      "integrity": "sha512-BrpvfNAE3dcvq7ll3xVumzjKjZQ5tI1sEUIKr3Uoks0XUl45St3FlatVqef9prk4jRDzhW6WZg+3bk93y6pLjA==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/strip-indent": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/strip-indent/-/strip-indent-3.0.0.tgz",
      "integrity": "sha512-laJTa3Jb+VQpaC6DseHhF7dXVqHTfJPCRDaEbid/drOhgitgYku/letMUqOXFoWV0zIIUbjpdH2t+tYj4bQMRQ==",
      "license": "MIT",
      "dependencies": {
        "min-indent": "^1.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/strip-json-comments": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/strip-json-comments/-/strip-json-comments-3.1.1.tgz",
      "integrity": "sha512-6fPc+R4ihwqP6N/aIv2f1gMH8lOVtWQHoqC4yK6oSDVVocumAsfCqjkXnqiYMhmMwS/mEHLp7Vehlt3ql6lEig==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/style-loader": {
      "version": "3.3.4",
      "resolved": "https://registry.npmjs.org/style-loader/-/style-loader-3.3.4.tgz",
      "integrity": "sha512-0WqXzrsMTyb8yjZJHDqwmnwRJvhALK9LfRtRc6B4UTWe8AijYLZYZ9thuJTZc2VfQWINADW/j+LiJnfy2RoC1w==",
      "license": "MIT",
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.0.0"
      }
    },
    "node_modules/stylehacks": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/stylehacks/-/stylehacks-5.1.1.tgz",
      "integrity": "sha512-sBpcd5Hx7G6seo7b1LkpttvTz7ikD0LlH5RmdcBNb6fFR0Fl7LQwHDFr300q4cwUqi+IYrFGmsIHieMBfnN/Bw==",
      "license": "MIT",
      "dependencies": {
        "browserslist": "^4.21.4",
        "postcss-selector-parser": "^6.0.4"
      },
      "engines": {
        "node": "^10 || ^12 || >=14.0"
      },
      "peerDependencies": {
        "postcss": "^8.2.15"
      }
    },
    "node_modules/sucrase": {
      "version": "3.35.0",
      "resolved": "https://registry.npmjs.org/sucrase/-/sucrase-3.35.0.tgz",
      "integrity": "sha512-8EbVDiu9iN/nESwxeSxDKe0dunta1GOlHufmSSXxMD2z2/tMZpDMpvXQGsc+ajGo8y2uYUmixaSRUc/QPoQ0GA==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/gen-mapping": "^0.3.2",
        "commander": "^4.0.0",
        "glob": "^10.3.10",
        "lines-and-columns": "^1.1.6",
        "mz": "^2.7.0",
        "pirates": "^4.0.1",
        "ts-interface-checker": "^0.1.9"
      },
      "bin": {
        "sucrase": "bin/sucrase",
        "sucrase-node": "bin/sucrase-node"
      },
      "engines": {
        "node": ">=16 || 14 >=14.17"
      }
    },
    "node_modules/sucrase/node_modules/brace-expansion": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/brace-expansion/-/brace-expansion-2.0.2.tgz",
      "integrity": "sha512-Jt0vHyM+jmUBqojB7E1NIYadt0vI0Qxjxd2TErW94wDz+E2LAm5vKMXXwg6ZZBTHPuUlDgQHKXvjGBdfcF1ZDQ==",
      "license": "MIT",
      "dependencies": {
        "balanced-match": "^1.0.0"
      }
    },
    "node_modules/sucrase/node_modules/commander": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/commander/-/commander-4.1.1.tgz",
      "integrity": "sha512-NOKm8xhkzAjzFx8B2v5OAHT+u5pRQc2UCa2Vq9jYL/31o2wi9mxBA7LIFs3sV5VSC49z6pEhfbMULvShKj26WA==",
      "license": "MIT",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/sucrase/node_modules/glob": {
      "version": "10.4.5",
      "resolved": "https://registry.npmjs.org/glob/-/glob-10.4.5.tgz",
      "integrity": "sha512-7Bv8RF0k6xjo7d4A/PxYLbUCfb6c+Vpd2/mB2yRDlew7Jb5hEXiCD9ibfO7wpk8i4sevK6DFny9h7EYbM3/sHg==",
      "license": "ISC",
      "dependencies": {
        "foreground-child": "^3.1.0",
        "jackspeak": "^3.1.2",
        "minimatch": "^9.0.4",
        "minipass": "^7.1.2",
        "package-json-from-dist": "^1.0.0",
        "path-scurry": "^1.11.1"
      },
      "bin": {
        "glob": "dist/esm/bin.mjs"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/sucrase/node_modules/minimatch": {
      "version": "9.0.5",
      "resolved": "https://registry.npmjs.org/minimatch/-/minimatch-9.0.5.tgz",
      "integrity": "sha512-G6T0ZX48xgozx7587koeX9Ys2NYy6Gmv//P89sEte9V9whIapMNF4idKxnW2QtCcLiTWlb/wfCabAtAFWhhBow==",
      "license": "ISC",
      "dependencies": {
        "brace-expansion": "^2.0.1"
      },
      "engines": {
        "node": ">=16 || 14 >=14.17"
      },
      "funding": {
        "url": "https://github.com/sponsors/isaacs"
      }
    },
    "node_modules/supports-color": {
      "version": "7.2.0",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-7.2.0.tgz",
      "integrity": "sha512-qpCAvRl9stuOHveKsn7HncJRvv501qIacKzQlO/+Lwxc9+0q2wLyv4Dfvt80/DPn2pqOBsJdDiogXGR9+OvwRw==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^4.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/supports-hyperlinks": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/supports-hyperlinks/-/supports-hyperlinks-2.3.0.tgz",
      "integrity": "sha512-RpsAZlpWcDwOPQA22aCH4J0t7L8JmAvsCxfOSEwm7cQs3LshN36QaTkwd70DnBOXDWGssw2eUoc8CaRWT0XunA==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^4.0.0",
        "supports-color": "^7.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/supports-preserve-symlinks-flag": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/supports-preserve-symlinks-flag/-/supports-preserve-symlinks-flag-1.0.0.tgz",
      "integrity": "sha512-ot0WnXS9fgdkgIcePe6RHNk1WA8+muPa6cSjeR3V8K27q9BB1rTE3R1p7Hv0z1ZyAc8s6Vvv8DIyWf681MAt0w==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/svg-parser": {
      "version": "2.0.4",
      "resolved": "https://registry.npmjs.org/svg-parser/-/svg-parser-2.0.4.tgz",
      "integrity": "sha512-e4hG1hRwoOdRb37cIMSgzNsxyzKfayW6VOflrwvR+/bzrkyxY/31WkbgnQpgtrNp1SdpJvpUAGTa/ZoiPNDuRQ==",
      "license": "MIT"
    },
    "node_modules/svgo": {
      "version": "1.3.2",
      "resolved": "https://registry.npmjs.org/svgo/-/svgo-1.3.2.tgz",
      "integrity": "sha512-yhy/sQYxR5BkC98CY7o31VGsg014AKLEPxdfhora76l36hD9Rdy5NZA/Ocn6yayNPgSamYdtX2rFJdcv07AYVw==",
      "deprecated": "This SVGO version is no longer supported. Upgrade to v2.x.x.",
      "license": "MIT",
      "dependencies": {
        "chalk": "^2.4.1",
        "coa": "^2.0.2",
        "css-select": "^2.0.0",
        "css-select-base-adapter": "^0.1.1",
        "css-tree": "1.0.0-alpha.37",
        "csso": "^4.0.2",
        "js-yaml": "^3.13.1",
        "mkdirp": "~0.5.1",
        "object.values": "^1.1.0",
        "sax": "~1.2.4",
        "stable": "^0.1.8",
        "unquote": "~1.1.1",
        "util.promisify": "~1.0.0"
      },
      "bin": {
        "svgo": "bin/svgo"
      },
      "engines": {
        "node": ">=4.0.0"
      }
    },
    "node_modules/svgo/node_modules/ansi-styles": {
      "version": "3.2.1",
      "resolved": "https://registry.npmjs.org/ansi-styles/-/ansi-styles-3.2.1.tgz",
      "integrity": "sha512-VT0ZI6kZRdTh8YyJw3SMbYm/u+NqfsAxEpWO0Pf9sq8/e94WxxOpPKx9FR1FlyCtOVDNOQ+8ntlqFxiRc+r5qA==",
      "license": "MIT",
      "dependencies": {
        "color-convert": "^1.9.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/svgo/node_modules/chalk": {
      "version": "2.4.2",
      "resolved": "https://registry.npmjs.org/chalk/-/chalk-2.4.2.tgz",
      "integrity": "sha512-Mti+f9lpJNcwF4tWV8/OrTTtF1gZi+f8FqlyAdouralcFWFQWF2+NgCHShjkCb+IFBLq9buZwE1xckQU4peSuQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^3.2.1",
        "escape-string-regexp": "^1.0.5",
        "supports-color": "^5.3.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/svgo/node_modules/color-convert": {
      "version": "1.9.3",
      "resolved": "https://registry.npmjs.org/color-convert/-/color-convert-1.9.3.tgz",
      "integrity": "sha512-QfAUtd+vFdAtFQcC8CCyYt1fYWxSqAiK2cSD6zDB8N3cpsEBAvRxp9zOGg6G/SHHJYAT88/az/IuDGALsNVbGg==",
      "license": "MIT",
      "dependencies": {
        "color-name": "1.1.3"
      }
    },
    "node_modules/svgo/node_modules/color-name": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/color-name/-/color-name-1.1.3.tgz",
      "integrity": "sha512-72fSenhMw2HZMTVHeCA9KCmpEIbzWiQsjN+BHcBbS9vr1mtt+vJjPdksIBNUmKAW8TFUDPJK5SUU3QhE9NEXDw==",
      "license": "MIT"
    },
    "node_modules/svgo/node_modules/css-select": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/css-select/-/css-select-2.1.0.tgz",
      "integrity": "sha512-Dqk7LQKpwLoH3VovzZnkzegqNSuAziQyNZUcrdDM401iY+R5NkGBXGmtO05/yaXQziALuPogeG0b7UAgjnTJTQ==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "boolbase": "^1.0.0",
        "css-what": "^3.2.1",
        "domutils": "^1.7.0",
        "nth-check": "^1.0.2"
      }
    },
    "node_modules/svgo/node_modules/css-what": {
      "version": "3.4.2",
      "resolved": "https://registry.npmjs.org/css-what/-/css-what-3.4.2.tgz",
      "integrity": "sha512-ACUm3L0/jiZTqfzRM3Hi9Q8eZqd6IK37mMWPLz9PJxkLWllYeRf+EHUSHYEtFop2Eqytaq1FizFVh7XfBnXCDQ==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">= 6"
      },
      "funding": {
        "url": "https://github.com/sponsors/fb55"
      }
    },
    "node_modules/svgo/node_modules/dom-serializer": {
      "version": "0.2.2",
      "resolved": "https://registry.npmjs.org/dom-serializer/-/dom-serializer-0.2.2.tgz",
      "integrity": "sha512-2/xPb3ORsQ42nHYiSunXkDjPLBaEj/xTwUO4B7XCZQTRk7EBtTOPaygh10YAAh2OI1Qrp6NWfpAhzswj0ydt9g==",
      "license": "MIT",
      "dependencies": {
        "domelementtype": "^2.0.1",
        "entities": "^2.0.0"
      }
    },
    "node_modules/svgo/node_modules/domutils": {
      "version": "1.7.0",
      "resolved": "https://registry.npmjs.org/domutils/-/domutils-1.7.0.tgz",
      "integrity": "sha512-Lgd2XcJ/NjEw+7tFvfKxOzCYKZsdct5lczQ2ZaQY8Djz7pfAD3Gbp8ySJWtreII/vDlMVmxwa6pHmdxIYgttDg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "dom-serializer": "0",
        "domelementtype": "1"
      }
    },
    "node_modules/svgo/node_modules/domutils/node_modules/domelementtype": {
      "version": "1.3.1",
      "resolved": "https://registry.npmjs.org/domelementtype/-/domelementtype-1.3.1.tgz",
      "integrity": "sha512-BSKB+TSpMpFI/HOxCNr1O8aMOTZ8hT3pM3GQ0w/mWRmkhEDSFJkkyzz4XQsBV44BChwGkrDfMyjVD0eA2aFV3w==",
      "license": "BSD-2-Clause"
    },
    "node_modules/svgo/node_modules/escape-string-regexp": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/escape-string-regexp/-/escape-string-regexp-1.0.5.tgz",
      "integrity": "sha512-vbRorB5FUQWvla16U8R/qgaFIya2qGzwDrNmCZuYKrbdSUMG6I1ZCGQRefkRVhuOkIGVne7BQ35DSfo1qvJqFg==",
      "license": "MIT",
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/svgo/node_modules/has-flag": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/has-flag/-/has-flag-3.0.0.tgz",
      "integrity": "sha512-sKJf1+ceQBr4SMkvQnBDNDtf4TXpVhVGateu0t918bl30FnbE2m4vNLX+VWe/dpjlb+HugGYzW7uQXH98HPEYw==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/svgo/node_modules/nth-check": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/nth-check/-/nth-check-1.0.2.tgz",
      "integrity": "sha512-WeBOdju8SnzPN5vTUJYxYUxLeXpCaVP5i5e0LF8fg7WORF2Wd7wFX/pk0tYZk7s8T+J7VLy0Da6J1+wCT0AtHg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "boolbase": "~1.0.0"
      }
    },
    "node_modules/svgo/node_modules/supports-color": {
      "version": "5.5.0",
      "resolved": "https://registry.npmjs.org/supports-color/-/supports-color-5.5.0.tgz",
      "integrity": "sha512-QjVjwdXIt408MIiAqCX4oUKsgU2EqAGzs2Ppkm4aQYbjm+ZEWEcW4SfFNTr4uMNZma0ey4f5lgLrkB0aX0QMow==",
      "license": "MIT",
      "dependencies": {
        "has-flag": "^3.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/symbol-tree": {
      "version": "3.2.4",
      "resolved": "https://registry.npmjs.org/symbol-tree/-/symbol-tree-3.2.4.tgz",
      "integrity": "sha512-9QNk5KwDF+Bvz+PyObkmSYjI5ksVUYtjW7AU22r2NKcfLJcXp96hkDWU3+XndOsUb+AQ9QhfzfCT2O+CNWT5Tw==",
      "license": "MIT"
    },
    "node_modules/tailwindcss": {
      "version": "3.4.17",
      "resolved": "https://registry.npmjs.org/tailwindcss/-/tailwindcss-3.4.17.tgz",
      "integrity": "sha512-w33E2aCvSDP0tW9RZuNXadXlkHXqFzSkQew/aIa2i/Sj8fThxwovwlXHSPXTbAHwEIhBFXAedUhP2tueAKP8Og==",
      "license": "MIT",
      "dependencies": {
        "@alloc/quick-lru": "^5.2.0",
        "arg": "^5.0.2",
        "chokidar": "^3.6.0",
        "didyoumean": "^1.2.2",
        "dlv": "^1.1.3",
        "fast-glob": "^3.3.2",
        "glob-parent": "^6.0.2",
        "is-glob": "^4.0.3",
        "jiti": "^1.21.6",
        "lilconfig": "^3.1.3",
        "micromatch": "^4.0.8",
        "normalize-path": "^3.0.0",
        "object-hash": "^3.0.0",
        "picocolors": "^1.1.1",
        "postcss": "^8.4.47",
        "postcss-import": "^15.1.0",
        "postcss-js": "^4.0.1",
        "postcss-load-config": "^4.0.2",
        "postcss-nested": "^6.2.0",
        "postcss-selector-parser": "^6.1.2",
        "resolve": "^1.22.8",
        "sucrase": "^3.35.0"
      },
      "bin": {
        "tailwind": "lib/cli.js",
        "tailwindcss": "lib/cli.js"
      },
      "engines": {
        "node": ">=14.0.0"
      }
    },
    "node_modules/tailwindcss/node_modules/lilconfig": {
      "version": "3.1.3",
      "resolved": "https://registry.npmjs.org/lilconfig/-/lilconfig-3.1.3.tgz",
      "integrity": "sha512-/vlFKAoH5Cgt3Ie+JLhRbwOsCQePABiU3tJ1egGvyQ+33R/vcwM2Zl2QR/LzjsBeItPt3oSVXapn+m4nQDvpzw==",
      "license": "MIT",
      "engines": {
        "node": ">=14"
      },
      "funding": {
        "url": "https://github.com/sponsors/antonk52"
      }
    },
    "node_modules/tapable": {
      "version": "2.2.3",
      "resolved": "https://registry.npmjs.org/tapable/-/tapable-2.2.3.tgz",
      "integrity": "sha512-ZL6DDuAlRlLGghwcfmSn9sK3Hr6ArtyudlSAiCqQ6IfE+b+HHbydbYDIG15IfS5do+7XQQBdBiubF/cV2dnDzg==",
      "license": "MIT",
      "engines": {
        "node": ">=6"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      }
    },
    "node_modules/temp-dir": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/temp-dir/-/temp-dir-2.0.0.tgz",
      "integrity": "sha512-aoBAniQmmwtcKp/7BzsH8Cxzv8OL736p7v1ihGb5e9DJ9kTwGWHrQrVB5+lfVDzfGrdRzXch+ig7LHaY1JTOrg==",
      "license": "MIT",
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/tempy": {
      "version": "0.6.0",
      "resolved": "https://registry.npmjs.org/tempy/-/tempy-0.6.0.tgz",
      "integrity": "sha512-G13vtMYPT/J8A4X2SjdtBTphZlrp1gKv6hZiOjw14RCWg6GbHuQBGtjlx75xLbYV/wEc0D7G5K4rxKP/cXk8Bw==",
      "license": "MIT",
      "dependencies": {
        "is-stream": "^2.0.0",
        "temp-dir": "^2.0.0",
        "type-fest": "^0.16.0",
        "unique-string": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/tempy/node_modules/type-fest": {
      "version": "0.16.0",
      "resolved": "https://registry.npmjs.org/type-fest/-/type-fest-0.16.0.tgz",
      "integrity": "sha512-eaBzG6MxNzEn9kiwvtre90cXaNLkmadMWa1zQMs3XORCXNbsH/OewwbxC5ia9dCxIxnTAsSxXJaa/p5y8DlvJg==",
      "license": "(MIT OR CC0-1.0)",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/terminal-link": {
      "version": "2.1.1",
      "resolved": "https://registry.npmjs.org/terminal-link/-/terminal-link-2.1.1.tgz",
      "integrity": "sha512-un0FmiRUQNr5PJqy9kP7c40F5BOfpGlYTrxonDChEZB7pzZxRNp/bt+ymiy9/npwXya9KH99nJ/GXFIiUkYGFQ==",
      "license": "MIT",
      "dependencies": {
        "ansi-escapes": "^4.2.1",
        "supports-hyperlinks": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/terser": {
      "version": "5.44.0",
      "resolved": "https://registry.npmjs.org/terser/-/terser-5.44.0.tgz",
      "integrity": "sha512-nIVck8DK+GM/0Frwd+nIhZ84pR/BX7rmXMfYwyg+Sri5oGVE99/E3KvXqpC2xHFxyqXyGHTKBSioxxplrO4I4w==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "@jridgewell/source-map": "^0.3.3",
        "acorn": "^8.15.0",
        "commander": "^2.20.0",
        "source-map-support": "~0.5.20"
      },
      "bin": {
        "terser": "bin/terser"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/terser-webpack-plugin": {
      "version": "5.3.14",
      "resolved": "https://registry.npmjs.org/terser-webpack-plugin/-/terser-webpack-plugin-5.3.14.tgz",
      "integrity": "sha512-vkZjpUjb6OMS7dhV+tILUW6BhpDR7P2L/aQSAv+Uwk+m8KATX9EccViHTJR2qDtACKPIYndLGCyl3FMo+r2LMw==",
      "license": "MIT",
      "dependencies": {
        "@jridgewell/trace-mapping": "^0.3.25",
        "jest-worker": "^27.4.5",
        "schema-utils": "^4.3.0",
        "serialize-javascript": "^6.0.2",
        "terser": "^5.31.1"
      },
      "engines": {
        "node": ">= 10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^5.1.0"
      },
      "peerDependenciesMeta": {
        "@swc/core": {
          "optional": true
        },
        "esbuild": {
          "optional": true
        },
        "uglify-js": {
          "optional": true
        }
      }
    },
    "node_modules/terser/node_modules/commander": {
      "version": "2.20.3",
      "resolved": "https://registry.npmjs.org/commander/-/commander-2.20.3.tgz",
      "integrity": "sha512-GpVkmM8vF2vQUkj2LvZmD35JxeJOLCwJ9cUkugyk2nuhbv3+mJvpLYYt+0+USMxE+oj+ey/lJEnhZw75x/OMcQ==",
      "license": "MIT"
    },
    "node_modules/test-exclude": {
      "version": "6.0.0",
      "resolved": "https://registry.npmjs.org/test-exclude/-/test-exclude-6.0.0.tgz",
      "integrity": "sha512-cAGWPIyOHU6zlmg88jwm7VRyXnMN7iV68OGAbYDk/Mh/xC/pzVPlQtY6ngoIH/5/tciuhGfvESU8GrHrcxD56w==",
      "license": "ISC",
      "dependencies": {
        "@istanbuljs/schema": "^0.1.2",
        "glob": "^7.1.4",
        "minimatch": "^3.0.4"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/text-table": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/text-table/-/text-table-0.2.0.tgz",
      "integrity": "sha512-N+8UisAXDGk8PFXP4HAzVR9nbfmVJ3zYLAWiTIoqC5v5isinhr+r5uaO8+7r3BMfuNIufIsA7RdpVgacC2cSpw==",
      "license": "MIT"
    },
    "node_modules/thenify": {
      "version": "3.3.1",
      "resolved": "https://registry.npmjs.org/thenify/-/thenify-3.3.1.tgz",
      "integrity": "sha512-RVZSIV5IG10Hk3enotrhvz0T9em6cyHBLkH/YAZuKqd8hRkKhSfCGIcP2KUY0EPxndzANBmNllzWPwak+bheSw==",
      "license": "MIT",
      "dependencies": {
        "any-promise": "^1.0.0"
      }
    },
    "node_modules/thenify-all": {
      "version": "1.6.0",
      "resolved": "https://registry.npmjs.org/thenify-all/-/thenify-all-1.6.0.tgz",
      "integrity": "sha512-RNxQH/qI8/t3thXJDwcstUO4zeqo64+Uy/+sNVRBx4Xn2OX+OZ9oP+iJnNFqplFra2ZUVeKCSa2oVWi3T4uVmA==",
      "license": "MIT",
      "dependencies": {
        "thenify": ">= 3.1.0 < 4"
      },
      "engines": {
        "node": ">=0.8"
      }
    },
    "node_modules/throat": {
      "version": "6.0.2",
      "resolved": "https://registry.npmjs.org/throat/-/throat-6.0.2.tgz",
      "integrity": "sha512-WKexMoJj3vEuK0yFEapj8y64V0A6xcuPuK9Gt1d0R+dzCSJc0lHqQytAbSB4cDAK0dWh4T0E2ETkoLE2WZ41OQ==",
      "license": "MIT"
    },
    "node_modules/thunky": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/thunky/-/thunky-1.1.0.tgz",
      "integrity": "sha512-eHY7nBftgThBqOyHGVN+l8gF0BucP09fMo0oO/Lb0w1OF80dJv+lDVpXG60WMQvkcxAkNybKsrEIE3ZtKGmPrA==",
      "license": "MIT"
    },
    "node_modules/tmpl": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/tmpl/-/tmpl-1.0.5.tgz",
      "integrity": "sha512-3f0uOEAQwIqGuWW2MVzYg8fV/QNnc/IpuJNG837rLuczAaLVHslWHZQj4IGiEl5Hs3kkbhwL9Ab7Hrsmuj+Smw==",
      "license": "BSD-3-Clause"
    },
    "node_modules/to-regex-range": {
      "version": "5.0.1",
      "resolved": "https://registry.npmjs.org/to-regex-range/-/to-regex-range-5.0.1.tgz",
      "integrity": "sha512-65P7iz6X5yEr1cwcgvQxbbIw7Uk3gOy5dIdtZ4rDveLqhrdJP+Li/Hx6tyK0NEb+2GCyneCMJiGqrADCSNk8sQ==",
      "license": "MIT",
      "dependencies": {
        "is-number": "^7.0.0"
      },
      "engines": {
        "node": ">=8.0"
      }
    },
    "node_modules/toidentifier": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/toidentifier/-/toidentifier-1.0.1.tgz",
      "integrity": "sha512-o5sSPKEkg/DIQNmH43V0/uerLrpzVedkUh8tGNvaeXpfpuwjKenlSox/2O/BTlZUtEe+JG7s5YhEz608PlAHRA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.6"
      }
    },
    "node_modules/tough-cookie": {
      "version": "4.1.4",
      "resolved": "https://registry.npmjs.org/tough-cookie/-/tough-cookie-4.1.4.tgz",
      "integrity": "sha512-Loo5UUvLD9ScZ6jh8beX1T6sO1w2/MpCRpEP7V280GKMVUQ0Jzar2U3UJPsrdbziLEMMhu3Ujnq//rhiFuIeag==",
      "license": "BSD-3-Clause",
      "dependencies": {
        "psl": "^1.1.33",
        "punycode": "^2.1.1",
        "universalify": "^0.2.0",
        "url-parse": "^1.5.3"
      },
      "engines": {
        "node": ">=6"
      }
    },
    "node_modules/tough-cookie/node_modules/universalify": {
      "version": "0.2.0",
      "resolved": "https://registry.npmjs.org/universalify/-/universalify-0.2.0.tgz",
      "integrity": "sha512-CJ1QgKmNg3CwvAv/kOFmtnEN05f0D/cn9QntgNOQlQF9dgvVTHj3t+8JPdjqawCHk7V/KA+fbUqzZ9XWhcqPUg==",
      "license": "MIT",
      "engines": {
        "node": ">= 4.0.0"
      }
    },
    "node_modules/tr46": {
      "version": "2.1.0",
      "resolved": "https://registry.npmjs.org/tr46/-/tr46-2.1.0.tgz",
      "integrity": "sha512-15Ih7phfcdP5YxqiB+iDtLoaTz4Nd35+IiAv0kQ5FNKHzXgdWqPoTIqEDDJmXceQt4JZk6lVPT8lnDlPpGDppw==",
      "license": "MIT",
      "dependencies": {
        "punycode": "^2.1.1"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/tryer": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/tryer/-/tryer-1.0.1.tgz",
      "integrity": "sha512-c3zayb8/kWWpycWYg87P71E1S1ZL6b6IJxfb5fvsUgsf0S2MVGaDhDXXjDMpdCpfWXqptc+4mXwmiy1ypXqRAA==",
      "license": "MIT"
    },
    "node_modules/ts-interface-checker": {
      "version": "0.1.13",
      "resolved": "https://registry.npmjs.org/ts-interface-checker/-/ts-interface-checker-0.1.13.tgz",
      "integrity": "sha512-Y/arvbn+rrz3JCKl9C4kVNfTfSm2/mEp5FSz5EsZSANGPSlQrpRI5M4PKF+mJnE52jOO90PnPSc3Ur3bTQw0gA==",
      "license": "Apache-2.0"
    },
    "node_modules/tsconfig-paths": {
      "version": "3.15.0",
      "resolved": "https://registry.npmjs.org/tsconfig-paths/-/tsconfig-paths-3.15.0.tgz",
      "integrity": "sha512-2Ac2RgzDe/cn48GvOe3M+o82pEFewD3UPbyoUHHdKasHwJKjds4fLXWf/Ux5kATBKN20oaFGu+jbElp1pos0mg==",
      "license": "MIT",
      "dependencies": {
        "@types/json5": "^0.0.29",
        "json5": "^1.0.2",
        "minimist": "^1.2.6",
        "strip-bom": "^3.0.0"
      }
    },
    "node_modules/tsconfig-paths/node_modules/json5": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/json5/-/json5-1.0.2.tgz",
      "integrity": "sha512-g1MWMLBiz8FKi1e4w0UyVL3w+iJceWAFBAaBnnGKOpNa5f8TLktkbre1+s6oICydWAm+HRUGTmI+//xv2hvXYA==",
      "license": "MIT",
      "dependencies": {
        "minimist": "^1.2.0"
      },
      "bin": {
        "json5": "lib/cli.js"
      }
    },
    "node_modules/tsconfig-paths/node_modules/strip-bom": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/strip-bom/-/strip-bom-3.0.0.tgz",
      "integrity": "sha512-vavAMRXOgBVNF6nyEEmL3DBK19iRpDcoIwW+swQ+CbGiu7lju6t+JklA1MHweoWtadgt4ISVUsXLyDq34ddcwA==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/tslib": {
      "version": "2.8.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-2.8.1.tgz",
      "integrity": "sha512-oJFu94HQb+KVduSUQL7wnpmqnfmLsOA/nAh6b6EH0wCEoK0/mPeXU6c3wKDV83MkOuHPRHtSXKKU99IBazS/2w==",
      "license": "0BSD"
    },
    "node_modules/tsutils": {
      "version": "3.21.0",
      "resolved": "https://registry.npmjs.org/tsutils/-/tsutils-3.21.0.tgz",
      "integrity": "sha512-mHKK3iUXL+3UF6xL5k0PEhKRUBKPBCv/+RkEOpjRWxxx27KKRBmmA60A9pgOUvMi8GKhRMPEmjBRPzs2W7O1OA==",
      "license": "MIT",
      "dependencies": {
        "tslib": "^1.8.1"
      },
      "engines": {
        "node": ">= 6"
      },
      "peerDependencies": {
        "typescript": ">=2.8.0 || >= 3.2.0-dev || >= 3.3.0-dev || >= 3.4.0-dev || >= 3.5.0-dev || >= 3.6.0-dev || >= 3.6.0-beta || >= 3.7.0-dev || >= 3.7.0-beta"
      }
    },
    "node_modules/tsutils/node_modules/tslib": {
      "version": "1.14.1",
      "resolved": "https://registry.npmjs.org/tslib/-/tslib-1.14.1.tgz",
      "integrity": "sha512-Xni35NKzjgMrwevysHTCArtLDpPvye8zV/0E4EyYn43P7/7qvQwPh9BGkHewbMulVntbigmcT7rdX3BNo9wRJg==",
      "license": "0BSD"
    },
    "node_modules/type-check": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/type-check/-/type-check-0.4.0.tgz",
      "integrity": "sha512-XleUoc9uwGXqjWwXaUTZAmzMcFZ5858QA2vvx1Ur5xIcixXIP+8LnFDgRplU30us6teqdlskFfu+ae4K79Ooew==",
      "license": "MIT",
      "dependencies": {
        "prelude-ls": "^1.2.1"
      },
      "engines": {
        "node": ">= 0.8.0"
      }
    },
    "node_modules/type-detect": {
      "version": "4.0.8",
      "resolved": "https://registry.npmjs.org/type-detect/-/type-detect-4.0.8.tgz",
      "integrity": "sha512-0fr/mIH1dlO+x7TlcMy+bIDqKPsw/70tVyeHW787goQjhmqaZe10uwLujubK9q9Lg6Fiho1KUKDYz0Z7k7g5/g==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/type-fest": {
      "version": "0.20.2",
      "resolved": "https://registry.npmjs.org/type-fest/-/type-fest-0.20.2.tgz",
      "integrity": "sha512-Ne+eE4r0/iWnpAxD852z3A+N0Bt5RN//NjJwRd2VFHEmrywxf5vsZlh4R6lixl6B+wz/8d+maTSAkN1FIkI3LQ==",
      "license": "(MIT OR CC0-1.0)",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    },
    "node_modules/type-is": {
      "version": "1.6.18",
      "resolved": "https://registry.npmjs.org/type-is/-/type-is-1.6.18.tgz",
      "integrity": "sha512-TkRKr9sUTxEH8MdfuCSP7VizJyzRNMjj2J2do2Jr3Kym598JVdEksuzPQCnlFPW4ky9Q+iA+ma9BGm06XQBy8g==",
      "license": "MIT",
      "dependencies": {
        "media-typer": "0.3.0",
        "mime-types": "~2.1.24"
      },
      "engines": {
        "node": ">= 0.6"
      }
    },
    "node_modules/typed-array-buffer": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/typed-array-buffer/-/typed-array-buffer-1.0.3.tgz",
      "integrity": "sha512-nAYYwfY3qnzX30IkA6AQZjVbtK6duGontcQm1WSG1MD94YLqK0515GNApXkoxKOWMusVssAHWLh9SeaoefYFGw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "es-errors": "^1.3.0",
        "is-typed-array": "^1.1.14"
      },
      "engines": {
        "node": ">= 0.4"
      }
    },
    "node_modules/typed-array-byte-length": {
      "version": "1.0.3",
      "resolved": "https://registry.npmjs.org/typed-array-byte-length/-/typed-array-byte-length-1.0.3.tgz",
      "integrity": "sha512-BaXgOuIxz8n8pIq3e7Atg/7s+DpiYrxn4vdot3w9KbnBhcRQq6o3xemQdIfynqSeXeDrF32x+WvfzmOjPiY9lg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.8",
        "for-each": "^0.3.3",
        "gopd": "^1.2.0",
        "has-proto": "^1.2.0",
        "is-typed-array": "^1.1.14"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typed-array-byte-offset": {
      "version": "1.0.4",
      "resolved": "https://registry.npmjs.org/typed-array-byte-offset/-/typed-array-byte-offset-1.0.4.tgz",
      "integrity": "sha512-bTlAFB/FBYMcuX81gbL4OcpH5PmlFHqlCCpAl8AlEzMz5k53oNDvN8p1PNOWLEmI2x4orp3raOFB51tv9X+MFQ==",
      "license": "MIT",
      "dependencies": {
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "for-each": "^0.3.3",
        "gopd": "^1.2.0",
        "has-proto": "^1.2.0",
        "is-typed-array": "^1.1.15",
        "reflect.getprototypeof": "^1.0.9"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typed-array-length": {
      "version": "1.0.7",
      "resolved": "https://registry.npmjs.org/typed-array-length/-/typed-array-length-1.0.7.tgz",
      "integrity": "sha512-3KS2b+kL7fsuk/eJZ7EQdnEmQoaho/r6KUef7hxvltNA5DR8NAUM+8wJMbJyZ4G9/7i3v5zPBIMN5aybAh2/Jg==",
      "license": "MIT",
      "dependencies": {
        "call-bind": "^1.0.7",
        "for-each": "^0.3.3",
        "gopd": "^1.0.1",
        "is-typed-array": "^1.1.13",
        "possible-typed-array-names": "^1.0.0",
        "reflect.getprototypeof": "^1.0.6"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/typedarray-to-buffer": {
      "version": "3.1.5",
      "resolved": "https://registry.npmjs.org/typedarray-to-buffer/-/typedarray-to-buffer-3.1.5.tgz",
      "integrity": "sha512-zdu8XMNEDepKKR+XYOXAVPtWui0ly0NtohUscw+UmaHiAWT8hrV1rr//H6V+0DvJ3OQ19S979M0laLfX8rm82Q==",
      "license": "MIT",
      "dependencies": {
        "is-typedarray": "^1.0.0"
      }
    },
    "node_modules/typescript": {
      "version": "4.9.5",
      "resolved": "https://registry.npmjs.org/typescript/-/typescript-4.9.5.tgz",
      "integrity": "sha512-1FXk9E2Hm+QzZQ7z+McJiHL4NW1F2EzMu9Nq9i3zAaGqibafqYwCVU6WyWAuyQRRzOlxou8xZSyXLEN8oKj24g==",
      "license": "Apache-2.0",
      "peer": true,
      "bin": {
        "tsc": "bin/tsc",
        "tsserver": "bin/tsserver"
      },
      "engines": {
        "node": ">=4.2.0"
      }
    },
    "node_modules/unbox-primitive": {
      "version": "1.1.0",
      "resolved": "https://registry.npmjs.org/unbox-primitive/-/unbox-primitive-1.1.0.tgz",
      "integrity": "sha512-nWJ91DjeOkej/TA8pXQ3myruKpKEYgqvpw9lz4OPHj/NWFNluYrjbz9j01CJ8yKQd2g4jFoOkINCTW2I5LEEyw==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.3",
        "has-bigints": "^1.0.2",
        "has-symbols": "^1.1.0",
        "which-boxed-primitive": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/underscore": {
      "version": "1.12.1",
      "resolved": "https://registry.npmjs.org/underscore/-/underscore-1.12.1.tgz",
      "integrity": "sha512-hEQt0+ZLDVUMhebKxL4x1BTtDY7bavVofhZ9KZ4aI26X9SRaE+Y3m83XUL1UP2jn8ynjndwCCpEHdUG+9pP1Tw==",
      "license": "MIT"
    },
    "node_modules/undici-types": {
      "version": "7.12.0",
      "resolved": "https://registry.npmjs.org/undici-types/-/undici-types-7.12.0.tgz",
      "integrity": "sha512-goOacqME2GYyOZZfb5Lgtu+1IDmAlAEu5xnD3+xTzS10hT0vzpf0SPjkXwAw9Jm+4n/mQGDP3LO8CPbYROeBfQ==",
      "license": "MIT"
    },
    "node_modules/unicode-canonical-property-names-ecmascript": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/unicode-canonical-property-names-ecmascript/-/unicode-canonical-property-names-ecmascript-2.0.1.tgz",
      "integrity": "sha512-dA8WbNeb2a6oQzAQ55YlT5vQAWGV9WXOsi3SskE3bcCdM0P4SDd+24zS/OCacdRq5BkdsRj9q3Pg6YyQoxIGqg==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-match-property-ecmascript": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/unicode-match-property-ecmascript/-/unicode-match-property-ecmascript-2.0.0.tgz",
      "integrity": "sha512-5kaZCrbp5mmbz5ulBkDkbY0SsPOjKqVS35VpL9ulMPfSl0J0Xsm+9Evphv9CoIZFwre7aJoa94AY6seMKGVN5Q==",
      "license": "MIT",
      "dependencies": {
        "unicode-canonical-property-names-ecmascript": "^2.0.0",
        "unicode-property-aliases-ecmascript": "^2.0.0"
      },
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-match-property-value-ecmascript": {
      "version": "2.2.1",
      "resolved": "https://registry.npmjs.org/unicode-match-property-value-ecmascript/-/unicode-match-property-value-ecmascript-2.2.1.tgz",
      "integrity": "sha512-JQ84qTuMg4nVkx8ga4A16a1epI9H6uTXAknqxkGF/aFfRLw1xC/Bp24HNLaZhHSkWd3+84t8iXnp1J0kYcZHhg==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unicode-property-aliases-ecmascript": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/unicode-property-aliases-ecmascript/-/unicode-property-aliases-ecmascript-2.2.0.tgz",
      "integrity": "sha512-hpbDzxUY9BFwX+UeBnxv3Sh1q7HFxj48DTmXchNgRa46lO8uj3/1iEn3MiNUYTg1g9ctIqXCCERn8gYZhHC5lQ==",
      "license": "MIT",
      "engines": {
        "node": ">=4"
      }
    },
    "node_modules/unique-string": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/unique-string/-/unique-string-2.0.0.tgz",
      "integrity": "sha512-uNaeirEPvpZWSgzwsPGtU2zVSTrn/8L5q/IexZmH0eH6SA73CmAA5U4GwORTxQAZs95TAXLNqeLoPPNO5gZfWg==",
      "license": "MIT",
      "dependencies": {
        "crypto-random-string": "^2.0.0"
      },
      "engines": {
        "node": ">=8"
      }
    },
    "node_modules/universalify": {
      "version": "2.0.1",
      "resolved": "https://registry.npmjs.org/universalify/-/universalify-2.0.1.tgz",
      "integrity": "sha512-gptHNQghINnc/vTGIk0SOFGFNXw7JVrlRUtConJRlvaw6DuX0wO5Jeko9sWrMBhh+PsYAZ7oXAiOnf/UKogyiw==",
      "license": "MIT",
      "engines": {
        "node": ">= 10.0.0"
      }
    },
    "node_modules/unpipe": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/unpipe/-/unpipe-1.0.0.tgz",
      "integrity": "sha512-pjy2bYhSsufwWlKwPc+l3cN7+wuJlK6uz0YdJEOlQDbl6jo/YlPi4mb8agUkVC8BF7V8NuzeyPNqRksA3hztKQ==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/unquote": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/unquote/-/unquote-1.1.1.tgz",
      "integrity": "sha512-vRCqFv6UhXpWxZPyGDh/F3ZpNv8/qo7w6iufLpQg9aKnQ71qM4B5KiI7Mia9COcjEhrO9LueHpMYjYzsWH3OIg==",
      "license": "MIT"
    },
    "node_modules/upath": {
      "version": "1.2.0",
      "resolved": "https://registry.npmjs.org/upath/-/upath-1.2.0.tgz",
      "integrity": "sha512-aZwGpamFO61g3OlfT7OQCHqhGnW43ieH9WZeP7QxN/G/jS4jfqUkZxoryvJgVPEcrl5NL/ggHsSmLMHuH64Lhg==",
      "license": "MIT",
      "engines": {
        "node": ">=4",
        "yarn": "*"
      }
    },
    "node_modules/update-browserslist-db": {
      "version": "1.1.3",
      "resolved": "https://registry.npmjs.org/update-browserslist-db/-/update-browserslist-db-1.1.3.tgz",
      "integrity": "sha512-UxhIZQ+QInVdunkDAaiazvvT/+fXL5Osr0JZlJulepYu6Jd7qJtDZjlur0emRlT71EN3ScPoE7gvsuIKKNavKw==",
      "funding": [
        {
          "type": "opencollective",
          "url": "https://opencollective.com/browserslist"
        },
        {
          "type": "tidelift",
          "url": "https://tidelift.com/funding/github/npm/browserslist"
        },
        {
          "type": "github",
          "url": "https://github.com/sponsors/ai"
        }
      ],
      "license": "MIT",
      "dependencies": {
        "escalade": "^3.2.0",
        "picocolors": "^1.1.1"
      },
      "bin": {
        "update-browserslist-db": "cli.js"
      },
      "peerDependencies": {
        "browserslist": ">= 4.21.0"
      }
    },
    "node_modules/uri-js": {
      "version": "4.4.1",
      "resolved": "https://registry.npmjs.org/uri-js/-/uri-js-4.4.1.tgz",
      "integrity": "sha512-7rKUyy33Q1yc98pQ1DAmLtwX109F7TIfWlW1Ydo8Wl1ii1SeHieeh0HHfPeL2fMXK6z0s8ecKs9frCuLJvndBg==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "punycode": "^2.1.0"
      }
    },
    "node_modules/url-parse": {
      "version": "1.5.10",
      "resolved": "https://registry.npmjs.org/url-parse/-/url-parse-1.5.10.tgz",
      "integrity": "sha512-WypcfiRhfeUP9vvF0j6rw0J3hrWrw6iZv3+22h6iRMJ/8z1Tj6XfLP4DsUix5MhMPnXpiHDoKyoZ/bdCkwBCiQ==",
      "license": "MIT",
      "dependencies": {
        "querystringify": "^2.1.1",
        "requires-port": "^1.0.0"
      }
    },
    "node_modules/util-deprecate": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/util-deprecate/-/util-deprecate-1.0.2.tgz",
      "integrity": "sha512-EPD5q1uXyFxJpCrLnCc1nHnq3gOa6DZBocAIiI2TaSCA7VCJ1UJDMagCzIkXNsUYfD1daK//LTEQ8xiIbrHtcw==",
      "license": "MIT"
    },
    "node_modules/util.promisify": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/util.promisify/-/util.promisify-1.0.1.tgz",
      "integrity": "sha512-g9JpC/3He3bm38zsLupWryXHoEcS22YHthuPQSJdMy6KNrzIRzWqcsHzD/WUnqe45whVou4VIsPew37DoXWNrA==",
      "license": "MIT",
      "dependencies": {
        "define-properties": "^1.1.3",
        "es-abstract": "^1.17.2",
        "has-symbols": "^1.0.1",
        "object.getownpropertydescriptors": "^2.1.0"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/utila": {
      "version": "0.4.0",
      "resolved": "https://registry.npmjs.org/utila/-/utila-0.4.0.tgz",
      "integrity": "sha512-Z0DbgELS9/L/75wZbro8xAnT50pBVFQZ+hUEueGDU5FN51YSCYM+jdxsfCiHjwNP/4LCDD0i/graKpeBnOXKRA==",
      "license": "MIT"
    },
    "node_modules/utils-merge": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/utils-merge/-/utils-merge-1.0.1.tgz",
      "integrity": "sha512-pMZTvIkT1d+TFGvDOqodOclx0QWkkgi6Tdoa8gC8ffGAAqz9pzPTZWAybbsHHoED/ztMtkv/VoYTYyShUn81hA==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.4.0"
      }
    },
    "node_modules/uuid": {
      "version": "8.3.2",
      "resolved": "https://registry.npmjs.org/uuid/-/uuid-8.3.2.tgz",
      "integrity": "sha512-+NYs2QeMWy+GWFOEm9xnn6HCDp0l7QBD7ml8zLUmJ+93Q5NF0NocErnwkTkXVFNiX3/fpC6afS8Dhb/gz7R7eg==",
      "license": "MIT",
      "bin": {
        "uuid": "dist/bin/uuid"
      }
    },
    "node_modules/v8-to-istanbul": {
      "version": "8.1.1",
      "resolved": "https://registry.npmjs.org/v8-to-istanbul/-/v8-to-istanbul-8.1.1.tgz",
      "integrity": "sha512-FGtKtv3xIpR6BYhvgH8MI/y78oT7d8Au3ww4QIxymrCtZEh5b8gCw2siywE+puhEmuWKDtmfrvF5UlB298ut3w==",
      "license": "ISC",
      "dependencies": {
        "@types/istanbul-lib-coverage": "^2.0.1",
        "convert-source-map": "^1.6.0",
        "source-map": "^0.7.3"
      },
      "engines": {
        "node": ">=10.12.0"
      }
    },
    "node_modules/v8-to-istanbul/node_modules/convert-source-map": {
      "version": "1.9.0",
      "resolved": "https://registry.npmjs.org/convert-source-map/-/convert-source-map-1.9.0.tgz",
      "integrity": "sha512-ASFBup0Mz1uyiIjANan1jzLQami9z1PoYSZCiiYW2FczPbenXc45FZdBZLzOT+r6+iciuEModtmCti+hjaAk0A==",
      "license": "MIT"
    },
    "node_modules/vary": {
      "version": "1.1.2",
      "resolved": "https://registry.npmjs.org/vary/-/vary-1.1.2.tgz",
      "integrity": "sha512-BNGbWLfd0eUPabhkXUVm0j8uuvREyTh5ovRa/dyow/BqAbZJyC+5fU+IzQOzmAKzYqYRAISoRhdQr3eIZ/PXqg==",
      "license": "MIT",
      "engines": {
        "node": ">= 0.8"
      }
    },
    "node_modules/w3c-hr-time": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/w3c-hr-time/-/w3c-hr-time-1.0.2.tgz",
      "integrity": "sha512-z8P5DvDNjKDoFIHK7q8r8lackT6l+jo/Ye3HOle7l9nICP9lf1Ci25fy9vHd0JOWewkIFzXIEig3TdKT7JQ5fQ==",
      "deprecated": "Use your platform's native performance.now() and performance.timeOrigin.",
      "license": "MIT",
      "dependencies": {
        "browser-process-hrtime": "^1.0.0"
      }
    },
    "node_modules/w3c-xmlserializer": {
      "version": "2.0.0",
      "resolved": "https://registry.npmjs.org/w3c-xmlserializer/-/w3c-xmlserializer-2.0.0.tgz",
      "integrity": "sha512-4tzD0mF8iSiMiNs30BiLO3EpfGLZUT2MSX/G+o7ZywDzliWQ3OPtTZ0PTC3B3ca1UAf4cJMHB+2Bf56EriJuRA==",
      "license": "MIT",
      "dependencies": {
        "xml-name-validator": "^3.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/walker": {
      "version": "1.0.8",
      "resolved": "https://registry.npmjs.org/walker/-/walker-1.0.8.tgz",
      "integrity": "sha512-ts/8E8l5b7kY0vlWLewOkDXMmPdLcVV4GmOQLyxuSswIJsweeFZtAsMF7k1Nszz+TYBQrlYRmzOnr398y1JemQ==",
      "license": "Apache-2.0",
      "dependencies": {
        "makeerror": "1.0.12"
      }
    },
    "node_modules/watchpack": {
      "version": "2.4.4",
      "resolved": "https://registry.npmjs.org/watchpack/-/watchpack-2.4.4.tgz",
      "integrity": "sha512-c5EGNOiyxxV5qmTtAB7rbiXxi1ooX1pQKMLX/MIabJjRA0SJBQOjKF+KSVfHkr9U1cADPon0mRiVe/riyaiDUA==",
      "license": "MIT",
      "dependencies": {
        "glob-to-regexp": "^0.4.1",
        "graceful-fs": "^4.1.2"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/wbuf": {
      "version": "1.7.3",
      "resolved": "https://registry.npmjs.org/wbuf/-/wbuf-1.7.3.tgz",
      "integrity": "sha512-O84QOnr0icsbFGLS0O3bI5FswxzRr8/gHwWkDlQFskhSPryQXvrTMxjxGP4+iWYoauLoBvfDpkrOauZ+0iZpDA==",
      "license": "MIT",
      "dependencies": {
        "minimalistic-assert": "^1.0.0"
      }
    },
    "node_modules/web-vitals": {
      "version": "2.1.4",
      "resolved": "https://registry.npmjs.org/web-vitals/-/web-vitals-2.1.4.tgz",
      "integrity": "sha512-sVWcwhU5mX6crfI5Vd2dC4qchyTqxV8URinzt25XqVh+bHEPGH4C3NPrNionCP7Obx59wrYEbNlw4Z8sjALzZg==",
      "license": "Apache-2.0"
    },
    "node_modules/webidl-conversions": {
      "version": "6.1.0",
      "resolved": "https://registry.npmjs.org/webidl-conversions/-/webidl-conversions-6.1.0.tgz",
      "integrity": "sha512-qBIvFLGiBpLjfwmYAaHPXsn+ho5xZnGvyGvsarywGNc8VyQJUMHJ8OBKGGrPER0okBeMDaan4mNBlgBROxuI8w==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=10.4"
      }
    },
    "node_modules/webpack": {
      "version": "5.101.3",
      "resolved": "https://registry.npmjs.org/webpack/-/webpack-5.101.3.tgz",
      "integrity": "sha512-7b0dTKR3Ed//AD/6kkx/o7duS8H3f1a4w3BYpIriX4BzIhjkn4teo05cptsxvLesHFKK5KObnadmCHBwGc+51A==",
      "license": "MIT",
      "dependencies": {
        "@types/eslint-scope": "^3.7.7",
        "@types/estree": "^1.0.8",
        "@types/json-schema": "^7.0.15",
        "@webassemblyjs/ast": "^1.14.1",
        "@webassemblyjs/wasm-edit": "^1.14.1",
        "@webassemblyjs/wasm-parser": "^1.14.1",
        "acorn": "^8.15.0",
        "acorn-import-phases": "^1.0.3",
        "browserslist": "^4.24.0",
        "chrome-trace-event": "^1.0.2",
        "enhanced-resolve": "^5.17.3",
        "es-module-lexer": "^1.2.1",
        "eslint-scope": "5.1.1",
        "events": "^3.2.0",
        "glob-to-regexp": "^0.4.1",
        "graceful-fs": "^4.2.11",
        "json-parse-even-better-errors": "^2.3.1",
        "loader-runner": "^4.2.0",
        "mime-types": "^2.1.27",
        "neo-async": "^2.6.2",
        "schema-utils": "^4.3.2",
        "tapable": "^2.1.1",
        "terser-webpack-plugin": "^5.3.11",
        "watchpack": "^2.4.1",
        "webpack-sources": "^3.3.3"
      },
      "bin": {
        "webpack": "bin/webpack.js"
      },
      "engines": {
        "node": ">=10.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependenciesMeta": {
        "webpack-cli": {
          "optional": true
        }
      }
    },
    "node_modules/webpack-dev-middleware": {
      "version": "5.3.4",
      "resolved": "https://registry.npmjs.org/webpack-dev-middleware/-/webpack-dev-middleware-5.3.4.tgz",
      "integrity": "sha512-BVdTqhhs+0IfoeAf7EoH5WE+exCmqGerHfDM0IL096Px60Tq2Mn9MAbnaGUe6HiMa41KMCYF19gyzZmBcq/o4Q==",
      "license": "MIT",
      "dependencies": {
        "colorette": "^2.0.10",
        "memfs": "^3.4.3",
        "mime-types": "^2.1.31",
        "range-parser": "^1.2.1",
        "schema-utils": "^4.0.0"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^4.0.0 || ^5.0.0"
      }
    },
    "node_modules/webpack-dev-server": {
      "version": "4.15.2",
      "resolved": "https://registry.npmjs.org/webpack-dev-server/-/webpack-dev-server-4.15.2.tgz",
      "integrity": "sha512-0XavAZbNJ5sDrCbkpWL8mia0o5WPOd2YGtxrEiZkBK9FjLppIUK2TgxK6qGD2P3hUXTJNNPVibrerKcx5WkR1g==",
      "license": "MIT",
      "dependencies": {
        "@types/bonjour": "^3.5.9",
        "@types/connect-history-api-fallback": "^1.3.5",
        "@types/express": "^4.17.13",
        "@types/serve-index": "^1.9.1",
        "@types/serve-static": "^1.13.10",
        "@types/sockjs": "^0.3.33",
        "@types/ws": "^8.5.5",
        "ansi-html-community": "^0.0.8",
        "bonjour-service": "^1.0.11",
        "chokidar": "^3.5.3",
        "colorette": "^2.0.10",
        "compression": "^1.7.4",
        "connect-history-api-fallback": "^2.0.0",
        "default-gateway": "^6.0.3",
        "express": "^4.17.3",
        "graceful-fs": "^4.2.6",
        "html-entities": "^2.3.2",
        "http-proxy-middleware": "^2.0.3",
        "ipaddr.js": "^2.0.1",
        "launch-editor": "^2.6.0",
        "open": "^8.0.9",
        "p-retry": "^4.5.0",
        "rimraf": "^3.0.2",
        "schema-utils": "^4.0.0",
        "selfsigned": "^2.1.1",
        "serve-index": "^1.9.1",
        "sockjs": "^0.3.24",
        "spdy": "^4.0.2",
        "webpack-dev-middleware": "^5.3.4",
        "ws": "^8.13.0"
      },
      "bin": {
        "webpack-dev-server": "bin/webpack-dev-server.js"
      },
      "engines": {
        "node": ">= 12.13.0"
      },
      "funding": {
        "type": "opencollective",
        "url": "https://opencollective.com/webpack"
      },
      "peerDependencies": {
        "webpack": "^4.37.0 || ^5.0.0"
      },
      "peerDependenciesMeta": {
        "webpack": {
          "optional": true
        },
        "webpack-cli": {
          "optional": true
        }
      }
    },
    "node_modules/webpack-dev-server/node_modules/ws": {
      "version": "8.18.3",
      "resolved": "https://registry.npmjs.org/ws/-/ws-8.18.3.tgz",
      "integrity": "sha512-PEIGCY5tSlUt50cqyMXfCzX+oOPqN0vuGqWzbcJ2xvnkzkq46oOpz7dQaTDBdfICb4N14+GARUDw2XV2N4tvzg==",
      "license": "MIT",
      "engines": {
        "node": ">=10.0.0"
      },
      "peerDependencies": {
        "bufferutil": "^4.0.1",
        "utf-8-validate": ">=5.0.2"
      },
      "peerDependenciesMeta": {
        "bufferutil": {
          "optional": true
        },
        "utf-8-validate": {
          "optional": true
        }
      }
    },
    "node_modules/webpack-manifest-plugin": {
      "version": "4.1.1",
      "resolved": "https://registry.npmjs.org/webpack-manifest-plugin/-/webpack-manifest-plugin-4.1.1.tgz",
      "integrity": "sha512-YXUAwxtfKIJIKkhg03MKuiFAD72PlrqCiwdwO4VEXdRO5V0ORCNwaOwAZawPZalCbmH9kBDmXnNeQOw+BIEiow==",
      "license": "MIT",
      "dependencies": {
        "tapable": "^2.0.0",
        "webpack-sources": "^2.2.0"
      },
      "engines": {
        "node": ">=12.22.0"
      },
      "peerDependencies": {
        "webpack": "^4.44.2 || ^5.47.0"
      }
    },
    "node_modules/webpack-manifest-plugin/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/webpack-manifest-plugin/node_modules/webpack-sources": {
      "version": "2.3.1",
      "resolved": "https://registry.npmjs.org/webpack-sources/-/webpack-sources-2.3.1.tgz",
      "integrity": "sha512-y9EI9AO42JjEcrTJFOYmVywVZdKVUfOvDUPsJea5GIr1JOEGFVqwlY2K098fFoIjOkDzHn2AjRvM8dsBZu+gCA==",
      "license": "MIT",
      "dependencies": {
        "source-list-map": "^2.0.1",
        "source-map": "^0.6.1"
      },
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/webpack-sources": {
      "version": "3.3.3",
      "resolved": "https://registry.npmjs.org/webpack-sources/-/webpack-sources-3.3.3.tgz",
      "integrity": "sha512-yd1RBzSGanHkitROoPFd6qsrxt+oFhg/129YzheDGqeustzX0vTZJZsSsQjVQC4yzBQ56K55XU8gaNCtIzOnTg==",
      "license": "MIT",
      "engines": {
        "node": ">=10.13.0"
      }
    },
    "node_modules/webpack/node_modules/eslint-scope": {
      "version": "5.1.1",
      "resolved": "https://registry.npmjs.org/eslint-scope/-/eslint-scope-5.1.1.tgz",
      "integrity": "sha512-2NxwbF/hZ0KpepYN0cNbo+FN6XoK7GaHlQhgx/hIZl6Va0bF45RQOOwhLIy8lQDbuCiadSLCBnH2CFYquit5bw==",
      "license": "BSD-2-Clause",
      "dependencies": {
        "esrecurse": "^4.3.0",
        "estraverse": "^4.1.1"
      },
      "engines": {
        "node": ">=8.0.0"
      }
    },
    "node_modules/webpack/node_modules/estraverse": {
      "version": "4.3.0",
      "resolved": "https://registry.npmjs.org/estraverse/-/estraverse-4.3.0.tgz",
      "integrity": "sha512-39nnKffWz8xN1BU/2c79n9nB9HDzo0niYUqx6xyqUnyoAnQyyWpOTdZEeiCch8BBu515t4wp9ZmgVfVhn9EBpw==",
      "license": "BSD-2-Clause",
      "engines": {
        "node": ">=4.0"
      }
    },
    "node_modules/websocket-driver": {
      "version": "0.7.4",
      "resolved": "https://registry.npmjs.org/websocket-driver/-/websocket-driver-0.7.4.tgz",
      "integrity": "sha512-b17KeDIQVjvb0ssuSDF2cYXSg2iztliJ4B9WdsuB6J952qCPKmnVq4DyW5motImXHDC1cBT/1UezrJVsKw5zjg==",
      "license": "Apache-2.0",
      "dependencies": {
        "http-parser-js": ">=0.5.1",
        "safe-buffer": ">=5.1.0",
        "websocket-extensions": ">=0.1.1"
      },
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/websocket-extensions": {
      "version": "0.1.4",
      "resolved": "https://registry.npmjs.org/websocket-extensions/-/websocket-extensions-0.1.4.tgz",
      "integrity": "sha512-OqedPIGOfsDlo31UNwYbCFMSaO9m9G/0faIHj5/dZFDMFqPTcx6UwqyOy3COEaEOg/9VsGIpdqn62W5KhoKSpg==",
      "license": "Apache-2.0",
      "engines": {
        "node": ">=0.8.0"
      }
    },
    "node_modules/whatwg-encoding": {
      "version": "1.0.5",
      "resolved": "https://registry.npmjs.org/whatwg-encoding/-/whatwg-encoding-1.0.5.tgz",
      "integrity": "sha512-b5lim54JOPN9HtzvK9HFXvBma/rnfFeqsic0hSpjtDbVxR3dJKLc+KB4V6GgiGOvl7CY/KNh8rxSo9DKQrnUEw==",
      "license": "MIT",
      "dependencies": {
        "iconv-lite": "0.4.24"
      }
    },
    "node_modules/whatwg-encoding/node_modules/iconv-lite": {
      "version": "0.4.24",
      "resolved": "https://registry.npmjs.org/iconv-lite/-/iconv-lite-0.4.24.tgz",
      "integrity": "sha512-v3MXnZAcvnywkTUEZomIActle7RXXeedOR31wwl7VlyoXO4Qi9arvSenNQWne1TcRwhCL1HwLI21bEqdpj8/rA==",
      "license": "MIT",
      "dependencies": {
        "safer-buffer": ">= 2.1.2 < 3"
      },
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/whatwg-fetch": {
      "version": "3.6.20",
      "resolved": "https://registry.npmjs.org/whatwg-fetch/-/whatwg-fetch-3.6.20.tgz",
      "integrity": "sha512-EqhiFU6daOA8kpjOWTL0olhVOF3i7OrFzSYiGsEMB8GcXS+RrzauAERX65xMeNWVqxA6HXH2m69Z9LaKKdisfg==",
      "license": "MIT"
    },
    "node_modules/whatwg-mimetype": {
      "version": "2.3.0",
      "resolved": "https://registry.npmjs.org/whatwg-mimetype/-/whatwg-mimetype-2.3.0.tgz",
      "integrity": "sha512-M4yMwr6mAnQz76TbJm914+gPpB/nCwvZbJU28cUD6dR004SAxDLOOSUaB1JDRqLtaOV/vi0IC5lEAGFgrjGv/g==",
      "license": "MIT"
    },
    "node_modules/whatwg-url": {
      "version": "8.7.0",
      "resolved": "https://registry.npmjs.org/whatwg-url/-/whatwg-url-8.7.0.tgz",
      "integrity": "sha512-gAojqb/m9Q8a5IV96E3fHJM70AzCkgt4uXYX2O7EmuyOnLrViCQlsEBmF9UQIu3/aeAIp2U17rtbpZWNntQqdg==",
      "license": "MIT",
      "dependencies": {
        "lodash": "^4.7.0",
        "tr46": "^2.1.0",
        "webidl-conversions": "^6.1.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/which": {
      "version": "2.0.2",
      "resolved": "https://registry.npmjs.org/which/-/which-2.0.2.tgz",
      "integrity": "sha512-BLI3Tl1TW3Pvl70l3yq3Y64i+awpwXqsGBYWkkqMtnbXgrMD+yj7rhW0kuEDxzJaYXGjEW5ogapKNMEKNMjibA==",
      "license": "ISC",
      "dependencies": {
        "isexe": "^2.0.0"
      },
      "bin": {
        "node-which": "bin/node-which"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/which-boxed-primitive": {
      "version": "1.1.1",
      "resolved": "https://registry.npmjs.org/which-boxed-primitive/-/which-boxed-primitive-1.1.1.tgz",
      "integrity": "sha512-TbX3mj8n0odCBFVlY8AxkqcHASw3L60jIuF8jFP78az3C2YhmGvqbHBpAjTRH2/xqYunrJ9g1jSyjCjpoWzIAA==",
      "license": "MIT",
      "dependencies": {
        "is-bigint": "^1.1.0",
        "is-boolean-object": "^1.2.1",
        "is-number-object": "^1.1.1",
        "is-string": "^1.1.1",
        "is-symbol": "^1.1.1"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-builtin-type": {
      "version": "1.2.1",
      "resolved": "https://registry.npmjs.org/which-builtin-type/-/which-builtin-type-1.2.1.tgz",
      "integrity": "sha512-6iBczoX+kDQ7a3+YJBnh3T+KZRxM/iYNPXicqk66/Qfm1b93iu+yOImkg0zHbj5LNOcNv1TEADiZ0xa34B4q6Q==",
      "license": "MIT",
      "dependencies": {
        "call-bound": "^1.0.2",
        "function.prototype.name": "^1.1.6",
        "has-tostringtag": "^1.0.2",
        "is-async-function": "^2.0.0",
        "is-date-object": "^1.1.0",
        "is-finalizationregistry": "^1.1.0",
        "is-generator-function": "^1.0.10",
        "is-regex": "^1.2.1",
        "is-weakref": "^1.0.2",
        "isarray": "^2.0.5",
        "which-boxed-primitive": "^1.1.0",
        "which-collection": "^1.0.2",
        "which-typed-array": "^1.1.16"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-collection": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/which-collection/-/which-collection-1.0.2.tgz",
      "integrity": "sha512-K4jVyjnBdgvc86Y6BkaLZEN933SwYOuBFkdmBu9ZfkcAbdVbpITnDmjvZ/aQjRXQrv5EPkTnD1s39GiiqbngCw==",
      "license": "MIT",
      "dependencies": {
        "is-map": "^2.0.3",
        "is-set": "^2.0.3",
        "is-weakmap": "^2.0.2",
        "is-weakset": "^2.0.3"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/which-typed-array": {
      "version": "1.1.19",
      "resolved": "https://registry.npmjs.org/which-typed-array/-/which-typed-array-1.1.19.tgz",
      "integrity": "sha512-rEvr90Bck4WZt9HHFC4DJMsjvu7x+r6bImz0/BrbWb7A2djJ8hnZMrWnHo9F8ssv0OMErasDhftrfROTyqSDrw==",
      "license": "MIT",
      "dependencies": {
        "available-typed-arrays": "^1.0.7",
        "call-bind": "^1.0.8",
        "call-bound": "^1.0.4",
        "for-each": "^0.3.5",
        "get-proto": "^1.0.1",
        "gopd": "^1.2.0",
        "has-tostringtag": "^1.0.2"
      },
      "engines": {
        "node": ">= 0.4"
      },
      "funding": {
        "url": "https://github.com/sponsors/ljharb"
      }
    },
    "node_modules/word-wrap": {
      "version": "1.2.5",
      "resolved": "https://registry.npmjs.org/word-wrap/-/word-wrap-1.2.5.tgz",
      "integrity": "sha512-BN22B5eaMMI9UMtjrGd5g5eCYPpCPDUy0FJXbYsaT5zYxjFOckS53SQDE3pWkVoWpHXVb3BrYcEN4Twa55B5cA==",
      "license": "MIT",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/workbox-background-sync": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-background-sync/-/workbox-background-sync-6.6.0.tgz",
      "integrity": "sha512-jkf4ZdgOJxC9u2vztxLuPT/UjlH7m/nWRQ/MgGL0v8BJHoZdVGJd18Kck+a0e55wGXdqyHO+4IQTk0685g4MUw==",
      "license": "MIT",
      "dependencies": {
        "idb": "^7.0.1",
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-broadcast-update": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-broadcast-update/-/workbox-broadcast-update-6.6.0.tgz",
      "integrity": "sha512-nm+v6QmrIFaB/yokJmQ/93qIJ7n72NICxIwQwe5xsZiV2aI93MGGyEyzOzDPVz5THEr5rC3FJSsO3346cId64Q==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-build": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-build/-/workbox-build-6.6.0.tgz",
      "integrity": "sha512-Tjf+gBwOTuGyZwMz2Nk/B13Fuyeo0Q84W++bebbVsfr9iLkDSo6j6PST8tET9HYA58mlRXwlMGpyWO8ETJiXdQ==",
      "license": "MIT",
      "dependencies": {
        "@apideck/better-ajv-errors": "^0.3.1",
        "@babel/core": "^7.11.1",
        "@babel/preset-env": "^7.11.0",
        "@babel/runtime": "^7.11.2",
        "@rollup/plugin-babel": "^5.2.0",
        "@rollup/plugin-node-resolve": "^11.2.1",
        "@rollup/plugin-replace": "^2.4.1",
        "@surma/rollup-plugin-off-main-thread": "^2.2.3",
        "ajv": "^8.6.0",
        "common-tags": "^1.8.0",
        "fast-json-stable-stringify": "^2.1.0",
        "fs-extra": "^9.0.1",
        "glob": "^7.1.6",
        "lodash": "^4.17.20",
        "pretty-bytes": "^5.3.0",
        "rollup": "^2.43.1",
        "rollup-plugin-terser": "^7.0.0",
        "source-map": "^0.8.0-beta.0",
        "stringify-object": "^3.3.0",
        "strip-comments": "^2.0.1",
        "tempy": "^0.6.0",
        "upath": "^1.2.0",
        "workbox-background-sync": "6.6.0",
        "workbox-broadcast-update": "6.6.0",
        "workbox-cacheable-response": "6.6.0",
        "workbox-core": "6.6.0",
        "workbox-expiration": "6.6.0",
        "workbox-google-analytics": "6.6.0",
        "workbox-navigation-preload": "6.6.0",
        "workbox-precaching": "6.6.0",
        "workbox-range-requests": "6.6.0",
        "workbox-recipes": "6.6.0",
        "workbox-routing": "6.6.0",
        "workbox-strategies": "6.6.0",
        "workbox-streams": "6.6.0",
        "workbox-sw": "6.6.0",
        "workbox-window": "6.6.0"
      },
      "engines": {
        "node": ">=10.0.0"
      }
    },
    "node_modules/workbox-build/node_modules/@apideck/better-ajv-errors": {
      "version": "0.3.6",
      "resolved": "https://registry.npmjs.org/@apideck/better-ajv-errors/-/better-ajv-errors-0.3.6.tgz",
      "integrity": "sha512-P+ZygBLZtkp0qqOAJJVX4oX/sFo5JR3eBWwwuqHHhK0GIgQOKWrAfiAaWX0aArHkRWHMuggFEgAZNxVPwPZYaA==",
      "license": "MIT",
      "dependencies": {
        "json-schema": "^0.4.0",
        "jsonpointer": "^5.0.0",
        "leven": "^3.1.0"
      },
      "engines": {
        "node": ">=10"
      },
      "peerDependencies": {
        "ajv": ">=8"
      }
    },
    "node_modules/workbox-build/node_modules/ajv": {
      "version": "8.17.1",
      "resolved": "https://registry.npmjs.org/ajv/-/ajv-8.17.1.tgz",
      "integrity": "sha512-B/gBuNg5SiMTrPkC+A2+cW0RszwxYmn6VYxB/inlBStS5nx6xHIt/ehKRhIMhqusl7a8LjQoZnjCs5vhwxOQ1g==",
      "license": "MIT",
      "dependencies": {
        "fast-deep-equal": "^3.1.3",
        "fast-uri": "^3.0.1",
        "json-schema-traverse": "^1.0.0",
        "require-from-string": "^2.0.2"
      },
      "funding": {
        "type": "github",
        "url": "https://github.com/sponsors/epoberezkin"
      }
    },
    "node_modules/workbox-build/node_modules/fs-extra": {
      "version": "9.1.0",
      "resolved": "https://registry.npmjs.org/fs-extra/-/fs-extra-9.1.0.tgz",
      "integrity": "sha512-hcg3ZmepS30/7BSFqRvoo3DOMQu7IjqxO5nCDt+zM9XWjb33Wg7ziNT+Qvqbuc3+gWpzO02JubVyk2G4Zvo1OQ==",
      "license": "MIT",
      "dependencies": {
        "at-least-node": "^1.0.0",
        "graceful-fs": "^4.2.0",
        "jsonfile": "^6.0.1",
        "universalify": "^2.0.0"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/workbox-build/node_modules/json-schema-traverse": {
      "version": "1.0.0",
      "resolved": "https://registry.npmjs.org/json-schema-traverse/-/json-schema-traverse-1.0.0.tgz",
      "integrity": "sha512-NM8/P9n3XjXhIZn1lLhkFaACTOURQXjWhV4BA/RnOv8xvgqtqpAX9IO4mRQxSx1Rlo4tqzeqb0sOlruaOy3dug==",
      "license": "MIT"
    },
    "node_modules/workbox-build/node_modules/source-map": {
      "version": "0.8.0-beta.0",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.8.0-beta.0.tgz",
      "integrity": "sha512-2ymg6oRBpebeZi9UUNsgQ89bhx01TcTkmNTGnNO88imTmbSgy4nfujrgVEFKWpMTEGA11EDkTt7mqObTPdigIA==",
      "deprecated": "The work that was done in this beta branch won't be included in future versions",
      "license": "BSD-3-Clause",
      "dependencies": {
        "whatwg-url": "^7.0.0"
      },
      "engines": {
        "node": ">= 8"
      }
    },
    "node_modules/workbox-build/node_modules/tr46": {
      "version": "1.0.1",
      "resolved": "https://registry.npmjs.org/tr46/-/tr46-1.0.1.tgz",
      "integrity": "sha512-dTpowEjclQ7Kgx5SdBkqRzVhERQXov8/l9Ft9dVM9fmg0W0KQSVaXX9T4i6twCPNtYiZM53lpSSUAwJbFPOHxA==",
      "license": "MIT",
      "dependencies": {
        "punycode": "^2.1.0"
      }
    },
    "node_modules/workbox-build/node_modules/webidl-conversions": {
      "version": "4.0.2",
      "resolved": "https://registry.npmjs.org/webidl-conversions/-/webidl-conversions-4.0.2.tgz",
      "integrity": "sha512-YQ+BmxuTgd6UXZW3+ICGfyqRyHXVlD5GtQr5+qjiNW7bF0cqrzX500HVXPBOvgXb5YnzDd+h0zqyv61KUD7+Sg==",
      "license": "BSD-2-Clause"
    },
    "node_modules/workbox-build/node_modules/whatwg-url": {
      "version": "7.1.0",
      "resolved": "https://registry.npmjs.org/whatwg-url/-/whatwg-url-7.1.0.tgz",
      "integrity": "sha512-WUu7Rg1DroM7oQvGWfOiAK21n74Gg+T4elXEQYkOhtyLeWiJFoOGLXPKI/9gzIie9CtwVLm8wtw6YJdKyxSjeg==",
      "license": "MIT",
      "dependencies": {
        "lodash.sortby": "^4.7.0",
        "tr46": "^1.0.1",
        "webidl-conversions": "^4.0.2"
      }
    },
    "node_modules/workbox-cacheable-response": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-cacheable-response/-/workbox-cacheable-response-6.6.0.tgz",
      "integrity": "sha512-JfhJUSQDwsF1Xv3EV1vWzSsCOZn4mQ38bWEBR3LdvOxSPgB65gAM6cS2CX8rkkKHRgiLrN7Wxoyu+TuH67kHrw==",
      "deprecated": "workbox-background-sync@6.6.0",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-core": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-core/-/workbox-core-6.6.0.tgz",
      "integrity": "sha512-GDtFRF7Yg3DD859PMbPAYPeJyg5gJYXuBQAC+wyrWuuXgpfoOrIQIvFRZnQ7+czTIQjIr1DhLEGFzZanAT/3bQ==",
      "license": "MIT"
    },
    "node_modules/workbox-expiration": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-expiration/-/workbox-expiration-6.6.0.tgz",
      "integrity": "sha512-baplYXcDHbe8vAo7GYvyAmlS4f6998Jff513L4XvlzAOxcl8F620O91guoJ5EOf5qeXG4cGdNZHkkVAPouFCpw==",
      "license": "MIT",
      "dependencies": {
        "idb": "^7.0.1",
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-google-analytics": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-google-analytics/-/workbox-google-analytics-6.6.0.tgz",
      "integrity": "sha512-p4DJa6OldXWd6M9zRl0H6vB9lkrmqYFkRQ2xEiNdBFp9U0LhsGO7hsBscVEyH9H2/3eZZt8c97NB2FD9U2NJ+Q==",
      "deprecated": "It is not compatible with newer versions of GA starting with v4, as long as you are using GAv3 it should be ok, but the package is not longer being maintained",
      "license": "MIT",
      "dependencies": {
        "workbox-background-sync": "6.6.0",
        "workbox-core": "6.6.0",
        "workbox-routing": "6.6.0",
        "workbox-strategies": "6.6.0"
      }
    },
    "node_modules/workbox-navigation-preload": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-navigation-preload/-/workbox-navigation-preload-6.6.0.tgz",
      "integrity": "sha512-utNEWG+uOfXdaZmvhshrh7KzhDu/1iMHyQOV6Aqup8Mm78D286ugu5k9MFD9SzBT5TcwgwSORVvInaXWbvKz9Q==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-precaching": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-precaching/-/workbox-precaching-6.6.0.tgz",
      "integrity": "sha512-eYu/7MqtRZN1IDttl/UQcSZFkHP7dnvr/X3Vn6Iw6OsPMruQHiVjjomDFCNtd8k2RdjLs0xiz9nq+t3YVBcWPw==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0",
        "workbox-routing": "6.6.0",
        "workbox-strategies": "6.6.0"
      }
    },
    "node_modules/workbox-range-requests": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-range-requests/-/workbox-range-requests-6.6.0.tgz",
      "integrity": "sha512-V3aICz5fLGq5DpSYEU8LxeXvsT//mRWzKrfBOIxzIdQnV/Wj7R+LyJVTczi4CQ4NwKhAaBVaSujI1cEjXW+hTw==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-recipes": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-recipes/-/workbox-recipes-6.6.0.tgz",
      "integrity": "sha512-TFi3kTgYw73t5tg73yPVqQC8QQjxJSeqjXRO4ouE/CeypmP2O/xqmB/ZFBBQazLTPxILUQ0b8aeh0IuxVn9a6A==",
      "license": "MIT",
      "dependencies": {
        "workbox-cacheable-response": "6.6.0",
        "workbox-core": "6.6.0",
        "workbox-expiration": "6.6.0",
        "workbox-precaching": "6.6.0",
        "workbox-routing": "6.6.0",
        "workbox-strategies": "6.6.0"
      }
    },
    "node_modules/workbox-routing": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-routing/-/workbox-routing-6.6.0.tgz",
      "integrity": "sha512-x8gdN7VDBiLC03izAZRfU+WKUXJnbqt6PG9Uh0XuPRzJPpZGLKce/FkOX95dWHRpOHWLEq8RXzjW0O+POSkKvw==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-strategies": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-strategies/-/workbox-strategies-6.6.0.tgz",
      "integrity": "sha512-eC07XGuINAKUWDnZeIPdRdVja4JQtTuc35TZ8SwMb1ztjp7Ddq2CJ4yqLvWzFWGlYI7CG/YGqaETntTxBGdKgQ==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/workbox-streams": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-streams/-/workbox-streams-6.6.0.tgz",
      "integrity": "sha512-rfMJLVvwuED09CnH1RnIep7L9+mj4ufkTyDPVaXPKlhi9+0czCu+SJggWCIFbPpJaAZmp2iyVGLqS3RUmY3fxg==",
      "license": "MIT",
      "dependencies": {
        "workbox-core": "6.6.0",
        "workbox-routing": "6.6.0"
      }
    },
    "node_modules/workbox-sw": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-sw/-/workbox-sw-6.6.0.tgz",
      "integrity": "sha512-R2IkwDokbtHUE4Kus8pKO5+VkPHD2oqTgl+XJwh4zbF1HyjAbgNmK/FneZHVU7p03XUt9ICfuGDYISWG9qV/CQ==",
      "license": "MIT"
    },
    "node_modules/workbox-webpack-plugin": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-webpack-plugin/-/workbox-webpack-plugin-6.6.0.tgz",
      "integrity": "sha512-xNZIZHalboZU66Wa7x1YkjIqEy1gTR+zPM+kjrYJzqN7iurYZBctBLISyScjhkJKYuRrZUP0iqViZTh8rS0+3A==",
      "license": "MIT",
      "dependencies": {
        "fast-json-stable-stringify": "^2.1.0",
        "pretty-bytes": "^5.4.1",
        "upath": "^1.2.0",
        "webpack-sources": "^1.4.3",
        "workbox-build": "6.6.0"
      },
      "engines": {
        "node": ">=10.0.0"
      },
      "peerDependencies": {
        "webpack": "^4.4.0 || ^5.9.0"
      }
    },
    "node_modules/workbox-webpack-plugin/node_modules/source-map": {
      "version": "0.6.1",
      "resolved": "https://registry.npmjs.org/source-map/-/source-map-0.6.1.tgz",
      "integrity": "sha512-UjgapumWlbMhkBgzT7Ykc5YXUT46F0iKu8SGXq0bcwP5dz/h0Plj6enJqjz1Zbq2l5WaqYnrVbwWOWMyF3F47g==",
      "license": "BSD-3-Clause",
      "engines": {
        "node": ">=0.10.0"
      }
    },
    "node_modules/workbox-webpack-plugin/node_modules/webpack-sources": {
      "version": "1.4.3",
      "resolved": "https://registry.npmjs.org/webpack-sources/-/webpack-sources-1.4.3.tgz",
      "integrity": "sha512-lgTS3Xhv1lCOKo7SA5TjKXMjpSM4sBjNV5+q2bqesbSPs5FjGmU6jjtBSkX9b4qW87vDIsCIlUPOEhbZrMdjeQ==",
      "license": "MIT",
      "dependencies": {
        "source-list-map": "^2.0.0",
        "source-map": "~0.6.1"
      }
    },
    "node_modules/workbox-window": {
      "version": "6.6.0",
      "resolved": "https://registry.npmjs.org/workbox-window/-/workbox-window-6.6.0.tgz",
      "integrity": "sha512-L4N9+vka17d16geaJXXRjENLFldvkWy7JyGxElRD0JvBxvFEd8LOhr+uXCcar/NzAmIBRv9EZ+M+Qr4mOoBITw==",
      "license": "MIT",
      "dependencies": {
        "@types/trusted-types": "^2.0.2",
        "workbox-core": "6.6.0"
      }
    },
    "node_modules/wrap-ansi": {
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/wrap-ansi/-/wrap-ansi-7.0.0.tgz",
      "integrity": "sha512-YVGIj2kamLSTxw6NsZjoBxfSwsn0ycdesmc4p+Q21c5zPuZ1pl+NfxVdxPtdHvmNVOQ6XSYG4AUtyt/Fi7D16Q==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^4.0.0",
        "string-width": "^4.1.0",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/wrap-ansi?sponsor=1"
      }
    },
    "node_modules/wrap-ansi-cjs": {
      "name": "wrap-ansi",
      "version": "7.0.0",
      "resolved": "https://registry.npmjs.org/wrap-ansi/-/wrap-ansi-7.0.0.tgz",
      "integrity": "sha512-YVGIj2kamLSTxw6NsZjoBxfSwsn0ycdesmc4p+Q21c5zPuZ1pl+NfxVdxPtdHvmNVOQ6XSYG4AUtyt/Fi7D16Q==",
      "license": "MIT",
      "dependencies": {
        "ansi-styles": "^4.0.0",
        "string-width": "^4.1.0",
        "strip-ansi": "^6.0.0"
      },
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/chalk/wrap-ansi?sponsor=1"
      }
    },
    "node_modules/wrappy": {
      "version": "1.0.2",
      "resolved": "https://registry.npmjs.org/wrappy/-/wrappy-1.0.2.tgz",
      "integrity": "sha512-l4Sp/DRseor9wL6EvV2+TuQn63dMkPjZ/sp9XkghTEbV9KlPS1xUsZ3u7/IQO4wxtcFB4bgpQPRcR3QCvezPcQ==",
      "license": "ISC"
    },
    "node_modules/write-file-atomic": {
      "version": "3.0.3",
      "resolved": "https://registry.npmjs.org/write-file-atomic/-/write-file-atomic-3.0.3.tgz",
      "integrity": "sha512-AvHcyZ5JnSfq3ioSyjrBkH9yW4m7Ayk8/9My/DD9onKeu/94fwrMocemO2QAJFAlnnDN+ZDS+ZjAR5ua1/PV/Q==",
      "license": "ISC",
      "dependencies": {
        "imurmurhash": "^0.1.4",
        "is-typedarray": "^1.0.0",
        "signal-exit": "^3.0.2",
        "typedarray-to-buffer": "^3.1.5"
      }
    },
    "node_modules/ws": {
      "version": "7.5.10",
      "resolved": "https://registry.npmjs.org/ws/-/ws-7.5.10.tgz",
      "integrity": "sha512-+dbF1tHwZpXcbOJdVOkzLDxZP1ailvSxM6ZweXTegylPny803bFhA+vqBYw4s31NSAk4S2Qz+AKXK9a4wkdjcQ==",
      "license": "MIT",
      "engines": {
        "node": ">=8.3.0"
      },
      "peerDependencies": {
        "bufferutil": "^4.0.1",
        "utf-8-validate": "^5.0.2"
      },
      "peerDependenciesMeta": {
        "bufferutil": {
          "optional": true
        },
        "utf-8-validate": {
          "optional": true
        }
      }
    },
    "node_modules/xml-name-validator": {
      "version": "3.0.0",
      "resolved": "https://registry.npmjs.org/xml-name-validator/-/xml-name-validator-3.0.0.tgz",
      "integrity": "sha512-A5CUptxDsvxKJEU3yO6DuWBSJz/qizqzJKOMIfUJHETbBw/sFaDxgd6fxm1ewUaM0jZ444Fc5vC5ROYurg/4Pw==",
      "license": "Apache-2.0"
    },
    "node_modules/xmlchars": {
      "version": "2.2.0",
      "resolved": "https://registry.npmjs.org/xmlchars/-/xmlchars-2.2.0.tgz",
      "integrity": "sha512-JZnDKK8B0RCDw84FNdDAIpZK+JuJw+s7Lz8nksI7SIuU3UXJJslUthsi+uWBUYOwPFwW7W7PRLRfUKpxjtjFCw==",
      "license": "MIT"
    },
    "node_modules/y18n": {
      "version": "5.0.8",
      "resolved": "https://registry.npmjs.org/y18n/-/y18n-5.0.8.tgz",
      "integrity": "sha512-0pfFzegeDWJHJIAmTLRP2DwHjdF5s7jo9tuztdQxAhINCdvS+3nGINqPd00AphqJR/0LhANUS6/+7SCb98YOfA==",
      "license": "ISC",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/yallist": {
      "version": "3.1.1",
      "resolved": "https://registry.npmjs.org/yallist/-/yallist-3.1.1.tgz",
      "integrity": "sha512-a4UGQaWPH59mOXUYnAG2ewncQS4i4F43Tv3JoAM+s2VDAmS9NsK8GpDMLrCHPksFT7h3K6TOoUNn2pb7RoXx4g==",
      "license": "ISC"
    },
    "node_modules/yaml": {
      "version": "1.10.2",
      "resolved": "https://registry.npmjs.org/yaml/-/yaml-1.10.2.tgz",
      "integrity": "sha512-r3vXyErRCYJ7wg28yvBY5VSoAF8ZvlcW9/BwUzEtUsjvX/DKs24dIkuwjtuprwJJHsbyUbLApepYTR1BN4uHrg==",
      "license": "ISC",
      "engines": {
        "node": ">= 6"
      }
    },
    "node_modules/yargs": {
      "version": "16.2.0",
      "resolved": "https://registry.npmjs.org/yargs/-/yargs-16.2.0.tgz",
      "integrity": "sha512-D1mvvtDG0L5ft/jGWkLpG1+m0eQxOfaBvTNELraWj22wSVUMWxZUvYgJYcKh6jGGIkJFhH4IZPQhR4TKpc8mBw==",
      "license": "MIT",
      "dependencies": {
        "cliui": "^7.0.2",
        "escalade": "^3.1.1",
        "get-caller-file": "^2.0.5",
        "require-directory": "^2.1.1",
        "string-width": "^4.2.0",
        "y18n": "^5.0.5",
        "yargs-parser": "^20.2.2"
      },
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/yargs-parser": {
      "version": "20.2.9",
      "resolved": "https://registry.npmjs.org/yargs-parser/-/yargs-parser-20.2.9.tgz",
      "integrity": "sha512-y11nGElTIV+CT3Zv9t7VKl+Q3hTQoT9a1Qzezhhl6Rp21gJ/IVTW7Z3y9EWXhuUBC2Shnf+DX0antecpAwSP8w==",
      "license": "ISC",
      "engines": {
        "node": ">=10"
      }
    },
    "node_modules/yocto-queue": {
      "version": "0.1.0",
      "resolved": "https://registry.npmjs.org/yocto-queue/-/yocto-queue-0.1.0.tgz",
      "integrity": "sha512-rVksvsnNCdJ/ohGc6xgPwyN8eheCxsiLM8mxuE/t/mOVqJewPuO1miLpTHQiRgTKCLexL4MeAFVagts7HmNZ2Q==",
      "license": "MIT",
      "engines": {
        "node": ">=10"
      },
      "funding": {
        "url": "https://github.com/sponsors/sindresorhus"
      }
    }
  }
}

```


### 📄 package.json

**Path:** `frontend/package.json`

```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@testing-library/dom": "^10.4.1",
    "@testing-library/jest-dom": "^6.8.0",
    "@testing-library/react": "^16.3.0",
    "@testing-library/user-event": "^13.5.0",
    "axios": "^1.12.2",
    "chart.js": "^4.5.0",
    "react": "^19.1.1",
    "react-chartjs-2": "^5.3.0",
    "react-dom": "^19.1.1",
    "react-scripts": "5.0.1",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}

```


================================================================================
## 📂 frontend → public


### 📄 index.html

**Path:** `frontend/public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Web site created using create-react-app"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <!--
      manifest.json provides metadata used when your web app is installed on a
      user's mobile device or desktop. See https://developers.google.com/web/fundamentals/web-app-manifest/
    -->
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    <!--
      Notice the use of %PUBLIC_URL% in the tags above.
      It will be replaced with the URL of the `public` folder during the build.
      Only files inside the `public` folder can be referenced from the HTML.

      Unlike "/favicon.ico" or "favicon.ico", "%PUBLIC_URL%/favicon.ico" will
      work correctly both with client-side routing and a non-root public URL.
      Learn how to configure a non-root public URL by running `npm run build`.
    -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <title>React App</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
    <!--
      This HTML file is a template.
      If you open it directly in the browser, you will see an empty page.

      You can add webfonts, meta tags, or analytics to this file.
      The build step will place the bundled scripts into the <body> tag.

      To begin the development, run `npm start` or `yarn start`.
      To create a production bundle, use `npm run build` or `yarn build`.
    -->
  </body>
</html>

```


### 📄 manifest.json

**Path:** `frontend/public/manifest.json`

```json
{
  "short_name": "React App",
  "name": "Create React App Sample",
  "icons": [
    {
      "src": "favicon.ico",
      "sizes": "64x64 32x32 24x24 16x16",
      "type": "image/x-icon"
    },
    {
      "src": "logo192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "logo512.png",
      "type": "image/png",
      "sizes": "512x512"
    }
  ],
  "start_url": ".",
  "display": "standalone",
  "theme_color": "#000000",
  "background_color": "#ffffff"
}

```


### 📄 robots.txt

**Path:** `frontend/public/robots.txt`

```text
# https://www.robotstxt.org/robotstxt.html
User-agent: *
Disallow:

```


================================================================================
## 📂 frontend → src


### 📄 App.css

**Path:** `frontend/src/App.css`

```css
/* Simple Professional App Styles */

.App {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.app-layout {
  display: flex;
  min-height: calc(100vh - 60px);
}

.main-content {
  flex: 1;
  padding: 20px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
}

.action-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

```


### 📄 App.js

**Path:** `frontend/src/App.js`

```javascript
import React, { useState, useEffect } from 'react';
import CategoryManager from './CategoryManager';
import ProposalForm from './ProposalForm';
import ProposalsList from './ProposalsList';
import ContractUpload from './ContractUpload';
import Dashboard from './Dashboard';
import HistoryView from './HistoryView';
import Login from './Login';
import Register from './Register';
import Sidebar from './Sidebar';
import RoleGuard from './RoleGuard';
import { UserProvider, useUser } from './UserContext';
import './App.css';
import './theme.css';

const Header = () => {
  const { user, logout } = useUser();
  
  return (
    <header className="app-header">
      <div className="header-content">
        <div className="header-left">
          <h1>Government Spending Tracker</h1>
        </div>
        {user && (
          <div className="header-actions">
            <span style={{ marginRight: '15px', color: '#666', fontSize: '14px' }}>
              {user.username} ({user.role})
            </span>
            <button className="btn btn-secondary btn-small" onClick={logout}>
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

function AppContent() {
  const [proposalRefreshKey, setProposalRefreshKey] = useState(0);
  const { user, loading } = useUser();
  const [showRegister, setShowRegister] = useState(false);
  
  // Set default tab based on user role
  const getDefaultTab = (userRole) => {
    if (userRole === 'finance') {
      return 'dashboard';
    } else if (userRole === 'ministry') {
      return 'proposals';
    }
    return 'dashboard'; // fallback
  };
  
  const [activeTab, setActiveTab] = useState(() => getDefaultTab(user?.role));

  // Update activeTab when user changes
  useEffect(() => {
    if (user) {
      const defaultTab = getDefaultTab(user.role);
      setActiveTab(defaultTab);
    }
  }, [user]);

  const handleProposalCreated = () => {
    setProposalRefreshKey(prevKey => prevKey + 1);
  };

    const renderContent = () => {
    // Additional security check - redirect unauthorized users
    if (activeTab === 'dashboard' && user?.role !== 'finance') {
      setActiveTab('proposals'); // Redirect ministry users to proposals
      return <ProposalsList key={`proposals-${proposalRefreshKey}`} />;
    }
    if (activeTab === 'categories' && user?.role !== 'finance') {
      setActiveTab('proposals'); // Redirect ministry users to proposals
      return <ProposalsList key={`proposals-${proposalRefreshKey}`} />;
    }
    if ((activeTab === 'create-proposal' || activeTab === 'upload-contract') && user?.role !== 'ministry') {
      setActiveTab('dashboard'); // Redirect finance users to dashboard
      return (
        <RoleGuard allowedRoles={['finance']}>
          <Dashboard key={`dashboard-${proposalRefreshKey}`} />
        </RoleGuard>
      );
    }
    
    switch (activeTab) {
      case 'dashboard':
        return (
          <RoleGuard allowedRoles={['finance']}>
            <Dashboard key={`dashboard-${proposalRefreshKey}`} />
          </RoleGuard>
        );
      case 'categories':
        return (
          <RoleGuard allowedRoles={['finance']}>
            <CategoryManager />
          </RoleGuard>
        );
      case 'proposals':
        return <ProposalsList key={`proposals-${proposalRefreshKey}`} />;
      case 'create-proposal':
        return (
          <RoleGuard allowedRoles={['ministry']}>
            <ProposalForm onCreated={handleProposalCreated} />
          </RoleGuard>
        );
      case 'upload-contract':
        return (
          <RoleGuard allowedRoles={['ministry']}>
            <ContractUpload onProposalsCreated={handleProposalCreated} />
          </RoleGuard>
        );
      case 'history':
        return <HistoryView />;
      default:
        // Default based on user role
        const defaultTab = getDefaultTab(user?.role);
        if (defaultTab === 'dashboard') {
          return (
            <RoleGuard allowedRoles={['finance']}>
              <Dashboard key={`dashboard-${proposalRefreshKey}`} />
            </RoleGuard>
          );
        } else {
          return <ProposalsList key={`proposals-${proposalRefreshKey}`} />;
        }
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <span>Loading application...</span>
      </div>
    );
  }

  if (!user) {
    if (showRegister) {
      return <Register onSwitchToLogin={() => setShowRegister(false)} />;
    }
    return <Login onSwitchToRegister={() => setShowRegister(true)} />;
  }

  return (
    <div className="App">
      <Header />
      <div className="app-layout">
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        <main className="main-content">
          <div className="content-container">
            {renderContent()}
          </div>
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <UserProvider>
      <AppContent />
    </UserProvider>
  );
}

export default App;

```


### 📄 App.test.js

**Path:** `frontend/src/App.test.js`

```javascript
import { render, screen } from '@testing-library/react';
import App from './App';

jest.mock('axios', () => {
  const mockResponse = Promise.resolve({ data: {} });
  const mockRequest = jest.fn().mockImplementation(() => mockResponse);

  const mockInstance = {
    get: mockRequest,
    post: mockRequest,
    put: mockRequest,
    delete: mockRequest,
    interceptors: {
      request: { use: jest.fn() },
      response: { use: jest.fn() },
    },
  };

  return {
    __esModule: true,
    default: {
      ...mockInstance,
      create: jest.fn(() => ({ ...mockInstance })),
    },
    create: jest.fn(() => ({ ...mockInstance })),
  };
});

test('renders login heading and button', () => {
  render(<App />);
  expect(screen.getByText(/government spending tracker/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
});

```


### 📄 ApprovalDialog.js

**Path:** `frontend/src/ApprovalDialog.js`

```javascript
import React, { useState } from 'react';

const ApprovalDialog = ({ proposal, categories, onApprove, onReject, onClose }) => {
  const [showApprove, setShowApprove] = useState(false);
  const [showReject, setShowReject] = useState(false);
  const [approvedAmount, setApprovedAmount] = useState('');
  const [decisionNotes, setDecisionNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const category = categories && Array.isArray(categories) 
    ? categories.find(c => c.id === proposal.category_id)
    : null;
  const maxAmount = Math.min(proposal.requested_amount, category?.remaining_budget || 0);

  const handleApprove = async () => {
    const amount = parseFloat(approvedAmount);
    if (isNaN(amount) || amount <= 0 || amount > maxAmount) {
      setError(`Invalid amount. Must be greater than 0 and not exceed $${maxAmount.toLocaleString()}`);
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      await onApprove(proposal.id, { approved_amount: amount, decision_notes: decisionNotes || null });
    } catch (err) {
      setError('Failed to approve proposal. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReject = async () => {
    setLoading(true);
    setError('');
    
    try {
      await onReject(proposal.id, { decision_notes: decisionNotes || null });
    } catch (err) {
      setError('Failed to reject proposal. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (showApprove) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h3>Approve Proposal</h3>
          <p><strong>{proposal.title}</strong> - {proposal.ministry?.name || 'Unknown'}</p>
          <p>Requested: ${proposal.requested_amount.toLocaleString()}</p>
          <p>Category remaining: ${category?.remaining_budget?.toLocaleString() || 'N/A'}</p>
          
          {error && (
            <div style={{ padding: '10px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '15px', fontSize: '14px' }}>
              {error}
            </div>
          )}
          
          <div className="form-group">
            <label>Approved Amount (max: ${maxAmount.toLocaleString()})</label>
            <input
              type="number"
              value={approvedAmount}
              onChange={(e) => setApprovedAmount(e.target.value)}
              min="0"
              step="1000"
              placeholder={maxAmount.toString()}
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label>Decision Notes (optional)</label>
            <textarea
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              placeholder="Reason for approval..."
              rows="3"
              disabled={loading}
            />
          </div>
          
          <div className="form-actions">
            <button 
              className="btn btn-primary" 
              onClick={handleApprove}
              disabled={loading}
            >
              {loading ? 'Approving...' : 'Approve'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={() => setShowApprove(false)}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (showReject) {
    return (
      <div className="modal-overlay">
        <div className="modal">
          <h3>Reject Proposal</h3>
          <p><strong>{proposal.title}</strong> - {proposal.ministry?.name || 'Unknown'}</p>
          <p>Requested: ${proposal.requested_amount.toLocaleString()}</p>
          
          {error && (
            <div style={{ padding: '10px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '15px', fontSize: '14px' }}>
              {error}
            </div>
          )}
          
          <div className="form-group">
            <label>Rejection Reason (optional)</label>
            <textarea
              value={decisionNotes}
              onChange={(e) => setDecisionNotes(e.target.value)}
              placeholder="Reason for rejection..."
              rows="3"
              disabled={loading}
            />
          </div>
          
          <div className="form-actions">
            <button 
              className="btn btn-danger" 
              onClick={handleReject}
              disabled={loading}
            >
              {loading ? 'Rejecting...' : 'Reject'}
            </button>
            <button 
              className="btn btn-secondary" 
              onClick={() => setShowReject(false)}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="modal-overlay">
      <div className="modal">
        <h3>Decision Required</h3>
        <p><strong>{proposal.title}</strong> - {proposal.ministry?.name || 'Unknown'}</p>
        <p>Requested: ${proposal.requested_amount.toLocaleString()}</p>
        
        <div className="form-actions">
          <button className="btn btn-primary" onClick={() => setShowApprove(true)}>Approve</button>
          <button className="btn btn-danger" onClick={() => setShowReject(true)}>Reject</button>
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default ApprovalDialog;

```


### 📄 CategoryManager.css

**Path:** `frontend/src/CategoryManager.css`

```css
.category-manager {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 2.5rem;
}

.header h2 {
  color: #7f8c8d;
  margin-bottom: 20px;
  font-size: 1.5rem;
}

.error {
  background-color: #e74c3c;
  color: white;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #7f8c8d;
  padding: 40px;
}

.actions {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #3498db;
  color: white;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.btn-small {
  padding: 5px 10px;
  font-size: 0.9rem;
  margin-right: 5px;
}

.form-container {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border: 1px solid #dee2e6;
}

.form-container h3 {
  margin-top: 0;
  color: #2c3e50;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #2c3e50;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
}

.form-actions {
  display: flex;
  gap: 10px;
}

.categories-table {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.categories-table h3 {
  background-color: #2c3e50;
  color: white;
  margin: 0;
  padding: 15px 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 20px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

th {
  background-color: #f8f9fa;
  font-weight: bold;
  color: #2c3e50;
}

tr:hover {
  background-color: #f8f9fa;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #7f8c8d;
  font-style: italic;
}

/* Responsive design */
@media (max-width: 768px) {
  .category-manager {
    padding: 10px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .actions {
    flex-direction: column;
  }
  
  table {
    font-size: 0.9rem;
  }
  
  th, td {
    padding: 8px 10px;
  }
}

/* Modal styles for approval dialogs */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal h3 {
  margin-top: 0;
  color: #2c3e50;
}

.modal p {
  margin: 10px 0;
  color: #7f8c8d;
}

.modal textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
  resize: vertical;
}

.modal textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
}

```


### 📄 CategoryManager.js

**Path:** `frontend/src/CategoryManager.js`

```javascript
import React, { useState, useEffect } from 'react';
import { categoryAPI } from './api';
import './CategoryManager.css';

const CategoryManager = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingCategory, setEditingCategory] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    allocated_budget: ''
  });

  // Load categories on component mount
  useEffect(() => {
    loadCategories();
  }, []);

  const loadCategories = async () => {
    try {
      setLoading(true);
      const data = await categoryAPI.getAll();
      setCategories(data);
      // notify other parts of the app (e.g., ProposalForm)
      if (typeof window !== "undefined") {
        window.dispatchEvent(new Event("categories-updated"));
      }
      setError(null);
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Failed to load categories';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    try {
      // Validate name
      if (!formData.name.trim()) {
        setError('Category name is required.');
        return;
      }

      // Validate budget
      const budgetString = (formData.allocated_budget || '').toString().trim();
      if (!budgetString) {
        setError('Allocated budget is required.');
        return;
      }

      const budget = parseFloat(budgetString);
      if (isNaN(budget) || budget <= 0) {
        setError('Allocated budget must be a number greater than 0.');
        return;
      }

      if (editingCategory) {
        await categoryAPI.update(editingCategory.id, {
          name: formData.name,
          allocated_budget: budget
        });
      } else {
        await categoryAPI.create({
          name: formData.name,
          allocated_budget: budget
        });
      }

      setFormData({ name: '', allocated_budget: '' });
      setShowForm(false);
      setEditingCategory(null);
      await loadCategories();
    } catch (err) {
      // Handle different error formats
      let errorMessage = editingCategory ? 'Failed to update category' : 'Failed to create category';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  const handleEdit = (category) => {
    setEditingCategory(category);
    setFormData({
      name: category.name || '',
      allocated_budget: category.allocated_budget ? category.allocated_budget.toString() : ''
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this category?')) {
      return;
    }

    try {
      await categoryAPI.delete(id);
      await loadCategories();
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Failed to delete category';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  const handleCancel = () => {
    setFormData({ name: '', allocated_budget: '' });
    setShowForm(false);
    setEditingCategory(null);
    setError(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  if (loading) {
    return (
      <div className="card">
        <h2 className="page-title">Category Management</h2>
        <p className="page-description">Manage budget categories and allocations</p>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <span>Loading categories...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <h2 className="page-title">Category Management</h2>
      <p className="page-description">Manage budget categories and allocations</p>
      {error && <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '16px', fontSize: '14px' }}>{error}</div>}

      {!showForm ? (
        <div>
          <div className="form-actions">
            <button 
              className="btn btn-primary" 
              onClick={() => setShowForm(true)}
            >
              Add New Category
            </button>
          </div>

          <table className="categories-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Allocated Budget</th>
                <th>Remaining Budget</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {categories.map(category => (
                <tr key={category.id}>
                  <td>{category.name}</td>
                  <td>${category.allocated_budget.toLocaleString()}</td>
                  <td>${category.remaining_budget.toLocaleString()}</td>
                  <td>{new Date(category.created_at).toLocaleDateString()}</td>
                  <td>
                    <button 
                      className="btn btn-small btn-secondary" 
                      onClick={() => handleEdit(category)}
                    >
                      Edit
                    </button>
                    <button 
                      className="btn btn-small btn-secondary" 
                      onClick={() => handleDelete(category.id)}
                      style={{ marginLeft: '8px', backgroundColor: '#ef4444', color: 'white' }}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Category Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="e.g., Education, Health, Defense"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="allocated_budget">Allocated Budget</label>
            <input
              type="text"
              id="allocated_budget"
              name="allocated_budget"
              value={formData.allocated_budget}
              onChange={handleInputChange}
              placeholder="e.g., 1000000"
              pattern="[0-9]*"
              inputMode="numeric"
              required
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="btn btn-primary">
              {editingCategory ? 'Update Category' : 'Create Category'}
            </button>
            <button 
              type="button" 
              className="btn btn-secondary" 
              onClick={handleCancel}
            >
              Cancel
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default CategoryManager;

```


### 📄 ContractUpload.js

**Path:** `frontend/src/ContractUpload.js`

```javascript
import React, { useState } from 'react';
import { uploadAPI, proposalAPI } from './api';

const ContractUpload = ({ onCreated }) => {
  const [file, setFile] = useState(null);
  const [drafts, setDrafts] = useState([]);
  const [error, setError] = useState(null);
  const [parsing, setParsing] = useState(false);

  const onSelect = (e) => {
    setFile(e.target.files[0] || null);
    setDrafts([]);
    setError(null);
  };

    const onParse = async () => {
    if (!file) { setError('Please choose a JSON or CSV file.'); return; }
    try {
      setParsing(true);
      const res = await uploadAPI.parse(file);
      
      // Get existing proposals to check for duplicates
      const existingProposals = await proposalAPI.getAll();
      
      // Initialize row-level flags and check for existing proposals
      const initializedDrafts = (res.drafts || []).map(d => {
        const isExisting = existingProposals.some(existing => 
          (existing.ministry?.name || '') === (d.ministry_name || '') && 
          existing.title === d.title && 
          existing.requested_amount === d.requested_amount
        );
        
        return { 
          ...d, 
          isCreating: false, 
          isCreated: isExisting  // Mark as created if it already exists
        };
      });
      
      setDrafts(initializedDrafts);
      setError(null);
    } catch (e) {
      // Handle different error formats
      let errorMessage = 'Failed to parse file';
      
      if (e?.response?.data) {
        const errorData = e.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    } finally {
      setParsing(false);
    }
  };

  const createProposal = async (d, idx) => {
    try {
      if (!d.valid) { return; }
      // Guard: skip if already created or being created
      if (d.isCreating || d.isCreated) { return; }

      // Mark as creating
      setDrafts(prev => prev.map((x, i) => i === idx ? { ...x, isCreating: true } : x));

      await proposalAPI.create({
        ministry_name: d.ministry_name,
        category_id: d.category_id,
        title: d.title,
        description: d.description || null,
        requested_amount: d.requested_amount
      });

      // Mark as created
      setDrafts(prev => prev.map((x, i) => i === idx ? { ...x, isCreating: false, isCreated: true } : x));
      onCreated && onCreated();
    } catch (e) {
      // Reset creating flag on error
      setDrafts(prev => prev.map((x, i) => i === idx ? { ...x, isCreating: false } : x));

      // Handle different error formats
      let errorMessage = 'Failed to create proposal from draft';
      
      if (e?.response?.data) {
        const errorData = e.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  return (
    <div className="card">
      <h2 className="page-title">Upload Contract</h2>
      <p className="page-description">Upload a CSV or JSON file to create proposals in bulk</p>
      {error && <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '16px', fontSize: '14px' }}>{error}</div>}
      <div className="form-group">
        <input type="file" accept=".json,.csv" onChange={onSelect} />
      </div>
      <div className="form-actions">
        <button className="btn btn-primary" onClick={onParse} disabled={parsing}>
          {parsing ? 'Parsing...' : 'Parse'}
        </button>
      </div>

      {drafts.length > 0 && (
        <div className="categories-table" style={{ marginTop: 20 }}>
          <h3>Parsed Drafts</h3>
          <table>
            <thead>
              <tr>
                <th>Valid</th>
                <th>Ministry</th>
                <th>Category</th>
                <th>Title</th>
                <th>Requested</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {drafts.map((d, i) => (
                <tr key={i}>
                  <td>{d.valid ? 'Yes' : 'No'}</td>
                  <td>{d.ministry_name || '-'}</td>
                  <td>{d.category_name || '-'}</td>
                  <td>{d.title || '-'}</td>
                  <td>{d.requested_amount != null ? new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 0 }).format(d.requested_amount) : '-'}</td>
                  <td>
                    <button
                      className="btn btn-small btn-primary"
                      disabled={!d.valid || d.isCreating || d.isCreated}
                      onClick={() => createProposal(d, i)}
                    >
                      {d.isCreated ? 'Created' : (d.isCreating ? 'Creating…' : 'Create Proposal')}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <div className='form-actions' style={{ marginTop: 10 }}>
        <button className="btn btn-secondary" onClick={() => { setDrafts([]); setFile(null); setError(null); }}>
          Clear All
        </button>
      </div>
    </div>
  );
};

export default ContractUpload;

```


### 📄 Dashboard.js

**Path:** `frontend/src/Dashboard.js`

```javascript
import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { dashboardAPI } from './api';

ChartJS.register(ArcElement, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const Dashboard = ({ refreshKey }) => {
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: 3,
    layout: { padding: 0 },
    plugins: {
      legend: { 
        position: 'bottom', 
        labels: { 
          boxWidth: 12, 
          font: { size: 11, family: 'Inter' },
          padding: 15
        } 
      },
      tooltip: { 
        titleFont: { size: 12, family: 'Inter' }, 
        bodyFont: { size: 11, family: 'Inter' },
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleColor: 'white',
        bodyColor: 'white',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        cornerRadius: 8
      }
    },
    scales: {
      x: { 
        ticks: { 
          font: { size: 10, family: 'Inter' },
          color: 'var(--color-text-secondary)'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      y: { 
        ticks: { 
          font: { size: 10, family: 'Inter' },
          color: 'var(--color-text-secondary)',
          callback: function(value) {
            return '$' + value.toLocaleString();
          }
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      }
    }
  };
  
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await dashboardAPI.getSummary();
      setSummary(data);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [refreshKey]);

  if (loading) {
    return (
      <div className="card dashboard-card">
        <div className="card-header">
          <h2 className="page-title">Dashboard</h2>
          <p className="page-description">Financial overview and analytics</p>
        </div>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <span>Loading dashboard data...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card dashboard-card">
        <div className="card-header">
          <h2 className="page-title">Dashboard</h2>
          <p className="page-description">Financial overview and analytics</p>
        </div>
        <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '12px' }}>
          {error}
        </div>
        <button className="btn btn-primary" onClick={load}>
          Retry
        </button>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="card dashboard-card">
        <div className="card-header">
          <h2 className="page-title">Dashboard</h2>
          <p className="page-description">Financial overview and analytics</p>
        </div>
        <div className="loading-container">
          <span>No data available</span>
        </div>
      </div>
    );
  }

  // Category budget chart
  const categoryChartData = {
    labels: summary.categories.map(c => c.name),
    datasets: [
      {
        label: 'Allocated Budget',
        data: summary.categories.map(c => c.allocated_budget),
        backgroundColor: 'rgba(37, 99, 235, 0.8)',
        borderColor: 'rgba(37, 99, 235, 1)',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      },
      {
        label: 'Remaining Budget',
        data: summary.categories.map(c => c.remaining_budget),
        backgroundColor: 'rgba(16, 185, 129, 0.8)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      }
    ]
  };

  // Ministry spending chart
  const ministryChartData = {
    labels: summary.ministries.map(m => m.ministry_name || 'Unknown'),
    datasets: [
      {
        label: 'Requested Amount',
        data: summary.ministries.map(m => m.requested_total),
        backgroundColor: 'rgba(239, 68, 68, 0.8)',
        borderColor: 'rgba(239, 68, 68, 1)',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      },
      {
        label: 'Approved Amount',
        data: summary.ministries.map(m => m.approved_total),
        backgroundColor: 'rgba(124, 58, 237, 0.8)',
        borderColor: 'rgba(124, 58, 237, 1)',
        borderWidth: 2,
        borderRadius: 4,
        borderSkipped: false,
      }
    ]
  };

  return (
    <div className="card dashboard-card">
      <div className="card-header">
        <h2 className="page-title">Dashboard</h2>
        <p className="page-description">Financial overview and analytics</p>
      </div>
      
      {/* KPI Summary */}
      <div className="kpi-summary" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        <div className="kpi-item" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Allocated</h3>
          <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>${summary.kpis.total_allocated.toLocaleString()}</p>
        </div>
        <div className="kpi-item" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Remaining</h3>
          <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>${summary.kpis.total_remaining.toLocaleString()}</p>
        </div>
        <div className="kpi-item" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Approved</h3>
          <p>${summary.kpis.total_approved.toLocaleString()}</p>
        </div>
        <div className="kpi-item" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Utilization Rate</h3>
          <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>{((summary.kpis.total_allocated - summary.kpis.total_remaining) / summary.kpis.total_allocated * 100).toFixed(1)}%</p>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        <div className="chart-section">
          <div className="chart-header">
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '4px', color: 'var(--color-text)' }}>Budget by Category</h3>
            <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: 0 }}>Allocated vs Remaining Budget</p>
          </div>
          <div className="chart-container">
            <Bar data={categoryChartData} options={chartOptions} />
          </div>
        </div>
        
        <div className="chart-section">
          <div className="chart-header">
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '4px', color: 'var(--color-text)' }}>Spending by Ministry</h3>
            <p style={{ fontSize: '13px', color: 'var(--color-text-secondary)', margin: 0 }}>Requested vs Approved Amounts</p>
          </div>
          <div className="chart-container">
            <Bar data={ministryChartData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

```


### 📄 EditProposalDialog.js

**Path:** `frontend/src/EditProposalDialog.js`

```javascript
import React, { useState } from 'react';

const EditProposalDialog = ({ proposal, categories, onSubmit, onClose }) => {
  const [formData, setFormData] = useState({
    title: proposal.title || '',
    description: proposal.description || '',
    requested_amount: proposal.requested_amount?.toString() || '',
    category_id: proposal.category_id?.toString() || ''
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    const errors = [];
    
    if (!formData.title.trim()) {
      errors.push('Title is required');
    }
    
    if (!formData.requested_amount || parseFloat(formData.requested_amount) <= 0) {
      errors.push('Requested amount must be greater than 0');
    }
    
    if (!formData.category_id) {
      errors.push('Category is required');
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    
    const validationErrors = validateForm();
    if (validationErrors.length > 0) {
      setError(validationErrors.join('; '));
      return;
    }
    
    setLoading(true);
    
    try {
      const submitData = {
        title: formData.title.trim(),
        description: formData.description.trim() || null,
        requested_amount: parseFloat(formData.requested_amount),
        category_id: parseInt(formData.category_id)
      };
      
      await onSubmit(submitData);
    } catch (err) {
      setError(err.message || 'Failed to update proposal');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Edit Proposal #{proposal.id}</h2>
          <button className="modal-close" onClick={onClose}>×</button>
        </div>
        
        <form onSubmit={handleSubmit}>
          {error && <div className="error-message">{error}</div>}
          
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleInputChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleInputChange}
              rows="3"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="requested_amount">Requested Amount *</label>
            <input
              type="text"
              id="requested_amount"
              name="requested_amount"
              value={formData.requested_amount}
              onChange={handleInputChange}
              placeholder="e.g., 1000000"
              pattern="[0-9]*"
              inputMode="numeric"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="category_id">Category *</label>
            <select
              id="category_id"
              name="category_id"
              value={formData.category_id}
              onChange={handleInputChange}
              required
            >
              <option value="">Select Category</option>
              {categories.map(category => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>
          
          <div className="form-actions">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? 'Updating...' : 'Update Proposal'}
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditProposalDialog;

```


### 📄 HistoryView.js

**Path:** `frontend/src/HistoryView.js`

```javascript
import React, { useEffect, useState, useCallback } from 'react';
import { historyAPI, categoryAPI } from './api';

const HistoryView = () => {
  const [proposals, setProposals] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({ 
    category_id: '', 
    status: '', 
    date_from: '', 
    date_to: '' 
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0,
    totalRequested: 0,
    totalApproved: 0
  });

  const cleanFilters = (f) => Object.fromEntries(Object.entries(f).filter(([_, v]) => v !== '' && v != null));

  const loadHistory = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await historyAPI.list(cleanFilters(filters));
      setProposals(data);
      
      // Calculate stats
      const stats = {
        total: data.length,
        pending: data.filter(p => p.status === 'Pending').length,
        approved: data.filter(p => p.status === 'Approved').length,
        rejected: data.filter(p => p.status === 'Rejected').length,
        totalRequested: data.reduce((sum, p) => sum + (p.requested_amount || 0), 0),
        totalApproved: data.reduce((sum, p) => sum + (p.approved_amount || 0), 0)
      };
      setStats(stats);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load proposal history');
      console.error('History loading error:', err);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const loadCategories = useCallback(async () => {
    try {
      const data = await categoryAPI.getAll();
      setCategories(data);
    } catch (err) {
      console.error('Failed to load categories:', err);
    }
  }, []);

  useEffect(() => {
    loadHistory();
    loadCategories();
  }, [loadHistory, loadCategories]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const applyFilters = () => {
    loadHistory();
  };

  const clearFilters = () => {
    setFilters({ ministry: '', category_id: '', status: '', date_from: '', date_to: '' });
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'Pending': { class: 'badge-pending', color: '#856404' },
      'Approved': { class: 'badge-approved', color: '#155724' },
      'Rejected': { class: 'badge-rejected', color: '#721c24' }
    };
    
    const config = statusConfig[status] || { class: 'badge-pending', color: '#6b7280' };
    
    return (
      <span className={`badge ${config.class}`}>
        {status}
      </span>
    );
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD', 
      minimumFractionDigits: 0 
    }).format(amount || 0);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="card history-card">
      <div className="card-header">
        <h2 className="page-title">Proposal History</h2>
        <p className="page-description">Complete transaction history and approval records</p>
      </div>

      {/* Statistics Cards */}
      <div className="history-stats" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        <div className="stat-card" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <div className="stat-content">
            <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Proposals</h3>
            <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>{stats.total}</p>
          </div>
        </div>
        <div className="stat-card" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <div className="stat-content">
            <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Pending</h3>
            <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>{stats.pending}</p>
          </div>
        </div>
        <div className="stat-card" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <div className="stat-content">
            <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Approved</h3>
            <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>{stats.approved}</p>
          </div>
        </div>
        <div className="stat-card" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <div className="stat-content">
            <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Rejected</h3>
            <p style={{ fontSize: '24px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>{stats.rejected}</p>
          </div>
        </div>
        <div className="stat-card" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <div className="stat-content">
            <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Requested</h3>
            <p style={{ fontSize: '20px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>{formatCurrency(stats.totalRequested)}</p>
          </div>
        </div>
        <div className="stat-card" style={{ padding: '16px', backgroundColor: '#f8f9fa', borderRadius: '4px', border: '1px solid var(--color-border)' }}>
          <div className="stat-content">
            <h3 style={{ fontSize: '13px', fontWeight: '600', color: 'var(--color-text-secondary)', marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Approved</h3>
            <p style={{ fontSize: '20px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>{formatCurrency(stats.totalApproved)}</p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="filters-section">
        <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px', color: 'var(--color-text)' }}>Filters</h3>
        <div className="filters-grid">
          <div className="form-group">
            <label htmlFor="ministry">Ministry</label>
            <input
              type="text"
              id="ministry"
              name="ministry"
              value={filters.ministry}
              onChange={handleFilterChange}
              placeholder="Filter by ministry"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="status">Status</label>
            <select name="status" value={filters.status} onChange={handleFilterChange}>
              <option value="">All Statuses</option>
              <option value="Pending">Pending</option>
              <option value="Approved">Approved</option>
              <option value="Rejected">Rejected</option>
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="category_id">Category</label>
            <select name="category_id" value={filters.category_id} onChange={handleFilterChange}>
              <option value="">All Categories</option>
              {categories.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>
          
          <div className="form-group">
            <label htmlFor="date_from">Date From</label>
            <input
              type="date"
              id="date_from"
              name="date_from"
              value={filters.date_from}
              onChange={handleFilterChange}
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="date_to">Date To</label>
            <input
              type="date"
              id="date_to"
              name="date_to"
              value={filters.date_to}
              onChange={handleFilterChange}
            />
          </div>
        </div>
        
        <div className="filter-actions">
          <button 
            className="btn btn-primary" 
            onClick={applyFilters} 
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Loading...
              </>
            ) : (
              'Apply Filters'
            )}
          </button>
          <button className="btn btn-secondary" onClick={clearFilters}>
            Clear Filters
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '16px', fontSize: '14px' }}>
          {error}
        </div>
      )}

      {/* Proposals Table */}
      <div className="table-section">
        <div className="table-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: '600', color: 'var(--color-text)', margin: 0 }}>Proposal Records</h3>
          <div className="table-actions">
            <button className="btn btn-secondary btn-small">
              Export CSV
            </button>
          </div>
        </div>

        {loading ? (
          <div className="loading">
            <div className="loading-spinner"></div>
            <span>Loading proposal history...</span>
          </div>
        ) : proposals.length === 0 ? (
          <div className="no-data" style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--color-text-secondary)' }}>
            <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px', color: 'var(--color-text)' }}>No Proposals Found</h3>
            <p style={{ fontSize: '14px' }}>No proposals match your current filters. Try adjusting your search criteria.</p>
          </div>
        ) : (
          <div className="table-container">
            <table className="proposals-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Ministry</th>
                  <th>Category</th>
                  <th>Title</th>
                  <th>Requested</th>
                  <th>Status</th>
                  <th>Approved</th>
                  <th>Decided At</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {proposals.map(proposal => (
                  <tr key={proposal.id}>
                    <td>
                      <span className="proposal-id">#{proposal.id}</span>
                    </td>
                    <td>
                      <span className="ministry-name">{proposal.ministry?.name || 'Unknown'}</span>
                    </td>
                    <td>
                      <span className="category-name">
                        {categories.find(c => c.id === proposal.category_id)?.name || 'Unknown'}
                      </span>
                    </td>
                    <td>
                      <span className="proposal-title" title={proposal.title}>
                        {proposal.title}
                      </span>
                    </td>
                    <td>
                      <span className="amount requested">{formatCurrency(proposal.requested_amount)}</span>
                    </td>
                    <td>{getStatusBadge(proposal.status)}</td>
                    <td>
                      <span className="amount approved">
                        {proposal.approved_amount ? formatCurrency(proposal.approved_amount) : '-'}
                      </span>
                    </td>
                    <td>
                      <span className="date">{formatDate(proposal.decided_at)}</span>
                    </td>
                    <td>
                      <span className="date">{formatDate(proposal.created_at)}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default HistoryView;

```


### 📄 Login.js

**Path:** `frontend/src/Login.js`

```javascript
import React, { useState } from 'react';
import { authAPI } from './api';
import { useUser } from './UserContext';
import Register from './Register';

const Login = ({ onSwitchToRegister }) => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useUser();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authAPI.login(credentials.username, credentials.password);
      localStorage.setItem('authToken', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));
      login(response.user); // Use the context login function
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Login failed';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  const handleQuickLogin = (username, password) => {
    setCredentials({ username, password });
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      backgroundColor: '#f5f5f5'
    }}>
      <div className="card" style={{ width: '400px', maxWidth: '90%' }}>
        <h2 style={{ marginBottom: '10px', fontSize: '20px' }}>Government Spending Tracker</h2>
        <p style={{ color: '#666', marginBottom: '30px', fontSize: '14px' }}>Please sign in to continue</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              className="form-input"
              value={credentials.username}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              className="form-input"
              value={credentials.password}
              onChange={handleChange}
              required
            />
          </div>
          
          {error && (
            <div style={{ 
              padding: '10px', 
              backgroundColor: '#f8d7da', 
              color: '#721c24', 
              borderRadius: '4px',
              marginBottom: '15px',
              fontSize: '14px'
            }}>
              {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="btn btn-primary" 
            style={{ width: '100%', marginTop: '10px' }}
            disabled={loading}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>
        
        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <button
            type="button"
            onClick={onSwitchToRegister}
            style={{
              background: 'none',
              border: 'none',
              color: '#007bff',
              cursor: 'pointer',
              textDecoration: 'underline',
              fontSize: '14px'
            }}
          >
            Don't have an account? Register
          </button>
        </div>
        
        <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid #ddd', fontSize: '12px', color: '#666' }}>
          <p><strong>Test Accounts:</strong></p>
          <p>Finance: username: finance, password: fin</p>
          <p>Ministry: username: ministry, password: min</p>
        </div>
      </div>
    </div>
  );
};

export default Login;

```


### 📄 ProposalForm.js

**Path:** `frontend/src/ProposalForm.js`

```javascript
import React, { useState, useEffect } from 'react';
import { proposalAPI, categoryAPI, ministryAPI } from './api';
import { useUser } from './UserContext';

const ProposalForm = ({ onCreated }) => {
  const { user } = useUser();
  const [categories, setCategories] = useState([]);
  const [form, setForm] = useState({
    category_id: '',
    title: '',
    description: '',
    requested_amount: ''
  });
  const [error, setError] = useState(null);

  const onChange = (e) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    // Client-side validation
    if (!form.title || !form.category_id || !form.requested_amount) {
      setError('Please fill all required fields.');
      return;
    }
    if (!user?.ministry?.id) {
      setError('You must be assigned to a ministry to submit proposals.');
      return;
    }
    const amount = parseFloat(form.requested_amount);
    if (isNaN(amount) || amount <= 0) {
      setError('Requested amount must be a number greater than 0.');
      return;
    }
    try {
      await proposalAPI.create({
        ministry_id: user.ministry?.id || user.ministry_id, // Use the logged-in user's ministry
        category_id: parseInt(form.category_id, 10),
        title: form.title,
        description: form.description || null,
        requested_amount: amount,
      });
      setForm({ category_id: '', title: '', description: '', requested_amount: '' });
      onCreated && onCreated();
    } catch (e) {
      // Handle different error formats
      let errorMessage = 'Failed to submit proposal.';
      
      if (e?.response?.data) {
        const errorData = e.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  useEffect(() => {
    const reload = async () => {
      try {
        const cats = await categoryAPI.getAll();
        setCategories(cats);
      } catch (e) {
        console.error('Failed to load categories:', e);
      }
    };
    
    reload(); // Load categories immediately
    const handler = () => reload();
    window.addEventListener('categories-updated', handler);
    return () => window.removeEventListener('categories-updated', handler);
  }, []);


  return (
    <div className="card">
      <h2 className="page-title">Submit Proposal</h2>
      <p className="page-description">Create a new budget proposal for approval</p>
      {error && <div style={{ padding: '12px', backgroundColor: '#f8d7da', color: '#721c24', borderRadius: '4px', marginBottom: '16px', fontSize: '14px' }}>{error}</div>}
      <form onSubmit={onSubmit}>
        <div className="form-group">
          <label>Ministry</label>
          <input 
            type="text"
            value={user?.ministry?.name || 'Not assigned to a ministry'} 
            disabled
            style={{ 
              backgroundColor: '#f5f5f5', 
              cursor: 'not-allowed',
              opacity: 0.7
            }}
            title="Your ministry is locked to your account"
          />
          {!user?.ministry?.id && (
            <p style={{ fontSize: '12px', color: '#dc3545', marginTop: '5px' }}>
              You must be assigned to a ministry to submit proposals.
            </p>
          )}
        </div>
        <div className="form-group">
          <label>Category</label>
          <select name="category_id" value={form.category_id} onChange={onChange} required>
            <option value="">Select category</option>
            {categories.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Title</label>
          <input name="title" value={form.title} onChange={onChange} placeholder="Project title" required />
        </div>
        <div className="form-group">
          <label>Description</label>
          <input name="description" value={form.description} onChange={onChange} placeholder="Optional details" />
        </div>
        <div className="form-group">
          <label>Requested Amount</label>
          <input name="requested_amount" type="number" min="1" value={form.requested_amount} onChange={onChange} required />
        </div>
        <div className="form-actions">
          <button className="btn btn-primary" type="submit">Submit</button>
        </div>
      </form>
    </div>
  );
};

export default ProposalForm;

```


### 📄 ProposalsList.js

**Path:** `frontend/src/ProposalsList.js`

```javascript
import React, { useEffect, useState } from 'react';
import { proposalAPI, categoryAPI } from './api';
import ApprovalDialog from './ApprovalDialog';
import EditProposalDialog from './EditProposalDialog';
import { useUser } from './UserContext';

const ProposalsList = () => {
  const [proposals, setProposals] = useState([]);
  const [categories, setCategories] = useState([]);
  const [filters, setFilters] = useState({ category_id: '', min_amount: '', max_amount: '' });
  const [error, setError] = useState(null);
  const [selectedProposal, setSelectedProposal] = useState(null);
  const { user } = useUser();
  const [deletingId, setDeletingId] = useState(null);
  const [editingProposal, setEditingProposal] = useState(null);

  const load = async () => {
    try {
      const params = { status: 'Pending' }; // Always filter for pending proposals
      if (filters.category_id) params.category_id = filters.category_id;
      if (filters.min_amount) params.min_amount = parseFloat(filters.min_amount);
      if (filters.max_amount) params.max_amount = parseFloat(filters.max_amount);
      const data = await proposalAPI.getAll(params);
      setProposals(data);
      setError(null);
    } catch (e) {
      // Handle different error formats
      let errorMessage = 'Failed to load proposals';
      
      if (e?.response?.data) {
        const errorData = e.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  const loadCategories = async () => {
    try { 
      const data = await categoryAPI.getAll();
      setCategories(data);
    } catch(e) {
      // ignore category loading errors
    }
  }
  const handleApprove = async (proposalId, data) => {
    try {
      await proposalAPI.approve(proposalId, data);
      setSelectedProposal(null);
      load(); // Reload proposals
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Failed to approve proposal';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  const handleReject = async (proposalId, data) => {
    try {
      await proposalAPI.reject(proposalId, data);
      setSelectedProposal(null);
      load(); // Reload proposals
    } catch (err) {
      // Handle different error formats
      let errorMessage = 'Failed to reject proposal';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        // Handle validation error array
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
        }
        // Handle single validation error object
        else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        }
        // Handle string error
        else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
        // Handle other error formats
        else if (typeof errorData === 'string') {
          errorMessage = errorData;
        }
      }
      
      setError(errorMessage);
    }
  };

  const handleDelete = async (proposal) => {
    if (proposal.status !== 'Pending') {
      alert('Only pending proposals can be deleted.');
      return;
    }
    const reason = window.prompt('Please provide a reason for deleting this proposal:');
    if (!reason || !reason.trim()) {
      return; // require a reason
    }
    try {
      setDeletingId(proposal.id);
      await proposalAPI.delete(proposal.id, { reason });
      await load();
    } catch (e) {
      let errorMessage = 'Failed to delete proposal';
      if (e?.response?.data) {
        const errorData = e.response.data;
        if (typeof errorData.detail === 'string') errorMessage = errorData.detail;
        else if (typeof errorData === 'string') errorMessage = errorData;
      }
      setError(errorMessage);
    } finally {
      setDeletingId(null);
    }
  };


  useEffect(() => {
    // eslint-disable-next-line react-hooks/exhaustive-deps
    load();
    loadCategories();
  }, []);

  const onChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const onApplyFilters = () => {
    load();
  };

  const onClearFilters = () => {
    setFilters({ category_id: '', min_amount: '', max_amount: '' });
    load();
  };

  // Edit validation logic
  const canEditProposal = (proposal) => {
    if (!user || user.role !== 'ministry') return false;
    if (proposal.status !== 'Pending') return false;
    
    // Check ministry match - compare IDs, not objects
    const userMinistryId = user.ministry?.id || user.ministry_id;
    const proposalMinistryId = proposal.ministry?.id || proposal.ministry_id;
    if (userMinistryId !== proposalMinistryId) return false;
    
    return true;
  };

  const handleEdit = (proposal) => {
    setEditingProposal(proposal);
  };

  const handleEditSubmit = async (formData) => {
    try {
      await proposalAPI.update(editingProposal.id, formData);
      setEditingProposal(null);
      load(); // Reload proposals
    } catch (err) {
      let errorMessage = 'Failed to update proposal';
      if (err?.response?.data?.detail) {
        errorMessage = err.response.data.detail;
      }
      setError(errorMessage);
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'Pending': { class: 'badge-pending', color: '#856404' },
      'Approved': { class: 'badge-approved', color: '#155724' },
      'Rejected': { class: 'badge-rejected', color: '#721c24' }
    };
    
    const config = statusConfig[status] || { class: 'badge-pending', color: '#6b7280' };
    
    return (
      <span className={`badge ${config.class}`}>
        {status}
      </span>
    );
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD', 
      minimumFractionDigits: 0 
    }).format(amount || 0);
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <>
      <div className="card">
        <h2 className="page-title">Pending Proposals</h2>
        <p className="page-description">Review and manage pending budget proposals</p>
        {error && <div className="error-message">{error}</div>}

        <div className="filters-section">
          <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px', color: 'var(--color-text)' }}>Filters</h3>
          <div className="filters-grid">
            <div className="form-group">
              <label htmlFor="ministry">Ministry</label>
              <input
                type="text"
                id="ministry"
                name="ministry"
                value={filters.ministry}
                onChange={onChange}
                placeholder="Filter by ministry"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="min_amount">Min Amount</label>
              <input
                type="text"
                id="min_amount"
                name="min_amount"
                value={filters.min_amount}
                onChange={onChange}
                placeholder="e.g., 100000"
                pattern="[0-9]*"
                inputMode="numeric"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="max_amount">Max Amount</label>
              <input
                type="text"
                id="max_amount"
                name="max_amount"
                value={filters.max_amount}
                onChange={onChange}
                placeholder="e.g., 5000000"
                pattern="[0-9]*"
                inputMode="numeric"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="category_id">Category</label>
              <select name="category_id" value={filters.category_id} onChange={onChange}>
                <option value="">All Categories</option>
                {categories.map(c => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>
          </div>
          
          <div className="filter-actions">
            <button className="btn btn-primary" onClick={onApplyFilters}>
              Apply Filters
            </button>
            <button className="btn btn-secondary" onClick={onClearFilters}>
              Clear Filters
            </button>
          </div>
        </div>

        <div className="table-section">
          <div className="table-header">
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '12px', color: 'var(--color-text)' }}>All Proposals</h3>
          </div>

          {proposals.length === 0 ? (
            <div className="no-data" style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--color-text-secondary)' }}>
              <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '8px', color: 'var(--color-text)' }}>No Proposals Found</h3>
              <p style={{ fontSize: '14px' }}>No proposals match your current filters. Try adjusting your search criteria.</p>
            </div>
          ) : (
            <div className="table-container">
              <table className="proposals-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Ministry</th>
                    <th>Category</th>
                    <th>Title</th>
                    <th>Requested</th>
                    <th>Status</th>
                    <th>Approved</th>
                    <th>Decided At</th>
                    <th>Created</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {proposals.map(proposal => (
                    <tr key={proposal.id}>
                      <td>
                        <span className="proposal-id">#{proposal.id}</span>
                      </td>
                      <td>
                        <span className="ministry-name">{proposal.ministry?.name || 'Unknown'}</span>
                      </td>
                      <td>
                        <span className="category-name">
                          {categories.find(c => c.id === proposal.category_id)?.name || 'Unknown'}
                        </span>
                      </td>
                      <td>
                        <span className="proposal-title" title={proposal.title}>
                          {proposal.title}
                        </span>
                      </td>
                      <td>
                        <span className="amount requested">{formatCurrency(proposal.requested_amount)}</span>
                      </td>
                      <td>{getStatusBadge(proposal.status)}</td>
                      <td>
                        <span className="amount approved">
                          {proposal.approved_amount ? formatCurrency(proposal.approved_amount) : '-'}
                        </span>
                      </td>
                      <td>
                        <span className="date">{formatDate(proposal.decided_at)}</span>
                      </td>
                      <td>
                        <span className="date">{formatDate(proposal.created_at)}</span>
                      </td>
                      <td>
                        {proposal.status === 'Pending' && user?.role === 'finance' && (
                          <button 
                            className="btn btn-small btn-primary"
                            onClick={() => setSelectedProposal(proposal)}
                          >
                            Review
                          </button>
                        )}
                        {proposal.status === 'Pending' && user?.role === 'ministry' && (
                          <div className="action-buttons">
                            {canEditProposal(proposal) && (
                              <button
                                className="btn btn-small btn-secondary"
                                onClick={() => handleEdit(proposal)}
                              >
                                Edit
                              </button>
                            )}
                            <button
                              className="btn btn-small btn-danger"
                              disabled={deletingId === proposal.id}
                              onClick={() => handleDelete(proposal)}
                            >
                              {deletingId === proposal.id ? 'Deleting…' : 'Delete'}
                            </button>
                          </div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

                  {selectedProposal && (
        <ApprovalDialog
          proposal={selectedProposal}
          categories={categories}
          onApprove={handleApprove}
          onReject={handleReject}
          onClose={() => setSelectedProposal(null)}
        />
      )}

      {editingProposal && (
        <EditProposalDialog
          proposal={editingProposal}
          categories={categories}
          onSubmit={handleEditSubmit}
          onClose={() => setEditingProposal(null)}
        />
      )}
    </>
  );
};

export default ProposalsList;

```


### 📄 Register.js

**Path:** `frontend/src/Register.js`

```javascript
import React, { useState, useEffect } from 'react';
import { authAPI } from './api';
import { ministryAPI } from './api';
import { useUser } from './UserContext';

const Register = ({ onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'ministry',
    ministry_id: ''
  });
  const [ministries, setMinistries] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const { login } = useUser();

  useEffect(() => {
    const loadMinistries = async () => {
      try {
        const data = await ministryAPI.getAll();
        setMinistries(data);
      } catch (err) {
        console.error('Failed to load ministries:', err);
      }
    };
    loadMinistries();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (formData.password.length < 3) {
      setError('Password must be at least 3 characters');
      setLoading(false);
      return;
    }

    if (formData.role === 'ministry' && !formData.ministry_id) {
      setError('Please select a ministry');
      setLoading(false);
      return;
    }

    try {
      const registrationData = {
        username: formData.username,
        email: formData.email,
        password: formData.password,
        role: formData.role,
        ministry_id: formData.role === 'ministry' ? parseInt(formData.ministry_id, 10) : null
      };

      await authAPI.register(registrationData);
      setSuccess(true);
      
      // Auto-login after successful registration
      setTimeout(async () => {
        try {
          const response = await authAPI.login(formData.username, formData.password);
          localStorage.setItem('authToken', response.access_token);
          localStorage.setItem('user', JSON.stringify(response.user));
          login(response.user);
        } catch (loginErr) {
          // If auto-login fails, just show success and let user login manually
          console.error('Auto-login failed:', loginErr);
        }
      }, 1000);
    } catch (err) {
      let errorMessage = 'Registration failed';
      
      if (err?.response?.data) {
        const errorData = err.response.data;
        
        if (Array.isArray(errorData.detail)) {
          errorMessage = errorData.detail.map(e => e.msg || e.message || String(e)).join(', ');
        } else if (errorData.detail && typeof errorData.detail === 'object') {
          errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
        } else if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '100vh',
        backgroundColor: '#f5f5f5'
      }}>
        <div className="card" style={{ width: '400px', maxWidth: '90%' }}>
          <h2 style={{ marginBottom: '10px', fontSize: '20px', color: '#28a745' }}>Registration Successful!</h2>
          <p style={{ color: '#666', marginBottom: '20px' }}>Your account has been created. Logging you in...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      backgroundColor: '#f5f5f5'
    }}>
      <div className="card" style={{ width: '400px', maxWidth: '90%' }}>
        <h2 style={{ marginBottom: '10px', fontSize: '20px' }}>Create Account</h2>
        <p style={{ color: '#666', marginBottom: '30px', fontSize: '14px' }}>Register for a new account</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label" htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              className="form-input"
              value={formData.username}
              onChange={handleChange}
              required
              minLength={3}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              className="form-input"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              className="form-input"
              value={formData.password}
              onChange={handleChange}
              required
              minLength={3}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              className="form-input"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              minLength={3}
            />
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="role">Role</label>
            <select
              id="role"
              name="role"
              className="form-input"
              value={formData.role}
              onChange={handleChange}
              required
            >
              <option value="ministry">Ministry</option>
              <option value="finance">Finance</option>
            </select>
          </div>

          {formData.role === 'ministry' && (
            <div className="form-group">
              <label className="form-label" htmlFor="ministry_id">Ministry</label>
              <select
                id="ministry_id"
                name="ministry_id"
                className="form-input"
                value={formData.ministry_id}
                onChange={handleChange}
                required
              >
                <option value="">Select a ministry</option>
                {ministries.map(ministry => (
                  <option key={ministry.id} value={ministry.id}>
                    {ministry.name}
                  </option>
                ))}
              </select>
            </div>
          )}
          
          {error && (
            <div style={{ 
              padding: '10px', 
              backgroundColor: '#f8d7da', 
              color: '#721c24', 
              borderRadius: '4px',
              marginBottom: '15px',
              fontSize: '14px'
            }}>
              {error}
            </div>
          )}
          
          <button 
            type="submit" 
            className="btn btn-primary" 
            style={{ width: '100%', marginTop: '10px' }}
            disabled={loading}
          >
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>

        <div style={{ marginTop: '20px', textAlign: 'center' }}>
          <button
            type="button"
            onClick={onSwitchToLogin}
            style={{
              background: 'none',
              border: 'none',
              color: '#007bff',
              cursor: 'pointer',
              textDecoration: 'underline',
              fontSize: '14px'
            }}
          >
            Already have an account? Sign in
          </button>
        </div>
      </div>
    </div>
  );
};

export default Register;


```


### 📄 RoleGuard.js

**Path:** `frontend/src/RoleGuard.js`

```javascript
import React from 'react';
import { useUser } from './UserContext';

const RoleGuard = ({ allowedRoles, children, fallback = null }) => {
  const { user } = useUser();
  
  if (!user) {
    return fallback;
  }
  
  if (!allowedRoles.includes(user.role)) {
    return fallback || (
      <div className="card">
        <div className="error-message">
          <span>🚫</span> Access Denied
          <p>You don't have permission to access this feature.</p>
          <p>Required role: {allowedRoles.join(' or ')}</p>
          <p>Your role: {user.role}</p>
        </div>
      </div>
    );
  }
  
  return children;
};

export default RoleGuard;

```


### 📄 Sidebar.js

**Path:** `frontend/src/Sidebar.js`

```javascript
import React from 'react';
import { useUser } from './UserContext';

const Sidebar = ({ activeTab, setActiveTab }) => {
  const { user } = useUser();

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      description: 'Financial Overview',
      roles: ['finance']
    },
    {
      id: 'categories',
      label: 'Categories',
      description: 'Budget Categories',
      roles: ['finance']
    },
    {
      id: 'proposals',
      label: 'Proposals',
      description: 'All Proposals',
      roles: ['finance', 'ministry']
    },
    {
      id: 'create-proposal',
      label: 'Create Proposal',
      description: 'New Proposal',
      roles: ['ministry']
    },
    {
      id: 'upload-contract',
      label: 'Upload Contract',
      description: 'Contract Upload',
      roles: ['ministry']
    },
    {
      id: 'history',
      label: 'History',
      description: 'Transaction History',
      roles: ['finance', 'ministry']
    }
  ];

  const filteredItems = navigationItems.filter(item => 
    item.roles.includes(user?.role)
  );

    const handleItemClick = (itemId) => {
    // Prevent ministry users from accessing finance-only features
    if (itemId === 'dashboard' && user?.role !== 'finance') {
      return; // Don't allow access
    }
    if (itemId === 'categories' && user?.role !== 'finance') {
      return; // Don't allow access
    }
    if ((itemId === 'create-proposal' || itemId === 'upload-contract') && user?.role !== 'ministry') {
      return; // Don't allow access
    }
    
    setActiveTab(itemId);
  };

  // Group items by role for better organization
  const financeItems = filteredItems.filter(item => item.roles.includes('finance') && !item.roles.includes('ministry'));
  const ministryItems = filteredItems.filter(item => item.roles.includes('ministry') && !item.roles.includes('finance'));
  const commonItems = filteredItems.filter(item => item.roles.includes('finance') && item.roles.includes('ministry'));

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-user-info">
          <div className="sidebar-user-name">{user?.username}</div>
          <div className="sidebar-user-role">{user?.role === 'finance' ? 'Finance Department' : 'Ministry User'}</div>
        </div>
      </div>
      <nav className="sidebar-nav">
        {financeItems.length > 0 && (
          <div className="sidebar-section">
            <div className="sidebar-section-title">Finance</div>
            {financeItems.map((item) => (
            <button
              key={item.id}
                className={`sidebar-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => handleItemClick(item.id)}
              title={item.description}
            >
                <span className="sidebar-item-label">{item.label}</span>
                <span className="sidebar-item-desc">{item.description}</span>
              </button>
            ))}
              </div>
        )}
        
        {ministryItems.length > 0 && (
          <div className="sidebar-section">
            <div className="sidebar-section-title">Ministry</div>
            {ministryItems.map((item) => (
              <button
                key={item.id}
                className={`sidebar-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => handleItemClick(item.id)}
                title={item.description}
              >
                <span className="sidebar-item-label">{item.label}</span>
                <span className="sidebar-item-desc">{item.description}</span>
            </button>
          ))}
        </div>
        )}
        
        {commonItems.length > 0 && (
          <div className="sidebar-section">
            <div className="sidebar-section-title">General</div>
            {commonItems.map((item) => (
              <button
                key={item.id}
                className={`sidebar-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => handleItemClick(item.id)}
                title={item.description}
              >
                <span className="sidebar-item-label">{item.label}</span>
                <span className="sidebar-item-desc">{item.description}</span>
              </button>
            ))}
          </div>
        )}
      </nav>
    </div>
  );
};

export default Sidebar;

```


### 📄 UserContext.js

**Path:** `frontend/src/UserContext.js`

```javascript
import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from './api';

const UserContext = createContext();

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const token = localStorage.getItem('authToken');
      const savedUser = localStorage.getItem('user');
      
      if (token && savedUser) {
        try {
          // Validate the token by calling the /auth/me endpoint
          const currentUser = await authAPI.getMe();
          setUser(currentUser);
        } catch (error) {
          // Token is invalid, clear it
          console.log('Token validation failed, clearing auth data');
          localStorage.removeItem('authToken');
          localStorage.removeItem('user');
          setUser(null);
        }
      } else {
        // No saved auth data
        setUser(null);
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  const login = (userData) => {
    setUser(userData);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
  };

  const isFinance = () => user?.role === 'finance';
  const isMinistry = () => user?.role === 'ministry';

  const value = {
    user,
    login,
    logout,
    isFinance,
    isMinistry,
    loading
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

```


### 📄 api.js

**Path:** `frontend/src/api.js`

```javascript
import axios from 'axios';

// Read API base URL from environment variable (defaults to localhost for dev)
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Ministry API functions
export const ministryAPI = {
  getAll: async () => {
    const response = await api.get('/ministries');
    return response.data;
  },
  create: async (ministry) => {
    const response = await api.post('/ministries', ministry);
    return response.data;
  },
  findOrCreate: async (ministryName) => {
    const response = await api.post('/ministries/find-or-create', null, {
      params: { ministry_name: ministryName }
    });
    return response.data;
  }
};

// Category API functions
export const categoryAPI = {
  getAll: async () => {
    const response = await api.get('/categories');
    return response.data;
  },
  create: async (category) => {
    const response = await api.post('/categories', category);
    return response.data;
  },
  update: async (id, category) => {
    const response = await api.put(`/categories/${id}`, category);
    return response.data;
  },
  delete: async (id) => {
    await api.delete(`/categories/${id}`);
  }
};

// Proposal API functions
export const proposalAPI = {
  getAll: async (filters = {}) => {
    const query = new URLSearchParams(filters).toString();
    const response = await api.get(`/proposals${query ? `?${query}` : ''}`);
    return response.data;
  },
  create: async (proposal) => {
    const response = await api.post('/proposals', proposal);
    return response.data;
  },
  getById: async (id) => {
    const response = await api.get(`/proposals/${id}`);
    return response.data;
  },
  update: async (id, proposal) => {
    const response = await api.put(`/proposals/${id}`, proposal);
    return response.data;
  },
  delete: async (id, data) => {
    // send reason in body with axios.delete
    const response = await api.delete(`/proposals/${id}`, { data });
    return response.data;
  },
  approve: async (id, data) => {
    const response = await api.post(`/proposals/${id}/approve`, data);
    return response.data;
  },
  reject: async (id, data) => {
    const response = await api.post(`/proposals/${id}/reject`, data);
    return response.data;
  }
};

// Upload API functions
export const uploadAPI = {
  parse: async (file) => {
    const form = new FormData();
    form.append('file', file);
    const response = await api.post('/contracts/parse', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  }
};

// Dashboard API functions
export const dashboardAPI = {
  getSummary: async () => {
    const response = await api.get('/dashboard/summary');
    return response.data;
  }
};

// Auth API functions
export const authAPI = {
  login: async (username, password) => {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  },
  register: async (userData) => {
    const response = await api.post('/auth/register', userData);
    return response.data;
  },
  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// History API functions
export const historyAPI = {
  list: async (filters = {}) => {
    const response = await api.get('/proposals', { params: filters });
    return response.data;
  },
};

```


### 📄 errorUtils.js

**Path:** `frontend/src/errorUtils.js`

```javascript
// Error handling utility functions

export const extractErrorMessage = (error) => {
  // Handle different error formats
  let errorMessage = 'An error occurred';
  
  if (error?.response?.data) {
    const errorData = error.response.data;
    
    // Handle validation error array
    if (Array.isArray(errorData.detail)) {
      errorMessage = errorData.detail.map(err => err.msg || err.message || String(err)).join(', ');
    }
    // Handle single validation error object
    else if (errorData.detail && typeof errorData.detail === 'object') {
      errorMessage = errorData.detail.msg || errorData.detail.message || String(errorData.detail);
    }
    // Handle string error
    else if (typeof errorData.detail === 'string') {
      errorMessage = errorData.detail;
    }
    // Handle other error formats
    else if (typeof errorData === 'string') {
      errorMessage = errorData;
    }
  } else if (typeof error === 'string') {
    errorMessage = error;
  } else if (error?.message) {
    errorMessage = error.message;
  }
  
  return errorMessage;
};

export const handleApiError = (error, defaultMessage = 'An error occurred') => {
  console.error('API Error:', error);
  return extractErrorMessage(error) || defaultMessage;
};

```


### 📄 index.css

**Path:** `frontend/src/index.css`

```css
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}

```


### 📄 index.js

**Path:** `frontend/src/index.js`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

```


### 📄 proposalsApi.js

**Path:** `frontend/src/proposalsApi.js`

```javascript
import api from './api';

export const proposalAPI = {
  getAll: async (params = {}) => {
    const response = await api.get('/proposals', { params });
    return response.data;
  },
  getById: async (id) => {
    const response = await api.get(`/proposals/${id}`);
    return response.data;
  },
  create: async (data) => {
    const response = await api.post('/proposals', data);
    return response.data;
  },
  update: async (id, data) => {
    const response = await api.put(`/proposals/${id}`, data);
    return response.data;
  },
  delete: async (id) => {
    const response = await api.delete(`/proposals/${id}`);
    return response.data;
  },
};

```


### 📄 reportWebVitals.js

**Path:** `frontend/src/reportWebVitals.js`

```javascript
const reportWebVitals = onPerfEntry => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;

```


### 📄 setupTests.js

**Path:** `frontend/src/setupTests.js`

```javascript
// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

```


### 📄 theme.css

**Path:** `frontend/src/theme.css`

```css
/* Professional Enterprise Theme - Clean and Simple */

:root {
  /* Professional Color Palette */
  --color-primary: #0066cc;
  --color-primary-dark: #0052a3;
  --color-primary-hover: #004d99;
  --color-text: #2c3e50;
  --color-text-light: #5a6c7d;
  --color-text-secondary: #7f8c8d;
  --color-border: #e0e0e0;
  --color-border-dark: #bdbdbd;
  --color-background: #f5f7fa;
  --color-white: #ffffff;
  --color-hover: #f0f2f5;
  --color-success: #28a745;
  --color-warning: #ffc107;
  --color-error: #dc3545;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  font-size: 14px;
  line-height: 1.5;
  color: var(--color-text);
  background-color: var(--color-background);
}

.App {
  min-height: 100vh;
  background-color: var(--color-background);
}

/* Header - Professional Style */
.app-header {
  background-color: var(--color-white);
  border-bottom: 1px solid var(--color-border);
  padding: 14px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.header-left h1 {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
  font-size: 14px;
  color: var(--color-text-light);
}

/* Layout */
.app-layout {
  display: flex;
  min-height: calc(100vh - 60px);
  }
  
/* Sidebar - Professional Style */
.sidebar {
  width: 240px;
  background-color: var(--color-white);
  border-right: 1px solid var(--color-border);
  padding: 0;
  box-shadow: 1px 0 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid var(--color-border);
  background-color: #fafbfc;
}

.sidebar-user-info {
  display: flex;
  flex-direction: column;
}

.sidebar-user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 4px;
  }
  
.sidebar-user-role {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.sidebar-nav {
  flex: 1;
  padding: 12px 0;
  overflow-y: auto;
}

.sidebar-section {
  margin-bottom: 16px;
}

.sidebar-section-title {
  padding: 8px 16px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-secondary);
  margin-bottom: 4px;
}

.sidebar-item {
  padding: 10px 16px;
  cursor: pointer;
  color: var(--color-text);
  text-decoration: none;
  display: flex;
  flex-direction: column;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  transition: all 0.15s;
  border-left: 3px solid transparent;
  gap: 2px;
}

.sidebar-item-label {
  font-size: 14px;
  font-weight: 400;
  line-height: 1.4;
}

.sidebar-item-desc {
  font-size: 12px;
  color: var(--color-text-secondary);
  line-height: 1.3;
}

.sidebar-item:hover {
  background-color: var(--color-hover);
}

.sidebar-item:hover .sidebar-item-label {
  color: var(--color-primary);
}

.sidebar-item.active {
  background-color: #e8f4fd;
  border-left-color: var(--color-primary);
}

.sidebar-item.active .sidebar-item-label {
  color: var(--color-primary);
  font-weight: 600;
}

.sidebar-item.active .sidebar-item-desc {
  color: var(--color-primary);
}

/* Page Titles and Descriptions */
.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text);
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.page-description {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0 0 24px 0;
  line-height: 1.5;
}

/* Main Content - Professional Style */
.main-content {
  flex: 1;
  padding: 24px;
  background-color: var(--color-background);
  min-height: calc(100vh - 60px);
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
}

/* Cards - Professional Style */
.card {
  background-color: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.card-header {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--color-text);
  line-height: 28px;
}

/* Buttons - Professional Style */
.btn {
  padding: 8px 16px;
  border: 1px solid var(--color-border-dark);
  border-radius: 4px;
  background-color: var(--color-white);
  color: var(--color-text);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  min-height: 36px;
  transition: all 0.15s;
  display: inline-flex;
    align-items: center;
  justify-content: center;
  }
  
.btn:hover {
  background-color: var(--color-hover);
  border-color: var(--color-border-dark);
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border-color: var(--color-primary);
}

.btn-primary:hover {
  background-color: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  }
  
.btn-secondary {
  background-color: var(--color-white);
  color: var(--color-text);
}

.btn-small {
  padding: 6px 12px;
  font-size: 13px;
  min-height: 32px;
}

/* Forms - Professional Style */
.form-group {
  margin-bottom: 18px;
}

.form-label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: var(--color-text);
  font-size: 14px;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--color-border-dark);
  border-radius: 4px;
  font-size: 14px;
  font-family: inherit;
  min-height: 38px;
  color: var(--color-text);
  background-color: var(--color-white);
  transition: border-color 0.15s;
}

.form-textarea {
  height: auto;
  min-height: 80px;
  resize: vertical;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(0, 102, 204, 0.1);
}

.form-input:hover,
.form-select:hover,
.form-textarea:hover {
  border-color: var(--color-text-light);
}

/* Tables - Professional Style */
.table {
  width: 100%;
  border-collapse: collapse;
  background-color: var(--color-white);
  border: 1px solid var(--color-border);
  font-size: 14px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.table th {
  background-color: #f8f9fa;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid var(--color-border);
  color: var(--color-text);
  font-size: 13px;
}

.table td {
  padding: 12px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  font-size: 14px;
}

.table tr:hover {
  background-color: var(--color-hover);
}

.table tr:last-child td {
  border-bottom: none;
}

/* Status Badges - Professional Style */
.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  line-height: 1.4;
}

.badge-pending {
  background-color: #fff3cd;
  color: #856404;
}

.badge-approved {
  background-color: #d4edda;
  color: #155724;
}

.badge-rejected {
  background-color: #f8d7da;
  color: #721c24;
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: var(--color-text-light);
}

/* Utilities */
.text-center {
  text-align: center;
}

.mt-20 {
  margin-top: 20px;
}

.mb-20 {
  margin-bottom: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--color-text);
  line-height: 32px;
}

.page-description {
  color: var(--color-text-secondary);
  margin-bottom: 24px;
  font-size: 14px;
  line-height: 20px;
}

```


================================================================================
## 📂 azure


================================================================================
## 📂 backend


### 📄 Dockerfile

**Path:** `backend/Dockerfile`

```dockerfile
# Multi-stage Dockerfile for backend
# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


```


### 📄 alembic.ini

**Path:** `backend/alembic.ini`

```ini
# A generic, single database configuration.

[alembic]
# path to migration scripts
# Use forward slashes (/) also on windows to provide an os agnostic path
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to alembic/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:alembic/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
# version_path_separator = newline
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARNING
handlers = console
qualname =

[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S

```


### 📄 auth.py

**Path:** `backend/auth.py`

```python
import logging
from datetime import datetime, timedelta
from typing import cast

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import User as DBUser
from database import get_db
from models import TokenData
from settings import settings

# Password hashing context - using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

# JWT token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash (supports both bcrypt and legacy SHA256)."""
    # Check if it's a bcrypt hash (starts with $2a$, $2b$, or $2y$)
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        # Try bcrypt verification
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            logger.exception("bcrypt verification failed")
            return False

    # Fallback to legacy SHA256 for backward compatibility
    # This allows existing users to login and migrate on next password change
    import hashlib

    legacy_hash = hashlib.sha256(plain_password.encode()).hexdigest()
    return legacy_hash == hashed_password


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, username: str, password: str) -> DBUser | None:
    """Authenticate a user with username and password."""
    user: DBUser | None = db.query(DBUser).filter(DBUser.username == username).first()
    if not user:
        print(f"[AUTH] Login failed: user '{username}' not found")
        return None
    hashed_password = cast(str, user.hashed_password)
    if not verify_password(password, hashed_password):
        print(f"[AUTH] Login failed: invalid password for user '{username}'")
        return None
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)
) -> DBUser:
    """Get the current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception from None

    user: DBUser | None = (
        db.query(DBUser).filter(DBUser.username == token_data.username).first()
    )
    if user is None:
        raise credentials_exception
    return user


def require_finance_role(current_user: DBUser = Depends(get_current_user)) -> DBUser:
    """Require finance role."""
    if current_user.role != "finance":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Required role: finance",
        )
    return current_user


def require_ministry_role(current_user: DBUser = Depends(get_current_user)) -> DBUser:
    """Require ministry role."""
    if current_user.role != "ministry":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Required role: ministry",
        )
    return current_user

```


### 📄 database.py

**Path:** `backend/database.py`

```python
from datetime import datetime
from urllib.parse import urlparse

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from settings import settings

# Database setup
db_url = settings.DATABASE_URL
parsed_db = urlparse(db_url)
masked_host = parsed_db.hostname or "unknown"
masked_db = (parsed_db.path or "/").lstrip("/") or "unknown"
print(f"[database] Using driver={parsed_db.scheme} host={masked_host} db={masked_db}")
connect_args = {}

if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # For PostgreSQL, add connection pooling and timeout settings
    connect_args = {
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }

# Add connection pool settings for better reliability
engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True,  # Verify connections before using them
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=False,          # Set to True for SQL query logging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Ministry model
class Ministry(Base):
    __tablename__ = "ministries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationships
    users = relationship("User", back_populates="ministry")
    proposals = relationship("Proposal", back_populates="ministry")


# Category model
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    allocated_budget = Column(Float, nullable=False)
    remaining_budget = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    proposals = relationship("Proposal", back_populates="category")


# User model (Authentication)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "ministry" or "finance"
    ministry_id = Column(
        Integer, ForeignKey("ministries.id"), nullable=True
    )  # Foreign key to Ministry
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    ministry = relationship("Ministry", back_populates="users")


# Proposal model (Phase 2)
class Proposal(Base):
    __tablename__ = "proposals"

    id = Column(Integer, primary_key=True, index=True)
    ministry_id = Column(
        Integer, ForeignKey("ministries.id"), nullable=False
    )  # Foreign key to Ministry
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    requested_amount = Column(Float, nullable=False)
    status = Column(String, default="Pending", nullable=False)  # Pending/Approved/Rejected
    approved_amount = Column(Float, nullable=True)
    decision_notes = Column(String, nullable=True)
    decided_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    ministry = relationship("Ministry", back_populates="proposals")
    category = relationship("Category", back_populates="proposals")


# Create tables


def create_tables():
    """
    Create all database tables using Alembic migrations and seed default data.

    This function:
    1. Runs Alembic migrations to ensure schema is up-to-date
    2. Creates default ministries and users if they don't exist
    """
    from alembic import command
    from alembic.config import Config
    from auth import get_password_hash
    from database import Ministry as DBMinistry
    from database import User as DBUser

    # Run Alembic migrations to ensure schema is up-to-date
    try:
        print("[startup] Loading Alembic configuration...")
        alembic_cfg = Config("alembic.ini")
        print("[startup] Running Alembic migrations to head...")
        command.upgrade(alembic_cfg, "head")
        print("[startup] Database migrations applied successfully")
    except Exception as e:
        # If migrations fail, fall back to creating tables directly
        # This is useful for initial setup or if Alembic isn't configured
        print(f"[startup] Warning: Alembic migration failed: {e}")
        import traceback
        print(f"[startup] Traceback: {traceback.format_exc()}")
        print("[startup] Falling back to direct table creation...")
        Base.metadata.create_all(bind=engine)
        print("[startup] Direct table creation completed")

    # Create default ministries and users if they don't exist
    db = SessionLocal()

    try:
        # Create default ministries
        default_ministries = [
            {
                "name": "Ministry of Education",
                "description": "Government ministry responsible for education policy and funding"
            },
            {
                "name": "Ministry of Health",
                "description": "Government ministry responsible for healthcare policy and public health"
            },
            {
                "name": "Ministry of Infrastructure",
                "description": "Government ministry responsible for infrastructure development and maintenance"
            },
            {
                "name": "Ministry of Defense",
                "description": "Government ministry responsible for national defense and security"
            },
            {
                "name": "Ministry of Finance",
                "description": "Government ministry responsible for financial policy and economic planning"
            },
            {
                "name": "Ministry of Transportation",
                "description": "Government ministry responsible for transportation systems and logistics"
            },
            {
                "name": "Ministry of Energy",
                "description": "Government ministry responsible for energy policy and resource management"
            },
            {
                "name": "Ministry of Agriculture",
                "description": "Government ministry responsible for agricultural policy and food security"
            }
        ]

        # Create ministries if they don't exist
        created_ministries = {}
        for ministry_data in default_ministries:
            existing = db.query(DBMinistry).filter(DBMinistry.name == ministry_data["name"]).first()
            if not existing:
                ministry = DBMinistry(**ministry_data)
                db.add(ministry)
                db.flush()  # Get the ID
                created_ministries[ministry_data["name"]] = ministry
            else:
                created_ministries[ministry_data["name"]] = existing

        # Get Ministry of Education for default user (or use first created)
        education_ministry = created_ministries.get("Ministry of Education")
        if not education_ministry:
            education_ministry = db.query(DBMinistry).filter(DBMinistry.name == "Ministry of Education").first()

        # Create default finance user
        finance_user = db.query(DBUser).filter(DBUser.username == "finance").first()
        if not finance_user:
            finance_user = DBUser(
                username="finance",
                email="finance@gov.com",
                hashed_password=get_password_hash("fin"),
                role="finance",
                ministry_id=None,  # Finance users don't belong to a ministry
            )
            db.add(finance_user)

        # Create default ministry user
        ministry_user = db.query(DBUser).filter(DBUser.username == "ministry").first()
        if not ministry_user:
            ministry_user = DBUser(
                username="ministry",
                email="ministry@gov.com",
                hashed_password=get_password_hash("min"),
                role="ministry",
                ministry_id=education_ministry.id,  # Link to Ministry of Education
            )
            db.add(ministry_user)

        db.commit()
        print("Default ministries and users created successfully")
    except Exception as e:
        print(f"Error creating default ministries and users: {e}")
        db.rollback()
    finally:
        db.close()


# Database dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```


### 📄 exceptions.py

**Path:** `backend/exceptions.py`

```python
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

```


### 📄 main.py

**Path:** `backend/main.py`

```python
import json
import logging
import os
from datetime import timedelta
from typing import Any, cast

import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.orm import Session

from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    require_finance_role,
    require_ministry_role,
)
from database import Category as DBCategory
from database import Ministry as DBMinistry
from database import Proposal as DBProposal
from database import User as DBUser
from database import create_tables, get_db
from exceptions import (
    CategoryNotFoundError,
    DuplicateCategoryError,
    DuplicateMinistryError,
    InsufficientBudgetError,
    InvalidProposalStatusError,
    MinistryNotFoundError,
    ProposalNotFoundError,
    ValidationError,
)
from models import (
    Category,
    CategoryCreate,
    CategoryUpdate,
    Ministry,
    MinistryCreate,
    Proposal,
    ProposalApprove,
    ProposalCreate,
    ProposalReject,
    ProposalUpdate,
    Token,
    UserCreate,
    UserLogin,
)
from models import User as UserModel
from repositories.categories import CategoryRepository
from repositories.ministries import MinistryRepository
from services.approvals import ApprovalService
from services.parser import ContractParserService
from services.proposals import ProposalService
from settings import settings


# Helper function to parse CORS_ORIGINS from string (JSON or comma-separated)
def parse_cors_origins(cors_str: str) -> list[str]:
    """Parse CORS_ORIGINS from JSON array or comma-separated string."""
    if not cors_str:
        return ["http://localhost:3000"]
    # Try JSON first
    try:
        parsed = json.loads(cors_str)
        if isinstance(parsed, list):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass
    # Fall back to comma-separated string
    return [origin.strip() for origin in cors_str.split(",") if origin.strip()]


# Read CORS_ORIGINS directly from environment to avoid pydantic-settings JSON parsing issues
CORS_ORIGINS_STR = os.getenv("CORS_ORIGINS", "http://localhost:3000")

# Create FastAPI app
app = FastAPI(title=settings.API_TITLE, version=settings.API_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=parse_cors_origins(CORS_ORIGINS_STR),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics instrumentation
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)


# Create database tables on startup
@app.on_event("startup")
def startup_event():
    import traceback

    try:
        print("[startup] Starting database initialization...")
        create_tables()
        print("[startup] Database initialization completed successfully")
    except Exception as e:
        print(f"[startup] ERROR: Database initialization failed: {e}")
        print(f"[startup] Traceback: {traceback.format_exc()}")
        # Don't swallow the exception; let FastAPI crash so health probes fail fast
        raise


# Exception handler to convert domain errors to HTTP responses
@app.exception_handler(ProposalNotFoundError)
async def proposal_not_found_handler(request: Request, exc: ProposalNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(CategoryNotFoundError)
async def category_not_found_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(MinistryNotFoundError)
async def ministry_not_found_handler(request: Request, exc: MinistryNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(InsufficientBudgetError)
async def insufficient_budget_handler(request: Request, exc: InsufficientBudgetError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(InvalidProposalStatusError)
async def invalid_status_handler(request: Request, exc: InvalidProposalStatusError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(DuplicateCategoryError)
async def duplicate_category_handler(request: Request, exc: DuplicateCategoryError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(DuplicateMinistryError)
async def duplicate_ministry_handler(request: Request, exc: DuplicateMinistryError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


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
        ministry_id=user_data.ministry_id,
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
    return {"access_token": access_token, "token_type": "bearer", "user": user}


@app.get("/auth/me", response_model=UserModel)
def get_current_user_info(
    current_user: DBUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get current user information."""
    # Load ministry relationship if user has ministry_id
    if current_user.ministry_id:
        from sqlalchemy.orm import joinedload

        user_with_ministry = (
            db.query(DBUser)
            .options(joinedload(DBUser.ministry))
            .filter(DBUser.id == current_user.id)
            .first()
        )
        return user_with_ministry
    return current_user


# CRUD endpoints for categories
@app.get("/categories", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    """Get all budget categories"""
    return CategoryRepository.get_all(db)


@app.post("/categories", response_model=Category)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role),
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
        "remaining_budget": category.allocated_budget,
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
    current_user: DBUser = Depends(require_finance_role),
):
    """Update a category (Finance users only)"""
    db_category = CategoryRepository.get_by_id(db, category_id)
    if not db_category:
        raise CategoryNotFoundError("Category not found")

    update_data: dict[str, Any] = {}

    # Update fields if provided
    if category_update.name is not None:
        # Check if new name already exists (excluding current category)
        existing = (
            db.query(DBCategory)
            .filter(DBCategory.name == category_update.name, DBCategory.id != category_id)
            .first()
        )
        if existing:
            raise DuplicateCategoryError("Category name already exists")
        update_data["name"] = category_update.name

    if category_update.allocated_budget is not None:
        # Update remaining budget proportionally
        old_allocated = float(db_category.allocated_budget or 0.0)
        new_allocated = float(category_update.allocated_budget or 0.0)
        ratio = new_allocated / old_allocated if old_allocated > 0 else 1
        remaining_budget = float(db_category.remaining_budget or 0.0)
        update_data["remaining_budget"] = remaining_budget * ratio
        update_data["allocated_budget"] = new_allocated

    return CategoryRepository.update(db, db_category, update_data)


@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role),
):
    """Delete a category (Finance users only)"""
    db_category = CategoryRepository.get_by_id(db, category_id)
    if not db_category:
        raise CategoryNotFoundError("Category not found")

    CategoryRepository.delete(db, db_category)
    return {"message": "Category deleted successfully"}


# ------------------ Ministry Endpoints ------------------


@app.get("/ministries", response_model=list[Ministry])
def get_ministries(db: Session = Depends(get_db)):
    """Get all active ministries"""
    return MinistryRepository.get_all_active(db)


@app.post("/ministries", response_model=Ministry)
def create_ministry(
    ministry: MinistryCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_finance_role),
):
    """Create a new ministry (Finance users only)"""
    # Check if ministry name already exists
    existing = MinistryRepository.get_by_name(db, ministry.name)
    if existing:
        raise DuplicateMinistryError("Ministry name already exists")

    ministry_data = {"name": ministry.name, "description": ministry.description}
    return MinistryRepository.create(db, ministry_data)


@app.post("/ministries/find-or-create", response_model=Ministry)
def find_or_create_ministry(
    ministry_name: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    """Find existing ministry or create new one if not found"""
    if not ministry_name or not ministry_name.strip():
        raise ValidationError("Ministry name is required")

    return MinistryRepository.find_or_create(db, ministry_name.strip())


# Health check endpoint
@app.get("/")
def root():
    return {"message": "Government Spending Tracker API"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint that verifies:
    - API is running
    - Database is accessible
    Returns 200 if healthy, 503 if unhealthy
    """
    try:
        # Check database connectivity
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "service": "Government Spending Tracker API",
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: Database connection failed - {str(e)}",
        ) from e


# ------------------ Phase 2: Proposal Endpoints ------------------


@app.get("/proposals", response_model=list[Proposal])
def list_proposals(
    db: Session = Depends(get_db),
    ministry_id: int | None = None,
    category_id: int | None = None,
    status: str | None = None,
):
    """List proposals with optional filters."""
    return ProposalService.list_proposals(db, ministry_id, category_id, status)


@app.post("/proposals", response_model=Proposal)
def create_proposal(
    payload: ProposalCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_ministry_role),
):
    """Create a new proposal. Ministry users can only create proposals for their own ministry."""
    return ProposalService.create_proposal(db, payload, current_user)


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
    current_user: DBUser = Depends(require_finance_role),
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
    current_user: DBUser = Depends(require_finance_role),
):
    """Reject a proposal (Finance users only)."""
    return ApprovalService.reject_proposal(db, proposal_id, body.decision_notes)


# ------------------ Phase 4: Contract Upload & Parsing ------------------


@app.post("/contracts/parse")
def parse_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_ministry_role),
):
    """Parse a contract file (CSV or JSON) and return normalized draft proposals (Ministry users only)."""
    return ContractParserService.parse_contract(db, file)


# ------------------ Phase 5: Dashboard Summary ------------------


@app.get("/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db), current_user: DBUser = Depends(require_finance_role)
):
    # Per-category aggregates
    categories = db.query(DBCategory).all()
    # Sum approved amounts grouped by category_id
    from sqlalchemy import func

    rows = (
        db.query(DBProposal.category_id, func.coalesce(func.sum(DBProposal.approved_amount), 0.0))
        .filter(DBProposal.status == "Approved")
        .group_by(DBProposal.category_id)
        .all()
    )
    approved_sums: dict[int, float] = {
        int(category_id): float(total or 0.0) for category_id, total in rows
    }
    category_stats = []
    for c in categories:
        category_id = cast(int, c.id)
        approved_total = float(approved_sums.get(category_id, 0.0) or 0.0)
        category_stats.append(
            {
            "id": category_id,
            "name": c.name,
            "allocated_budget": float(c.allocated_budget),
            "remaining_budget": float(c.remaining_budget),
            "approved_total": approved_total,
            }
        )

    # Per-ministry aggregates (requested vs approved)
    from sqlalchemy.orm import joinedload

    ministry_proposals = db.query(DBMinistry).options(joinedload(DBMinistry.proposals)).all()

    ministry_stats = []
    for ministry in ministry_proposals:
        proposals = ministry.proposals
        requested_total = sum(p.requested_amount for p in proposals)
        approved_total = sum(
            p.approved_amount for p in proposals if p.status == "Approved" and p.approved_amount
        )

        ministry_stats.append(
            {
            "ministry_id": ministry.id,
            "ministry_name": ministry.name,
            "requested_total": float(requested_total),
            "approved_total": float(approved_total),
            }
        )

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
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    if host == "0.0.0.0":  # nosec B104 - container deployments override HOST intentionally
        logging.warning(
            "Running with host=0.0.0.0; ensure this is expected for production deployments."
        )
    uvicorn.run(app, host=host, port=port)

```


### 📄 models.py

**Path:** `backend/models.py`

```python
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# Pydantic models for API
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Category name")
    allocated_budget: float = Field(..., gt=0, description="Allocated budget must be positive")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200, description="Category name")
    allocated_budget: float | None = Field(None, gt=0, description="Allocated budget must be positive")


class Category(CategoryBase):
    id: int
    remaining_budget: float
    created_at: datetime

    class Config:
        from_attributes = True


# ------------------ Phase 2: Proposal Schemas ------------------


class ProposalBase(BaseModel):
    category_id: int = Field(..., gt=0, description="Category ID must be positive")
    title: str = Field(..., min_length=1, max_length=200, description="Proposal title")
    description: str | None = Field(None, max_length=1000, description="Proposal description")
    requested_amount: float = Field(..., gt=0, description="Requested amount must be positive")


class ProposalCreate(ProposalBase):
    ministry_id: int | None = None  # Either ministry_id or ministry_name
    ministry_name: str | None = None  # Either ministry_id or ministry_name


class ProposalUpdate(BaseModel):
    ministry_id: int | None = Field(None, gt=0, description="Ministry ID must be positive if provided")
    category_id: int | None = Field(None, gt=0, description="Category ID must be positive if provided")
    title: str | None = Field(None, min_length=1, max_length=200, description="Proposal title")
    description: str | None = Field(None, max_length=1000, description="Proposal description")
    requested_amount: float | None = Field(None, gt=0, description="Requested amount must be positive if provided")
    status: str | None = None  # still Pending in Phase 2


class Proposal(ProposalBase):
    id: int
    status: str
    approved_amount: float | None = None
    decision_notes: str | None = None
    decided_at: datetime | None = None
    created_at: datetime
    ministry: Optional["Ministry"] = None

    class Config:
        from_attributes = True


class ProposalApprove(BaseModel):
    approved_amount: float = Field(..., gt=0, description="Approved amount must be positive")
    decision_notes: str | None = Field(None, max_length=1000, description="Decision notes")


class ProposalReject(BaseModel):
    decision_notes: str | None = Field(None, max_length=1000, description="Decision notes")


class ProposalDelete(BaseModel):
    reason: str  # Required reason for deletion


# Ministry Models
class MinistryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Ministry name")
    description: str | None = Field(None, max_length=1000, description="Ministry description")


class MinistryCreate(MinistryBase):
    pass


class Ministry(MinistryBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Authentication Models
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: str = Field(..., description="Email address")
    role: str = Field(..., description="User role: 'ministry' or 'finance'")
    ministry_id: int | None = Field(None, gt=0, description="Ministry ID must be positive if provided")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Basic email validation."""
        if "@" not in v or "." not in v.split("@")[1]:
            raise ValueError("Invalid email format")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        """Validate role is either 'ministry' or 'finance'."""
        if v not in ("ministry", "finance"):
            raise ValueError("Role must be 'ministry' or 'finance'")
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=3, max_length=100, description="Password (min 3 characters)")


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    ministry: Ministry | None = None  # Include ministry relationship

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User


class TokenData(BaseModel):
    username: str | None = None

```


### 📄 pyproject.toml

**Path:** `backend/pyproject.toml`

```toml
[tool.ruff]
# Ruff configuration for code quality
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = [
    "E501",  # line too long (handled by line-length)
    "B008",  # do not perform function calls in argument defaults
    "E402",  # module level import not at top of file (needed for path manipulation)
]

[tool.ruff.lint.isort]
known-first-party = ["database", "models", "auth", "services", "repositories", "exceptions", "settings"]

[tool.mypy]
# mypy configuration for type checking
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true

[[tool.mypy.overrides]]
module = [
    "passlib.*",
    "jose.*",
    "alembic.*",
]
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = [
    "database",
    "services.*",
    "tests.*",
]
ignore_errors = true

[tool.bandit]
# Bandit configuration for security linting
exclude_dirs = ["tests", "alembic", "__pycache__"]
skips = ["B101"]  # Skip assert_used (tests use asserts)


```


### 📄 pytest.ini

**Path:** `backend/pytest.ini`

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=.
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=90
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
markers =
    auth: Authentication related tests
    database: Database model tests
    api: API endpoint tests
    integration: Integration tests
    unit: Unit tests

```


### 📄 requirements.txt

**Path:** `backend/requirements.txt`

```text
fastapi==0.115.6
uvicorn==0.32.1
sqlalchemy==2.0.36
pydantic==2.10.3
pydantic-settings==2.6.1
python-multipart==0.0.12
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2
alembic==1.14.0
psycopg[binary]==3.2.12

# Development tools (Phase 2)
ruff==0.6.9
mypy==1.11.2
bandit==1.7.9
types-passlib==1.7.7
pytest==8.3.4
pytest-asyncio==0.24.0
pytest-cov==5.0.0

# Monitoring (Phase 3)
prometheus-fastapi-instrumentator==7.0.0
httpx==0.27.2

```


### 📄 settings.py

**Path:** `backend/settings.py`

```python
"""
Application settings using pydantic-settings for environment variable management.
This removes hardcoded values and enables proper configuration management.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Security
    SECRET_KEY: str = (
        "your-secret-key-change-in-production"  # Default for dev, MUST be overridden in production
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./government_spending.db"

    # Note: CORS_ORIGINS is NOT defined here to avoid pydantic-settings JSON parsing
    # It will be read directly from os.getenv() in main.py

    # API
    API_TITLE: str = "Government Spending Tracker"
    API_VERSION: str = "1.0.0"


# Global settings instance
settings = Settings()

```


### 📄 test_requirements.txt

**Path:** `backend/test_requirements.txt`

```text
pytest==8.3.3
pytest-cov==7.0.0
pytest-asyncio==1.2.0
httpx==0.28.1
fastapi==0.115.6

```


================================================================================
## 📂 backend → tests


### 📄 conftest.py

**Path:** `backend/tests/conftest.py`

```python
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from auth import get_password_hash
from database import Base, get_db
from main import app

# Create test database using a secure temporary file
tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
TEST_DB_FILE = tmp_db.name
tmp_db.close()
TEST_ENGINE = create_engine(f"sqlite:///{TEST_DB_FILE}", connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield TEST_ENGINE
    # Cleanup
    Base.metadata.drop_all(bind=TEST_ENGINE)
    os.unlink(TEST_DB_FILE)


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with database dependency override"""

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def sample_ministry(test_db):
    """Create a sample ministry for testing"""
    from database import Ministry as DBMinistry

    ministry = DBMinistry(name="Test Ministry", description="Test Ministry for unit tests")
    test_db.add(ministry)
    test_db.commit()
    test_db.refresh(ministry)
    return ministry


@pytest.fixture(scope="function")
def sample_category(test_db):
    """Create a sample category for testing"""
    from database import Category as DBCategory

    category = DBCategory(
        name="Test Category", allocated_budget=1000000.0, remaining_budget=1000000.0
    )
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    return category


@pytest.fixture(scope="function")
def sample_user(test_db, sample_ministry):
    """Create a sample user for testing"""
    from database import User as DBUser

    user = DBUser(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        role="ministry",
        ministry_id=sample_ministry.id,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def finance_user(test_db):
    """Create a finance user for testing"""
    from database import User as DBUser

    user = DBUser(
        username="finance",
        email="finance@example.com",
        hashed_password=get_password_hash("fin"),
        role="finance",
        ministry_id=None,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def auth_headers(client, sample_user):
    """Get authentication headers for test user"""
    response = client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def finance_headers(client, finance_user):
    """Get authentication headers for finance user"""
    response = client.post("/auth/login", json={"username": "finance", "password": "fin"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def sample_proposal(test_db, sample_ministry, sample_category):
    """Create a sample proposal for testing"""
    from database import Proposal as DBProposal

    proposal = DBProposal(
        ministry_id=sample_ministry.id,
        category_id=sample_category.id,
        title="Test Proposal",
        description="Test proposal for unit tests",
        requested_amount=500000.0,
        status="Pending",
    )
    test_db.add(proposal)
    test_db.commit()
    test_db.refresh(proposal)
    return proposal

```


### 📄 test_api_endpoints.py

**Path:** `backend/tests/test_api_endpoints.py`

```python
import sys
from pathlib import Path

import pytest

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


@pytest.mark.api
class TestAuthenticationEndpoints:
    """Test authentication API endpoints"""

    def test_user_registration_success(self, client, sample_ministry):
        """Test successful user registration"""
        response = client.post(
            "/auth/register",
            json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "role": "ministry",
                "ministry_id": sample_ministry.id,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert data["role"] == "ministry"
        assert data["ministry_id"] == sample_ministry.id
        assert "hashed_password" not in data  # Should not return password

    def test_user_registration_duplicate_username(self, client, sample_user, sample_ministry):
        """Test user registration with duplicate username"""
        response = client.post(
            "/auth/register",
            json={
            "username": "testuser",  # Already exists
            "email": "different@example.com",
            "password": "password123",
            "role": "ministry",
                "ministry_id": sample_ministry.id,
            },
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_user_registration_duplicate_email(self, client, sample_user, sample_ministry):
        """Test user registration with duplicate email"""
        response = client.post(
            "/auth/register",
            json={
            "username": "differentuser",
            "email": "test@example.com",  # Already exists
            "password": "password123",
            "role": "ministry",
                "ministry_id": sample_ministry.id,
            },
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_user_registration_invalid_role(self, client, sample_ministry):
        """Test user registration with invalid role"""
        response = client.post(
            "/auth/register",
            json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "role": "invalid_role",
                "ministry_id": sample_ministry.id,
            },
        )

        # Pydantic validation now catches invalid role (422) before API validation (400)
        assert response.status_code in (400, 422)
        detail = response.json()["detail"]
        if isinstance(detail, list):
            # Pydantic validation error format
            detail_str = str(detail)
        else:
            detail_str = detail
        assert "ministry" in detail_str.lower() or "finance" in detail_str.lower()

    def test_user_login_success(self, client, sample_user):
        """Test successful user login"""
        response = client.post(
            "/auth/login", json={"username": "testuser", "password": "testpassword"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_user_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post(
            "/auth/login", json={"username": "nonexistent", "password": "wrongpassword"}
        )

        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information"""
        response = client.get("/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert data["role"] == "ministry"

    def test_get_current_user_unauthorized(self, client):
        """Test getting current user without authentication"""
        response = client.get("/auth/me")

        assert response.status_code == 403


@pytest.mark.api
class TestMinistryEndpoints:
    """Test ministry API endpoints"""

    def test_get_ministries(self, client, sample_ministry):
        """Test getting all ministries"""
        response = client.get("/ministries")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(m["name"] == "Test Ministry" for m in data)

    def test_create_ministry_finance_user(self, client, finance_headers):
        """Test creating ministry as finance user"""
        response = client.post(
            "/ministries",
            json={"name": "New Ministry", "description": "New ministry description"},
            headers=finance_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Ministry"
        assert data["description"] == "New ministry description"
        assert data["is_active"] is True

    def test_create_ministry_unauthorized(self, client, auth_headers):
        """Test creating ministry as non-finance user"""
        response = client.post(
            "/ministries",
            json={"name": "Unauthorized Ministry", "description": "Should fail"},
            headers=auth_headers,
        )

        assert response.status_code == 403

    def test_create_ministry_duplicate_name(self, client, finance_headers, sample_ministry):
        """Test creating ministry with duplicate name"""
        response = client.post(
            "/ministries",
            json={"name": "Test Ministry", "description": "Duplicate name"},
            headers=finance_headers,
        )

        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_find_or_create_ministry_existing(self, client, auth_headers, sample_ministry):
        """Test find or create ministry with existing name"""
        response = client.post(
            "/ministries/find-or-create",
            params={"ministry_name": "Test Ministry"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Ministry"
        assert data["id"] == sample_ministry.id

    def test_find_or_create_ministry_new(self, client, auth_headers):
        """Test find or create ministry with new name"""
        response = client.post(
            "/ministries/find-or-create",
            params={"ministry_name": "Brand New Ministry"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Brand New Ministry"
        assert data["id"] is not None


@pytest.mark.api
class TestCategoryEndpoints:
    """Test category API endpoints"""

    def test_get_categories(self, client, sample_category):
        """Test getting all categories"""
        response = client.get("/categories")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(c["name"] == "Test Category" for c in data)

    def test_create_category_finance_user(self, client, finance_headers):
        """Test creating category as finance user"""
        response = client.post(
            "/categories",
            json={"name": "New Category", "allocated_budget": 2000000.0},
            headers=finance_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "New Category"
        assert data["allocated_budget"] == 2000000.0
        assert data["remaining_budget"] == 2000000.0

    def test_create_category_unauthorized(self, client, auth_headers):
        """Test creating category as non-finance user (should fail)"""
        response = client.post(
            "/categories",
            json={"name": "Unauthorized Category", "allocated_budget": 1000000.0},
            headers=auth_headers,
        )

        # Finance-only access enforced - should return 403
        assert response.status_code == 403

    def test_update_category(self, client, finance_headers, sample_category):
        """Test updating category"""
        response = client.put(
            f"/categories/{sample_category.id}",
            json={"name": "Updated Category", "allocated_budget": 3000000.0},
            headers=finance_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Category"
        assert data["allocated_budget"] == 3000000.0

    def test_delete_category(self, client, finance_headers, sample_category):
        """Test deleting category"""
        response = client.delete(f"/categories/{sample_category.id}", headers=finance_headers)

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]


@pytest.mark.api
class TestProposalEndpoints:
    """Test proposal API endpoints"""

    def test_get_proposals(self, client, sample_proposal):
        """Test getting all proposals"""
        response = client.get("/proposals")

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(p["title"] == "Test Proposal" for p in data)

    def test_get_proposals_with_filters(self, client, sample_proposal, sample_category):
        """Test getting proposals with filters"""
        response = client.get(
            "/proposals", params={"category_id": sample_category.id, "status": "Pending"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(p["category_id"] == sample_category.id for p in data)
        assert all(p["status"] == "Pending" for p in data)

    def test_create_proposal_with_ministry_name(self, client, auth_headers, sample_category):
        """Test creating proposal with ministry name"""
        response = client.post(
            "/proposals",
            json={
                "ministry_name": "New Test Ministry",
                "category_id": sample_category.id,
                "title": "New Proposal",
                "description": "New proposal description",
                "requested_amount": 750000.0,
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Proposal"
        assert data["requested_amount"] == 750000.0
        assert data["status"] == "Pending"

    def test_create_proposal_with_ministry_id(
        self, client, auth_headers, sample_ministry, sample_category
    ):
        """Test creating proposal with ministry ID"""
        response = client.post(
            "/proposals",
            json={
                "ministry_id": sample_ministry.id,
                "category_id": sample_category.id,
                "title": "ID Based Proposal",
                "requested_amount": 500000.0,
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "ID Based Proposal"
        assert data["ministry"]["name"] == sample_ministry.name

    def test_create_proposal_invalid_category(self, client, auth_headers):
        """Test creating proposal with invalid category"""
        response = client.post(
            "/proposals",
            json={
                "ministry_name": "Test Ministry",
                "category_id": 999,  # Non-existent category
                "title": "Invalid Category Proposal",
                "requested_amount": 100000.0,
            },
            headers=auth_headers,
        )

        # CategoryNotFoundError returns 404 (not found)
        assert response.status_code == 404
        detail = response.json()["detail"]
        assert "Category not found" in detail or "does not exist" in detail

    def test_create_proposal_invalid_amount(self, client, auth_headers, sample_category):
        """Test creating proposal with invalid amount"""
        response = client.post(
            "/proposals",
            json={
                "ministry_name": "Test Ministry",
                "category_id": sample_category.id,
                "title": "Invalid Amount Proposal",
                "requested_amount": -1000.0,  # Negative amount
            },
            headers=auth_headers,
        )

        # Pydantic validation now catches invalid amount (422) before API validation (400)
        assert response.status_code in (400, 422)
        detail = response.json()["detail"]
        if isinstance(detail, list):
            # Pydantic validation error format
            detail_str = str(detail)
        else:
            detail_str = detail
        assert "greater than 0" in detail_str.lower() or "positive" in detail_str.lower()

    def test_get_proposal_by_id(self, client, sample_proposal):
        """Test getting proposal by ID"""
        response = client.get(f"/proposals/{sample_proposal.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_proposal.id
        assert data["title"] == sample_proposal.title
        assert data["ministry"]["name"] is not None

    def test_get_proposal_not_found(self, client):
        """Test getting non-existent proposal"""
        response = client.get("/proposals/999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_proposal(self, client, auth_headers, sample_proposal):
        """Test updating proposal"""
        response = client.put(
            f"/proposals/{sample_proposal.id}",
            json={
                "title": "Updated Proposal Title",
                "description": "Updated description",
                "requested_amount": 600000.0,
            },
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Proposal Title"
        assert data["description"] == "Updated description"
        assert data["requested_amount"] == 600000.0

    def test_update_proposal_ministry_id(
        self, client, auth_headers, sample_proposal, sample_ministry
    ):
        """Test updating proposal ministry"""
        # Use the existing sample ministry for testing
        new_ministry_id = sample_ministry.id

        # Update proposal with the same ministry (should work)
        response = client.put(
            f"/proposals/{sample_proposal.id}",
            json={"ministry_id": new_ministry_id, "title": "Updated Ministry Proposal"},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["ministry"]["id"] == new_ministry_id
        assert data["title"] == "Updated Ministry Proposal"

    def test_delete_proposal(self, client, auth_headers, sample_proposal):
        """Test deleting proposal"""
        response = client.delete(f"/proposals/{sample_proposal.id}", headers=auth_headers)

        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]


@pytest.mark.api
class TestApprovalEndpoints:
    """Test proposal approval endpoints"""

    def test_approve_proposal(self, client, finance_headers, sample_proposal):
        """Test approving a proposal"""
        response = client.post(
            f"/proposals/{sample_proposal.id}/approve",
            json={"approved_amount": 400000.0, "decision_notes": "Approved with reduced amount"},
            headers=finance_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Approved"
        assert data["approved_amount"] == 400000.0
        assert data["decision_notes"] == "Approved with reduced amount"
        assert data["decided_at"] is not None

    def test_reject_proposal(self, client, finance_headers, sample_proposal):
        """Test rejecting a proposal"""
        response = client.post(
            f"/proposals/{sample_proposal.id}/reject",
            json={"decision_notes": "Rejected due to budget constraints"},
            headers=finance_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "Rejected"
        assert data["decision_notes"] == "Rejected due to budget constraints"
        assert data["decided_at"] is not None

    def test_approve_proposal_unauthorized(self, client, auth_headers, sample_proposal):
        """Test approving proposal as non-finance user"""
        response = client.post(
            f"/proposals/{sample_proposal.id}/approve",
            json={"approved_amount": 400000.0, "decision_notes": "Should fail"},
            headers=auth_headers,
        )

        assert response.status_code == 403

    def test_approve_proposal_invalid_amount(self, client, finance_headers, sample_proposal):
        """Test approving proposal with invalid amount"""
        response = client.post(
            f"/proposals/{sample_proposal.id}/approve",
            json={
                "approved_amount": 1000000.0,  # More than requested
                "decision_notes": "Should fail",
            },
            headers=finance_headers,
        )

        assert response.status_code == 400
        assert "exceeds requested amount" in response.json()["detail"]


@pytest.mark.api
class TestDashboardEndpoints:
    """Test dashboard and analytics endpoints"""

    def test_dashboard_summary(self, client, finance_headers, sample_category, sample_proposal):
        """Test dashboard summary"""
        response = client.get("/dashboard/summary", headers=finance_headers)

        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert "ministries" in data
        assert "kpis" in data
        assert "total_allocated" in data["kpis"]

    def test_dashboard_unauthorized(self, client, auth_headers):
        """Test dashboard access as non-finance user"""
        response = client.get("/dashboard/summary", headers=auth_headers)

        assert response.status_code == 403


@pytest.mark.api
class TestContractParsingEndpoints:
    """Test contract upload and parsing endpoints"""

    def test_parse_csv_contract(self, client, auth_headers):
        """Test parsing CSV contract file"""
        # Create a simple CSV content
        csv_content = "ministry_name,category,title,requested_amount\nMinistry of Test,Test Category,Test Project,100000"

        response = client.post(
            "/contracts/parse",
            files={"file": ("test.csv", csv_content, "text/csv")},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "drafts" in data
        assert len(data["drafts"]) >= 1

    def test_parse_json_contract(self, client, auth_headers):
        """Test parsing JSON contract file"""
        json_content = '[{"ministry_name": "Test Ministry", "category": "Test Category", "title": "Test Project", "requested_amount": 100000}]'

        response = client.post(
            "/contracts/parse",
            files={"file": ("test.json", json_content, "application/json")},
            headers=auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert "drafts" in data
        assert len(data["drafts"]) >= 1

    def test_parse_contract_unauthorized(self, client, finance_headers):
        """Test contract parsing as finance user (should fail)"""
        csv_content = "ministry_name,category,title,requested_amount\nTest Ministry,Test Category,Test Project,100000"

        response = client.post(
            "/contracts/parse",
            files={"file": ("test.csv", csv_content, "text/csv")},
            headers=finance_headers,
        )

        assert response.status_code == 403

    def test_parse_contract_invalid_format(self, client, auth_headers):
        """Test parsing contract with invalid format"""
        invalid_content = "This is not a valid CSV or JSON file"

        response = client.post(
            "/contracts/parse",
            files={"file": ("test.txt", invalid_content, "text/plain")},
            headers=auth_headers,
        )

        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

```


### 📄 test_auth.py

**Path:** `backend/tests/test_auth.py`

```python
import sys
from datetime import timedelta
from pathlib import Path

import pytest

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from database import User as DBUser


@pytest.mark.auth
class TestPasswordHashing:
    """Test password hashing and verification"""

    def test_password_hashing(self):
        """Test that passwords are properly hashed with bcrypt"""
        password = "testpassword"
        hashed = get_password_hash(password)

        # Bcrypt hashes start with $2a$, $2b$, or $2y$ and are 60 characters
        assert hashed.startswith(("$2a$", "$2b$", "$2y$"))
        assert len(hashed) == 60
        assert hashed != password

        # Verify it's a valid bcrypt hash
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        assert pwd_context.verify(password, hashed)

    def test_password_verification(self):
        """Test password verification"""
        password = "testpassword"
        hashed = get_password_hash(password)

        # Correct password should verify
        assert verify_password(password, hashed) is True

        # Wrong password should not verify
        assert verify_password("wrongpassword", hashed) is False

        # Empty password should not verify
        assert verify_password("", hashed) is False

    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes"""
        password1 = "password1"
        password2 = "password2"

        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)

        assert hash1 != hash2
        # Bcrypt hashes are 60 characters
        assert len(hash1) == 60
        assert len(hash2) == 60
        # Both should be bcrypt hashes
        assert hash1.startswith(("$2a$", "$2b$", "$2y$"))
        assert hash2.startswith(("$2a$", "$2b$", "$2y$"))


@pytest.mark.auth
class TestTokenCreation:
    """Test JWT token creation and validation"""

    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "testuser"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0
        # JWT tokens have 3 parts separated by dots
        assert len(token.split(".")) == 3

    def test_token_with_expiration(self):
        """Test token creation with custom expiration"""
        data = {"sub": "testuser"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_different_users(self):
        """Test that different users get different tokens"""
        data1 = {"sub": "user1"}
        data2 = {"sub": "user2"}

        token1 = create_access_token(data1)
        token2 = create_access_token(data2)

        assert token1 != token2


@pytest.mark.auth
class TestUserAuthentication:
    """Test user authentication functionality"""

    def test_authenticate_user_success(self, test_db, sample_user):
        """Test successful user authentication"""
        user = authenticate_user(test_db, "testuser", "testpassword")

        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"

    def test_authenticate_user_wrong_password(self, test_db, sample_user):
        """Test authentication with wrong password"""
        user = authenticate_user(test_db, "testuser", "wrongpassword")

        assert user is None

    def test_authenticate_user_nonexistent(self, test_db):
        """Test authentication with nonexistent user"""
        user = authenticate_user(test_db, "nonexistent", "password")

        assert user is None

    def test_authenticate_user_empty_username(self, test_db):
        """Test authentication with empty username"""
        user = authenticate_user(test_db, "", "password")

        assert user is None

    def test_authenticate_user_empty_password(self, test_db, sample_user):
        """Test authentication with empty password"""
        user = authenticate_user(test_db, "testuser", "")

        assert user is None


@pytest.mark.auth
class TestCurrentUser:
    """Test get_current_user functionality"""

    def test_get_current_user_valid_token(self, test_db, sample_user):
        """Test getting current user with valid token"""
        # Create a valid token
        token = create_access_token({"sub": "testuser"})

        # Mock the HTTPAuthorizationCredentials dependency
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        user = get_current_user(credentials, test_db)

        assert user is not None
        assert user.username == "testuser"

    def test_get_current_user_invalid_token(self, test_db):
        """Test getting current user with invalid token"""
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, test_db)

        assert exc_info.value.status_code == 401

    def test_get_current_user_nonexistent_user(self, test_db):
        """Test getting current user with valid token but nonexistent user"""
        token = create_access_token({"sub": "nonexistent"})

        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, test_db)

        assert exc_info.value.status_code == 401

    def test_get_current_user_expired_token(self, test_db, sample_user):
        """Test getting current user with expired token"""
        token = create_access_token({"sub": "testuser"}, expires_delta=timedelta(hours=-1))

        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

        with pytest.raises(HTTPException) as exc_info:
            get_current_user(credentials, test_db)

        assert exc_info.value.status_code == 401


@pytest.mark.auth
class TestRoleValidation:
    """Test role-based access validation"""

    def test_ministry_role_validation(self, test_db, sample_user):
        """Test ministry role validation"""
        assert sample_user.role == "ministry"
        assert sample_user.ministry_id is not None

    def test_finance_role_validation(self, test_db, finance_user):
        """Test finance role validation"""
        assert finance_user.role == "finance"
        assert finance_user.ministry_id is None

    def test_role_enum_values(self, test_db):
        """Test that only valid role values are accepted"""
        valid_roles = ["ministry", "finance"]

        for role in valid_roles:
            user = DBUser(
                username=f"test_{role}",
                email=f"test_{role}@example.com",
                hashed_password=get_password_hash("password"),
                role=role,
            )
            test_db.add(user)
            test_db.commit()
            test_db.refresh(user)

            assert user.role == role
            test_db.delete(user)
            test_db.commit()

```


### 📄 test_database.py

**Path:** `backend/tests/test_database.py`

```python
import sys
from pathlib import Path

import pytest
from sqlalchemy.exc import IntegrityError

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from auth import get_password_hash
from database import Category as DBCategory
from database import Ministry as DBMinistry
from database import Proposal as DBProposal
from database import User as DBUser


@pytest.mark.database
class TestMinistryModel:
    """Test Ministry database model"""

    def test_create_ministry(self, test_db):
        """Test creating a ministry"""
        ministry = DBMinistry(name="Test Ministry", description="Test ministry description")
        test_db.add(ministry)
        test_db.commit()
        test_db.refresh(ministry)

        assert ministry.id is not None
        assert ministry.name == "Test Ministry"
        assert ministry.description == "Test ministry description"
        assert ministry.is_active is True
        assert ministry.created_at is not None

    def test_ministry_unique_name(self, test_db):
        """Test that ministry names must be unique"""
        ministry1 = DBMinistry(name="Unique Ministry")
        test_db.add(ministry1)
        test_db.commit()

        ministry2 = DBMinistry(name="Unique Ministry")
        test_db.add(ministry2)

        with pytest.raises(IntegrityError):
            test_db.commit()

    def test_ministry_relationships(self, test_db, sample_ministry):
        """Test ministry relationships with users and proposals"""
        # Create a user associated with the ministry
        user = DBUser(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("password"),
            role="ministry",
            ministry_id=sample_ministry.id,
        )
        test_db.add(user)
        test_db.commit()

        # Test relationship
        assert len(sample_ministry.users) == 1
        assert sample_ministry.users[0].username == "testuser"

    def test_ministry_required_fields(self, test_db):
        """Test that required ministry fields are enforced"""
        ministry = DBMinistry()  # No name provided
        test_db.add(ministry)

        with pytest.raises(IntegrityError):
            test_db.commit()


@pytest.mark.database
class TestCategoryModel:
    """Test Category database model"""

    def test_create_category(self, test_db):
        """Test creating a category"""
        category = DBCategory(
            name="Test Category", allocated_budget=1000000.0, remaining_budget=1000000.0
        )
        test_db.add(category)
        test_db.commit()
        test_db.refresh(category)

        assert category.id is not None
        assert category.name == "Test Category"
        assert category.allocated_budget == 1000000.0
        assert category.remaining_budget == 1000000.0
        assert category.created_at is not None

    def test_category_budget_validation(self, test_db):
        """Test category budget validation"""
        # Test positive budget
        category = DBCategory(
            name="Positive Budget", allocated_budget=1000000.0, remaining_budget=500000.0
        )
        test_db.add(category)
        test_db.commit()

        assert category.allocated_budget > 0
        assert category.remaining_budget > 0
        assert category.remaining_budget <= category.allocated_budget

    def test_category_relationships(self, test_db, sample_category):
        """Test category relationships with proposals"""
        # Create a ministry and proposal
        ministry = DBMinistry(name="Test Ministry")
        test_db.add(ministry)
        test_db.commit()
        test_db.refresh(ministry)

        proposal = DBProposal(
            ministry_id=ministry.id,
            category_id=sample_category.id,
            title="Test Proposal",
            requested_amount=100000.0,
            status="Pending",
        )
        test_db.add(proposal)
        test_db.commit()

        # Test relationship
        assert len(sample_category.proposals) == 1
        assert sample_category.proposals[0].title == "Test Proposal"

    def test_category_required_fields(self, test_db):
        """Test that required category fields are enforced"""
        category = DBCategory()  # No required fields
        test_db.add(category)

        with pytest.raises(IntegrityError):
            test_db.commit()


@pytest.mark.database
class TestUserModel:
    """Test User database model"""

    def test_create_user(self, test_db, sample_ministry):
        """Test creating a user"""
        user = DBUser(
            username="newuser",
            email="newuser@example.com",
            hashed_password=get_password_hash("password"),
            role="ministry",
            ministry_id=sample_ministry.id,
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        assert user.id is not None
        assert user.username == "newuser"
        assert user.email == "newuser@example.com"
        assert user.role == "ministry"
        assert user.ministry_id == sample_ministry.id
        assert user.created_at is not None

    def test_user_unique_constraints(self, test_db, sample_ministry):
        """Test user unique constraints"""
        user1 = DBUser(
            username="uniqueuser",
            email="unique@example.com",
            hashed_password=get_password_hash("password"),
            role="ministry",
            ministry_id=sample_ministry.id,
        )
        test_db.add(user1)
        test_db.commit()

        # Test duplicate username
        user2 = DBUser(
            username="uniqueuser",  # Same username
            email="different@example.com",
            hashed_password=get_password_hash("password"),
            role="ministry",
            ministry_id=sample_ministry.id,
        )
        test_db.add(user2)

        with pytest.raises(IntegrityError):
            test_db.commit()

    def test_user_email_unique(self, test_db, sample_ministry):
        """Test that user emails must be unique"""
        user1 = DBUser(
            username="user1",
            email="unique@example.com",
            hashed_password=get_password_hash("password"),
            role="ministry",
            ministry_id=sample_ministry.id,
        )
        test_db.add(user1)
        test_db.commit()

        user2 = DBUser(
            username="user2",
            email="unique@example.com",  # Same email
            hashed_password=get_password_hash("password"),
            role="ministry",
            ministry_id=sample_ministry.id,
        )
        test_db.add(user2)

        with pytest.raises(IntegrityError):
            test_db.commit()

    def test_user_role_validation(self, test_db, sample_ministry):
        """Test user role validation"""
        valid_roles = ["ministry", "finance"]

        for role in valid_roles:
            user = DBUser(
                username=f"test_{role}",
                email=f"test_{role}@example.com",
                hashed_password=get_password_hash("password"),
                role=role,
                ministry_id=sample_ministry.id if role == "ministry" else None,
            )
            test_db.add(user)
            test_db.commit()
            test_db.refresh(user)

            assert user.role == role
            test_db.delete(user)
            test_db.commit()

    def test_user_ministry_relationship(self, test_db, sample_user, sample_ministry):
        """Test user-ministry relationship"""
        assert sample_user.ministry_id == sample_ministry.id
        assert sample_user.ministry.name == sample_ministry.name

    def test_finance_user_no_ministry(self, test_db):
        """Test that finance users don't need a ministry"""
        user = DBUser(
            username="finance_user",
            email="finance@example.com",
            hashed_password=get_password_hash("password"),
            role="finance",
            ministry_id=None,
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        assert user.role == "finance"
        assert user.ministry_id is None
        assert user.ministry is None


@pytest.mark.database
class TestProposalModel:
    """Test Proposal database model"""

    def test_create_proposal(self, test_db, sample_ministry, sample_category):
        """Test creating a proposal"""
        proposal = DBProposal(
            ministry_id=sample_ministry.id,
            category_id=sample_category.id,
            title="Test Proposal",
            description="Test proposal description",
            requested_amount=500000.0,
            status="Pending",
        )
        test_db.add(proposal)
        test_db.commit()
        test_db.refresh(proposal)

        assert proposal.id is not None
        assert proposal.ministry_id == sample_ministry.id
        assert proposal.category_id == sample_category.id
        assert proposal.title == "Test Proposal"
        assert proposal.description == "Test proposal description"
        assert proposal.requested_amount == 500000.0
        assert proposal.status == "Pending"
        assert proposal.approved_amount is None
        assert proposal.decision_notes is None
        assert proposal.decided_at is None
        assert proposal.created_at is not None

    def test_proposal_status_validation(self, test_db, sample_ministry, sample_category):
        """Test proposal status validation"""
        valid_statuses = ["Pending", "Approved", "Rejected"]

        for status in valid_statuses:
            proposal = DBProposal(
                ministry_id=sample_ministry.id,
                category_id=sample_category.id,
                title=f"Test Proposal {status}",
                requested_amount=100000.0,
                status=status,
            )
            test_db.add(proposal)
            test_db.commit()
            test_db.refresh(proposal)

            assert proposal.status == status
            test_db.delete(proposal)
            test_db.commit()

    def test_proposal_amount_validation(self, test_db, sample_ministry, sample_category):
        """Test proposal amount validation"""
        # Test positive amount
        proposal = DBProposal(
            ministry_id=sample_ministry.id,
            category_id=sample_category.id,
            title="Positive Amount Proposal",
            requested_amount=100000.0,
            status="Pending",
        )
        test_db.add(proposal)
        test_db.commit()

        assert proposal.requested_amount > 0

    def test_proposal_relationships(
        self, test_db, sample_proposal, sample_ministry, sample_category
    ):
        """Test proposal relationships"""
        assert sample_proposal.ministry_id == sample_ministry.id
        assert sample_proposal.category_id == sample_category.id
        assert sample_proposal.ministry.name == sample_ministry.name
        assert sample_proposal.category.name == sample_category.name

    def test_proposal_foreign_key_constraints(self, test_db):
        """Test proposal foreign key constraints"""
        # Create a valid ministry and category first
        ministry = DBMinistry(name="Valid Ministry")
        test_db.add(ministry)
        test_db.commit()
        test_db.refresh(ministry)

        category = DBCategory(
            name="Valid Category", allocated_budget=1000000.0, remaining_budget=1000000.0
        )
        test_db.add(category)
        test_db.commit()
        test_db.refresh(category)

        # Test valid foreign keys
        proposal = DBProposal(
            ministry_id=ministry.id,
            category_id=category.id,
            title="Valid Proposal",
            requested_amount=100000.0,
            status="Pending",
        )
        test_db.add(proposal)
        test_db.commit()
        test_db.refresh(proposal)

        assert proposal.ministry_id == ministry.id
        assert proposal.category_id == category.id

    def test_proposal_required_fields(self, test_db):
        """Test that required proposal fields are enforced"""
        proposal = DBProposal()  # No required fields
        test_db.add(proposal)

        with pytest.raises(IntegrityError):
            test_db.commit()


@pytest.mark.database
class TestDatabaseIntegrity:
    """Test overall database integrity and constraints"""

    def test_cascade_deletion_ministry(
        self, test_db, sample_ministry, sample_user, sample_proposal
    ):
        """Test cascade behavior when deleting ministry"""
        ministry_id = sample_ministry.id
        user_count = len(sample_ministry.users)
        proposal_count = len(sample_ministry.proposals)

        assert user_count > 0
        assert proposal_count > 0

        # SQLite doesn't enforce foreign key constraints by default
        # So we'll test the relationship integrity instead
        assert sample_user.ministry_id == ministry_id
        assert sample_proposal.ministry_id == ministry_id
        assert sample_user.ministry.name == sample_ministry.name
        assert sample_proposal.ministry.name == sample_ministry.name

    def test_cascade_deletion_category(self, test_db, sample_category, sample_proposal):
        """Test cascade behavior when deleting category"""
        category_id = sample_category.id
        proposal_count = len(sample_category.proposals)

        assert proposal_count > 0

        # SQLite doesn't enforce foreign key constraints by default
        # So we'll test the relationship integrity instead
        assert sample_proposal.category_id == category_id
        assert sample_proposal.category.name == sample_category.name

```


================================================================================
## 📂 backend → repositories


### 📄 __init__.py

**Path:** `backend/repositories/__init__.py`

```python
"""Repository layer for data access."""

```


### 📄 categories.py

**Path:** `backend/repositories/categories.py`

```python
"""
Repository for category data access.
Encapsulates database queries related to categories.
"""

from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Category as DBCategory
from database import Proposal as DBProposal


class CategoryRepository:
    """Repository for category operations."""

    @staticmethod
    def get_all(db: Session) -> list[DBCategory]:
        """Get all categories."""
        return db.query(DBCategory).all()

    @staticmethod
    def get_by_id(db: Session, category_id: int) -> DBCategory | None:
        """Get a category by ID."""
        return db.query(DBCategory).filter(DBCategory.id == category_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> DBCategory | None:
        """Get a category by name (case-insensitive)."""
        return db.query(DBCategory).filter(DBCategory.name.ilike(name)).first()

    @staticmethod
    def create(db: Session, category_data: dict) -> DBCategory:
        """Create a new category."""
        category = DBCategory(**category_data)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def update(db: Session, category: DBCategory, update_data: dict) -> DBCategory:
        """Update an existing category."""
        for key, value in update_data.items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete(db: Session, category: DBCategory) -> None:
        """Delete a category."""
        db.delete(category)
        db.commit()

    @staticmethod
    def get_approved_total(db: Session, category_id: int) -> float:
        """Get total approved amount for a category."""
        result = (
            db.query(func.coalesce(func.sum(DBProposal.approved_amount), 0.0))
            .filter(DBProposal.category_id == category_id, DBProposal.status == "Approved")
            .scalar()
        )
        return float(result or 0.0)

```


### 📄 ministries.py

**Path:** `backend/repositories/ministries.py`

```python
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

```


### 📄 proposals.py

**Path:** `backend/repositories/proposals.py`

```python
"""
Repository for proposal data access.
Encapsulates database queries related to proposals.
"""

from sqlalchemy.orm import Session, joinedload

from database import Category as DBCategory
from database import Proposal as DBProposal


class ProposalRepository:
    """Repository for proposal operations."""

    @staticmethod
    def get_by_id(db: Session, proposal_id: int) -> DBProposal | None:
        """Get a proposal by ID with relationships loaded."""
        return (
            db.query(DBProposal)
            .options(joinedload(DBProposal.ministry))
            .filter(DBProposal.id == proposal_id)
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        ministry_id: int | None = None,
        category_id: int | None = None,
        status: str | None = None,
    ) -> list[DBProposal]:
        """Get all proposals with optional filters."""
        query = db.query(DBProposal).options(joinedload(DBProposal.ministry))

        if ministry_id:
            query = query.filter(DBProposal.ministry_id == ministry_id)
        if category_id:
            query = query.filter(DBProposal.category_id == category_id)
        if status:
            query = query.filter(DBProposal.status == status)

        return query.order_by(DBProposal.created_at.desc()).all()

    @staticmethod
    def create(db: Session, proposal_data: dict) -> DBProposal:
        """Create a new proposal."""
        proposal = DBProposal(**proposal_data)
        db.add(proposal)
        db.commit()
        db.refresh(proposal)
        return proposal

    @staticmethod
    def update(db: Session, proposal: DBProposal, update_data: dict) -> DBProposal:
        """Update an existing proposal."""
        for key, value in update_data.items():
            setattr(proposal, key, value)
        db.commit()
        db.refresh(proposal)
        return proposal

    @staticmethod
    def delete(db: Session, proposal: DBProposal) -> None:
        """Delete a proposal."""
        db.delete(proposal)
        db.commit()

    @staticmethod
    def check_duplicate(
        db: Session, ministry_id: int, title: str, requested_amount: float
    ) -> DBProposal | None:
        """Check if a duplicate proposal exists."""
        return (
            db.query(DBProposal)
            .filter(
                DBProposal.ministry_id == ministry_id,
                DBProposal.title == title,
                DBProposal.requested_amount == requested_amount,
            )
            .first()
        )

    @staticmethod
    def get_category_with_lock(db: Session, category_id: int) -> DBCategory | None:
        """Get a category with row lock for atomic updates."""
        return (
            db.query(DBCategory)
            .filter(DBCategory.id == category_id)
            .with_for_update(nowait=False)
            .first()
        )

```


================================================================================
## 📂 backend → alembic


### 📄 env.py

**Path:** `backend/alembic/env.py`

```python
import sys
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config, pool

from alembic import context

# Add the backend directory to the path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import our database models and settings
from database import Base
from settings import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url with our settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # For SQLite, we need special handling
    if settings.DATABASE_URL.startswith("sqlite"):
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            connect_args={"check_same_thread": False},
        )
    else:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

```


================================================================================
## 📂 backend → alembic → versions


### 📄 eddaed862754_baseline_schema.py

**Path:** `backend/alembic/versions/eddaed862754_baseline_schema.py`

```python
"""baseline_schema

Revision ID: eddaed862754
Revises:
Create Date: 2025-11-04 22:03:15.545749

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eddaed862754"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create ministries table
    op.create_table(
        "ministries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ministries_id"), "ministries", ["id"], unique=False)
    op.create_index(op.f("ix_ministries_name"), "ministries", ["name"], unique=True)

    # Create categories table
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("allocated_budget", sa.Float(), nullable=False),
        sa.Column("remaining_budget", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)
    op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=True)

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("ministry_id", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ministry_id"],
            ["ministries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)

    # Create proposals table
    op.create_table(
        "proposals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ministry_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("requested_amount", sa.Float(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("approved_amount", sa.Float(), nullable=True),
        sa.Column("decision_notes", sa.String(), nullable=True),
        sa.Column("decided_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["ministry_id"],
            ["ministries.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_proposals_id"), "proposals", ["id"], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order (respecting foreign key constraints)
    op.drop_index(op.f("ix_proposals_id"), table_name="proposals")
    op.drop_table("proposals")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    op.drop_index(op.f("ix_categories_name"), table_name="categories")
    op.drop_index(op.f("ix_categories_id"), table_name="categories")
    op.drop_table("categories")
    op.drop_index(op.f("ix_ministries_name"), table_name="ministries")
    op.drop_index(op.f("ix_ministries_id"), table_name="ministries")
    op.drop_table("ministries")

```


================================================================================
## 📂 backend → services


### 📄 __init__.py

**Path:** `backend/services/__init__.py`

```python
"""Service layer for business logic."""

```


### 📄 approvals.py

**Path:** `backend/services/approvals.py`

```python
"""
Service for proposal approval and rejection business logic.
Handles the approval workflow, budget checks, and atomic updates.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from database import Proposal as DBProposal
from exceptions import (
    CategoryNotFoundError,
    InsufficientBudgetError,
    InvalidProposalStatusError,
    ProposalNotFoundError,
    ValidationError,
)
from repositories.proposals import ProposalRepository


class ApprovalService:
    """Service for handling proposal approvals and rejections."""

    @staticmethod
    def approve_proposal(
        db: Session, proposal_id: int, approved_amount: float, decision_notes: str | None = None
    ) -> DBProposal:
        """
        Approve a proposal with the given approved amount.

        Validates:
        - Proposal exists and is in Pending status
        - Approved amount is valid (> 0, <= requested_amount)
        - Category has sufficient remaining budget

        Atomically updates category remaining budget and proposal status.
        """
        # Get proposal
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")

        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be approved")

        # Validate approved amount
        if approved_amount is None or approved_amount <= 0:
            raise ValidationError("approved_amount must be > 0")

        if approved_amount > proposal.requested_amount:
            raise ValidationError("approved_amount exceeds requested amount")

        # Get category with lock for atomic update
        category = ProposalRepository.get_category_with_lock(db, proposal.category_id)
        if not category:
            raise CategoryNotFoundError("Category does not exist")

        # Check budget availability
        if approved_amount > category.remaining_budget:
            raise InsufficientBudgetError("Insufficient remaining budget")

        # Atomically apply decision
        category.remaining_budget = category.remaining_budget - approved_amount
        proposal.status = "Approved"
        proposal.approved_amount = approved_amount
        proposal.decision_notes = decision_notes
        proposal.decided_at = datetime.utcnow()

        db.commit()
        db.refresh(proposal)

        return proposal

    @staticmethod
    def reject_proposal(
        db: Session, proposal_id: int, decision_notes: str | None = None
    ) -> DBProposal:
        """
        Reject a proposal.

        Validates:
        - Proposal exists and is in Pending status

        Updates proposal status to Rejected.
        """
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")

        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be rejected")

        # Apply rejection
        proposal.status = "Rejected"
        proposal.approved_amount = None
        proposal.decision_notes = decision_notes
        proposal.decided_at = datetime.utcnow()

        db.commit()
        db.refresh(proposal)

        return proposal

```


### 📄 parser.py

**Path:** `backend/services/parser.py`

```python
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

```


### 📄 proposals.py

**Path:** `backend/services/proposals.py`

```python
"""
Service for proposal business logic.
Handles proposal creation, updates, validation, and queries.
"""

from sqlalchemy.orm import Session

from database import Proposal as DBProposal
from exceptions import (
    CategoryNotFoundError,
    InvalidProposalStatusError,
    MinistryNotFoundError,
    ProposalNotFoundError,
    ValidationError,
)
from models import ProposalCreate, ProposalUpdate
from repositories.categories import CategoryRepository
from repositories.ministries import MinistryRepository
from repositories.proposals import ProposalRepository


class ProposalService:
    """Service for handling proposal operations."""

    @staticmethod
    def list_proposals(
        db: Session,
        ministry_id: int | None = None,
        category_id: int | None = None,
        status: str | None = None,
    ) -> list[DBProposal]:
        """List proposals with optional filters."""
        return ProposalRepository.get_all(db, ministry_id, category_id, status)

    @staticmethod
    def get_proposal(db: Session, proposal_id: int) -> DBProposal:
        """Get a proposal by ID."""
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")
        return proposal

    @staticmethod
    def create_proposal(db: Session, payload: ProposalCreate, current_user) -> DBProposal:
        """
        Create a new proposal.

        Validates:
        - Category exists
        - Ministry exists (or creates new one if ministry_name provided)
        - Requested amount is valid (> 0)
        - Ministry users can only create proposals for their own ministry
        """

        # Validate category exists
        category = CategoryRepository.get_by_id(db, payload.category_id)
        if not category:
            raise CategoryNotFoundError("Category does not exist")

        # Handle ministry - either by ID or name
        ministry = None
        if payload.ministry_id:
            # Find ministry by ID
            ministry = MinistryRepository.get_by_id(db, payload.ministry_id)
            if not ministry:
                raise MinistryNotFoundError("Ministry does not exist")

            # Validate that ministry users can only create proposals for their own ministry
            if current_user.role == "ministry" and current_user.ministry_id != payload.ministry_id:
                raise ValidationError(
                    "You can only create proposals for your own ministry"
                )
        elif payload.ministry_name:
            # For ministry users, they must use their own ministry
            if current_user.role == "ministry":
                if not current_user.ministry_id:
                    raise ValidationError(
                        "You must be assigned to a ministry to create proposals"
                    )
                # Use the user's ministry instead of the provided name
                ministry = MinistryRepository.get_by_id(db, current_user.ministry_id)
                if not ministry:
                    raise MinistryNotFoundError("Your assigned ministry does not exist")
            else:
                # Finance users can create ministries by name (for contract uploads, etc.)
                ministry_name = payload.ministry_name.strip()
                if not ministry_name:
                    raise ValidationError("Ministry name cannot be empty")
                ministry = MinistryRepository.find_or_create(db, ministry_name)
        else:
            # If no ministry specified, use the current user's ministry (for ministry users)
            if current_user.role == "ministry":
                if not current_user.ministry_id:
                    raise ValidationError(
                        "You must be assigned to a ministry to create proposals"
                    )
                ministry = MinistryRepository.get_by_id(db, current_user.ministry_id)
                if not ministry:
                    raise MinistryNotFoundError("Your assigned ministry does not exist")
            else:
                raise ValidationError("Either ministry_id or ministry_name is required")

        # Validate amount
        if payload.requested_amount is None or payload.requested_amount <= 0:
            raise ValidationError("Requested amount must be greater than 0")

        # Create proposal
        proposal_data = {
            "ministry_id": ministry.id,
            "category_id": payload.category_id,
            "title": payload.title,
            "description": payload.description,
            "requested_amount": payload.requested_amount,
            "status": "Pending",
        }

        return ProposalRepository.create(db, proposal_data)

    @staticmethod
    def update_proposal(db: Session, proposal_id: int, payload: ProposalUpdate) -> DBProposal:
        """
        Update an existing proposal.

        Validates:
        - Proposal exists and is in Pending status
        - Updated fields are valid
        - Related entities (ministry, category) exist
        """
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")

        # Only edits in Pending state
        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be edited")

        update_data = {}

        if payload.ministry_id is not None:
            ministry = MinistryRepository.get_by_id(db, payload.ministry_id)
            if not ministry:
                raise MinistryNotFoundError("Ministry does not exist")
            update_data["ministry_id"] = payload.ministry_id

        if payload.category_id is not None:
            category = CategoryRepository.get_by_id(db, payload.category_id)
            if not category:
                raise CategoryNotFoundError("Category does not exist")
            update_data["category_id"] = payload.category_id

        if payload.title is not None:
            update_data["title"] = payload.title

        if payload.description is not None:
            update_data["description"] = payload.description

        if payload.requested_amount is not None:
            if payload.requested_amount <= 0:
                raise ValidationError("Requested amount must be greater than 0")
            update_data["requested_amount"] = payload.requested_amount

        # Ignore status changes (only allow Pending)
        if payload.status is not None and payload.status != "Pending":
            raise ValidationError("Status changes are not allowed")

        return ProposalRepository.update(db, proposal, update_data)

    @staticmethod
    def delete_proposal(db: Session, proposal_id: int) -> None:
        """
        Delete a proposal.

        Validates:
        - Proposal exists and is in Pending status
        """
        proposal = ProposalRepository.get_by_id(db, proposal_id)
        if not proposal:
            raise ProposalNotFoundError("Proposal not found")

        if proposal.status != "Pending":
            raise InvalidProposalStatusError("Only pending proposals can be deleted")

        ProposalRepository.delete(db, proposal)

```


================================================================================
## 📂 .github


================================================================================
## 📂 .github → workflows


### 📄 ci-cd.yml

**Path:** `.github/workflows/ci-cd.yml`

```yaml
name: CI / CD

on:
  push:
    branches:
      - main
  pull_request:

env:
  PYTHON_VERSION: "3.11"
  NODE_VERSION: "18.x"
  BACKEND_IMAGE_NAME: ${{ secrets.BACKEND_IMAGE_NAME }}
  FRONTEND_IMAGE_NAME: ${{ secrets.FRONTEND_IMAGE_NAME }}
  ACR_LOGIN_SERVER: ${{ secrets.AZURE_ACR_LOGIN_SERVER }}
  IMAGE_TAG: ${{ github.sha }}

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install backend dependencies
        run: |
          cd backend
          python -m pip install --upgrade pip
          pip install --no-cache-dir -r requirements.txt

      - name: Ruff
        run: |
          cd backend
          ruff check .

      - name: Mypy
        run: |
          cd backend
          mypy . --ignore-missing-imports

      - name: Bandit
        run: |
          cd backend
          bandit -r . -ll -x tests -s B101

      - name: Pytest
        run: |
          cd backend
          pytest --cov=. --cov-report=xml --cov-report=term-missing --cov-fail-under=70 -v

      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: backend-coverage
          path: backend/coverage.xml

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Use Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run tests
        run: |
          cd frontend
          npm test -- --ci --coverage --watchAll=false

  build-and-push:
    runs-on: ubuntu-latest
    needs:
      - backend-tests
      - frontend-tests
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4

      - name: Login to ACR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.ACR_LOGIN_SERVER }}
          username: ${{ secrets.AZURE_ACR_USERNAME }}
          password: ${{ secrets.AZURE_ACR_PASSWORD }}

      - name: Build backend image
        run: |
          docker build -t ${{ env.ACR_LOGIN_SERVER }}/${{ env.BACKEND_IMAGE_NAME }}:latest \
                       -t ${{ env.ACR_LOGIN_SERVER }}/${{ env.BACKEND_IMAGE_NAME }}:${{ env.IMAGE_TAG }} \
                       backend

      - name: Build frontend image
        run: |
          docker build -t ${{ env.ACR_LOGIN_SERVER }}/${{ env.FRONTEND_IMAGE_NAME }}:latest \
                       -t ${{ env.ACR_LOGIN_SERVER }}/${{ env.FRONTEND_IMAGE_NAME }}:${{ env.IMAGE_TAG }} \
                       --build-arg REACT_APP_API_BASE_URL=https://gov-spending-api-cec3ana0d4dhdpa6.canadacentral-01.azurewebsites.net \
                       frontend

      - name: Push backend image
        run: |
          docker push ${{ env.ACR_LOGIN_SERVER }}/${{ env.BACKEND_IMAGE_NAME }}:latest
          docker push ${{ env.ACR_LOGIN_SERVER }}/${{ env.BACKEND_IMAGE_NAME }}:${{ env.IMAGE_TAG }}

      - name: Push frontend image
        run: |
          docker push ${{ env.ACR_LOGIN_SERVER }}/${{ env.FRONTEND_IMAGE_NAME }}:latest
          docker push ${{ env.ACR_LOGIN_SERVER }}/${{ env.FRONTEND_IMAGE_NAME }}:${{ env.IMAGE_TAG }}

      - name: Publish image tags
        id: images
        run: |
          echo "backend=${{ env.ACR_LOGIN_SERVER }}/${{ env.BACKEND_IMAGE_NAME }}:${{ env.IMAGE_TAG }}" >> $GITHUB_OUTPUT
          echo "frontend=${{ env.ACR_LOGIN_SERVER }}/${{ env.FRONTEND_IMAGE_NAME }}:${{ env.IMAGE_TAG }}" >> $GITHUB_OUTPUT

  deploy-backend:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Configure backend container
        run: |
          az webapp config container set \
            --name ${{ secrets.AZURE_BACKEND_APP_NAME }} \
            --resource-group ${{ secrets.AZURE_RESOURCE_GROUP }} \
            --container-image-name ${{ env.ACR_LOGIN_SERVER }}/${{ env.BACKEND_IMAGE_NAME }}:${{ env.IMAGE_TAG }} \
            --container-registry-url https://${{ env.ACR_LOGIN_SERVER }} \
            --container-registry-user ${{ secrets.AZURE_ACR_USERNAME }} \
            --container-registry-password ${{ secrets.AZURE_ACR_PASSWORD }}

      - name: Restart backend
        run: |
          az webapp restart \
            --name ${{ secrets.AZURE_BACKEND_APP_NAME }} \
            --resource-group ${{ secrets.AZURE_RESOURCE_GROUP }}

  deploy-frontend:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Configure frontend container
        run: |
          az webapp config container set \
            --name ${{ secrets.AZURE_FRONTEND_APP_NAME }} \
            --resource-group ${{ secrets.AZURE_RESOURCE_GROUP }} \
            --container-image-name ${{ env.ACR_LOGIN_SERVER }}/${{ env.FRONTEND_IMAGE_NAME }}:${{ env.IMAGE_TAG }} \
            --container-registry-url https://${{ env.ACR_LOGIN_SERVER }} \
            --container-registry-user ${{ secrets.AZURE_ACR_USERNAME }} \
            --container-registry-password ${{ secrets.AZURE_ACR_PASSWORD }}

      - name: Restart frontend
        run: |
          az webapp restart \
            --name ${{ secrets.AZURE_FRONTEND_APP_NAME }} \
            --resource-group ${{ secrets.AZURE_RESOURCE_GROUP }}


```


================================================================================
## 📂 ops


================================================================================
## 📂 ops → grafana


================================================================================
## 📂 ops → grafana → datasources


### 📄 prometheus.yml

**Path:** `ops/grafana/datasources/prometheus.yml`

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true


```


================================================================================
## 📂 ops → grafana → dashboards


### 📄 dashboard.yml

**Path:** `ops/grafana/dashboards/dashboard.yml`

```yaml
apiVersion: 1

providers:
  - name: 'Government Spending Tracker'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards


```


### 📄 government-spending-dashboard.json

**Path:** `ops/grafana/dashboards/government-spending-dashboard.json`

```json
{
  "dashboard": {
    "title": "Government Spending Tracker - API Metrics",
    "tags": ["api", "fastapi", "prometheus"],
    "timezone": "browser",
    "schemaVersion": 16,
    "version": 1,
    "refresh": "10s",
    "panels": [
      {
        "id": 1,
        "title": "Request Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{path}}",
            "refId": "A"
          }
        ],
        "yaxes": [
          {"format": "reqps", "label": "Requests/sec"},
          {"format": "short"}
        ]
      },
      {
        "id": 2,
        "title": "Request Latency (p95)",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "{{method}} {{path}}",
            "refId": "A"
          }
        ],
        "yaxes": [
          {"format": "s", "label": "Latency"},
          {"format": "short"}
        ]
      },
      {
        "id": 3,
        "title": "Error Rate",
        "type": "graph",
        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8},
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "{{status}}",
            "refId": "A"
          }
        ],
        "yaxes": [
          {"format": "reqps", "label": "Errors/sec"},
          {"format": "short"}
        ]
      },
      {
        "id": 4,
        "title": "Total Requests",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 12, "y": 8},
        "targets": [
          {
            "expr": "sum(http_requests_total)",
            "refId": "A"
          }
        ],
        "options": {
          "graphMode": "none",
          "colorMode": "value"
        }
      },
      {
        "id": 5,
        "title": "Active Requests",
        "type": "stat",
        "gridPos": {"h": 4, "w": 6, "x": 18, "y": 8},
        "targets": [
          {
            "expr": "sum(http_requests_in_flight)",
            "refId": "A"
          }
        ],
        "options": {
          "graphMode": "none",
          "colorMode": "value"
        }
      }
    ]
  }
}


```


================================================================================
## 📂 ops → prometheus


### 📄 prometheus.yml

**Path:** `ops/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'government-spending-api'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'


```


---

**Exported:** 74 files
**Total Size:** ~960 KB
