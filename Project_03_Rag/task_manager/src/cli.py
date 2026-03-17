"""Command-line interface for the task management system."""

from src import TaskManager, TaskPriority, TaskStatus
from typing import Optional
import sys


class TaskManagerCLI:
    """Command-line interface for task management."""
    
    def __init__(self, manager: Optional[TaskManager] = None):
        """Initialize CLI with a task manager instance.
        
        Args:
            manager: TaskManager instance (creates new if not provided)
        """
        self.manager = manager or TaskManager()
        self.running = True
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*50)
        print("TASK MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add new task")
        print("2. List all tasks")
        print("3. List pending tasks")
        print("4. List high priority tasks")
        print("5. View task details")
        print("6. Mark task as in progress")
        print("7. Mark task as completed")
        print("8. Delete task")
        print("9. View statistics")
        print("10. Add tag to task")
        print("11. Save tasks to file")
        print("12. Load tasks from file")
        print("13. Exit")
        print("="*50)
    
    def add_task(self) -> None:
        """Add a new task through user input."""
        title = input("Enter task title: ").strip()
        if not title:
            print("❌ Title cannot be empty")
            return
        
        description = input("Enter task description: ").strip()
        if not description:
            print("❌ Description cannot be empty")
            return
        
        # Priority selection
        print("\nSelect priority:")
        print("1. LOW")
        print("2. MEDIUM (default)")
        print("3. HIGH")
        print("4. CRITICAL")
        
        priority_map = {
            "1": TaskPriority.LOW,
            "2": TaskPriority.MEDIUM,
            "3": TaskPriority.HIGH,
            "4": TaskPriority.CRITICAL,
        }
        priority_input = input("Choice (1-4): ").strip() or "2"
        priority = priority_map.get(priority_input, TaskPriority.MEDIUM)
        
        due_date = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip() or None
        
        task = self.manager.add_task(title, description, priority, due_date)
        print(f"\n✅ Task created with ID: {task.task_id}")
    
    def list_all_tasks(self) -> None:
        """Display all tasks."""
        tasks = self.manager.get_all_tasks()
        if not tasks:
            print("\n✓ No tasks found")
            return
        
        print("\n" + "-"*70)
        print(f"{'ID':<4} {'Title':<25} {'Priority':<10} {'Status':<15}")
        print("-"*70)
        for task in tasks:
            status_indicator = self._get_status_indicator(task.status)
            print(f"{task.task_id:<4} {task.title:<25} {task.priority.name:<10} {status_indicator}")
        print("-"*70)
    
    def list_pending_tasks(self) -> None:
        """Display pending tasks sorted by priority."""
        tasks = self.manager.get_pending_tasks()
        if not tasks:
            print("\n✓ No pending tasks")
            return
        
        print("\n📋 PENDING TASKS (sorted by priority):")
        print("-"*70)
        for idx, task in enumerate(tasks, 1):
            priority_emoji = self._get_priority_emoji(task.priority)
            print(f"{idx}. {priority_emoji} [{task.task_id}] {task.title}")
            if task.due_date:
                print(f"   Due: {task.due_date}")
            print()
    
    def list_high_priority_tasks(self) -> None:
        """Display high priority and critical tasks."""
        tasks = self.manager.get_high_priority_tasks()
        if not tasks:
            print("\n✓ No high priority tasks")
            return
        
        print("\n🔴 HIGH PRIORITY/CRITICAL TASKS:")
        print("-"*70)
        for task in tasks:
            emoji = "🚨" if task.priority == TaskPriority.CRITICAL else "⚠️ "
            print(f"{emoji} [{task.task_id}] {task.title}")
            print(f"   Status: {task.status.value}")
    
    def view_task_details(self) -> None:
        """Display detailed information about a specific task."""
        try:
            task_id = int(input("\nEnter task ID: ").strip())
        except ValueError:
            print("❌ Invalid task ID")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print(f"❌ Task {task_id} not found")
            return
        
        print("\n" + "="*50)
        print(f"TASK #{task.task_id}")
        print("="*50)
        print(f"Title:       {task.title}")
        print(f"Description: {task.description}")
        print(f"Priority:    {task.priority.name}")
        print(f"Status:      {task.status.value}")
        print(f"Due Date:    {task.due_date or 'Not set'}")
        print(f"Created:     {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        if task.completed_at:
            print(f"Completed:   {task.completed_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Tags:        {', '.join(task.tags) if task.tags else 'None'}")
        print("="*50)
    
    def mark_in_progress(self) -> None:
        """Mark a task as in progress."""
        try:
            task_id = int(input("\nEnter task ID: ").strip())
        except ValueError:
            print("❌ Invalid task ID")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print(f"❌ Task {task_id} not found")
            return
        
        task.mark_in_progress()
        print(f"✅ Task {task_id} marked as in progress")
    
    def mark_completed(self) -> None:
        """Mark a task as completed."""
        try:
            task_id = int(input("\nEnter task ID: ").strip())
        except ValueError:
            print("❌ Invalid task ID")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print(f"❌ Task {task_id} not found")
            return
        
        task.mark_completed()
        print(f"✅ Task {task_id} completed!")
    
    def delete_task(self) -> None:
        """Delete a task."""
        try:
            task_id = int(input("\nEnter task ID to delete: ").strip())
        except ValueError:
            print("❌ Invalid task ID")
            return
        
        confirmation = input(f"Are you sure you want to delete task {task_id}? (y/n): ").lower()
        if confirmation != 'y':
            print("❌ Deletion cancelled")
            return
        
        if self.manager.delete_task(task_id):
            print(f"✅ Task {task_id} deleted")
        else:
            print(f"❌ Task {task_id} not found")
    
    def view_statistics(self) -> None:
        """Display task statistics."""
        stats = self.manager.get_statistics()
        
        print("\n" + "="*50)
        print("TASK STATISTICS")
        print("="*50)
        print(f"Total Tasks:              {stats['total_tasks']}")
        print(f"  Pending:                {stats['pending']}")
        print(f"  In Progress:            {stats['in_progress']}")
        print(f"  Completed:              {stats['completed']}")
        print(f"  Cancelled:              {stats['cancelled']}")
        print(f"  On Hold:                {stats['on_hold']}")
        print(f"\nHigh Priority Pending:    {stats['high_priority_pending']}")
        
        if stats['total_tasks'] > 0:
            completion_rate = (stats['completed'] / stats['total_tasks']) * 100
            print(f"Completion Rate:          {completion_rate:.1f}%")
        print("="*50)
    
    def add_tag(self) -> None:
        """Add a tag to a task."""
        try:
            task_id = int(input("\nEnter task ID: ").strip())
        except ValueError:
            print("❌ Invalid task ID")
            return
        
        task = self.manager.get_task(task_id)
        if not task:
            print(f"❌ Task {task_id} not found")
            return
        
        tag = input("Enter tag name: ").strip().lower()
        if not tag:
            print("❌ Tag cannot be empty")
            return
        
        task.add_tag(tag)
        print(f"✅ Tag '{tag}' added to task {task_id}")
    
    def save_tasks(self) -> None:
        """Save tasks to file."""
        filename = input("Enter filename (default: tasks.json): ").strip() or "tasks.json"
        try:
            self.manager.save_to_file(filename)
            print(f"✅ Tasks saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving tasks: {e}")
    
    def load_tasks(self) -> None:
        """Load tasks from file."""
        filename = input("Enter filename (default: tasks.json): ").strip() or "tasks.json"
        try:
            self.manager.load_from_file(filename)
            print(f"✅ Tasks loaded from {filename}")
        except FileNotFoundError:
            print(f"❌ File {filename} not found")
        except Exception as e:
            print(f"❌ Error loading tasks: {e}")
    
    def run(self) -> None:
        """Run the main CLI loop."""
        print("\n🎯 Welcome to Task Manager!")
        
        while self.running:
            self.display_menu()
            choice = input("Enter your choice (1-13): ").strip()
            
            actions = {
                "1": self.add_task,
                "2": self.list_all_tasks,
                "3": self.list_pending_tasks,
                "4": self.list_high_priority_tasks,
                "5": self.view_task_details,
                "6": self.mark_in_progress,
                "7": self.mark_completed,
                "8": self.delete_task,
                "9": self.view_statistics,
                "10": self.add_tag,
                "11": self.save_tasks,
                "12": self.load_tasks,
                "13": self.exit_cli,
            }
            
            action = actions.get(choice)
            if action:
                action()
            else:
                print("❌ Invalid choice. Please try again.")
    
    def exit_cli(self) -> None:
        """Exit the CLI."""
        print("\n👋 Thank you for using Task Manager!")
        self.running = False
    
    @staticmethod
    def _get_status_indicator(status: TaskStatus) -> str:
        """Get a visual indicator for task status."""
        indicators = {
            TaskStatus.PENDING: "⏳ pending",
            TaskStatus.IN_PROGRESS: "🔄 in_progress",
            TaskStatus.COMPLETED: "✅ completed",
            TaskStatus.CANCELLED: "❌ cancelled",
            TaskStatus.ON_HOLD: "⏸️ on_hold",
        }
        return indicators.get(status, status.value)
    
    @staticmethod
    def _get_priority_emoji(priority: TaskPriority) -> str:
        """Get an emoji for priority level."""
        emojis = {
            TaskPriority.LOW: "🟢",
            TaskPriority.MEDIUM: "🟡",
            TaskPriority.HIGH: "🔴",
            TaskPriority.CRITICAL: "🚨",
        }
        return emojis.get(priority, "")


def main():
    """Main entry point."""
    cli = TaskManagerCLI()
    cli.run()


if __name__ == "__main__":
    main()
