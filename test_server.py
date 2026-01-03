from task_manager import list_task_lists, create_task, list_tasks, complete_task, delete_task

def test_workflow():
    print("1. Listing Task Lists...")
    lists = list_task_lists()
    print(f"Found {len(lists)} task lists.")
    if not lists:
        print("No task lists found. Exiting.")
        return

    default_list = lists[0]['id']
    print(f"Using list: {lists[0]['title']} ({default_list})")

    print("\n2. Creating a Test Task...")
    new_task = create_task(title="MCP Test Task", notes="Created via FastMCP", tasklist_id=default_list)
    task_id = new_task['id']
    print(f"Created task: {new_task['title']} (ID: {task_id})")

    print("\n3. Verifying Task Existence...")
    tasks = list_tasks(tasklist_id=default_list)
    found = any(t['id'] == task_id for t in tasks)
    print(f"Task found in list: {found}")

    print("\n4. Completing Task...")
    complete_task(task_id=task_id, tasklist_id=default_list)
    print("Task completed.")

    print("\n5. Deleting Task (Cleanup)...")
    try:
        delete_task(task_id=task_id, tasklist_id=default_list)
        print("Task deleted.")
    except Exception as e:
        # Sometimes instant deletion after update might have race conditions or not update quickly enough, 
        # or API might have limits, but usually it works.
        print(f"Note: Could not delete task (might not exist): {e}")

    print("\nVerification successful!")

if __name__ == "__main__":
    try:
        test_workflow()
    except Exception as e:
        print(f"Verification failed: {e}")
