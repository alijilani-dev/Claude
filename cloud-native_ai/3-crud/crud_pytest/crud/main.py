from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
app = FastAPI(title="FastAPI PyTest Spin..")

class TodoItem(BaseModel):
    id: int
    task: str
    time_estimate: int = None # in minutes

class TodoItemResponse(BaseModel):
    id: int
    task: str
    time_estimate: Optional [int] = None # in minutes
    completed: bool = False

@app.get("/")
def read_root():
    """Root endpoint returning a Hello World message."""
    return {"message": "Hello World"}

@app.get("/todo")
def todo() -> list[TodoItemResponse]:
    expected = [
        TodoItemResponse(id = 1, task = "Buy groceries", completed = False),
        TodoItemResponse(id = 2, task = "Walk the dog", completed = False)
    ]
    return expected

@app.post("/todo")
def add_todo(todo: TodoItem) -> TodoItemResponse:
    todo_response = TodoItemResponse (**todo.model_dump(), completed= False)
    return todo_response

@app.delete("/todo/{item_id}")
def delete_todo(item_id: int):
    """Delete an item by its ID"""
    return {"message": f"Todo item with id {item_id} deleted."}

@app.put("/todo/{item_id}")
def update_todo(item_id: int, todo: TodoItem) -> TodoItemResponse:
    todo_response = TodoItemResponse(**todo.dict(), completed=False)
    return todo_response

@app.patch("/todo/{item_id}/complete")
def complete_todo(item_id: int) -> TodoItemResponse:
    """Mark a todo item as completed."""
    todo_response = TodoItemResponse(id = item_id, task = "sample task", time_estimate = None, completed = True)
    return todo_response

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)