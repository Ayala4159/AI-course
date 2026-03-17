# Usage Examples and Tutorials

## Installation and Setup

### Step 1: Clone/Setup Project
```bash
cd task_manager
pip install -r requirements.txt
```

### Step 2: Basic Import
```python
from src import TaskManager, TaskPriority, TaskStatus
```

## Example 1: Creating and Managing Tasks

### Create a Task Manager
```python
manager = TaskManager()
```

### Add Tasks
```python
# Add a simple task
task1 = manager.add_task(
    "Write project documentation",
    "Create comprehensive documentation for the project"
)

# Add task with priority and due date
task2 = manager.add_task(
    "Review pull requests",
    "Conduct code review for pending PRs",
    priority=TaskPriority.HIGH,
    due_date="2026-03-15"
)

# Add critical task
task3 = manager.add_task(
    "Fix critical bug",
    "Resolve the authentication issue in API",
    priority=TaskPriority.CRITICAL
)
```

### Check Task Properties
```python
print(f"Task ID: {task1.task_id}")
print(f"Title: {task1.title}")
print(f"Priority: {task1.priority.name}")
print(f"Status: {task1.status.value}")
print(f"Created: {task1.created_at}")
```

## Example 2: Task Lifecycle

### Update Task Status
```python
# Start working on a task
manager.update_task_status(task1.task_id, TaskStatus.IN_PROGRESS)

# Complete the task
task = manager.get_task(task1.task_id)
task.mark_completed()
print(f"Completed at: {task.completed_at}")
```

### Retrieve Task
```python
# Get specific task
task = manager.get_task(1)
if task:
    print(f"Found: {task.title}")
else:
    print("Task not found")
```

## Example 3: Filtering and Querying

### Get All Pending Tasks
```python
pending_tasks = manager.get_pending_tasks()
for task in pending_tasks:
    print(f"[{task.priority.name}] {task.title}")
```

### Get High Priority Tasks
```python
critical_work = manager.get_high_priority_tasks()
print(f"Critical items: {len(critical_work)}")
```

### Filter by Status
```python
in_progress = manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)
completed = manager.get_tasks_by_status(TaskStatus.COMPLETED)
```

### Filter by Priority
```python
high_priority_tasks = manager.get_tasks_by_priority(TaskPriority.HIGH)
low_priority_tasks = manager.get_tasks_by_priority(TaskPriority.LOW)
```

## Example 4: Using Tags

### Add Tags to Task
```python
task = manager.get_task(1)
task.add_tag("backend")
task.add_tag("urgent")
task.add_tag("python")

print(f"Tags: {task.tags}")
# Tags: ['backend', 'urgent', 'python']
```

### Remove Tags
```python
task.remove_tag("urgent")
```

### Filter by Tag
```python
backend_tasks = manager.get_tasks_by_tag("backend")
print(f"Backend tasks: {len(backend_tasks)}")
```

## Example 5: Persistence

### Save Tasks to File
```python
manager.save_to_file("my_tasks.json")
print("Tasks saved!")
```

### Load Tasks from File
```python
new_manager = TaskManager()
new_manager.load_from_file("my_tasks.json")
all_tasks = new_manager.get_all_tasks()
print(f"Loaded {len(all_tasks)} tasks")
```

### Example JSON Output
```json
[
  {
    "task_id": 1,
    "title": "Write project documentation",
    "description": "Create comprehensive documentation for the project",
    "priority": "MEDIUM",
    "status": "pending",
    "due_date": null,
    "created_at": "2026-03-11T10:30:00.123456",
    "completed_at": null,
    "tags": []
  }
]
```

## Example 6: Analytics and Statistics

### Get Task Statistics
```python
stats = manager.get_statistics()

print(f"Total Tasks: {stats['total_tasks']}")
print(f"Pending: {stats['pending']}")
print(f"In Progress: {stats['in_progress']}")
print(f"Completed: {stats['completed']}")
print(f"High Priority Pending: {stats['high_priority_pending']}")
```

### Generate Report
```python
def generate_task_report(manager):
    """Generate a text report of current tasks."""
    stats = manager.get_statistics()
    print("\n=== TASK REPORT ===\n")
    print(f"Total Tasks: {stats['total_tasks']}")
    print(f"  - Pending: {stats['pending']}")
    print(f"  - In Progress: {stats['in_progress']}")
    print(f"  - Completed: {stats['completed']}\n")
    
    print("HIGH PRIORITY ITEMS:")
    for task in manager.get_high_priority_tasks():
        print(f"  [{task.priority.name}] {task.title}")
    
    print("\nPENDING TASKS (by priority):")
    for task in manager.get_pending_tasks():
        print(f"  [{task.priority.name}] {task.title}")

# Usage
generate_task_report(manager)
```

## Example 7: Complete Workflow

```python
# Initialize
manager = TaskManager()

# Add tasks for a project sprint
sprint_tasks = [
    ("Implement API endpoints", "Create CRUD endpoints", TaskPriority.HIGH),
    ("Write unit tests", "Cover new endpoints", TaskPriority.HIGH),
    ("Update documentation", "Document new API", TaskPriority.MEDIUM),
    ("Code review", "Review team PRs", TaskPriority.MEDIUM),
    ("Optimize database queries", "Improve performance", TaskPriority.LOW),
]

for title, desc, priority in sprint_tasks:
    task = manager.add_task(title, desc, priority=priority)
    task.add_tag("sprint-1")
    task.add_tag("backend")

# Check sprint status
sprint_tasks = manager.get_tasks_by_tag("sprint-1")
print(f"Sprint 1 has {len(sprint_tasks)} tasks")

# Start working
for task in manager.get_pending_tasks()[:2]:  # Start with top 2
    task.mark_in_progress()

# Complete a task
task = manager.get_task(1)
task.mark_completed()

# Generate report
print(manager.get_statistics())

# Save progress
manager.save_to_file("sprint_1_progress.json")
```

## Troubleshooting

### Task Not Found
```python
task = manager.get_task(999)
if task is None:
    print("Task ID does not exist")
```

### Duplicate Tags Not Added
```python
task.add_tag("important")
task.add_tag("important")  # This won't be added twice
print(task.tags)  # ['important'] - only appears once
```

### File Not Loading
```python
try:
    manager.load_from_file("nonexistent.json")
except FileNotFoundError:
    print("File not found. Creating new task list.")
```
