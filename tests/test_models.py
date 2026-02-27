"""
tests/test_models.py
Unit tests for the Project Manager CLI tool.
Tests cover:
    - Person / User / Project / Task model validation
    - Relationships between models
    - Serialization (to_dict / from_dict)
    - Service layer logic (add, list, complete)
    - Edge cases and error handling

Run with:
    pytest tests/test_models.py -v
"""

import pytest
import sys
import os

# Make sure the root folder is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project_manager.models import User, Project, Task


# ─────────────────────────────────────────────
# FIXTURES — reusable test data
# ─────────────────────────────────────────────

@pytest.fixture
def sample_user():
    """Return a fresh User instance for testing."""
    return User(name="Alex", email="alex@email.com")


@pytest.fixture
def sample_project():
    """Return a fresh Project instance for testing."""
    return Project(title="CLI Tool", description="A test project", due_date="2025-12-31")


@pytest.fixture
def sample_task():
    """Return a fresh Task instance for testing."""
    return Task(title="Write tests", assigned_to="Alex", status="pending")


@pytest.fixture
def user_with_project_and_task():
    """Return a fully linked User → Project → Task for integration tests."""
    user = User(name="Jordan", email="jordan@email.com")
    project = Project(title="Full Stack App")
    task = Task(title="Setup database")
    project.add_task(task)
    user.add_project(project)
    return user, project, task


# ─────────────────────────────────────────────
# PERSON / USER TESTS
# ─────────────────────────────────────────────

class TestUser:
    """Tests for the User model (inherits from Person)."""

    def test_user_creation(self, sample_user):
        """User should be created with correct name and email."""
        assert sample_user.name == "Alex"
        assert sample_user.email == "alex@email.com"

    def test_user_has_id(self, sample_user):
        """User should have an auto-assigned integer ID."""
        assert isinstance(sample_user.id, int)
        assert sample_user.id >= 1

    def test_user_starts_with_no_projects(self, sample_user):
        """A new user should have an empty projects list."""
        assert sample_user.projects == []

    def test_user_name_setter_strips_whitespace(self):
        """Name setter should strip leading/trailing whitespace."""
        user = User(name="  Alex  ", email="alex@email.com")
        user.name = "  Jordan  "
        assert user.name == "Jordan"

    def test_user_name_cannot_be_empty(self, sample_user):
        """Setting an empty name should raise ValueError."""
        with pytest.raises(ValueError):
            sample_user.name = ""

    def test_user_name_cannot_be_whitespace(self, sample_user):
        """Setting a whitespace-only name should raise ValueError."""
        with pytest.raises(ValueError):
            sample_user.name = "   "

    def test_user_email_validation(self, sample_user):
        """Setting an invalid email should raise ValueError."""
        with pytest.raises(ValueError):
            sample_user.email = "not-an-email"

    def test_user_valid_email_update(self, sample_user):
        """Valid email update should work correctly."""
        sample_user.email = "newemail@test.com"
        assert sample_user.email == "newemail@test.com"

    def test_user_str(self, sample_user):
        """__str__ should return a readable string."""
        result = str(sample_user)
        assert "Alex" in result
        assert "alex@email.com" in result

    def test_user_repr(self, sample_user):
        """__repr__ should return a developer-friendly string."""
        result = repr(sample_user)
        assert "User" in result
        assert "Alex" in result


# ─────────────────────────────────────────────
# PROJECT TESTS
# ─────────────────────────────────────────────

class TestProject:
    """Tests for the Project model."""

    def test_project_creation(self, sample_project):
        """Project should be created with correct attributes."""
        assert sample_project.title == "CLI Tool"
        assert sample_project.description == "A test project"
        assert sample_project.due_date == "2025-12-31"

    def test_project_has_id(self, sample_project):
        """Project should have an auto-assigned integer ID."""
        assert isinstance(sample_project.id, int)
        assert sample_project.id >= 1

    def test_project_starts_with_no_tasks(self, sample_project):
        """A new project should have an empty tasks list."""
        assert sample_project.tasks == []

    def test_project_title_cannot_be_empty(self, sample_project):
        """Setting an empty title should raise ValueError."""
        with pytest.raises(ValueError):
            sample_project.title = ""

    def test_project_default_values(self):
        """Project created with only a title should have empty description and due_date."""
        project = Project(title="Minimal Project")
        assert project.description == ""
        assert project.due_date == ""

    def test_project_str(self, sample_project):
        """__str__ should contain the project title."""
        assert "CLI Tool" in str(sample_project)

    def test_project_repr(self, sample_project):
        """__repr__ should contain Project and title."""
        assert "Project" in repr(sample_project)
        assert "CLI Tool" in repr(sample_project)


# ─────────────────────────────────────────────
# TASK TESTS
# ─────────────────────────────────────────────

class TestTask:
    """Tests for the Task model."""

    def test_task_creation(self, sample_task):
        """Task should be created with correct attributes."""
        assert sample_task.title == "Write tests"
        assert sample_task.assigned_to == "Alex"
        assert sample_task.status == "pending"

    def test_task_has_id(self, sample_task):
        """Task should have an auto-assigned integer ID."""
        assert isinstance(sample_task.id, int)
        assert sample_task.id >= 1

    def test_task_default_status(self):
        """Task created without a status should default to 'pending'."""
        task = Task(title="Default task")
        assert task.status == "pending"

    def test_task_complete_method(self, sample_task):
        """Calling complete() should set status to 'complete'."""
        sample_task.complete()
        assert sample_task.status == "complete"

    def test_task_invalid_status(self, sample_task):
        """Setting an invalid status should raise ValueError."""
        with pytest.raises(ValueError):
            sample_task.status = "done"  # not in VALID_STATUSES

    def test_task_valid_status_update(self, sample_task):
        """Updating to a valid status should work."""
        sample_task.status = "in-progress"
        assert sample_task.status == "in-progress"

    def test_task_title_cannot_be_empty(self, sample_task):
        """Setting an empty title should raise ValueError."""
        with pytest.raises(ValueError):
            sample_task.title = ""

    def test_task_str(self, sample_task):
        """__str__ should contain title and status."""
        result = str(sample_task)
        assert "Write tests" in result
        assert "pending" in result


# ─────────────────────────────────────────────
# RELATIONSHIP TESTS
# ─────────────────────────────────────────────

class TestRelationships:
    """Tests for one-to-many relationships between models."""

    def test_user_add_project(self, sample_user, sample_project):
        """User should be able to add a project."""
        sample_user.add_project(sample_project)
        assert len(sample_user.projects) == 1
        assert sample_user.projects[0].title == "CLI Tool"

    def test_user_add_multiple_projects(self, sample_user):
        """User should support multiple projects."""
        sample_user.add_project(Project(title="Project A"))
        sample_user.add_project(Project(title="Project B"))
        assert len(sample_user.projects) == 2

    def test_user_add_project_type_error(self, sample_user):
        """Adding a non-Project to user should raise TypeError."""
        with pytest.raises(TypeError):
            sample_user.add_project("not a project")

    def test_project_add_task(self, sample_project, sample_task):
        """Project should be able to add a task."""
        sample_project.add_task(sample_task)
        assert len(sample_project.tasks) == 1
        assert sample_project.tasks[0].title == "Write tests"

    def test_project_add_multiple_tasks(self, sample_project):
        """Project should support multiple tasks."""
        sample_project.add_task(Task(title="Task A"))
        sample_project.add_task(Task(title="Task B"))
        sample_project.add_task(Task(title="Task C"))
        assert len(sample_project.tasks) == 3

    def test_project_add_task_type_error(self, sample_project):
        """Adding a non-Task to project should raise TypeError."""
        with pytest.raises(TypeError):
            sample_project.add_task(42)

    def test_full_chain(self, user_with_project_and_task):
        """Full chain User → Project → Task should be accessible."""
        user, project, task = user_with_project_and_task
        assert user.projects[0].title == "Full Stack App"
        assert user.projects[0].tasks[0].title == "Setup database"


# ─────────────────────────────────────────────
# SERIALIZATION TESTS
# ─────────────────────────────────────────────

class TestSerialization:
    """Tests for to_dict() and from_dict() methods."""

    def test_task_to_dict(self, sample_task):
        """Task.to_dict() should return correct keys and values."""
        d = sample_task.to_dict()
        assert d["title"] == "Write tests"
        assert d["assigned_to"] == "Alex"
        assert d["status"] == "pending"
        assert "id" in d

    def test_task_from_dict(self):
        """Task.from_dict() should reconstruct a Task correctly."""
        data = {"id": 99, "title": "Restored Task", "assigned_to": "Sam", "status": "in-progress"}
        task = Task.from_dict(data)
        assert task.title == "Restored Task"
        assert task.assigned_to == "Sam"
        assert task.status == "in-progress"
        assert task.id == 99

    def test_project_to_dict(self, sample_project, sample_task):
        """Project.to_dict() should include nested tasks."""
        sample_project.add_task(sample_task)
        d = sample_project.to_dict()
        assert d["title"] == "CLI Tool"
        assert len(d["tasks"]) == 1
        assert d["tasks"][0]["title"] == "Write tests"

    def test_project_from_dict(self):
        """Project.from_dict() should reconstruct project and nested tasks."""
        data = {
            "id": 99,
            "title": "Restored Project",
            "description": "From file",
            "due_date": "2025-01-01",
            "tasks": [
                {"id": 1, "title": "Task One", "assigned_to": "", "status": "pending"}
            ]
        }
        project = Project.from_dict(data)
        assert project.title == "Restored Project"
        assert len(project.tasks) == 1
        assert project.tasks[0].title == "Task One"

    def test_user_to_dict(self, sample_user, sample_project):
        """User.to_dict() should include nested projects."""
        sample_user.add_project(sample_project)
        d = sample_user.to_dict()
        assert d["name"] == "Alex"
        assert d["email"] == "alex@email.com"
        assert len(d["projects"]) == 1

    def test_user_from_dict(self):
        """User.from_dict() should reconstruct user with nested projects and tasks."""
        data = {
            "id": 99,
            "name": "Restored User",
            "email": "restore@email.com",
            "projects": [
                {
                    "id": 1,
                    "title": "Restored Project",
                    "description": "",
                    "due_date": "",
                    "tasks": []
                }
            ]
        }
        user = User.from_dict(data)
        assert user.name == "Restored User"
        assert len(user.projects) == 1
        assert user.projects[0].title == "Restored Project"

    def test_round_trip(self, sample_user, sample_project, sample_task):
        """Full round trip: object → dict → object should preserve data."""
        sample_project.add_task(sample_task)
        sample_user.add_project(sample_project)

        # Serialize
        d = sample_user.to_dict()

        # Deserialize
        restored = User.from_dict(d)

        assert restored.name == sample_user.name
        assert restored.projects[0].title == sample_project.title
        assert restored.projects[0].tasks[0].title == sample_task.title


# ─────────────────────────────────────────────
# SERVICES TESTS
# ─────────────────────────────────────────────

class TestServices:
    """
    Tests for the services layer.
    Uses monkeypatching to avoid reading/writing real JSON files.
    """

    def test_add_user_success(self, monkeypatch):
        """add_user should return success when user doesn't exist."""
        from project_manager import services

        monkeypatch.setattr(services.storage, "load_users", lambda: [])
        monkeypatch.setattr(services.storage, "save_users", lambda users: None)

        result = services.add_user("TestUser", "test@email.com")
        assert result["success"] is True
        assert "TestUser" in result["message"]

    def test_add_user_duplicate(self, monkeypatch):
        """add_user should fail if user already exists."""
        from project_manager import services

        existing = User(name="TestUser", email="test@email.com")
        monkeypatch.setattr(services.storage, "load_users", lambda: [existing])
        monkeypatch.setattr(services.storage, "save_users", lambda users: None)

        result = services.add_user("TestUser", "other@email.com")
        assert result["success"] is False
        assert "already exists" in result["message"]

    def test_add_project_success(self, monkeypatch):
        """add_project should succeed when user exists and project is new."""
        from project_manager import services

        user = User(name="Alex", email="alex@email.com")
        monkeypatch.setattr(services.storage, "load_users", lambda: [user])
        monkeypatch.setattr(services.storage, "save_users", lambda users: None)

        result = services.add_project("Alex", "New Project")
        assert result["success"] is True

    def test_add_project_user_not_found(self, monkeypatch):
        """add_project should fail if user doesn't exist."""
        from project_manager import services

        monkeypatch.setattr(services.storage, "load_users", lambda: [])
        monkeypatch.setattr(services.storage, "save_users", lambda users: None)

        result = services.add_project("Ghost", "Some Project")
        assert result["success"] is False
        assert "not found" in result["message"]

    def test_add_task_success(self, monkeypatch):
        """add_task should succeed when user and project exist."""
        from project_manager import services

        user = User(name="Alex", email="alex@email.com")
        project = Project(title="My Project")
        user.add_project(project)

        monkeypatch.setattr(services.storage, "load_users", lambda: [user])
        monkeypatch.setattr(services.storage, "save_users", lambda users: None)

        result = services.add_task("Alex", "My Project", "Do something")
        assert result["success"] is True

    def test_complete_task_success(self, monkeypatch):
        """complete_task should mark the task as complete."""
        from project_manager import services

        user = User(name="Alex", email="alex@email.com")
        project = Project(title="My Project")
        task = Task(title="Fix bug")
        project.add_task(task)
        user.add_project(project)

        monkeypatch.setattr(services.storage, "load_users", lambda: [user])
        monkeypatch.setattr(services.storage, "save_users", lambda users: None)

        result = services.complete_task("Alex", "My Project", "Fix bug")
        assert result["success"] is True
        assert task.status == "complete"

    def test_complete_task_already_complete(self, monkeypatch):
        """complete_task should fail if task is already complete."""
        from project_manager import services

        user = User(name="Alex", email="alex@email.com")
        project = Project(title="My Project")
        task = Task(title="Fix bug", status="complete")
        project.add_task(task)
        user.add_project(project)

        monkeypatch.setattr(services.storage, "load_users", lambda: [user])
        monkeypatch.setattr(services.storage, "save_users", lambda users: None)

        result = services.complete_task("Alex", "My Project", "Fix bug")
        assert result["success"] is False
        assert "already complete" in result["message"]