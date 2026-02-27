"""
cli.py
Command-Line Interface for the Project Manager.
Uses argparse for command structure and rich for styled terminal output.

Available commands:
    add-user        --name --email
    list-users
    add-project     --user --title --desc --due
    list-projects   --user
    add-task        --user --project --title --assign
    list-tasks      --user --project
    complete-task   --user --project --task
"""

import argparse
from rich.console import Console
from rich.table import Table
from rich import box

from project_manager import services

# ─────────────────────────────────────────────
# RICH CONSOLE SETUP
# ─────────────────────────────────────────────

console = Console()  # global rich console used for all output


# ─────────────────────────────────────────────
# OUTPUT HELPERS
# ─────────────────────────────────────────────

def print_success(message: str):
    """Print a green success message."""
    console.print(f"[bold green]✔ {message}[/bold green]")


def print_error(message: str):
    """Print a red error message."""
    console.print(f"[bold red]✘ {message}[/bold red]")


def print_info(message: str):
    """Print a cyan info message."""
    console.print(f"[cyan]{message}[/cyan]")


# ─────────────────────────────────────────────
# COMMAND HANDLERS
# ─────────────────────────────────────────────

def handle_add_user(args):
    """
    Handle the add-user command.
    Creates a new user with the given name and email.
    """
    result = services.add_user(name=args.name, email=args.email)
    if result["success"]:
        print_success(result["message"])
    else:
        print_error(result["message"])


def handle_list_users(args):
    """
    Handle the list-users command.
    Displays all users in a rich table.
    """
    result = services.list_users()

    if not result["success"]:
        print_error(result["message"])
        return

    # Build a rich table
    table = Table(title="👥 All Users", box=box.ROUNDED, highlight=True)
    table.add_column("ID",      style="dim",          width=6)
    table.add_column("Name",    style="bold white",   min_width=15)
    table.add_column("Email",   style="cyan",         min_width=20)
    table.add_column("Projects",style="magenta",      width=10)

    for user in result["data"]:
        table.add_row(
            str(user.id),
            user.name,
            user.email,
            str(len(user.projects))
        )

    console.print(table)


def handle_add_project(args):
    """
    Handle the add-project command.
    Adds a new project to the specified user.
    """
    result = services.add_project(
        username=args.user,
        title=args.title,
        description=args.desc or "",
        due_date=args.due or ""
    )
    if result["success"]:
        print_success(result["message"])
    else:
        print_error(result["message"])


def handle_list_projects(args):
    """
    Handle the list-projects command.
    Displays all projects for a given user in a rich table.
    """
    result = services.list_projects(username=args.user)

    if not result["success"]:
        print_error(result["message"])
        return

    table = Table(title=f"📁 Projects for '{args.user}'", box=box.ROUNDED, highlight=True)
    table.add_column("ID",          style="dim",        width=6)
    table.add_column("Title",       style="bold white", min_width=20)
    table.add_column("Description", style="white",      min_width=25)
    table.add_column("Due Date",    style="yellow",     width=12)
    table.add_column("Tasks",       style="magenta",    width=8)

    for project in result["data"]:
        table.add_row(
            str(project.id),
            project.title,
            project.description or "—",
            project.due_date or "—",
            str(len(project.tasks))
        )

    console.print(table)


def handle_add_task(args):
    """
    Handle the add-task command.
    Adds a task to a project belonging to the specified user.
    """
    result = services.add_task(
        username=args.user,
        project_title=args.project,
        title=args.title,
        assigned_to=args.assign or ""
    )
    if result["success"]:
        print_success(result["message"])
    else:
        print_error(result["message"])


def handle_list_tasks(args):
    """
    Handle the list-tasks command.
    Displays all tasks for a given project in a rich table.
    """
    result = services.list_tasks(username=args.user, project_title=args.project)

    if not result["success"]:
        print_error(result["message"])
        return

    # Color-code status
    status_colors = {
        "pending":     "yellow",
        "in-progress": "cyan",
        "complete":    "green"
    }

    table = Table(title=f"✅ Tasks in '{args.project}'", box=box.ROUNDED, highlight=True)
    table.add_column("ID",          style="dim",        width=6)
    table.add_column("Title",       style="bold white", min_width=25)
    table.add_column("Assigned To", style="cyan",       min_width=15)
    table.add_column("Status",      min_width=12)

    for task in result["data"]:
        color = status_colors.get(task.status, "white")
        table.add_row(
            str(task.id),
            task.title,
            task.assigned_to or "—",
            f"[{color}]{task.status}[/{color}]"
        )

    console.print(table)


def handle_complete_task(args):
    """
    Handle the complete-task command.
    Marks the specified task as complete.
    """
    result = services.complete_task(
        username=args.user,
        project_title=args.project,
        task_title=args.task
    )
    if result["success"]:
        print_success(result["message"])
    else:
        print_error(result["message"])


# ─────────────────────────────────────────────
# CLI SETUP
# ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the argparse CLI parser with all subcommands.

    Returns:
        argparse.ArgumentParser: Fully configured parser.
    """
    parser = argparse.ArgumentParser(
        prog="project-manager",
        description="🛠  A CLI tool for managing users, projects, and tasks.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.required = True  # show help if no command is given

    # ── add-user ──────────────────────────────
    p_add_user = subparsers.add_parser("add-user", help="Create a new user")
    p_add_user.add_argument("--name",  required=True, help="User's full name")
    p_add_user.add_argument("--email", required=True, help="User's email address")
    p_add_user.set_defaults(func=handle_add_user)

    # ── list-users ────────────────────────────
    p_list_users = subparsers.add_parser("list-users", help="List all users")
    p_list_users.set_defaults(func=handle_list_users)

    # ── add-project ───────────────────────────
    p_add_proj = subparsers.add_parser("add-project", help="Add a project to a user")
    p_add_proj.add_argument("--user",  required=True, help="Name of the user")
    p_add_proj.add_argument("--title", required=True, help="Project title")
    p_add_proj.add_argument("--desc",  required=False, help="Project description")
    p_add_proj.add_argument("--due",   required=False, help="Due date (e.g. 2025-12-31)")
    p_add_proj.set_defaults(func=handle_add_project)

    # ── list-projects ─────────────────────────
    p_list_proj = subparsers.add_parser("list-projects", help="List all projects for a user")
    p_list_proj.add_argument("--user", required=True, help="Name of the user")
    p_list_proj.set_defaults(func=handle_list_projects)

    # ── add-task ──────────────────────────────
    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--user",    required=True, help="Name of the user who owns the project")
    p_add_task.add_argument("--project", required=True, help="Project title")
    p_add_task.add_argument("--title",   required=True, help="Task title")
    p_add_task.add_argument("--assign",  required=False, help="Name of person assigned to the task")
    p_add_task.set_defaults(func=handle_add_task)

    # ── list-tasks ────────────────────────────
    p_list_tasks = subparsers.add_parser("list-tasks", help="List all tasks in a project")
    p_list_tasks.add_argument("--user",    required=True, help="Name of the user")
    p_list_tasks.add_argument("--project", required=True, help="Project title")
    p_list_tasks.set_defaults(func=handle_list_tasks)

    # ── complete-task ─────────────────────────
    p_complete = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p_complete.add_argument("--user",    required=True, help="Name of the user")
    p_complete.add_argument("--project", required=True, help="Project title")
    p_complete.add_argument("--task",    required=True, help="Task title to mark complete")
    p_complete.set_defaults(func=handle_complete_task)

    return parser


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

def main():
    """
    Main entry point for the CLI.
    Parses arguments and dispatches to the correct handler function.
    """
    parser = build_parser()

    try:
        args = parser.parse_args()
        args.func(args)  # call the handler function set by set_defaults(func=...)
    except KeyboardInterrupt:
        print_info("\nOperation cancelled by user.")
    except Exception as e:
        print_error(f"Unexpected error: {e}")