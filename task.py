import sys
import json
import os
from datetime import datetime

# File to persist tasks data
FILE_NAME = 'tasks.json'

# ============== UTILITY FUNCTIONS ==============
# These functions handle file operations and data management

def ensure_file():
    """Create tasks.json file if it doesn't exist with an empty task list."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as f:
            json.dump([], f, indent=2)

def read_tasks():
    """Read and return all tasks from the JSON file."""
    ensure_file()
    with open(FILE_NAME, 'r') as f:
        return json.load(f)
    
def write_tasks(tasks):
    """Write/save the tasks list to the JSON file."""
    with open(FILE_NAME, 'w') as f:
        json.dump(tasks, f, indent=2)

def generate_id(tasks):
    """Generate a unique ID for a new task (increments the max ID by 1)."""
    return max((task["id"] for task in tasks), default=0) + 1

def current_time():
    """Get the current timestamp in ISO 8601 format."""
    return datetime.now().isoformat(timespec="seconds")


# ============== CLI COMMAND FUNCTIONS ==============
# Each function handles a specific task operation

def add_task(description):
    """
    Create and add a new task to the list.
    
    Args:
        description (str): Task description
    """
    if not description:
        print("❌ Description is required.")
        return

    tasks = read_tasks()
    now = current_time()

    # Create a new task object with unique ID and metadata
    task = {
        "id": generate_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }

    tasks.append(task)
    write_tasks(tasks)
    print("✅ Task added:", task)

def update_task(task_id, description):
    """
    Update an existing task's description.
    
    Args:
        task_id (int): The ID of the task to update
        description (str): New task description
    """
    if not description:
        print("❌ Description is required.")
        return
    
    tasks = read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = description
            task["updatedAt"] = current_time()
            write_tasks(tasks)
            print("✅ Task updated:", task)
            return
    
    print(f"❌ Task with id {task_id} not found.")

def delete_task(task_id):
    """
    Delete a task by its ID.
    
    Args:
        task_id (int): The ID of the task to delete
    """
    tasks = read_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            removed = tasks.pop(i)
            write_tasks(tasks)
            print(f"✅ Task deleted:", removed)
            return
    
    print(f"❌ Task with id {task_id} not found.")

def mark_task(task_id, status):
    """
    Update a task's status (todo, in-progress, or done).
    
    Args:
        task_id (int): The ID of the task to update
        status (str): New status ('todo', 'in-progress', or 'done')
    """
    if status not in ["todo", "in-progress", "done"]:
        print("❌ Invalid status. Use 'todo', 'in-progress', or 'done'.")
        return
    
    tasks = read_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = current_time()
            write_tasks(tasks)
            print(f"✅ Task marked as {status}:", task)
            return
    
    print(f"❌ Task with id {task_id} not found.")

def list_tasks(status_filter=None):
    """
    Display all tasks or filter by status.
    
    Args:
        status_filter (str, optional): Filter tasks by status ('todo', 'in-progress', 'done')
    """
    tasks = read_tasks()
    
    if not tasks:
        print("📋 No tasks found.")
        return
    
    # Apply status filter if provided
    if status_filter:
        tasks = [task for task in tasks if task["status"] == status_filter]
        if not tasks:
            print(f"📋 No tasks with status '{status_filter}'.")
            return
    
    # Display tasks with formatting
    print("\n📋 Tasks:")
    print("-" * 80)
    for task in tasks:
        # Use emoji to represent task status visually
        status_emoji = "✅" if task["status"] == "done" else "⏳" if task["status"] == "in-progress" else "📝"
        print(f"{status_emoji} [{task['id']}] {task['description']}")
        print(f"   Status: {task['status']} | Created: {task['createdAt']} | Updated: {task['updatedAt']}")
    print("-" * 80)


def main():
    """
    Main entry point for the task tracker CLI.
    Parses command-line arguments and executes the appropriate command.
    """
    # Display help if no command is provided
    if len(sys.argv) < 2:
        print("Usage: python task.py [add|update|delete|mark|list] [arguments]")
        print("\nCommands:")
        print("  add <description>           - Add a new task")
        print("  update <id> <description>   - Update a task")
        print("  delete <id>                 - Delete a task")
        print("  mark <id> <status>          - Mark task as 'todo', 'in-progress', or 'done'")
        print("  list [status]               - List all tasks or filter by status")
        return
    
    command = sys.argv[1]
    
    # Route commands to appropriate functions
    if command == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif command == "update" and len(sys.argv) > 3:
        try:
            task_id = int(sys.argv[2])
            description = " ".join(sys.argv[3:])
            update_task(task_id, description)
        except ValueError:
            print("❌ Task id must be an integer.")
    elif command == "delete" and len(sys.argv) > 2:
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("❌ Task id must be an integer.")
    elif command == "mark" and len(sys.argv) > 3:
        try:
            task_id = int(sys.argv[2])
            status = sys.argv[3]
            mark_task(task_id, status)
        except ValueError:
            print("❌ Task id must be an integer.")
    elif command == "list":
        # Optional status filter for listing
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status_filter)
    else:
        print("❌ Invalid command or missing arguments.")
        print("Usage: python task.py [add|update|delete|mark|list] [arguments]")

# ============== ENTRY POINT ==============
# Run the main function when the script is executed directly
if __name__ == "__main__":
    main()
