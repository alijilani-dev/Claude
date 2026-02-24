"""Task Manager API - FastAPI application."""

import os
import httpx
from fastapi import FastAPI, HTTPException, status
from uuid import uuid4

from task_manager.models import Task, TaskCreate, TaskUpdate, TaskList
from task_manager.store import tasks_store

# Progress Tracker service URL (configurable via environment variable)
PROGRESS_TRACKER_URL = os.getenv("PROGRESS_TRACKER_URL", "http://localhost:8001")

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="A minimalistic task management API with in-memory storage",
)


def log_progress(task_id: str, task_title: str, action: str, details: str | None = None) -> None:
    """Log a progress entry to the Progress Tracker service."""
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.post(
                f"{PROGRESS_TRACKER_URL}/progress",
                json={
                    "task_id": task_id,
                    "task_title": task_title,
                    "action": action,
                    "details": details,
                },
            )
            response.raise_for_status()
    except httpx.RequestError as e:
        # Log error but don't fail the main operation
        print(f"Warning: Failed to log progress to tracker: {e}")
    except httpx.HTTPStatusError as e:
        print(f"Warning: Progress tracker returned error: {e.response.status_code}")


@app.get("/")
def root() -> dict[str, str]:
    """Health check and API info."""
    return {"service": "Task Manager API", "status": "healthy", "docs": "/docs"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/tasks", response_model=TaskList)
def list_tasks() -> TaskList:
    """List all tasks."""
    tasks = [Task(**t) for t in tasks_store.get_all()]
    return TaskList(tasks=tasks, count=len(tasks))


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Task:
    """Create a new task."""
    task_id = str(uuid4())
    task_data = {"id": task_id, **task.model_dump()}
    tasks_store.create(task_data, task_id)

    # Log to Progress Tracker
    log_progress(
        task_id=task_id,
        task_title=task.title,
        action="created",
        details=f"Task created with description: {task.description or 'N/A'}",
    )

    return Task(**task_data)


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: str) -> Task:
    """Get a specific task by ID."""
    task_data = tasks_store.get(task_id)
    if task_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )
    return Task(**task_data)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, task: TaskUpdate) -> Task:
    """Update an existing task."""
    existing = tasks_store.get(task_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )

    update_data = task.model_dump(exclude_none=True)
    updated_task = {**existing, **update_data}
    tasks_store.update(task_id, updated_task)

    # Log to Progress Tracker
    changes = ", ".join(f"{k}={v}" for k, v in update_data.items())
    log_progress(
        task_id=task_id,
        task_title=updated_task["title"],
        action="updated",
        details=f"Fields updated: {changes}" if changes else "No changes",
    )

    return Task(**updated_task)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    """Delete a task."""
    existing = tasks_store.get(task_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )

    task_title = existing["title"]
    tasks_store.delete(task_id)

    # Log to Progress Tracker
    log_progress(
        task_id=task_id,
        task_title=task_title,
        action="deleted",
        details="Task permanently deleted",
    )
