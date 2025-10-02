# Database Entity Relationship Diagram (ERD)

## Current Database Schema

### Tables Overview
- **ministries** - Government ministries (unique entities)
- **categories** - Budget categories for government spending
- **users** - System users (ministry and finance roles)
- **proposals** - Spending proposals submitted by ministries

---

## Table Details

### 1. **ministries** Table
```sql
CREATE TABLE ministries (
    id INTEGER PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    description VARCHAR,
    created_at DATETIME,
    is_active BOOLEAN DEFAULT TRUE
);
```

**Purpose**: Stores government ministries with unique names and metadata.

**Fields**:
- `id` - Primary key (auto-increment)
- `name` - Ministry name (unique, required)
- `description` - Optional description of ministry purpose
- `created_at` - Timestamp when ministry was created
- `is_active` - Whether ministry is currently active

**Default Ministries**:
- Ministry of Education (ID: 1)

---

### 2. **categories** Table
```sql
CREATE TABLE categories (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    allocated_budget FLOAT NOT NULL,
    remaining_budget FLOAT NOT NULL,
    created_at DATETIME
);
```

**Purpose**: Stores budget categories with allocated and remaining amounts.

**Fields**:
- `id` - Primary key (auto-increment)
- `name` - Category name (unique)
- `allocated_budget` - Total budget allocated to this category
- `remaining_budget` - Remaining budget available
- `created_at` - Timestamp when category was created

---

### 3. **users** Table
```sql
CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    ministry_id INTEGER REFERENCES ministries(id),
    is_active BOOLEAN,
    created_at DATETIME
);
```

**Purpose**: Stores system users with authentication and role information.

**Fields**:
- `id` - Primary key (auto-increment)
- `username` - Unique username for login
- `email` - Unique email address
- `hashed_password` - SHA256 hashed password
- `role` - User role ("ministry" or "finance")
- `ministry_id` - Foreign key to ministries table (for ministry users only)
- `is_active` - Account status flag
- `created_at` - Timestamp when user was created

**Default Users**:
- Finance: `username: finance`, `password: fin`, `ministry_id: NULL`
- Ministry: `username: ministry`, `password: min`, `ministry_id: 1`

---

### 4. **proposals** Table
```sql
CREATE TABLE proposals (
    id INTEGER NOT NULL PRIMARY KEY,
    ministry_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    requested_amount FLOAT NOT NULL,
    status VARCHAR NOT NULL,
    approved_amount FLOAT,
    decision_notes VARCHAR,
    decided_at DATETIME,
    created_at DATETIME,
    FOREIGN KEY(ministry_id) REFERENCES ministries (id),
    FOREIGN KEY(category_id) REFERENCES categories (id)
);
```

**Purpose**: Stores spending proposals submitted by ministries.

**Fields**:
- `id` - Primary key (auto-increment)
- `ministry_id` - Foreign key to ministries table
- `category_id` - Foreign key to categories table
- `title` - Proposal title
- `description` - Detailed proposal description
- `requested_amount` - Amount requested by ministry
- `status` - Current status ("Pending", "Approved", "Rejected")
- `approved_amount` - Final approved amount (set by finance)
- `decision_notes` - Notes from finance decision
- `decided_at` - Timestamp when decision was made
- `created_at` - Timestamp when proposal was created

---

## Relationships

### 1. **ministries ↔ users**
- **Type**: One-to-Many
- **Description**: One ministry can have many users
- **Foreign Key**: `users.ministry_id` → `ministries.id`
- **Business Rule**: Ministry users must belong to exactly one ministry

### 2. **ministries ↔ proposals**
- **Type**: One-to-Many
- **Description**: One ministry can have many proposals
- **Foreign Key**: `proposals.ministry_id` → `ministries.id`
- **Business Rule**: Each proposal must belong to exactly one ministry

### 3. **categories ↔ proposals**
- **Type**: One-to-Many
- **Description**: One category can have many proposals
- **Foreign Key**: `proposals.category_id` → `categories.id`
- **Business Rule**: Each proposal must belong to exactly one category

---

## Entity Relationship Diagram (Text Format)

```
┌─────────────────┐
│    ministries   │
├─────────────────┤
│ id (PK)         │
│ name (UK)       │
│ description     │
│ created_at      │
│ is_active       │
└─────────────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ username (UK)   │
│ email (UK)      │
│ hashed_password │
│ role            │
│ ministry_id (FK)│
│ is_active       │
│ created_at      │
└─────────────────┘

┌─────────────────┐
│   categories    │
├─────────────────┤
│ id (PK)         │
│ name (UK)       │
│ allocated_budget│
│ remaining_budget│
│ created_at      │
└─────────────────┘
         │
         │ 1:N
         │
         ▼
┌─────────────────┐
│    proposals    │
├─────────────────┤
│ id (PK)         │
│ ministry_id (FK)│ ──────┐
│ category_id (FK)│       │
│ title           │       │
│ description     │       │
│ requested_amount│       │
│ status          │       │
│ approved_amount │       │
│ decision_notes  │       │
│ decided_at      │       │
│ created_at      │       │
└─────────────────┘       │
                          │
                          │ 1:N
                          │
                          ▼
                ┌─────────────────┐
                │    ministries   │
                └─────────────────┘
```

---

## Database Indexes

### Ministries Table
- `ix_ministries_name` - Unique index on name
- `ix_ministries_id` - Index on id (primary key)

### Categories Table
- `ix_categories_name` - Unique index on name
- `ix_categories_id` - Index on id (primary key)

### Users Table
- `ix_users_username` - Unique index on username
- `ix_users_id` - Index on id (primary key)
- `ix_users_email` - Unique index on email

### Proposals Table
- `ix_proposals_ministry_id` - Index on ministry_id (for filtering)
- `ix_proposals_id` - Index on id (primary key)

---

## Business Rules

1. **Ministry Management**:
   - Each ministry must have a unique name
   - Ministries can be activated/deactivated (soft delete)
   - Only finance users can create new ministries

2. **Category Management**:
   - Each category must have a unique name
   - Allocated budget must be >= 0
   - Remaining budget must be <= allocated budget

3. **User Management**:
   - Each user must have a unique username and email
   - Ministry users must have a valid ministry_id (foreign key)
   - Finance users don't need a ministry_id (can be NULL)

4. **Proposal Management**:
   - Each proposal must belong to an existing ministry (foreign key)
   - Each proposal must belong to an existing category (foreign key)
   - Status can only be "Pending", "Approved", or "Rejected"
   - Approved proposals must have an approved_amount
   - Rejected proposals can have decision_notes

5. **Workflow**:
   - Only ministry users can create proposals
   - Only finance users can approve/reject proposals
   - Ministry users can edit their own pending proposals (with restrictions)
   - Referential integrity ensures no orphaned proposals or users

---

## Sample Data

### Ministries
- Ministry of Education (ID: 1, active: true)

### Categories
- Education (allocated: $10,000,000)
- Healthcare (allocated: $15,000,000)
- Infrastructure (allocated: $20,000,000)

### Users
- finance/fin (Finance role, ministry_id: NULL)
- ministry/min (Ministry role, ministry_id: 1)

### Proposals
- Various pending/approved/rejected proposals across different categories
- All proposals must reference valid ministry_id and category_id
