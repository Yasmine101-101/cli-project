
"""
models.py
Defines the core data models: Person, User, Project, and Task.
Relationships:
    - User inherits from Person
    - User has many Projects (one-to-many)
    - Project has many Tasks (one-to-many)
"""


# ─────────────────────────────────────────────
# BASE CLASS
# ─────────────────────────────────────────────

class Person:
    """
    Base class representing a generic person.
    Provides shared attributes: name and email.
    User inherits from this class.
    """

    def __init__(self, name: str, email: str):
        """Initialize a Person with a name and email."""
        self._name = name
        self._email = email

    # --- Properties ---

    @property
    def name(self):
        """Get the person's name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set name with validation — cannot be empty."""
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value.strip()

    @property
    def email(self):
        """Get the person's email."""
        return self._email

    @email.setter
    def email(self, value: str):
        """Set email with basic validation."""
        if "@" not in value:
            raise ValueError("Invalid email address. Must contain '@'.")
        self._email = value.strip()

    def __str__(self):
        return f"{self._name} <{self._email}>"

    def __repr__(self):
        return f"Person(name={self._name!r}, email={self._email!r})"


# ─────────────────────────────────────────────
# USER CLASS
# ─────────────────────────────────────────────

class User(Person):
    """
    Represents a system user. Inherits from Person.
    Each user can own multiple projects.

    Class Attribute:
        _id_counter (int): Auto-increments to assign unique IDs.
    """

    _id_counter = 1  # class-level ID counter (shared across all instances)

    def __init__(self, name: str, email: str, user_id: int = None):
        """
        Initialize a User.

        Args:
            name (str): User's full name.
            email (str): User's email address.
            user_id (int, optional): Manually set ID (used when loading from file).
        """
        super().__init__(name, email)  # call Person's __init__

        # Assign ID — use provided one (from file) or auto-generate
        if user_id is not None:
            self._id = user_id
        else:
            self._id = User._id_counter
            User._id_counter += 1

        self._projects = []  # list of Project objects belonging to this user

    # --- Properties ---

    @property
    def id(self):
        """Get user ID."""
        return self._id

    @property
    def projects(self):
        """Get the list of projects for this user."""
        return self._projects

    # --- Instance Methods ---

    def add_project(self, project):
        """
        Add a Project to this user's project list.

        Args:
            project (Project): The project to add.
        """
        if not isinstance(project, Project):
            raise TypeError("Only Project instances can be added.")
        self._projects.append(project)

    def to_dict(self):
        """
        Serialize User to a dictionary for JSON storage.

        Returns:
            dict: User data as a plain dictionary.
        """
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "projects": [p.to_dict() for p in self._projects]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Deserialize a User from a dictionary (loaded from JSON).

        Args:
            data (dict): Dictionary with user data.

        Returns:
            User: Reconstructed User instance.
        """
        user = cls(
            name=data["name"],
            email=data["email"],
            user_id=data["id"]
        )
        # Rebuild nested projects
        for p_data in data.get("projects", []):
            user.add_project(Project.from_dict(p_data))

        # Keep ID counter ahead of loaded IDs to avoid conflicts
        if data["id"] >= User._id_counter:
            User._id_counter = data["id"] + 1

        return user

    def __str__(self):
        return f"[User #{self._id}] {self._name} <{self._email}> | Projects: {len(self._projects)}"

    def __repr__(self):
        return f"User(id={self._id}, name={self._name!r}, email={self._email!r})"


# ─────────────────────────────────────────────
# PROJECT CLASS
# ─────────────────────────────────────────────

class Project:
    """
    Represents a project owned by a User.
    Each project can have multiple tasks.

    Class Attribute:
        _id_counter (int): Auto-increments to assign unique IDs.
    """

    _id_counter = 1

    def __init__(self, title: str, description: str = "", due_date: str = "", project_id: int = None):
        """
        Initialize a Project.

        Args:
            title (str): Project title.
            description (str): Optional project description.
            due_date (str): Optional due date as a string (e.g. "2025-12-31").
            project_id (int, optional): Manually set ID (used when loading from file).
        """
        self._title = title
        self._description = description
        self._due_date = due_date
        self._tasks = []  # list of Task objects

        if project_id is not None:
            self._id = project_id
        else:
            self._id = Project._id_counter
            Project._id_counter += 1

    # --- Properties ---

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        """Set title with validation."""
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        self._due_date = value

    @property
    def tasks(self):
        return self._tasks

    # --- Instance Methods ---

    def add_task(self, task):
        """
        Add a Task to this project.

        Args:
            task (Task): The task to add.
        """
        if not isinstance(task, Task):
            raise TypeError("Only Task instances can be added.")
        self._tasks.append(task)

    def to_dict(self):
        """Serialize Project to a dictionary for JSON storage."""
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "tasks": [t.to_dict() for t in self._tasks]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Deserialize a Project from a dictionary."""
        project = cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            project_id=data["id"]
        )
        for t_data in data.get("tasks", []):
            project.add_task(Task.from_dict(t_data))

        if data["id"] >= Project._id_counter:
            Project._id_counter = data["id"] + 1

        return project

    def __str__(self):
        status = f"{len(self._tasks)} task(s)"
        due = f" | Due: {self._due_date}" if self._due_date else ""
        return f"[Project #{self._id}] {self._title}{due} | {status}"

    def __repr__(self):
        return f"Project(id={self._id}, title={self._title!r})"


# ─────────────────────────────────────────────
# TASK CLASS
# ─────────────────────────────────────────────

class Task:
    """
    Represents a task within a project.

    Class Attribute:
        _id_counter (int): Auto-increments to assign unique IDs.
    """

    _id_counter = 1
    VALID_STATUSES = ["pending", "in-progress", "complete"]

    def __init__(self, title: str, assigned_to: str = "", status: str = "pending", task_id: int = None):
        """
        Initialize a Task.

        Args:
            title (str): Task title.
            assigned_to (str): Name of the person assigned to this task.
            status (str): Task status — 'pending', 'in-progress', or 'complete'.
            task_id (int, optional): Manually set ID (used when loading from file).
        """
        self._title = title
        self._assigned_to = assigned_to
        self._status = status

        if task_id is not None:
            self._id = task_id
        else:
            self._id = Task._id_counter
            Task._id_counter += 1

    # --- Properties ---

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: str):
        self._assigned_to = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        """Validate status before setting."""
        if value not in Task.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {Task.VALID_STATUSES}")
        self._status = value

    def complete(self):
        """Mark this task as complete."""
        self._status = "complete"

    def to_dict(self):
        """Serialize Task to a dictionary for JSON storage."""
        return {
            "id": self._id,
            "title": self._title,
            "assigned_to": self._assigned_to,
            "status": self._status
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Deserialize a Task from a dictionary."""
        task = cls(
            title=data["title"],
            assigned_to=data.get("assigned_to", ""),
            status=data.get("status", "pending"),
            task_id=data["id"]
        )
        if data["id"] >= Task._id_counter:
            Task._id_counter = data["id"] + 1
        return task

    def __str__(self):
        assignee = f" | Assigned to: {self._assigned_to}" if self._assigned_to else ""
        return f"[Task #{self._id}] {self._title} | Status: {self._status}{assignee}"

    def __repr__(self):
        return f"Task(id={self._id}, title={self._title!r}, status={self._status!r})"