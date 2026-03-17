"""Main task manager module for managing tasks."""

from typing import Optional, List
from src.task import Task, TaskPriority, TaskStatus
import json


class TaskManager:
    """Main class for managing tasks."""
    
    def __init__(self):
        """Initialize the task manager."""
        self.tasks: dict[int, Task] = {}
        self.next_task_id: int = 1
        
    def add_task(self, title: str, description: str, 
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 due_date: Optional[str] = None) -> Task:
        """Add a new task to the manager.
        
        Args:
            title: Task title
            description: Task description
            priority: Task priority level
            due_date: Optional due date in YYYY-MM-DD format
            
        Returns:
            The created task object
        """
        task = Task(
            task_id=self.next_task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        self.tasks[self.next_task_id] = task
        self.next_task_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID.
        
        Args:
            task_id: The task ID to retrieve
            
        Returns:
            The task object or None if not found
        """
        return self.tasks.get(task_id)
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.
        
        Args:
            task_id: The task ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.
        
        Returns:
            List of all tasks
        """
        return list(self.tasks.values())
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with a specific status.
        
        Args:
            status: The status to filter by
            
        Returns:
            List of tasks with the specified status
        """
        return [task for task in self.tasks.values() if task.status == status]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Get all tasks with a specific priority.
        
        Args:
            priority: The priority level to filter by
            
        Returns:
            List of tasks with the specified priority
        """
        return [task for task in self.tasks.values() if task.priority == priority]
    
    def get_tasks_by_tag(self, tag: str) -> List[Task]:
        """Get all tasks with a specific tag.
        
        Args:
            tag: The tag to filter by
            
        Returns:
            List of tasks with the specified tag
        """
        return [task for task in self.tasks.values() if tag in task.tags]
    
    def update_task_status(self, task_id: int, status: TaskStatus) -> bool:
        """Update the status of a task.
        
        Args:
            task_id: The task ID to update
            status: The new status
            
        Returns:
            True if successful, False if task not found
        """
        task = self.get_task(task_id)
        if task:
            task.status = status
            return True
        return False
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks.
        
        Returns:
            List of pending tasks sorted by priority (descending)
        """
        pending = self.get_tasks_by_status(TaskStatus.PENDING)
        return sorted(pending, key=lambda t: t.priority.value, reverse=True)
    
    def get_high_priority_tasks(self) -> List[Task]:
        """Get all high priority or critical tasks.
        
        Returns:
            List of high priority/critical tasks not yet completed
        """
        high_priority = [
            task for task in self.tasks.values()
            if task.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]
            and task.status != TaskStatus.COMPLETED
        ]
        return high_priority
    
    def save_to_file(self, filename: str) -> None:
        """Save tasks to a JSON file.
        
        Args:
            filename: Path to the output file
        """
        tasks_data = [task.to_dict() for task in self.tasks.values()]
        with open(filename, 'w') as f:
            json.dump(tasks_data, f, indent=2)
    
    def load_from_file(self, filename: str) -> None:
        """Load tasks from a JSON file.
        
        Args:
            filename: Path to the input file
        """
        with open(filename, 'r') as f:
            tasks_data = json.load(f)
            
        self.tasks.clear()
        self.next_task_id = 1
        
        for task_data in tasks_data:
            task = Task(
                task_id=task_data['task_id'],
                title=task_data['title'],
                description=task_data['description'],
                priority=TaskPriority[task_data['priority']],
                status=TaskStatus(task_data['status']),
                due_date=task_data.get('due_date')
            )
            self.tasks[task.task_id] = task
            if task.task_id >= self.next_task_id:
                self.next_task_id = task.task_id + 1
    
    def get_statistics(self) -> dict:
        """Get statistics about tasks.
        
        Returns:
            Dictionary containing task statistics
        """
        all_tasks = self.get_all_tasks()
        return {
            "total_tasks": len(all_tasks),
            "pending": len(self.get_tasks_by_status(TaskStatus.PENDING)),
            "in_progress": len(self.get_tasks_by_status(TaskStatus.IN_PROGRESS)),
            "completed": len(self.get_tasks_by_status(TaskStatus.COMPLETED)),
            "cancelled": len(self.get_tasks_by_status(TaskStatus.CANCELLED)),
            "on_hold": len(self.get_tasks_by_status(TaskStatus.ON_HOLD)),
            "high_priority_pending": len([
                t for t in all_tasks 
                if t.priority in [TaskPriority.HIGH, TaskPriority.CRITICAL]
                and t.status == TaskStatus.PENDING
            ])
        }
