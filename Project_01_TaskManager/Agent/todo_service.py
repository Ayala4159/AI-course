from datetime import datetime

tasks = []
id_counter = 1

def add_task(title, description="", task_type="אישי", start_date=None, end_date=None):
    global id_counter
    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    
    new_task = {
        "id": id_counter,
        "title": title,
        "description": description,
        "type": task_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": "pending"
    }
    tasks.append(new_task)
    id_counter += 1
    return f"Success: Task '{title}' added with ID {new_task['id']}"

def get_tasks(date_filter=None, status=None):
    if not tasks:
        return "אין משימות במערכת."
    
    filtered = tasks
    if date_filter:
        filtered = [t for t in filtered if t['start_date'] == date_filter]
    if status:
        filtered = [t for t in filtered if t['status'] == status]
    
    return filtered if filtered else "לא נמצאו משימות מתאימות."

def update_task(task_id, **kwargs):
    for task in tasks:
        if task['id'] == int(task_id):
            for key, value in kwargs.items():
                if value is not None and key in task:
                    task[key] = value
            return f"משימה {task_id} עודכנה בהצלחה."
    return "משימה לא נמצאה."

def delete_task(task_id):
    global tasks
    initial_len = len(tasks)
    tasks = [t for t in tasks if t['id'] != int(task_id)]
    if len(tasks) < initial_len:
        return f"משימה {task_id} נמחקה."
    return "לא נמצאה משימה למחיקה."