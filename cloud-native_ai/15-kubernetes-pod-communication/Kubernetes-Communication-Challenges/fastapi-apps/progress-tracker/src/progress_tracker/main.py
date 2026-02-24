"""Progress Tracker API - FastAPI application."""

from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, status
from uuid import uuid4

from progress_tracker.models import ProgressEntry, ProgressEntryCreate, ProgressEntryList
from progress_tracker.store import progress_store

app = FastAPI(
    title="Progress Tracker API",
    version="1.0.0",
    description="API for tracking task mutations (create, update, delete) from the Task Manager",
)


@app.get("/")
def root() -> dict[str, str]:
    """Health check and API info."""
    return {"service": "Progress Tracker API", "status": "healthy", "docs": "/docs"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/progress", response_model=ProgressEntryList)
def list_progress_entries() -> ProgressEntryList:
    """List all progress entries."""
    entries = [ProgressEntry(**e) for e in progress_store.get_all()]
    # Sort by timestamp descending (most recent first)
    entries.sort(key=lambda x: x.timestamp, reverse=True)
    return ProgressEntryList(entries=entries, count=len(entries))


@app.post("/progress", response_model=ProgressEntry, status_code=status.HTTP_201_CREATED)
def create_progress_entry(entry: ProgressEntryCreate) -> ProgressEntry:
    """Create a new progress entry (called by Task Manager on mutations)."""
    entry_id = str(uuid4())
    entry_data = {
        "id": entry_id,
        **entry.model_dump(),
        "timestamp": datetime.now(timezone.utc),
    }
    progress_store.create(entry_data, entry_id)
    return ProgressEntry(**entry_data)


@app.get("/progress/{entry_id}", response_model=ProgressEntry)
def get_progress_entry(entry_id: str) -> ProgressEntry:
    """Get a specific progress entry by ID."""
    entry_data = progress_store.get(entry_id)
    if entry_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Progress entry with id '{entry_id}' not found",
        )
    return ProgressEntry(**entry_data)


@app.get("/progress/task/{task_id}", response_model=ProgressEntryList)
def get_progress_by_task(task_id: str) -> ProgressEntryList:
    """Get all progress entries for a specific task."""
    entries = [ProgressEntry(**e) for e in progress_store.filter_by_task(task_id)]
    entries.sort(key=lambda x: x.timestamp, reverse=True)
    return ProgressEntryList(entries=entries, count=len(entries))


@app.delete("/progress/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_progress_entry(entry_id: str) -> None:
    """Delete a progress entry."""
    if not progress_store.delete(entry_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Progress entry with id '{entry_id}' not found",
        )


@app.delete("/progress", status_code=status.HTTP_200_OK)
def clear_all_progress() -> dict[str, int]:
    """Clear all progress entries."""
    count = progress_store.clear()
    return {"deleted_count": count}
