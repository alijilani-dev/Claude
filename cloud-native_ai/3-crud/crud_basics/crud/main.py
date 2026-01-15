from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
app = FastAPI(title="FastAPI PyTest Spin..")

class TodoItem(BaseModel):
    id: int
    task: str
    time_estimate: int = None # in minutes

class TodoItemResponse(BaseModel):
    id: int
    task: str
    time_estimate: int = None # in minutes
    completed: bool = False

@app.get("/")
def read_root():
    """Root endpoint returning a Hello World message."""
    return {"message": "Hello World"}

@app.get("/todo")
def todo() -> list[TodoItemResponse]:
    my_todo_list = [
        TodoItemResponse(id = 1, task = "Buy groceries", time_estimate = 30, completed = True),
        TodoItemResponse(id = 2, task = "Walk the dog", time_estimate = 20, completed = True),
        TodoItemResponse(id = 3, task = "Read a book", time_estimate = 60, completed = True)
    ]
    return my_todo_list

@app.post("/todo")
def add_todo(todo: TodoItem) -> TodoItemResponse:
    todo_response = TodoItemResponse (**todo.dict(), completed= False)
    return todo_response

@app.delete("/todo/{item_id}")
def delete_todo(item_id: int):
    """Delete an item by its ID"""
    return {"message": f"Todo item with Id {item_id} deleted."}

@app.put("/todo/{item_id}")
def update_todo(item_id: int, todo: TodoItem) -> TodoItemResponse:
    todo_response = TodoItemResponse(**todo.dict(), completed=False)
    return todo_response

@app.patch("/todo/{item_id}/complete")
def complete_todo(item_id: int) -> TodoItemResponse:
    """Mark a todo item as completed."""
    todo_response = TodoItemResponse(id=item_id, task="Sample Task", completed=True)
    return todo_response

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)