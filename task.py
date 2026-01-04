import sys
import json
import os
from datetime import datetime

FILE_NAME = 'tasks.json'

# ------------Utility Function--------------
def ensure_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'w') as f:
            json.dump([], f, indent=2)

def read_tasks():
    ensure_file()
    with open(FILE_NAME, 'r') as f:
        return json.load(f)
    
def write_tasks(tasks):
    with open(FILE_NAME, 'w') as f:
        json.dump(tasks, f, indent=2)

def generate_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1

def current_time():
    return datetime.now().isoformat(timespec="seconds")


# -----------------Cli logic ---------------------

def add_task(description):
    if not description:
        print("❌ Description is required.")
        return

    tasks = read_tasks()
    now = current_time()

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
    tasks = read_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            removed = tasks.pop(i)
            write_tasks(tasks)
            print(f"✅ Task deleted:", removed)
            return
    
    print(f"❌ Task with id {task_id} not found.")

def mark_task(task_id, status):
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
    tasks = read_tasks()
    
    if not tasks:
        print("📋 No tasks found.")
        return
    
    if status_filter:
        tasks = [task for task in tasks if task["status"] == status_filter]
        if not tasks:
            print(f"📋 No tasks with status '{status_filter}'.")
            return
    
    print("\n📋 Tasks:")
    print("-" * 80)
    for task in tasks:
        status_emoji = "✅" if task["status"] == "done" else "⏳" if task["status"] == "in-progress" else "📝"
        print(f"{status_emoji} [{task['id']}] {task['description']}")
        print(f"   Status: {task['status']} | Created: {task['createdAt']} | Updated: {task['updatedAt']}")
    print("-" * 80)

def main():
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
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status_filter)
    else:
        print("❌ Invalid command or missing arguments.")
        print("Usage: python task.py [add|update|delete|mark|list] [arguments]")

if __name__ == "__main__":
    main()
