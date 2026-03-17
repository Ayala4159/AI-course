# Quick Start and Reference Guide

## 🚀 Getting Started

### Installation

```bash
# Navigate to project directory
cd task_manager

# Install dependencies (optional, project has no external dependencies)
pip install -r requirements.txt
```

### Run the CLI Interface

```bash
# Run the interactive task manager CLI
python -m src.cli
```

### Run Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
pytest --cov=src tests/

# Or use unittest
python -m unittest discover tests/
```

---

## 📚 Documentation Quick Links

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [README.md](README.md) | Project overview and features | 5 min |
| [docs/EXAMPLES.md](docs/EXAMPLES.md) | Usage examples and tutorials | 20 min |
| [docs/DESIGN.md](docs/DESIGN.md) | Architecture and API reference | 15 min |
| [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) | Developer guidelines | 10 min |
| [docs/CODE_ANALYSIS.md](docs/CODE_ANALYSIS.md) | Code review and improvements | 30 min |
| [docs/ENHANCEMENTS.md](docs/ENHANCEMENTS.md) | Proposed features | 25 min |
| [docs/AGENTIC_ACTIVITIES.md](docs/AGENTIC_ACTIVITIES.md) | AI tool usage audit trail | 20 min |

---

## 💻 Code Examples

### Basic Usage

```python
from src import TaskManager, TaskPriority, TaskStatus

# Create manager
manager = TaskManager()

# Add a task
task = manager.add_task(
    "Write documentation",
    "Create comprehensive API docs",
    priority=TaskPriority.HIGH,
    due_date="2026-03-20"
)

# Get all pending tasks
pending = manager.get_pending_tasks()

# Mark as completed
task.mark_completed()

# Get statistics
stats = manager.get_statistics()
print(f"Total: {stats['total_tasks']}, Completed: {stats['completed']}")
```

### Filtering Tasks

```python
# By status
pending = manager.get_tasks_by_status(TaskStatus.PENDING)

# By priority
critical = manager.get_tasks_by_priority(TaskPriority.CRITICAL)

# By tag
backend_tasks = manager.get_tasks_by_tag("backend")

# High priority items
urgent = manager.get_high_priority_tasks()
```

### Persistence

```python
# Save to file
manager.save_to_file("my_tasks.json")

# Load from file
new_manager = TaskManager()
new_manager.load_from_file("my_tasks.json")
```

### Tag Management

```python
task = manager.get_task(1)

# Add tags
task.add_tag("urgent")
task.add_tag("backend")

# Remove tags
task.remove_tag("urgent")

# View tags
print(task.tags)  # ['backend']
```

---

## 🎯 Key Classes and Methods

### TaskManager

**Creation**:
```python
manager = TaskManager()
```

**CRUD Operations**:
- `add_task(title, description, priority, due_date)` → Task
- `get_task(task_id)` → Task | None
- `delete_task(task_id)` → bool
- `get_all_tasks()` → List[Task]

**Filtering**:
- `get_tasks_by_status(status)` → List[Task]
- `get_tasks_by_priority(priority)` → List[Task]
- `get_tasks_by_tag(tag)` → List[Task]
- `get_pending_tasks()` → List[Task]
- `get_high_priority_tasks()` → List[Task]

**Persistence**:
- `save_to_file(filename)` → None
- `load_from_file(filename)` → None

**Analytics**:
- `get_statistics()` → dict

### Task

**Creation**:
```python
task = Task(task_id, title, description, priority, status, due_date)
```

**Methods**:
- `mark_completed()` - Mark task done
- `mark_in_progress()` - Mark task in progress
- `add_tag(tag)` - Add organizational tag
- `remove_tag(tag)` - Remove tag
- `to_dict()` - Serialize to dictionary

**Properties**:
- `task_id` - Unique identifier
- `title` - Task name
- `description` - Details
- `priority` - TaskPriority enum
- `status` - TaskStatus enum
- `due_date` - Optional deadline
- `created_at` - Timestamp
- `completed_at` - Completion timestamp
- `tags` - List of tags

### Enums

**TaskPriority**:
```python
TaskPriority.LOW
TaskPriority.MEDIUM
TaskPriority.HIGH
TaskPriority.CRITICAL
```

**TaskStatus**:
```python
TaskStatus.PENDING
TaskStatus.IN_PROGRESS
TaskStatus.COMPLETED
TaskStatus.CANCELLED
TaskStatus.ON_HOLD
```

---

## 🧪 Testing

### Test Files

- `tests/test_task.py` - 6 tests for Task class
- `tests/test_task_manager.py` - 7 tests for TaskManager

### Run Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_task.py -v

# With coverage
pytest --cov=src --cov-report=html tests/
```

### Example Test

```python
def test_mark_completed(self):
    task = Task(1, "Test", "Description")
    task.mark_completed()
    self.assertEqual(task.status, TaskStatus.COMPLETED)
    self.assertIsNotNone(task.completed_at)
```

---

## 📊 Project Structure

```
task_manager/
├── src/                    # Source code
│   ├── __init__.py        # Package exports
│   ├── task.py            # Task class
│   ├── task_manager.py    # TaskManager class
│   └── cli.py             # CLI interface
├── tests/                  # Test suite
│   ├── test_task.py       # Task tests
│   └── test_task_manager.py # Manager tests
├── docs/                   # Documentation
│   ├── DESIGN.md          # Architecture
│   ├── DEVELOPMENT.md     # Guidelines
│   ├── EXAMPLES.md        # Examples
│   ├── CODE_ANALYSIS.md   # Code review
│   ├── ENHANCEMENTS.md    # Proposals
│   └── AGENTIC_ACTIVITIES.md # Tool usage
├── README.md              # Quick start
├── setup.py               # Package config
├── requirements.txt       # Dependencies
└── PROJECT_SUMMARY.md     # This summary
```

---

## 🔧 Common Tasks

### Add a New Feature

1. Plan the feature in docs/ENHANCEMENTS.md
2. Write tests first in tests/
3. Implement in src/
4. Update docstrings
5. Add examples to docs/EXAMPLES.md

### Run Full Test Suite

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Check Type Hints (if mypy installed)

```bash
mypy src/
```

### Generate Documentation

Already included in docs/ folder. Update with any new features.

---

## 📝 Common Patterns

### Creating and Managing Tasks

```python
manager = TaskManager()

# Create
task = manager.add_task("Build API", "RESTful endpoints", 
                        priority=TaskPriority.HIGH)

# Track progress
task.mark_in_progress()

# Organize
task.add_tag("backend")
task.add_tag("python")

# Complete
task.mark_completed()

# Retrieve
completed = manager.get_task(task.task_id)
print(f"✓ {completed.title}")
```

### Reporting

```python
# Get statistics
stats = manager.get_statistics()
print(f"Progress: {stats['completed']}/{stats['total_tasks']}")

# List by priority
urgent = manager.get_pending_tasks()
for task in urgent:
    print(f"[{task.priority.name}] {task.title}")

# Filter by tag
backend = manager.get_tasks_by_tag("backend")
print(f"Backend tasks: {len(backend)}")
```

### Persistence

```python
# Save progress
manager.save_to_file("sprint_tasks.json")

# Load later
new_manager = TaskManager()
new_manager.load_from_file("sprint_tasks.json")

# Continue working
for task in new_manager.get_pending_tasks():
    print(f"TODO: {task.title}")
```

---

## 🚨 Troubleshooting

### Task not found
```python
task = manager.get_task(999)
if task is None:
    print("Task does not exist")
```

### Invalid date format
```python
# Use YYYY-MM-DD format
task = manager.add_task("Task", "Description", due_date="2026-03-20")
```

### File not found on load
```python
try:
    manager.load_from_file("tasks.json")
except FileNotFoundError:
    print("Create tasks first, then save")
```

---

## 📊 Statistics Example

```python
manager = TaskManager()

# Add example tasks
manager.add_task("Task 1", "Description", TaskPriority.CRITICAL)
manager.add_task("Task 2", "Description", TaskPriority.HIGH)
manager.add_task("Task 3", "Description", TaskPriority.MEDIUM)

# Get stats
stats = manager.get_statistics()

# Output:
# {
#   'total_tasks': 3,
#   'pending': 3,
#   'in_progress': 0,
#   'completed': 0,
#   'cancelled': 0,
#   'on_hold': 0,
#   'high_priority_pending': 2
# }
```

---

## 🎓 Learning Path

**Beginner**:
1. Read README.md
2. Run examples in docs/EXAMPLES.md
3. Try the CLI: `python -m src.cli`

**Intermediate**:
1. Study docs/DESIGN.md
2. Review src/task.py
3. Explore src/task_manager.py
4. Run tests with pytest

**Advanced**:
1. Read docs/CODE_ANALYSIS.md
2. Review docs/ENHANCEMENTS.md
3. Consider refactoring opportunities
4. Plan feature additions

---

## 📞 Key Files Reference

| Task | File |
|------|------|
| Understand architecture | docs/DESIGN.md |
| See code examples | docs/EXAMPLES.md |
| Follow dev guidelines | docs/DEVELOPMENT.md |
| Analyze code | docs/CODE_ANALYSIS.md |
| Plan improvements | docs/ENHANCEMENTS.md |
| Track tool usage | docs/AGENTIC_ACTIVITIES.md |
| View implementations | src/task.py, src/task_manager.py |
| Study patterns | tests/ |

---

## ✅ Quick Checklist

- [x] Run tests: `pytest tests/`
- [x] Review docs: Start with README.md
- [x] Try CLI: `python -m src.cli`
- [x] Read architecture: docs/DESIGN.md
- [x] Check examples: docs/EXAMPLES.md
- [x] Plan features: docs/ENHANCEMENTS.md
- [x] Study code: src/ directory
- [x] Run analysis: docs/CODE_ANALYSIS.md

---

## 🎯 Project Status

✅ **Complete**: All core features implemented  
✅ **Tested**: 13 unit tests with coverage  
✅ **Documented**: 2,500+ lines of documentation  
✅ **Ready**: For use, enhancement, or learning  

**Next Steps**:
- Implement enhancements from ENHANCEMENTS.md
- Add database backend support
- Build REST API layer
- Create web UI
- Deploy to production

---

## 📚 Additional Resources

- Python docs: https://docs.python.org/3/
- Pytest guide: https://docs.pytest.org/
- Type hints: https://docs.python.org/3/library/typing.html
- Design patterns: https://refactoring.guru/design-patterns

---

**Quick Start Complete!**  
You're ready to explore, use, and enhance the Task Management System.

For detailed information, see [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md).
