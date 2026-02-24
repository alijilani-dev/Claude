"""In-memory data store for tasks."""

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

    def update(self, item_id: str, item: T) -> T | None:
        if item_id not in self._data:
            return None
        self._data[item_id] = item
        return item

    def delete(self, item_id: str) -> bool:
        if item_id not in self._data:
            return False
        del self._data[item_id]
        return True

    def exists(self, item_id: str) -> bool:
        return item_id in self._data


# Global store instance
tasks_store: InMemoryStore[dict] = InMemoryStore()
