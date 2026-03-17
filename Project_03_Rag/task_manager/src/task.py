from enum import Enum
from datetime import datetime
from typing import Optional

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"

class Task:
    def __init__(self, task_id: int, title: str, description: str, 
                 priority: TaskPriority = TaskPriority.MEDIUM,
                 status: TaskStatus = TaskStatus.PENDING,
                 due_date: Optional[str] = None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.due_date = due_date
        self.created_at = datetime.now()
        self.completed_at = None
        self.tags = []

    # שאר הפונקציות (to_dict, mark_completed וכו') נשארות אותו דבר
    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.name,
            "status": self.status.value
        }