"""Pydantic models for Task Manager API using Python 3.13+ typing."""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    completed: bool = False


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    completed: bool | None = None


class Task(BaseModel):
    """Full task representation."""
    id: str
    title: str
    description: str | None = None
    completed: bool = False


class TaskList(BaseModel):
    """Response model for list of tasks."""
    tasks: list[Task]
    count: int
