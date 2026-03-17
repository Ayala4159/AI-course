"""Graphical User Interface for Task Manager using tkinter."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from src.task_manager import TaskManager
from src.task import TaskPriority, TaskStatus
from datetime import datetime


class TaskManagerGUI:
    """GUI Application for Task Manager."""
    
    def __init__(self, root):
        """Initialize the GUI.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.manager = TaskManager()
        
        self.setup_styles()
        self.create_menu()
        self.create_widgets()
        self.refresh_tasks()
    
    def setup_styles(self):
        """Setup tkinter styles."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#f0f0f0')
        style.configure('Header.TLabel', font=('Arial', 10, 'bold'), background='#f0f0f0')
        style.configure('TButton', font=('Arial', 10))
        style.configure('TLabel', font=('Arial', 10), background='#f0f0f0')
        style.configure('Treeview', rowheight=25, font=('Arial', 9))
        style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
    
    def create_menu(self):
        """Create menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save Tasks", command=self.save_tasks)
        file_menu.add_command(label="Load Tasks", command=self.load_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main GUI widgets."""
        # Title
        title_frame = ttk.Frame(self.root)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(title_frame, text="📋 Task Manager", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Add task
        left_panel = ttk.LabelFrame(main_frame, text="Add New Task")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        self.create_add_task_form(left_panel)
        
        # Right panel - Task list
        right_panel = ttk.LabelFrame(main_frame, text="Tasks")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_task_list(right_panel)
        
        # Bottom panel - Statistics
        bottom_frame = ttk.LabelFrame(self.root, text="Statistics")
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        self.stats_label = ttk.Label(bottom_frame, text="", justify=tk.LEFT)
        self.stats_label.pack(padx=10, pady=10)
    
    def create_add_task_form(self, parent):
        """Create form to add new task."""
        # Title
        ttk.Label(parent, text="Title:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.title_entry = ttk.Entry(parent, width=25)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Description
        ttk.Label(parent, text="Description:").grid(row=1, column=0, sticky=tk.NW, padx=10, pady=5)
        self.desc_text = tk.Text(parent, width=25, height=5, font=('Arial', 9))
        self.desc_text.grid(row=1, column=1, padx=10, pady=5)
        
        # Priority
        ttk.Label(parent, text="Priority:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.priority_var = tk.StringVar(value="MEDIUM")
        priority_combo = ttk.Combobox(parent, textvariable=self.priority_var, 
                                      values=["LOW", "MEDIUM", "HIGH", "CRITICAL"], 
                                      state="readonly", width=22)
        priority_combo.grid(row=2, column=1, padx=10, pady=5)
        
        # Due Date
        ttk.Label(parent, text="Due Date (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.due_date_entry = ttk.Entry(parent, width=25)
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Tag
        ttk.Label(parent, text="Tags (comma-separated):").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.tags_entry = ttk.Entry(parent, width=25)
        self.tags_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Add button
        ttk.Button(parent, text="➕ Add Task", command=self.add_task).grid(row=5, column=0, columnspan=2, 
                                                                             padx=10, pady=15, sticky=tk.EW)
        
        # Add some spacing
        for i in range(6, 10):
            ttk.Label(parent, text="").grid(row=i, column=0)
    
    def create_task_list(self, parent):
        """Create task list display."""
        # Filter buttons
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT)
        ttk.Button(filter_frame, text="All", command=lambda: self.filter_tasks("all")).pack(side=tk.LEFT, padx=2)
        ttk.Button(filter_frame, text="Pending", command=lambda: self.filter_tasks("pending")).pack(side=tk.LEFT, padx=2)
        ttk.Button(filter_frame, text="In Progress", command=lambda: self.filter_tasks("in_progress")).pack(side=tk.LEFT, padx=2)
        ttk.Button(filter_frame, text="Completed", command=lambda: self.filter_tasks("completed")).pack(side=tk.LEFT, padx=2)
        
        # Treeview
        columns = ("ID", "Title", "Priority", "Status", "Due Date")
        self.tree = ttk.Treeview(parent, columns=columns, height=15, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=30)
            elif col == "Title":
                self.tree.column(col, width=250)
            elif col == "Priority":
                self.tree.column(col, width=80)
            elif col == "Status":
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree.bind("<Double-1>", self.on_task_select)
        
        # Button frame
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="▶️ In Progress", command=self.mark_in_progress).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="✅ Complete", command=self.mark_completed).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🏷️ Add Tag", command=self.add_tag).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🗑️ Delete", command=self.delete_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🔄 Refresh", command=self.refresh_tasks).pack(side=tk.LEFT, padx=2)
    
    def add_task(self):
        """Add a new task."""
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        priority_str = self.priority_var.get()
        due_date = self.due_date_entry.get().strip() or None
        tags_str = self.tags_entry.get().strip()
        
        # Validation
        if not title:
            messagebox.showerror("Error", "Please enter a task title")
            return
        
        if not description:
            messagebox.showerror("Error", "Please enter a description")
            return
        
        try:
            priority = TaskPriority[priority_str]
            
            task = self.manager.add_task(title, description, priority, due_date)
            
            # Add tags
            if tags_str:
                for tag in tags_str.split(","):
                    task.add_tag(tag.strip())
            
            messagebox.showinfo("Success", f"✅ Task '{title}' added successfully!")
            
            # Clear form
            self.title_entry.delete(0, tk.END)
            self.desc_text.delete("1.0", tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.tags_entry.delete(0, tk.END)
            
            self.refresh_tasks()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add task: {str(e)}")
    
    def on_task_select(self, event):
        """Handle task selection to show details."""
        selection = self.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        task_id = int(values[0])
        
        task = self.manager.get_task(task_id)
        if task:
            details = f"""
Task ID: {task.task_id}
Title: {task.title}
Description: {task.description}
Priority: {task.priority.name}
Status: {task.status.value}
Due Date: {task.due_date or 'Not set'}
Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}
Tags: {', '.join(task.tags) if task.tags else 'None'}
            """
            messagebox.showinfo("Task Details", details)
    
    def mark_in_progress(self):
        """Mark selected task as in progress."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task")
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        task_id = int(values[0])
        
        task = self.manager.get_task(task_id)
        if task:
            task.mark_in_progress()
            messagebox.showinfo("Success", f"✅ Task marked as in progress")
            self.refresh_tasks()
    
    def mark_completed(self):
        """Mark selected task as completed."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task")
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        task_id = int(values[0])
        
        task = self.manager.get_task(task_id)
        if task:
            task.mark_completed()
            messagebox.showinfo("Success", f"✅ Task completed!")
            self.refresh_tasks()
    
    def add_tag(self):
        """Add tag to selected task."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task")
            return
        
        item = selection[0]
        values = self.tree.item(item, 'values')
        task_id = int(values[0])
        
        task = self.manager.get_task(task_id)
        if task:
            tag = simpledialog.askstring("Add Tag", "Enter tag name:")
            if tag:
                task.add_tag(tag.strip())
                messagebox.showinfo("Success", f"✅ Tag '{tag}' added!")
                self.refresh_tasks()
    
    def delete_task(self):
        """Delete selected task."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a task")
            return
        
        if messagebox.askyesno("Confirm", "Delete this task?"):
            item = selection[0]
            values = self.tree.item(item, 'values')
            task_id = int(values[0])
            
            self.manager.delete_task(task_id)
            messagebox.showinfo("Success", "✅ Task deleted!")
            self.refresh_tasks()
    
    def filter_tasks(self, filter_type):
        """Filter tasks by status."""
        self.current_filter = filter_type
        self.refresh_tasks()
    
    def refresh_tasks(self):
        """Refresh task list display."""
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get tasks based on filter
        filter_type = getattr(self, 'current_filter', 'all')
        
        if filter_type == "pending":
            tasks = self.manager.get_tasks_by_status(TaskStatus.PENDING)
        elif filter_type == "in_progress":
            tasks = self.manager.get_tasks_by_status(TaskStatus.IN_PROGRESS)
        elif filter_type == "completed":
            tasks = self.manager.get_tasks_by_status(TaskStatus.COMPLETED)
        else:
            tasks = self.manager.get_all_tasks()
        
        # Add tasks to tree
        for task in tasks:
            self.tree.insert("", "end", values=(
                task.task_id,
                task.title,
                task.priority.name,
                task.status.value,
                task.due_date or "-"
            ))
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        """Update statistics display."""
        stats = self.manager.get_statistics()
        
        stats_text = f"""
Total Tasks: {stats['total_tasks']} | Pending: {stats['pending']} | In Progress: {stats['in_progress']} | 
Completed: {stats['completed']} | Cancelled: {stats['cancelled']} | High Priority: {stats['high_priority_pending']}
        """
        
        self.stats_label.config(text=stats_text.strip())
    
    def save_tasks(self):
        """Save tasks to file."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.manager.save_to_file(filename)
                messagebox.showinfo("Success", f"✅ Tasks saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save: {str(e)}")
    
    def load_tasks(self):
        """Load tasks from file."""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.manager.load_from_file(filename)
                messagebox.showinfo("Success", f"✅ Tasks loaded from {filename}")
                self.refresh_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {str(e)}")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """Task Manager v1.0

A simple and efficient task management application.

Features:
• Create, update, and delete tasks
• Organize with priorities and tags
• Track task status
• Save/load tasks from JSON files
• View statistics

© 2026 Task Management Project
        """
        messagebox.showinfo("About Task Manager", about_text)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
