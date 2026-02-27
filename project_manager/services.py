"""
services.py
Business logic layer for the project manager.
All operations (add, list, update) go through here.
The CLI calls these functions — services call storage for persistence.

Flow:
    CLI (cli.py) → Services (services.py) → Storage (storage.py) → data/users.json
"""

from project_manager.models import User, Project, Task
from project_manager import storage




def _get_all_users() -> list:
    """Load and return all users from storage."""
    return storage.load_users()


def _save_all_users(users: list):
    """Persist all users to storage."""
    storage.save_users(users)


def _find_user(users: list, name: str):
    """
    Find a user by name (case-insensitive).

    Args:
        users (list): List of User instances.
        name (str): Name to search for.

    Returns:
        User or None: Matched user, or None if not found.
    """
    for user in users:
        if user.name.lower() == name.lower():
            return user
    return None


def _find_project(user: User, title: str):
    """
    Find a project by title within a user's projects (case-insensitive).

    Args:
        user (User): The user to search within.
        title (str): Project title to look for.

    Returns:
        Project or None: Matched project, or None if not found.
    """
    for project in user.projects:
        if project.title.lower() == title.lower():
            return project
    return None


def _find_task(project: Project, title: str):
    """
    Find a task by title within a project (case-insensitive).

    Args:
        project (Project): The project to search within.
        title (str): Task title to look for.

    Returns:
        Task or None: Matched task, or None if not found.
    """
    for task in project.tasks:
        if task.title.lower() == title.lower():
            return task
    return None


# ─────────────────────────────────────────────
# USER SERVICES
# ─────────────────────────────────────────────

def add_user(name: str, email: str) -> dict:
    """
    Create and persist a new user.

    Args:
        name (str): User's name.
        email (str): User's email.

    Returns:
        dict: Result with 'success' (bool) and 'message' (str).
    """
    users = _get_all_users()

    # Check for duplicate name
    if _find_user(users, name):
        return {"success": False, "message": f"User '{name}' already exists."}

    try:
        new_user = User(name=name, email=email)
        users.append(new_user)
        _save_all_users(users)
        return {"success": True, "message": f"User '{name}' created successfully."}
    except ValueError as e:
        return {"success": False, "message": str(e)}


def list_users() -> dict:
    """
    Retrieve all users.

    Returns:
        dict: Result with 'success' (bool), 'message' (str), and 'data' (list of User).
    """
    users = _get_all_users()

    if not users:
        return {"success": False, "message": "No users found.", "data": []}

    return {"success": True, "message": f"{len(users)} user(s) found.", "data": users}


# ─────────────────────────────────────────────
# PROJECT SERVICES
# ─────────────────────────────────────────────

def add_project(username: str, title: str, description: str = "", due_date: str = "") -> dict:
    """
    Add a project to an existing user.

    Args:
        username (str): Name of the user to assign the project to.
        title (str): Project title.
        description (str): Optional project description.
        due_date (str): Optional due date string.

    Returns:
        dict: Result with 'success' and 'message'.
    """
    users = _get_all_users()
    user = _find_user(users, username)

    if not user:
        return {"success": False, "message": f"User '{username}' not found."}

    # Check for duplicate project title under this user
    if _find_project(user, title):
        return {"success": False, "message": f"Project '{title}' already exists for '{username}'."}

    try:
        new_project = Project(title=title, description=description, due_date=due_date)
        user.add_project(new_project)
        _save_all_users(users)
        return {"success": True, "message": f"Project '{title}' added to user '{username}'."}
    except ValueError as e:
        return {"success": False, "message": str(e)}


def list_projects(username: str) -> dict:
    """
    List all projects for a given user.

    Args:
        username (str): Name of the user.

    Returns:
        dict: Result with 'success', 'message', and 'data' (list of Project).
    """
    users = _get_all_users()
    user = _find_user(users, username)

    if not user:
        return {"success": False, "message": f"User '{username}' not found.", "data": []}

    if not user.projects:
        return {"success": False, "message": f"No projects found for '{username}'.", "data": []}

    return {"success": True, "message": f"{len(user.projects)} project(s) found.", "data": user.projects}


# ─────────────────────────────────────────────
# TASK SERVICES
# ─────────────────────────────────────────────

def add_task(username: str, project_title: str, title: str, assigned_to: str = "") -> dict:
    """
    Add a task to a project belonging to a user.

    Args:
        username (str): Name of the user who owns the project.
        project_title (str): Title of the project.
        title (str): Task title.
        assigned_to (str): Optional name of person assigned to the task.

    Returns:
        dict: Result with 'success' and 'message'.
    """
    users = _get_all_users()
    user = _find_user(users, username)

    if not user:
        return {"success": False, "message": f"User '{username}' not found."}

    project = _find_project(user, project_title)

    if not project:
        return {"success": False, "message": f"Project '{project_title}' not found for '{username}'."}

    # Check for duplicate task title within the project
    if _find_task(project, title):
        return {"success": False, "message": f"Task '{title}' already exists in '{project_title}'."}

    try:
        new_task = Task(title=title, assigned_to=assigned_to)
        project.add_task(new_task)
        _save_all_users(users)
        return {"success": True, "message": f"Task '{title}' added to project '{project_title}'."}
    except ValueError as e:
        return {"success": False, "message": str(e)}


def list_tasks(username: str, project_title: str) -> dict:
    """
    List all tasks for a given project.

    Args:
        username (str): Name of the user who owns the project.
        project_title (str): Title of the project.

    Returns:
        dict: Result with 'success', 'message', and 'data' (list of Task).
    """
    users = _get_all_users()
    user = _find_user(users, username)

    if not user:
        return {"success": False, "message": f"User '{username}' not found.", "data": []}

    project = _find_project(user, project_title)

    if not project:
        return {"success": False, "message": f"Project '{project_title}' not found.", "data": []}

    if not project.tasks:
        return {"success": False, "message": f"No tasks found in '{project_title}'.", "data": []}

    return {"success": True, "message": f"{len(project.tasks)} task(s) found.", "data": project.tasks}


def complete_task(username: str, project_title: str, task_title: str) -> dict:
    """
    Mark a task as complete.

    Args:
        username (str): Name of the user who owns the project.
        project_title (str): Title of the project.
        task_title (str): Title of the task to mark complete.

    Returns:
        dict: Result with 'success' and 'message'.
    """
    users = _get_all_users()
    user = _find_user(users, username)

    if not user:
        return {"success": False, "message": f"User '{username}' not found."}

    project = _find_project(user, project_title)

    if not project:
        return {"success": False, "message": f"Project '{project_title}' not found."}

    task = _find_task(project, task_title)

    if not task:
        return {"success": False, "message": f"Task '{task_title}' not found in '{project_title}'."}

    if task.status == "complete":
        return {"success": False, "message": f"Task '{task_title}' is already complete."}

    task.complete()
    _save_all_users(users)
    return {"success": True, "message": f"Task '{task_title}' marked as complete."}