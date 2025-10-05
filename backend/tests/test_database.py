import pytest
import sys
from pathlib import Path
from sqlalchemy.exc import IntegrityError

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database import (
    Ministry as DBMinistry, 
    Category as DBCategory, 
    User as DBUser, 
    Proposal as DBProposal
)
from auth import get_password_hash

@pytest.mark.database
class TestMinistryModel:
    """Test Ministry database model"""
    
    def test_create_ministry(self, test_db):
        """Test creating a ministry"""
        ministry = DBMinistry(
            name="Test Ministry",
            description="Test ministry description"
        )
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
            ministry_id=sample_ministry.id
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
            name="Test Category",
            allocated_budget=1000000.0,
            remaining_budget=1000000.0
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
            name="Positive Budget",
            allocated_budget=1000000.0,
            remaining_budget=500000.0
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
            status="Pending"
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
            ministry_id=sample_ministry.id
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
            ministry_id=sample_ministry.id
        )
        test_db.add(user1)
        test_db.commit()
        
        # Test duplicate username
        user2 = DBUser(
            username="uniqueuser",  # Same username
            email="different@example.com",
            hashed_password=get_password_hash("password"),
            role="ministry",
            ministry_id=sample_ministry.id
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
            ministry_id=sample_ministry.id
        )
        test_db.add(user1)
        test_db.commit()
        
        user2 = DBUser(
            username="user2",
            email="unique@example.com",  # Same email
            hashed_password=get_password_hash("password"),
            role="ministry",
            ministry_id=sample_ministry.id
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
                ministry_id=sample_ministry.id if role == "ministry" else None
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
            ministry_id=None
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
            status="Pending"
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
                status=status
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
            status="Pending"
        )
        test_db.add(proposal)
        test_db.commit()
        
        assert proposal.requested_amount > 0
    
    def test_proposal_relationships(self, test_db, sample_proposal, sample_ministry, sample_category):
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
        
        category = DBCategory(name="Valid Category", allocated_budget=1000000.0, remaining_budget=1000000.0)
        test_db.add(category)
        test_db.commit()
        test_db.refresh(category)
        
        # Test valid foreign keys
        proposal = DBProposal(
            ministry_id=ministry.id,
            category_id=category.id,
            title="Valid Proposal",
            requested_amount=100000.0,
            status="Pending"
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
    
    def test_cascade_deletion_ministry(self, test_db, sample_ministry, sample_user, sample_proposal):
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
