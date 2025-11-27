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
