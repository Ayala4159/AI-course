# Task Management System - Design Documentation

## Architecture Overview

The Task Management System is built on a modular architecture with clear separation of concerns:

### Core Components

#### 1. Task Module (`src/task.py`)

Defines the fundamental data structures and models for the system:

- **TaskPriority Enum**: Defines priority levels
  - LOW (1)
  - MEDIUM (2)
  - HIGH (3)
  - CRITICAL (4)

- **TaskStatus Enum**: Defines task lifecycle states
  - PENDING: Initial state
  - IN_PROGRESS: Task is actively being worked on
  - COMPLETED: Task has been finished
  - CANCELLED: Task was cancelled
  - ON_HOLD: Task is temporarily paused

- **Task Class**: Represents an individual task with:
  - Unique identifier
  - Metadata (title, description)
  - Status and priority
  - Timestamps (created_at, completed_at)
  - Tag system for organization
  - Methods for state transitions

#### 2. TaskManager Module (`src/task_manager.py`)

High-level orchestration and management of tasks:

- **TaskManager Class**: Provides:
  - Task CRUD operations
  - Advanced filtering and querying
  - Statistical analysis
  - Persistence (JSON serialization)

### Design Patterns Used

#### 1. **Enum Pattern**
Used for TaskPriority and TaskStatus to provide type-safe constants and eliminate magic strings.

```python
class TaskPriority(Enum):
    CRITICAL = 4
```

#### 2. **Repository Pattern**
TaskManager acts as a repository, managing the collection of tasks and providing data access methods.

#### 3. **State Pattern**
Tasks have well-defined states (PENDING, IN_PROGRESS, etc.) with controlled transitions.

#### 4. **Fluent Interface**
Methods like `add_task()` return the created object for further chaining if needed.

### Data Flow

```
User Input
    ↓
TaskManager (Orchestration)
    ↓
Task (Data Model)
    ↓
Enums (Type Safety)
    ↓
Persistence Layer (JSON)
```

## API Reference

### Task Class

#### Constructor
```python
Task(task_id: int, title: str, description: str, 
     priority: TaskPriority = TaskPriority.MEDIUM,
     status: TaskStatus = TaskStatus.PENDING,
     due_date: Optional[str] = None)
```

#### Key Methods

| Method | Purpose |
|--------|---------|
| `mark_completed()` | Marks task as completed with timestamp |
| `mark_in_progress()` | Marks task as in progress |
| `add_tag(tag: str)` | Adds a tag (no duplicates) |
| `remove_tag(tag: str)` | Removes a tag if present |
| `to_dict()` | Serializes task to dictionary |

### TaskManager Class

#### Constructor
```python
TaskManager()  # Initializes empty task collection
```

#### Task Operations

| Method | Returns | Purpose |
|--------|---------|---------|
| `add_task(...)` | Task | Creates and adds new task |
| `get_task(task_id)` | Task \| None | Retrieves specific task |
| `delete_task(task_id)` | bool | Removes task, returns success |
| `get_all_tasks()` | List[Task] | Returns all tasks |

#### Filtering Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_tasks_by_status(status)` | List[Task] | Filter by TaskStatus |
| `get_tasks_by_priority(priority)` | List[Task] | Filter by TaskPriority |
| `get_tasks_by_tag(tag)` | List[Task] | Filter by tag |
| `get_pending_tasks()` | List[Task] | All pending tasks, sorted by priority |
| `get_high_priority_tasks()` | List[Task] | HIGH and CRITICAL non-completed |

#### Persistence

| Method | Purpose |
|--------|---------|
| `save_to_file(filename)` | Saves all tasks to JSON |
| `load_from_file(filename)` | Loads tasks from JSON |

#### Analytics

| Method | Returns | Purpose |
|--------|---------|---------|
| `get_statistics()` | dict | Task counts by status/priority |

## Implementation Notes

### Type Hints
Full type hints are used throughout for better IDE support and type checking with mypy.

### Datetime Handling
- `created_at`: Set automatically when task is created
- `completed_at`: Set when task is marked completed
- Format: ISO 8601 (via datetime.isoformat())

### Tag System
- Tags are stored as a list of strings
- Duplicates are prevented when adding
- Useful for categorical organization beyond priority/status

### JSON Serialization
Tasks are serialized with all metadata including timestamps and tags for full persistence.

## Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Task dependencies and relationships
- [ ] Recurring tasks
- [ ] Task assignments and ownership
- [ ] Collaboration features
- [ ] REST API layer
- [ ] Web UI
- [ ] Notification system
