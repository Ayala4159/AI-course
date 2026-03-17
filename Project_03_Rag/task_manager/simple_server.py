import http.server
import socketserver
import json
import os
import sys
from urllib.parse import parse_qs

# הגדרת נתיבים
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.task_manager import TaskManager
from src.task import TaskPriority, TaskStatus

PORT = 8000
manager = TaskManager()

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/tasks':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            tasks = [t.to_dict() for t in manager.get_all_tasks()]
            self.wfile.write(json.dumps(tasks).encode())
            
        elif self.path.startswith('/update_status/'):
            try:
                parts = self.path.split('/')
                task_id = int(parts[2])
                status_name = parts[3].upper()
                manager.update_task_status(task_id, TaskStatus[status_name])
            except: pass
            self.send_response(303); self.send_header('Location', '/'); self.end_headers()

        elif self.path.startswith('/delete_task/'):
            try:
                task_id = int(self.path.split('/')[-1])
                manager.delete_task(task_id)
            except: pass
            self.send_response(303); self.send_header('Location', '/'); self.end_headers()
            
        else:
            if self.path == '/': self.path = '/templates/index.html'
            return super().do_GET()

    def do_POST(self):
        if self.path == '/add_task':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            # וידוא שמות השדות
            title = params.get('title', [''])[0]
            desc = params.get('description', [''])[0]
            prio = params.get('priority', ['MEDIUM'])[0]
            
            if title:
                manager.add_task(title=title, description=desc, priority=TaskPriority[prio])
            
            self.send_response(303); self.send_header('Location', '/'); self.end_headers()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server started at http://localhost:{PORT}")
    httpd.serve_forever()