# 🛠 Project Manager CLI Tool

A command-line tool for managing users, projects, and tasks. Built with Python using OOP principles, JSON file persistence, and a rich terminal interface.

---

## 📁 Project Structure

```
CLI-PROJECT/
├── main.py                  # Entry point
├── requirements.txt         # External dependencies
├── README.md                # Project documentation
├── data/
│   └── users.json           # Persistent data storage
├── tests/
│   └── test_models.py       # Unit tests
└── project_manager/
    ├── __init__.py          # Package initializer
    ├── models.py            # User, Project, Task classes
    ├── services.py          # Business logic layer
    ├── storage.py           # JSON file I/O
    └── cli.py               # CLI commands (argparse + rich)
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd CLI-PROJECT
```

### 2. Create and activate a virtual environment
```bash
# Create
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate

# Activate — Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run CLI Commands

All commands are run from the root folder where `main.py` lives.

### Get help
```bash
python main.py --help
```

---

### 👥 User Commands

| Command | Description |
|---|---|
| `add-user` | Create a new user |
| `list-users` | Display all users |

```bash
# Add a user
python main.py add-user --name "Alex" --email "alex@email.com"

# List all users
python main.py list-users
```

---

### 📁 Project Commands

| Command | Description |
|---|---|
| `add-project` | Add a project to a user |
| `list-projects` | List all projects for a user |

```bash
# Add a project
python main.py add-project --user "Alex" --title "CLI Tool" --desc "A cool project" --due "2025-12-31"

# List projects
python main.py list-projects --user "Alex"
```

---

### ✅ Task Commands

| Command | Description |
|---|---|
| `add-task` | Add a task to a project |
| `list-tasks` | List all tasks in a project |
| `complete-task` | Mark a task as complete |

```bash
# Add a task
python main.py add-task --user "Alex" --project "CLI Tool" --title "Fix bug" --assign "Alex"

# List tasks
python main.py list-tasks --user "Alex" --project "CLI Tool"

# Complete a task
python main.py complete-task --user "Alex" --project "CLI Tool" --task "Fix bug"
```

---

## 🧪 Running Tests

```bash
pytest tests/test_models.py -v
```

Tests cover:
- Model creation and validation
- One-to-many relationships (User → Projects → Tasks)
- Serialization round trips (to_dict / from_dict)
- Service layer logic with mocked storage
- Edge cases: empty fields, duplicates, invalid status

---

## ✨ Features Overview

- **User management** — create and list users with name and email
- **Project management** — assign projects to users with description and due date
- **Task management** — add tasks to projects, assign contributors, track status
- **Persistent storage** — all data saved automatically to `data/users.json`
- **Rich terminal UI** — color-coded tables and styled output powered by `rich`
- **Full test suite** — 37 unit tests across all layers using `pytest`

---

## 🏗 Architecture

```
CLI (cli.py)
  └── Services (services.py)    ← business logic
        └── Storage (storage.py)    ← file I/O
              └── Models (models.py)    ← data classes
                    └── data/users.json    ← persistence
```

---

## 📦 Dependencies

| Package | Purpose |
|---|---|
| `rich` | Styled terminal output and tables |
| `pytest` | Unit testing framework |

Install with:
```bash
pip install -r requirements.txt
```

---

## 🐛 Known Issues

- User names are case-insensitive for lookups but stored as entered — avoid creating "alex" and "Alex" as separate users
- Due dates are stored as plain strings — no date format validation yet
- No update/delete commands yet — only add, list, and complete are supported

---

## 🔄 Git Workflow

```bash
# Create a feature branch
git checkout -b feature/add-user

# Stage and commit
git add .
git commit -m "feat: add User model with property validation"

# Push to GitHub
git push origin feature/add-user
```

---

## 👤 Author

Built as a summative lab project demonstrating Python OOP, CLI design, file persistence, and unit testing.