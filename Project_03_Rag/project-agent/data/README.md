# Task Management Project

A comprehensive Python task management system with priority tracking, status management, and comprehensive filtering capabilities.

## Features

- **Task Management**: Create, read, update, and delete tasks
- **Priority Levels**: Support for LOW, MEDIUM, HIGH, and CRITICAL priorities
- **Status Tracking**: Track tasks with statuses: PENDING, IN_PROGRESS, COMPLETED, CANCELLED, ON_HOLD
- **Tag System**: Add and remove tags for better task organization
- **Filtering**: Filter tasks by status, priority, tags, and more
- **Persistence**: Save and load tasks from JSON files
- **Statistics**: Generate task statistics and summaries

## Project Structure

```
task_manager/
├── src/
│   ├── __init__.py
│   ├── task.py              # Task class definition
│   └── task_manager.py      # TaskManager class implementation
├── tests/
│   ├── test_task.py
│   └── test_task_manager.py
├── docs/
│   └── (documentation files)
├── requirements.txt
├── setup.py
└── README.md
```

## Quick Start

### Installation

```bash
cd task_manager
pip install -r requirements.txt
```

### Basic Usage

```python
from src import TaskManager, TaskPriority, TaskStatus

# Create manager
manager = TaskManager()

# Add tasks
task = manager.add_task(
    "Important Project",
    "Complete the Q1 report",
    priority=TaskPriority.HIGH,
    due_date="2026-03-20"
)

# Get pending tasks
pending = manager.get_pending_tasks()

# Mark as completed
manager.update_task_status(task.task_id, TaskStatus.COMPLETED)

# Save to file
manager.save_to_file("tasks.json")
```

## Running Tests

```bash
python -m pytest tests/
# or
python -m unittest discover tests/
```

## API Documentation

See [DESIGN.md](docs/DESIGN.md) for detailed API documentation and design patterns.
