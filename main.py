"""
main.py
Entry point for the Project Manager CLI tool.
Run this file to start the application.

Usage:
    python main.py <command> [options]

Examples:
    python main.py add-user --name "Alex" --email "alex@email.com"
    python main.py list-users
    python main.py add-project --user "Alex" --title "CLI Tool" --desc "A cool project" --due "2025-12-31"
    python main.py list-projects --user "Alex"
    python main.py add-task --user "Alex" --project "CLI Tool" --title "Implement storage" --assign "Alex"
    python main.py list-tasks --user "Alex" --project "CLI Tool"
    python main.py complete-task --user "Alex" --project "CLI Tool" --task "Implement storage"
"""

import sys
import os

# ─────────────────────────────────────────────
# PATH SETUP
# ─────────────────────────────────────────────

# Make sure the root project folder is on the Python path
# so that `from project_manager import ...` works correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────────────────────────
# IMPORT & RUN
# ─────────────────────────────────────────────

from project_manager.cli import main

if __name__ == "__main__":
    main()