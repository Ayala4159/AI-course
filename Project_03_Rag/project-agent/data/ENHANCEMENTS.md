# Proposed Enhancements and Implementation Guide

## Overview

This document outlines proposed enhancements to the Task Management System and provides implementation guidance for extending the current codebase.

---

## Enhancement 1: Input Validation

### Current State
```python
def __init__(self, task_id: int, title: str, description: str, ...):
    self.title = title  # No validation
    self.description = description  # No validation
    self.due_date = due_date  # No format check
```

### Proposed Enhancement

#### 1.1 Validation Helper Class

```python
from datetime import datetime
from typing import Optional
import re

class TaskValidator:
    """Validation utilities for task operations."""
    
    MIN_TITLE_LENGTH = 1
    MAX_TITLE_LENGTH = 200
    MAX_DESCRIPTION_LENGTH = 5000
    DATE_FORMAT = "%Y-%m-%d"
    TAG_PATTERN = r"^[a-z0-9]+$"
    
    @staticmethod
    def validate_title(title: str) -> bool:
        """Validate task title."""
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        
        title = title.strip()
        if len(title) < TaskValidator.MIN_TITLE_LENGTH:
            raise ValueError("Title cannot be empty")
        if len(title) > TaskValidator.MAX_TITLE_LENGTH:
            raise ValueError(f"Title cannot exceed {TaskValidator.MAX_TITLE_LENGTH} characters")
        
        return True
    
    @staticmethod
    def validate_description(description: str) -> bool:
        """Validate task description."""
        if not isinstance(description, str):
            raise TypeError("Description must be a string")
        
        description = description.strip()
        if len(description) < 1:
            raise ValueError("Description cannot be empty")
        if len(description) > TaskValidator.MAX_DESCRIPTION_LENGTH:
            raise ValueError(f"Description cannot exceed {TaskValidator.MAX_DESCRIPTION_LENGTH} characters")
        
        return True
    
    @staticmethod
    def validate_date(date_string: Optional[str]) -> bool:
        """Validate date format (YYYY-MM-DD)."""
        if date_string is None:
            return True
        
        try:
            datetime.strptime(date_string, TaskValidator.DATE_FORMAT)
            return True
        except ValueError:
            raise ValueError(f"Invalid date format. Use {TaskValidator.DATE_FORMAT}")
    
    @staticmethod
    def validate_tag(tag: str) -> bool:
        """Validate tag format."""
        if not isinstance(tag, str):
            raise TypeError("Tag must be a string")
        
        tag = tag.strip().lower()
        if not tag:
            raise ValueError("Tag cannot be empty")
        
        if not re.match(TaskValidator.TAG_PATTERN, tag):
            raise ValueError("Tags must be lowercase alphanumeric")
        
        return True
```

#### 1.2 Updated Task Class

```python
class Task:
    def __init__(self, task_id: int, title: str, description: str, 
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 status: TaskStatus = TaskStatus.PENDING,
                 due_date: Optional[str] = None):
        # Validate inputs
        TaskValidator.validate_title(title)
        TaskValidator.validate_description(description)
        TaskValidator.validate_date(due_date)
        
        self.task_id = task_id
        self.title = title.strip()
        self.description = description.strip()
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.tags: list[str] = []
    
    def add_tag(self, tag: str) -> None:
        """Add a tag with validation."""
        TaskValidator.validate_tag(tag)
        tag = tag.strip().lower()
        if tag not in self.tags:
            self.tags.append(tag)
```

---

## Enhancement 2: Custom Exceptions

### Current State
```python
def get_task(self, task_id: int) -> Optional[Task]:
    return self.tasks.get(task_id)  # Silent failure

# Usage: can't distinguish "not found" from other errors
```

### Proposed Enhancement

```python
class TaskManagerError(Exception):
    """Base exception for task management errors."""
    pass

class TaskNotFoundError(TaskManagerError):
    """Raised when a task is not found."""
    pass

class InvalidTaskStateError(TaskManagerError):
    """Raised when task state transition is invalid."""
    pass

class TaskValidationError(TaskManagerError):
    """Raised when task validation fails."""
    pass

# Updated TaskManager methods
class TaskManager:
    def get_task(self, task_id: int) -> Task:
        """Retrieve a task by ID.
        
        Raises:
            TaskNotFoundError: If task is not found
        """
        task = self.tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task
    
    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.
        
        Raises:
            TaskNotFoundError: If task is not found
        """
        if task_id not in self.tasks:
            raise TaskNotFoundError(f"Cannot delete non-existent task {task_id}")
        del self.tasks[task_id]

# Usage with better error handling
try:
    task = manager.get_task(999)
except TaskNotFoundError as e:
    print(f"Error: {e}")
```

---

## Enhancement 3: Task Indexing for Performance

### Current State
```python
def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
    return [task for task in self.tasks.values() if task.status == status]
    # O(n) - scans all tasks every time
```

### Proposed Enhancement

```python
class TaskManager:
    def __init__(self):
        self.tasks: dict[int, Task] = {}
        self.next_task_id: int = 1
        
        # Add indexes for fast lookups
        self._status_index: dict[TaskStatus, set[int]] = {
            status: set() for status in TaskStatus
        }
        self._priority_index: dict[TaskPriority, set[int]] = {
            priority: set() for priority in TaskPriority
        }
        self._tag_index: dict[str, set[int]] = {}  # tag -> task_ids
    
    def add_task(self, title: str, description: str, 
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 due_date: Optional[str] = None) -> Task:
        """Add task and update indexes."""
        task = Task(
            task_id=self.next_task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        
        task_id = self.next_task_id
        self.tasks[task_id] = task
        
        # Update indexes
        self._status_index[task.status].add(task_id)
        self._priority_index[task.priority].add(task_id)
        
        self.next_task_id += 1
        return task
    
    def _update_task_indexes(self, task: Task) -> None:
        """Update indexes when task state changes."""
        task_id = task.task_id
        
        # Update status index if status changed
        for status, task_ids in self._status_index.items():
            if task.status == status:
                task_ids.add(task_id)
            else:
                task_ids.discard(task_id)
        
        # Update priority index if priority changed
        for priority, task_ids in self._priority_index.items():
            if task.priority == priority:
                task_ids.add(task_id)
            else:
                task_ids.discard(task_id)
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get tasks by status - O(1) index lookup + O(k) where k = result count."""
        task_ids = self._status_index[status]
        return [self.tasks[tid] for tid in task_ids]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Get tasks by priority - optimized with index."""
        task_ids = self._priority_index[priority]
        return [self.tasks[tid] for tid in task_ids]
    
    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """Get tasks by tag - optimized with index."""
        task_ids = self._tag_index.get(tag, set())
        return [self.tasks[tid] for tid in task_ids]
```

**Performance Improvement**:
- Before: O(n) per filter operation
- After: O(k) where k = result count

---

## Enhancement 4: State Machine for Task States

### Current State
```python
def mark_in_progress(self) -> None:
    self.status = TaskStatus.IN_PROGRESS
    # Any status can transition to any other status
```

### Proposed Enhancement

```python
class TaskStateMachine:
    """Manages valid task state transitions."""
    
    VALID_TRANSITIONS = {
        TaskStatus.PENDING: {
            TaskStatus.IN_PROGRESS,
            TaskStatus.ON_HOLD,
            TaskStatus.CANCELLED
        },
        TaskStatus.IN_PROGRESS: {
            TaskStatus.COMPLETED,
            TaskStatus.ON_HOLD,
            TaskStatus.CANCELLED
        },
        TaskStatus.ON_HOLD: {
            TaskStatus.IN_PROGRESS,
            TaskStatus.PENDING,
            TaskStatus.CANCELLED
        },
        TaskStatus.COMPLETED: {
            TaskStatus.PENDING  # Allow re-opening completed tasks
        },
        TaskStatus.CANCELLED: {
            TaskStatus.PENDING  # Allow re-opening cancelled tasks
        }
    }
    
    @classmethod
    def can_transition(cls, from_status: TaskStatus, to_status: TaskStatus) -> bool:
        """Check if state transition is valid."""
        return to_status in cls.VALID_TRANSITIONS.get(from_status, set())
    
    @classmethod
    def transition(cls, task: Task, new_status: TaskStatus) -> None:
        """Perform a state transition with validation."""
        if not cls.can_transition(task.status, new_status):
            raise InvalidTaskStateError(
                f"Cannot transition from {task.status.value} to {new_status.value}"
            )
        
        task.status = new_status
        if new_status == TaskStatus.COMPLETED:
            task.completed_at = datetime.now()

# Usage
try:
    TaskStateMachine.transition(task, TaskStatus.COMPLETED)
except InvalidTaskStateError as e:
    print(f"Invalid transition: {e}")
```

---

## Enhancement 5: Batch Operations

### Proposed Enhancement

```python
class TaskManager:
    def add_tasks_batch(self, task_data: list[dict]) -> list[Task]:
        """Add multiple tasks in a batch operation.
        
        Args:
            task_data: List of task specifications
            
        Returns:
            List of created Task objects
        """
        created_tasks = []
        for data in task_data:
            task = self.add_task(
                title=data['title'],
                description=data['description'],
                priority=data.get('priority', TaskPriority.MEDIUM),
                due_date=data.get('due_date')
            )
            created_tasks.append(task)
        return created_tasks
    
    def delete_tasks_by_status(self, status: TaskStatus) -> int:
        """Delete all tasks with a specific status.
        
        Returns:
            Number of deleted tasks
        """
        tasks_to_delete = self.get_tasks_by_status(status)
        count = 0
        for task in tasks_to_delete:
            self.delete_task(task.task_id)
            count += 1
        return count
    
    def mark_tasks_completed(self, task_ids: list[int]) -> int:
        """Mark multiple tasks as completed.
        
        Returns:
            Number of successfully updated tasks
        """
        count = 0
        for task_id in task_ids:
            try:
                task = self.get_task(task_id)
                TaskStateMachine.transition(task, TaskStatus.COMPLETED)
                count += 1
            except TaskNotFoundError:
                continue
        return count
```

---

## Enhancement 6: Task Caching

### Proposed Enhancement

```python
from functools import lru_cache
from datetime import datetime, timedelta

class TaskCache:
    """Simple caching layer for frequently accessed data."""
    
    def __init__(self, ttl_seconds: int = 300):
        """Initialize cache with time-to-live.
        
        Args:
            ttl_seconds: Cache validity duration in seconds
        """
        self.cache = {}
        self.ttl_seconds = ttl_seconds
        self.timestamps = {}
    
    def get(self, key: str):
        """Get cached value if not expired."""
        if key not in self.cache:
            return None
        
        # Check if cache is still valid
        age = (datetime.now() - self.timestamps[key]).total_seconds()
        if age > self.ttl_seconds:
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        return self.cache[key]
    
    def set(self, key: str, value) -> None:
        """Store value in cache."""
        self.cache[key] = value
        self.timestamps[key] = datetime.now()
    
    def invalidate(self, key: str) -> None:
        """Invalidate cache entry."""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache."""
        self.cache.clear()
        self.timestamps.clear()

# Integration with TaskManager
class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.next_task_id = 1
        self.cache = TaskCache(ttl_seconds=60)  # 1 minute TTL
    
    def get_statistics(self) -> dict:
        """Get statistics with caching."""
        cached = self.cache.get("statistics")
        if cached is not None:
            return cached
        
        # Compute statistics
        stats = {
            "total_tasks": len(self.tasks),
            "pending": len(self.get_tasks_by_status(TaskStatus.PENDING)),
            # ... other stats
        }
        
        self.cache.set("statistics", stats)
        return stats
    
    def _invalidate_stats_cache(self) -> None:
        """Invalidate stats cache when tasks change."""
        self.cache.invalidate("statistics")
```

---

## Implementation Roadmap

### Phase 1: Validation (Week 1)
- [ ] Add TaskValidator class
- [ ] Update Task.__init__ with validation
- [ ] Add validation tests
- [ ] Update requirements documentation

### Phase 2: Error Handling (Week 2)
- [ ] Define exception hierarchy
- [ ] Update TaskManager methods to raise exceptions
- [ ] Update CLI to handle exceptions
- [ ] Add exception handling tests

### Phase 3: Performance (Week 3)
- [ ] Implement task indexing
- [ ] Add batch operations
- [ ] Implement caching
- [ ] Performance benchmarks

### Phase 4: State Management (Week 4)
- [ ] Implement TaskStateMachine
- [ ] Add state transition tests
- [ ] Update documentation

---

## Backward Compatibility Considerations

When implementing these enhancements:

1. **Validation**: May cause existing code to fail - handle gracefully
2. **Exceptions**: Requires updating existing error handling code
3. **Indexing**: Transparent improvement, no API change needed
4. **State Machine**: May restrict previously allowed transitions

---

## Testing Strategy for Enhancements

Add tests for:
- Invalid inputs (empty strings, bad dates, etc.)
- State machine transitions
- Index consistency
- Cache invalidation
- Batch operations
- Exception raising

Example:
```python
def test_invalid_title_raises_error(self):
    with self.assertRaises(ValueError):
        Task(1, "", "Description")

def test_invalid_state_transition_raises_error(self):
    task = Task(1, "Title", "Desc", status=TaskStatus.COMPLETED)
    with self.assertRaises(InvalidTaskStateError):
        TaskStateMachine.transition(task, TaskStatus.IN_PROGRESS)
```

---

## Conclusion

These enhancements provide:
- ✅ Robust input validation
- ✅ Better error handling
- ✅ Improved performance for large datasets
- ✅ Proper state management
- ✅ Caching for frequently accessed data

Implementation should be done incrementally with thorough testing and documentation updates.
