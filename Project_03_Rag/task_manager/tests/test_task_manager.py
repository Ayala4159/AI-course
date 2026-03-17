"""Unit tests for the TaskManager class."""

import unittest
import os
import json
from src.task_manager import TaskManager
from src.task import TaskPriority, TaskStatus


class TestTaskManager(unittest.TestCase):
    """Test cases for TaskManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = TaskManager()
    
    def test_add_task(self):
        """Test adding a task."""
        task = self.manager.add_task(
            "New Task",
            "Task description",
            priority=TaskPriority.MEDIUM
        )
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "New Task")
    
    def test_get_task(self):
        """Test retrieving a task."""
        task = self.manager.add_task("Task", "Description")
        retrieved = self.manager.get_task(task.task_id)
        self.assertEqual(retrieved.title, "Task")
    
    def test_delete_task(self):
        """Test deleting a task."""
        task = self.manager.add_task("Task", "Description")
        result = self.manager.delete_task(task.task_id)
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_task(task.task_id))
    
    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        self.manager.add_task("Task 1", "Description 1")
        self.manager.add_task("Task 2", "Description 2")
        tasks = self.manager.get_all_tasks()
        self.assertEqual(len(tasks), 2)
    
    def test_get_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        self.manager.add_task("High Priority", "Desc", priority=TaskPriority.HIGH)
        self.manager.add_task("Low Priority", "Desc", priority=TaskPriority.LOW)
        
        high_priority = self.manager.get_tasks_by_priority(TaskPriority.HIGH)
        self.assertEqual(len(high_priority), 1)
        self.assertEqual(high_priority[0].title, "High Priority")
    
    def test_get_pending_tasks(self):
        """Test retrieving pending tasks."""
        self.manager.add_task("Task 1", "Desc", priority=TaskPriority.LOW)
        task2 = self.manager.add_task("Task 2", "Desc", priority=TaskPriority.HIGH)
        task2.mark_completed()
        
        pending = self.manager.get_pending_tasks()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].title, "Task 1")
    
    def test_get_high_priority_tasks(self):
        """Test retrieving high priority tasks."""
        self.manager.add_task("Critical Task", "Desc", priority=TaskPriority.CRITICAL)
        high = self.manager.get_high_priority_tasks()
        self.assertEqual(len(high), 1)
    
    def test_get_statistics(self):
        """Test getting task statistics."""
        self.manager.add_task("Task 1", "Desc")
        task2 = self.manager.add_task("Task 2", "Desc")
        task2.mark_completed()
        
        stats = self.manager.get_statistics()
        self.assertEqual(stats['total_tasks'], 2)
        self.assertEqual(stats['pending'], 1)
        self.assertEqual(stats['completed'], 1)


if __name__ == '__main__':
    unittest.main()
