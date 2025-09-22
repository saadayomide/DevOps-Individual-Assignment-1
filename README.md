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

## 🎉 Phase 1 Complete - Full Stack Application

### Frontend Setup (COMPLETED)
- **React Application** - Modern React app with professional UI
- **Category Management Interface** - Complete CRUD operations
- **API Integration** - Seamless connection to FastAPI backend
- **Responsive Design** - Works on desktop and mobile

### Full Stack Features (WORKING)
- **Create Categories** - Add new budget categories with name and amount
- **View Categories** - Table display with all category information
- **Edit Categories** - Update existing category details
- **Delete Categories** - Remove categories with confirmation
- **Real-time Updates** - Changes reflect immediately in the UI
- **Error Handling** - User-friendly error messages
- **Professional Styling** - Clean, modern interface

### How to Run the Full Application

1. **Start Backend Server**
   ```bash
   cd backend
   python3 main.py
   ```
   Backend runs on: http://localhost:8000

2. **Start Frontend Server** (in a new terminal)
   ```bash
   cd frontend
   npm start
   ```
   Frontend runs on: http://localhost:3000

3. **Access the Application**
   - Open http://localhost:3000 in your browser
   - You'll see the Government Spending Tracker interface
   - Create, edit, and manage budget categories

### What You Can Do Now
- Add budget categories (Education, Health, Defense, etc.)
- Set allocated budgets for each category
- View all categories in a professional table
- Edit category names and budget amounts
- Delete categories you no longer need
- See real-time updates from the database

### Technical Implementation
- **Frontend**: React with modern hooks (useState, useEffect)
- **API Communication**: Axios for HTTP requests
- **Styling**: Custom CSS with responsive design
- **State Management**: Local component state
- **Error Handling**: Try-catch blocks with user feedback
- **Data Validation**: Form validation and API error handling

## 🚀 Ready for Phase 2

The foundation is complete! We now have a fully functional budget category management system. The next phase will add proposal submission functionality for ministries.

## Phase 2: Proposal Submission (COMPLETED)

### Backend
- Endpoints
  - `GET /proposals?ministry=&category_id=&status=`
  - `POST /proposals`
  - `GET /proposals/{id}`
  - `PUT /proposals/{id}` (Pending only)
  - `DELETE /proposals/{id}` (Pending only)
- Validation: `requested_amount > 0`, `category_id` must exist. No budget deduction yet (Phase 3).

### Frontend
- Proposal form with client-side validation
- Proposals list with filters
- Live category dropdown updates when categories change

### How to use
1. Create categories in the table above
2. Use the Proposal form to submit a proposal
3. View submitted proposals in the list (status: Pending)
