from auth import get_service

def list_task_lists():
    """List all task lists."""
    service = get_service()
    all_items = []
    page_token = None
    while True:
        results = service.tasklists().list(
            maxResults=100,
            pageToken=page_token
        ).execute()
        all_items.extend(results.get("items", []))
        page_token = results.get("nextPageToken")
        if not page_token:
            break
    return all_items

def create_task_list(title: str):
    """Create a new task list."""
    service = get_service()
    tasklist = {"title": title}
    result = service.tasklists().insert(body=tasklist).execute()
    return result

def list_tasks(tasklist_id: str = "@default", show_completed: bool = False, show_hidden: bool = False):
    """List tasks in a specific task list, with subtasks nested under their parents."""
    service = get_service()
    all_items = []
    page_token = None
    while True:
        results = service.tasks().list(
            tasklist=tasklist_id,
            showCompleted=show_completed,
            showHidden=show_hidden,
            maxResults=100,
            pageToken=page_token
        ).execute()
        all_items.extend(results.get("items", []))
        page_token = results.get("nextPageToken")
        if not page_token:
            break

    # Build a lookup of tasks by ID
    tasks_by_id = {t["id"]: t for t in all_items}

    # Nest subtasks under their parent's "subtasks" key
    top_level = []
    for task in all_items:
        parent_id = task.get("parent")
        if parent_id and parent_id in tasks_by_id:
            parent = tasks_by_id[parent_id]
            parent.setdefault("subtasks", []).append(task)
        else:
            top_level.append(task)

    return top_level

def get_task(task_id: str, tasklist_id: str = "@default"):
    """Get a single task's full details."""
    service = get_service()
    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    return task

def get_subtasks(task_id: str, tasklist_id: str = "@default"):
    """Get all subtasks for a given parent task."""
    all_tasks = list_tasks(tasklist_id)
    return [t for t in all_tasks if t.get("parent") == task_id]

def create_task(title: str, notes: str = None, due: str = None, tasklist_id: str = "@default"):
    """Create a new task.
    
    Args:
        title: Task title
        notes: Task notes/description
        due: Due date in RFC 3339 timestamp format (e.g. 2023-10-01T00:00:00Z)
        tasklist_id: ID of the task list (default is "@default")
    """
    service = get_service()
    task = {"title": title}
    if notes:
        task["notes"] = notes
    if due:
        task["due"] = due
        
    result = service.tasks().insert(tasklist=tasklist_id, body=task).execute()
    return result

def complete_task(task_id: str, tasklist_id: str = "@default"):
    """Mark a task as completed."""
    service = get_service()
    # First get the task to keep other fields
    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    
    task["status"] = "completed"
    
    result = service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
    return result

def delete_task(task_id: str, tasklist_id: str = "@default"):
    """Delete a task."""
    service = get_service()
    service.tasks().delete(tasklist=tasklist_id, task=task_id).execute()
    return f"Task {task_id} deleted"

def update_task(task_id: str, title: str = None, notes: str = None, due: str = None, status: str = None, tasklist_id: str = "@default"):
    """Update an existing task."""
    service = get_service()
    task = service.tasks().get(tasklist=tasklist_id, task=task_id).execute()
    
    if title:
        task["title"] = title
    if notes:
        task["notes"] = notes
    if due:
        task["due"] = due
    if status:
        task["status"] = status # "needsAction" or "completed"
        
    result = service.tasks().update(tasklist=tasklist_id, task=task_id, body=task).execute()
    return result

def move_task(task_id: str, parent: str = None, previous: str = None, tasklist_id: str = "@default"):
    """Move a task to another position, either as a subtask (parent) or after another task (previous).
    
    Args:
        task_id: Task to move
        parent: The new parent task ID (for subtasks)
        previous: The task ID to move this task after
        tasklist_id: The task list ID
    """
    service = get_service()
    service.tasks().move(
        tasklist=tasklist_id, 
        task=task_id, 
        parent=parent, 
        previous=previous
    ).execute()
    return f"Task {task_id} moved"
