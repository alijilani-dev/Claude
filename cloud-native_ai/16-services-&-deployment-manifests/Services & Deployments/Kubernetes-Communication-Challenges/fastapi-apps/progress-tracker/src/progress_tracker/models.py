"""Pydantic models for Progress Tracker API."""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """Type of action performed on a task."""
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


class ProgressEntryCreate(BaseModel):
    """Schema for creating a new progress entry."""
    task_id: str = Field(..., description="ID of the task that was modified")
    task_title: str = Field(..., description="Title of the task")
    action: ActionType = Field(..., description="Type of action performed")
    details: str | None = Field(None, description="Additional details about the action")


class ProgressEntry(BaseModel):
    """Full progress entry representation."""
    id: str
    task_id: str
    task_title: str
    action: ActionType
    details: str | None = None
    timestamp: datetime


class ProgressEntryList(BaseModel):
    """Response model for list of progress entries."""
    entries: list[ProgressEntry]
    count: int
