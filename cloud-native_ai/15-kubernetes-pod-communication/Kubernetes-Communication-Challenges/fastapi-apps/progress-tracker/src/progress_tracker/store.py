"""In-memory data store for progress entries."""

from uuid import uuid4


class InMemoryStore[T]:
    """Generic in-memory store with CRUD operations."""

    def __init__(self) -> None:
        self._data: dict[str, T] = {}

    def get_all(self) -> list[T]:
        return list(self._data.values())

    def get(self, item_id: str) -> T | None:
        return self._data.get(item_id)

    def create(self, item: T, item_id: str | None = None) -> tuple[str, T]:
        new_id = item_id or str(uuid4())
        self._data[new_id] = item
        return new_id, item

    def delete(self, item_id: str) -> bool:
        if item_id not in self._data:
            return False
        del self._data[item_id]
        return True

    def clear(self) -> int:
        """Clear all entries and return count of deleted items."""
        count = len(self._data)
        self._data.clear()
        return count

    def filter_by_task(self, task_id: str) -> list[T]:
        """Filter entries by task ID."""
        return [item for item in self._data.values() if item.get("task_id") == task_id]


# Global store instance
progress_store: InMemoryStore[dict] = InMemoryStore()
