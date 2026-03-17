"""Simple web server for Task Manager using built-in Python modules."""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from src.task_manager import TaskManager
from src.task import TaskPriority, TaskStatus
from datetime import datetime

# Global task manager instance
task_manager = TaskManager()

# HTML template
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📋 Task Manager</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}

        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .header h1 {{
            color: #2d3748;
            font-size: 2.5rem;
            font-weight: 700;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}

        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #667eea;
        }}

        .stat-label {{
            color: #718096;
            margin-top: 8px;
        }}

        .card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 24px;
            padding: 24px;
        }}

        .card h2 {{
            color: #2d3748;
            margin-bottom: 20px;
        }}

        form {{
            display: grid;
            gap: 15px;
        }}

        input, textarea, select {{
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            font-family: inherit;
        }}

        input:focus, textarea:focus, select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        button {{
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
        }}

        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }}

        .task-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border-left: 4px solid #667eea;
        }}

        .task-card h3 {{
            color: #2d3748;
            margin-bottom: 8px;
        }}

        .task-actions {{
            display: flex;
            gap: 8px;
            margin-top: 12px;
            flex-wrap: wrap;
        }}

        .task-actions button {{
            padding: 8px 16px;
            font-size: 0.9rem;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 8px;
        }}

        .badge-pending {{ background: #e2e8f0; color: #4a5568; }}
        .badge-in-progress {{ background: #bee3f8; color: #2a4365; }}
        .badge-completed {{ background: #c6f6d5; color: #22543d; }}

        .priority-low {{ background: #c6f6d5; color: #22543d; }}
        .priority-medium {{ background: #fef5e7; color: #744210; }}
        .priority-high {{ background: #fed7d7; color: #742a2a; }}
        .priority-critical {{ background: #feb2b2; color: #9b2c2c; }}

        .error {{
            background: #fed7d7;
            color: #742a2a;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 16px;
        }}

        .success {{
            background: #c6f6d5;
            color: #22543d;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 16px;
        }}

        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.75rem; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1><i class="fas fa-tasks"></i> Task Manager</h1>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_tasks}</div>
                <div class="stat-label">Total Tasks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{pending}</div>
                <div class="stat-label">Pending</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{in_progress}</div>
                <div class="stat-label">In Progress</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{completed}</div>
                <div class="stat-label">Completed</div>
            </div>
        </div>

        {message}

        <div class="card">
            <h2><i class="fas fa-plus-circle"></i> Add New Task</h2>
            <form method="POST" action="/add_task">
                <input type="text" name="title" placeholder="Task Title" required>
                <textarea name="description" placeholder="Task Description" required></textarea>
                <select name="priority">
                    <option value="LOW">🟢 Low</option>
                    <option value="MEDIUM" selected>🟡 Medium</option>
                    <option value="HIGH">🔴 High</option>
                    <option value="CRITICAL">🚨 Critical</option>
                </select>
                <input type="date" name="due_date" placeholder="Due Date">
                <input type="text" name="tags" placeholder="Tags (comma-separated)">
                <button type="submit"><i class="fas fa-plus"></i> Add Task</button>
            </form>
        </div>

        <div class="card">
            <h2><i class="fas fa-list"></i> Tasks</h2>
            {tasks_html}
        </div>
    </div>

    <script>
        function deleteTask(taskId) {{
            if (confirm('Delete this task?')) {{
                document.location = '/delete_task/' + taskId;
            }}
        }}

        function updateStatus(taskId, newStatus) {{
            document.location = '/update_status/' + taskId + '?status=' + newStatus;
        }}
    </script>
</body>
</html>"""


class TaskManagerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the task manager."""

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == '/' or path == '/index.html':
            self.serve_index()
        elif path.startswith('/delete_task/'):
            task_id = int(path.split('/')[-1])
            task_manager.delete_task(task_id)
            self.redirect('/')
        elif path.startswith('/update_status/'):
            task_id = int(path.split('/')[-1])
            status = query_params.get('status', ['IN_PROGRESS'])[0]
            try:
                task_manager.update_task_status(task_id, TaskStatus[status])
            except:
                pass
            self.redirect('/')
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            params = parse_qs(post_data.decode('utf-8'))
            
            if path == '/add_task':
                title = params.get('title', [''])[0].strip()
                description = params.get('description', [''])[0].strip()
                priority_str = params.get('priority', ['MEDIUM'])[0]
                due_date = params.get('due_date', [''])[0].strip() or None
                tags_str = params.get('tags', [''])[0].strip()

                if title and description:
                    priority = TaskPriority[priority_str]
                    task = task_manager.add_task(title, description, priority, due_date)
                    
                    if tags_str:
                        for tag in tags_str.split(','):
                            tag = tag.strip()
                            if tag:
                                task.add_tag(tag)

            self.redirect('/')
        except Exception as e:
            self.send_error(500, str(e))

    def serve_index(self):
        """Serve the main index page."""
        try:
            stats = task_manager.get_statistics()
            tasks = task_manager.get_all_tasks()

            # Generate tasks HTML
            tasks_html = ""
            if tasks:
                for task in tasks:
                    priority_class = f"priority-{task.priority.name.lower()}"
                    status_class = f"badge-{task.status.value.lower().replace('_', '-')}"
                    
                    tasks_html += f"""
                    <div class="task-card">
                        <h3>{task.title}</h3>
                        <p>{task.description}</p>
                        <div>
                            <span class="badge {priority_class}">{task.priority.name}</span>
                            <span class="badge {status_class}">{task.status.value.replace('_', ' ')}</span>
                            {'<span style="color: #718096; font-size: 0.9rem;">📅 ' + task.due_date + '</span>' if task.due_date else ''}
                        </div>
                        {'<div>' + ', '.join([f'<span class="badge" style="background: #667eea; color: white;">{tag}</span>' for tag in task.tags]) + '</div>' if task.tags else ''}
                        <div class="task-actions">
                            {'<button onclick="updateStatus(' + str(task.task_id) + ', \'IN_PROGRESS\')"><i class="fas fa-play"></i> Start</button>' if task.status.value == 'pending' else ''}
                            {'<button onclick="updateStatus(' + str(task.task_id) + ', \'COMPLETED\')"><i class="fas fa-check"></i> Complete</button>' if task.status.value == 'in_progress' else ''}
                            <button style="background: #f5576c;" onclick="deleteTask({task.task_id})"><i class="fas fa-trash"></i> Delete</button>
                        </div>
                    </div>
                    """
            else:
                tasks_html = '<p style="text-align: center; color: #718096;">No tasks yet. Create one to get started!</p>'

            html = TEMPLATE.format(
                total_tasks=stats.get('total_tasks', 0),
                pending=stats.get('pending', 0),
                in_progress=stats.get('in_progress', 0),
                completed=stats.get('completed', 0),
                tasks_html=tasks_html,
                message=""
            )

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))

    def redirect(self, location):
        """Redirect to another page."""
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_server(port=5000):
    """Run the web server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, TaskManagerHandler)
    print(f"✅ Task Manager running at http://localhost:{port}")
    print(f"Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✋ Server stopped")
        httpd.server_close()


if __name__ == '__main__':
    run_server(5000)
