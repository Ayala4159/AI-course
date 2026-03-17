"""Unit tests for the Task class."""

import unittest
from src.task import Task, TaskPriority, TaskStatus


class TestTask(unittest.TestCase):
    """Test cases for Task class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.task = Task(
            task_id=1,
            title="Test Task",
            description="This is a test task",
            priority=TaskPriority.HIGH,
            due_date="2026-03-20"
        )
    
    def test_task_creation(self):
        """Test task creation."""
        self.assertEqual(self.task.task_id, 1)
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.priority, TaskPriority.HIGH)
        self.assertEqual(self.task.status, TaskStatus.PENDING)
    
    def test_mark_completed(self):
        """Test marking task as completed."""
        self.task.mark_completed()
        self.assertEqual(self.task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(self.task.completed_at)
    
    def test_mark_in_progress(self):
        """Test marking task as in progress."""
        self.task.mark_in_progress()
        self.assertEqual(self.task.status, TaskStatus.IN_PROGRESS)
    
    def test_add_tag(self):
        """Test adding tags."""
        self.task.add_tag("urgent")
        self.assertIn("urgent", self.task.tags)
    
    def test_remove_tag(self):
        """Test removing tags."""
        self.task.add_tag("urgent")
        self.task.remove_tag("urgent")
        self.assertNotIn("urgent", self.task.tags)
    
    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task_dict = self.task.to_dict()
        self.assertEqual(task_dict['title'], "Test Task")
        self.assertEqual(task_dict['priority'], 'HIGH')
        self.assertEqual(task_dict['status'], 'pending')


if __name__ == '__main__':
    unittest.main()
