# Project Plan: Two FastAPI Web Applications

## Overview

This plan outlines the development of two separate FastAPI applications:
1. **Task Manager API** - A simple task/todo management service (Port 8000)
2. **User Directory API** - A user management service (Port 8001)

Both applications will use in-memory storage (Python dictionaries), Python 3.13+ with modern typing, and be managed with `uv`.

---

## Folder Structure

```
fastapi-apps/
├── task-manager/
│   ├── pyproject.toml
│   ├── .python-version          # Contains: 3.13
│   └── src/
│       └── task_manager/
│           ├── __init__.py
│           ├── main.py          # FastAPI app entry point
│           ├── models.py        # Pydantic models with modern typing
│           └── store.py         # In-memory data store
│
└── user-directory/
    ├── pyproject.toml
    ├── .python-version          # Contains: 3.13
    └── src/
        └── user_directory/
            ├── __init__.py
            ├── main.py          # FastAPI app entry point
            ├── models.py        # Pydantic models with modern typing
            └── store.py         # In-memory data store
```

---

## Operations Plan

### Task Manager API - Ops Breakdown

| Operation | File | Description |
|-----------|------|-------------|
| `store.py` | In-memory store | Thread-safe dict wrapper for tasks |
| `models.py` | Data models | `Task`, `TaskCreate`, `TaskUpdate` with Python 3.13+ typing |
| `main.py` | API routes | CRUD endpoints for tasks |

**Endpoints:**
- `GET /` → Health check / API info
- `GET /tasks` → List all tasks
- `POST /tasks` → Create task
- `GET /tasks/{task_id}` → Get single task
- `PUT /tasks/{task_id}` → Update task
- `DELETE /tasks/{task_id}` → Delete task

### User Directory API - Ops Breakdown

| Operation | File | Description |
|-----------|------|-------------|
| `store.py` | In-memory store | Thread-safe dict wrapper for users |
| `models.py` | Data models | `User`, `UserCreate`, `UserUpdate` with Python 3.13+ typing |
| `main.py` | API routes | CRUD endpoints for users + search |

**Endpoints:**
- `GET /` → Health check / API info
- `GET /users` → List all users
- `POST /users` → Create user
- `GET /users/{user_id}` → Get single user
- `PUT /users/{user_id}` → Update user
- `DELETE /users/{user_id}` → Delete user
- `GET /users/search/` → Search users by department

---

## Step-by-Step Implementation

### Step 1: Create Root Directory

```bash
mkdir fastapi-apps
cd fastapi-apps
```

---

### Step 2: Initialize Task Manager Application

#### 2.1 Create and initialize project

```bash
uv init task-manager --package --python 3.13
cd task-manager
```

#### 2.2 Add dependencies

```bash
uv add fastapi uvicorn
```

#### 2.3 Create the store module

Create `src/task_manager/store.py`:

```python
"""In-memory data store for tasks."""

from typing import TypeVar, Generic
from uuid import uuid4

T = TypeVar("T")


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
```

#### 2.4 Create the models module

Create `src/task_manager/models.py`:

```python
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
```

#### 2.5 Create the main application

Create `src/task_manager/main.py`:

```python
"""Task Manager API - FastAPI application."""

from fastapi import FastAPI, HTTPException, status
from uuid import uuid4

from task_manager.models import Task, TaskCreate, TaskUpdate, TaskList
from task_manager.store import tasks_store

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="A minimalistic task management API with in-memory storage",
)


@app.get("/")
def root() -> dict[str, str]:
    """Health check and API info."""
    return {"service": "Task Manager API", "status": "healthy", "docs": "/docs"}


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
    return Task(**updated_task)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str) -> None:
    """Delete a task."""
    if not tasks_store.delete(task_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id '{task_id}' not found",
        )
```

#### 2.6 Run the Task Manager (Port 8000)

```bash
uv run uvicorn task_manager.main:app --reload --port 8000
```

---

### Step 3: Initialize User Directory Application

#### 3.1 Navigate back and create project

```bash
cd ../
uv init user-directory --package --python 3.13
cd user-directory
```

#### 3.2 Add dependencies

```bash
uv add fastapi uvicorn
```

#### 3.3 Create the store module

Create `src/user_directory/store.py`:

```python
"""In-memory data store for users."""

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

    def filter(self, predicate: callable) -> list[T]:
        """Filter items by a predicate function."""
        return [item for item in self._data.values() if predicate(item)]


# Global store instance
users_store: InMemoryStore[dict] = InMemoryStore()
```

#### 3.4 Create the models module

Create `src/user_directory/models.py`:

```python
"""Pydantic models for User Directory API using Python 3.13+ typing."""

from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=254)
    department: str | None = None


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, min_length=3, max_length=254)
    department: str | None = None


class User(BaseModel):
    """Full user representation."""
    id: str
    name: str
    email: str
    department: str | None = None


class UserList(BaseModel):
    """Response model for list of users."""
    users: list[User]
    count: int
```

#### 3.5 Create the main application

Create `src/user_directory/main.py`:

```python
"""User Directory API - FastAPI application."""

from fastapi import FastAPI, HTTPException, Query, status
from uuid import uuid4

from user_directory.models import User, UserCreate, UserUpdate, UserList
from user_directory.store import users_store

app = FastAPI(
    title="User Directory API",
    version="1.0.0",
    description="A minimalistic user directory API with in-memory storage",
)


@app.get("/")
def root() -> dict[str, str]:
    """Health check and API info."""
    return {"service": "User Directory API", "status": "healthy", "docs": "/docs"}


@app.get("/users", response_model=UserList)
def list_users() -> UserList:
    """List all users."""
    users = [User(**u) for u in users_store.get_all()]
    return UserList(users=users, count=len(users))


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> User:
    """Create a new user."""
    user_id = str(uuid4())
    user_data = {"id": user_id, **user.model_dump()}
    users_store.create(user_data, user_id)
    return User(**user_data)


@app.get("/users/search", response_model=UserList)
def search_users(department: str | None = Query(default=None)) -> UserList:
    """Search users by department."""
    if department:
        filtered = users_store.filter(lambda u: u.get("department") == department)
        users = [User(**u) for u in filtered]
    else:
        users = [User(**u) for u in users_store.get_all()]
    return UserList(users=users, count=len(users))


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: str) -> User:
    """Get a specific user by ID."""
    user_data = users_store.get(user_id)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found",
        )
    return User(**user_data)


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate) -> User:
    """Update an existing user."""
    existing = users_store.get(user_id)
    if existing is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found",
        )

    update_data = user.model_dump(exclude_none=True)
    updated_user = {**existing, **update_data}
    users_store.update(user_id, updated_user)
    return User(**updated_user)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str) -> None:
    """Delete a user."""
    if not users_store.delete(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found",
        )
```

#### 3.6 Run the User Directory (Port 8001)

```bash
uv run uvicorn user_directory.main:app --reload --port 8001
```

---

## Quick Reference: All Commands

| Step | Command | Description |
|------|---------|-------------|
| 1 | `mkdir fastapi-apps && cd fastapi-apps` | Create root directory |
| 2 | `uv init task-manager --package --python 3.13` | Initialize task-manager project |
| 3 | `cd task-manager && uv add fastapi uvicorn` | Add dependencies |
| 4 | `uv run uvicorn task_manager.main:app --reload --port 8000` | Run task-manager |
| 5 | `cd .. && uv init user-directory --package --python 3.13` | Initialize user-directory project |
| 6 | `cd user-directory && uv add fastapi uvicorn` | Add dependencies |
| 7 | `uv run uvicorn user_directory.main:app --reload --port 8001` | Run user-directory |

---

## Python 3.13+ Typing Features Used

| Feature | Example | Description |
|---------|---------|-------------|
| Union shorthand | `str \| None` | Replaces `Optional[str]` and `Union[str, None]` |
| Generic class syntax | `class Store[T]:` | PEP 695 type parameter syntax |
| Built-in generics | `dict[str, T]` | No need for `typing.Dict` |
| `list` builtin | `list[Task]` | No need for `typing.List` |

---

## API Endpoints Summary

### Task Manager API (Port 8000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check / API info |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task |
| GET | `/tasks/{id}` | Get a task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

### User Directory API (Port 8001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check / API info |
| GET | `/users` | List all users |
| POST | `/users` | Create a user |
| GET | `/users/search` | Search users by department |
| GET | `/users/{id}` | Get a user |
| PUT | `/users/{id}` | Update a user |
| DELETE | `/users/{id}` | Delete a user |

---

## Testing the APIs

### Task Manager (Terminal 1)

```bash
# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete project", "description": "Finish FastAPI apps"}'

# List tasks
curl http://localhost:8000/tasks

# Get specific task
curl http://localhost:8000/tasks/{task_id}

# Update task
curl -X PUT http://localhost:8000/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete task
curl -X DELETE http://localhost:8000/tasks/{task_id}
```

### User Directory (Terminal 2)

```bash
# Create a user
curl -X POST http://localhost:8001/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "department": "Engineering"}'

# List users
curl http://localhost:8001/users

# Search by department
curl "http://localhost:8001/users/search?department=Engineering"

# Get specific user
curl http://localhost:8001/users/{user_id}

# Update user
curl -X PUT http://localhost:8001/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{"department": "Product"}'

# Delete user
curl -X DELETE http://localhost:8001/users/{user_id}
```

---

## Interactive Documentation

Once running, access Swagger UI:
- Task Manager: http://localhost:8000/docs
- User Directory: http://localhost:8001/docs

ReDoc (alternative docs):
- Task Manager: http://localhost:8000/redoc
- User Directory: http://localhost:8001/redoc
