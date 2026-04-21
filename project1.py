#!/usr/bin/env python3
"""
CLI To-Do List with File Storage
A command-line todo app that saves tasks to a JSON file.
Add, delete, mark done, list tasks.
"""

import argparse
import json
import os
from datetime import datetime
from typing import List, Dict

TODO_FILE = "todos.json"

def load_todos() -> List[Dict]:
    """Load todos from JSON file."""
    if not os.path.exists(TODO_FILE):
        return []
    
    try:
        with open(TODO_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos: List[Dict]) -> None:
    """Save todos to JSON file."""
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

def add_task(task: str) -> None:
    """Add a new task."""
    todos = load_todos()
    new_task = {
        'id': len(todos) + 1,
        'task': task,
        'created': datetime.now().isoformat(),
        'completed': False
    }
    todos.append(new_task)
    save_todos(todos)
    print(f"Added: {task}")

def list_tasks(show_all: bool = False) -> None:
    """List all tasks or only pending tasks."""
    todos = load_todos()
    
    if not todos:
        print("No tasks found.")
        return
    
    filtered_todos = todos if show_all else [t for t in todos if not t['completed']]
    
    if not filtered_todos:
        print("No pending tasks.")
        return
    
    print("\nTasks:")
    print("-" * 50)
    for todo in filtered_todos:
        status = "DONE" if todo['completed'] else "TODO"
        created = todo['created'][:10]  # Just the date
        print(f"[{todo['id']}] [{status}] {todo['task']} (Created: {created})")

def mark_done(task_id: int) -> None:
    """Mark a task as completed."""
    todos = load_todos()
    
    for todo in todos:
        if todo['id'] == task_id:
            todo['completed'] = True
            todo['completed_date'] = datetime.now().isoformat()
            save_todos(todos)
            print(f"Marked as done: {todo['task']}")
            return
    
    print(f"Task with ID {task_id} not found.")

def delete_task(task_id: int) -> None:
    """Delete a task."""
    todos = load_todos()
    
    for i, todo in enumerate(todos):
        if todo['id'] == task_id:
            deleted_task = todos.pop(i)
            save_todos(todos)
            print(f"Deleted: {deleted_task['task']}")
            return
    
    print(f"Task with ID {task_id} not found.")

def clear_completed() -> None:
    """Remove all completed tasks."""
    todos = load_todos()
    original_count = len(todos)
    todos = [t for t in todos if not t['completed']]
    
    if len(todos) == original_count:
        print("No completed tasks to clear.")
        return
    
    save_todos(todos)
    cleared_count = original_count - len(todos)
    print(f"Cleared {cleared_count} completed task(s).")

def main():
    parser = argparse.ArgumentParser(description="CLI To-Do List Manager")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('task', help='Task description')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--all', action='store_true', help='Show all tasks including completed')
    
    # Done command
    done_parser = subparsers.add_parser('done', help='Mark task as completed')
    done_parser.add_argument('id', type=int, help='Task ID to mark as done')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID to delete')
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear completed tasks')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_task(args.task)
    elif args.command == 'list':
        list_tasks(args.all)
    elif args.command == 'done':
        mark_done(args.id)
    elif args.command == 'delete':
        delete_task(args.id)
    elif args.command == 'clear':
        clear_completed()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
