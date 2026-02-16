from fastmcp import FastMCP
import task_manager

# Initialize FastMCP
mcp = FastMCP("google-tasks")

@mcp.tool()
def list_task_lists():
    """List all task lists."""
    return task_manager.list_task_lists()

@mcp.tool()
def create_task_list(title: str):
    """Create a new task list."""
    return task_manager.create_task_list(title)

@mcp.tool()
def list_tasks(tasklist_id: str = "@default", show_completed: bool = False, show_hidden: bool = False):
    """List tasks in a specific task list."""
    return task_manager.list_tasks(tasklist_id, show_completed, show_hidden)

@mcp.tool()
def get_task(task_id: str, tasklist_id: str = "@default"):
    """Get a single task's full details including title, notes, status, due date, and links."""
    return task_manager.get_task(task_id, tasklist_id)

@mcp.tool()
def get_subtasks(task_id: str, tasklist_id: str = "@default"):
    """Get all subtasks for a given parent task."""
    return task_manager.get_subtasks(task_id, tasklist_id)

@mcp.tool()
def create_task(title: str, notes: str = None, due: str = None, tasklist_id: str = "@default"):
    """Create a new task.
    
    Args:
        title: Task title
        notes: Task notes/description
        due: Due date in RFC 3339 timestamp format (e.g. 2023-10-01T00:00:00Z)
        tasklist_id: ID of the task list (default is "@default")
    """
    return task_manager.create_task(title, notes, due, tasklist_id)

@mcp.tool()
def complete_task(task_id: str, tasklist_id: str = "@default"):
    """Mark a task as completed."""
    return task_manager.complete_task(task_id, tasklist_id)

@mcp.tool()
def delete_task(task_id: str, tasklist_id: str = "@default"):
    """Delete a task."""
    return task_manager.delete_task(task_id, tasklist_id)

@mcp.tool()
def update_task(task_id: str, title: str = None, notes: str = None, due: str = None, status: str = None, tasklist_id: str = "@default"):
    """Update an existing task."""
    return task_manager.update_task(task_id, title, notes, due, status, tasklist_id)

@mcp.tool()
def move_task(task_id: str, parent: str = None, previous: str = None, tasklist_id: str = "@default"):
    """Move a task to another position, either as a subtask (parent) or after another task (previous).
    
    Args:
        task_id: Task to move
        parent: The new parent task ID (for subtasks)
        previous: The task ID to move this task after
        tasklist_id: The task list ID
    """
    return task_manager.move_task(task_id, parent, previous, tasklist_id)

if __name__ == "__main__":
    mcp.run()
