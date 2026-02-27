"""
storage.py
Handles all file I/O operations for the project manager.
Reads and writes data to JSON files in the data/ directory.

Files:
    - data/users.json    → stores all user data (including nested projects and tasks)
"""

import json
import os

# ─────────────────────────────────────────────
# FILE PATH CONFIGURATION
# ─────────────────────────────────────────────

# Build the path to the data/ folder relative to this file's location

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")


def _ensure_data_dir():
    """
    Ensure the data/ directory exists.
    Creates it if it doesn't already exist.
    """
    os.makedirs(DATA_DIR, exist_ok=True)


# ─────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────

def save_users(users: list):
    """
    Serialize and save a list of User objects to users.json.

    Args:
        users (list): List of User instances to persist.
    """
    _ensure_data_dir()

    try:
        data = [user.to_dict() for user in users]  # serialize each user

        with open(USERS_FILE, "w") as f:
            json.dump(data, f, indent=4)  # write pretty-printed JSON

    except IOError as e:
        print(f"[ERROR] Could not save data: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error while saving: {e}")


# ─────────────────────────────────────────────
# LOAD
# ─────────────────────────────────────────────

def load_users() -> list:
    """
    Load and deserialize all users from users.json.

    Returns:
        list: List of User instances. Returns empty list if file
              doesn't exist or is malformed.
    """
    
    from project_manager.models import User

    _ensure_data_dir()

    # If the file doesn't exist yet, return an empty list
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)  

        return [User.from_dict(u) for u in data]  # rebuild User objects

    except json.JSONDecodeError:
        print("[ERROR] users.json is corrupted or malformed. Starting fresh.")
        return []
    except KeyError as e:
        print(f"[ERROR] Missing expected field in users.json: {e}")
        return []
    except Exception as e:
        print(f"[ERROR] Unexpected error while loading: {e}")
        return []