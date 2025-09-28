# Government Spending Tracker

A web application that simulates how government ministries submit budget proposals to the Ministry of Finance. Finance can approve, partially approve, or reject requests. The system updates category budgets in real time and provides dashboards, history views, and CSV exports for transparency.

## Overview

- Categories represent budget lines (e.g., Education, Health). Each category has an allocated and remaining budget.
- Ministries submit proposals against categories.
- Finance reviews proposals and decides: Approved, Partially Approved, or Rejected.
- Approved amounts are deducted from the category's remaining budget.
- Dashboards visualize allocations and approvals; history views allow filtering and export.

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
│   └── requirements.txt       # Backend dependencies
├── frontend/
│   ├── src/
│   │   ├── api.js             # API clients (categories, proposals, uploads, history)
│   │   ├── CategoryManager.js # Category CRUD UI
│   │   ├── ProposalForm.js    # Proposal submission UI
│   │   ├── ProposalsList.js   # Proposals with actions (Decide)
│   │   ├── ApprovalDialog.js  # Approve/Reject dialog
│   │   ├── ContractUpload.js  # Upload and parse JSON/CSV into proposal drafts
│   │   ├── Dashboard.js       # Charts and KPIs
│   │   ├── HistoryView.js     # History with filters and CSV export
│   │   ├── CategoryManager.css# Styling
│   │   └── App.js             # Composition
│   └── package.json
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

## Notes and Limitations

- Authentication/roles are not included yet; can be added in a future phase
- SQLite is used for local development; Postgres is recommended for multi-user deployments
- FastAPI `on_event` startup is currently used; consider lifespan handlers in future refactors

## Roadmap (Optional next steps)

- Phase 7: Simulation mode, overspending alerts, and basic roles
- DevOps: Docker, docker-compose, CI pipeline, Postgres migrations
- Tests: unit tests for approvals, parsing, and summary aggregation
- UX: drill-down from charts to filtered history, saved filter presets

