from fastapi import FastAPI

app = FastAPI()

@app.get("/tasks")
def todo() -> list[dict[str, int | str]]:
    return [{"id": 1, "task": "Buy groceries"},
            {"id": 2, "task": "Buy a book"},
            {"id": 3, "task": "Write code"},
            {"id": 4, "task": "Go for a walk"}]

# @app.get("/tasks/{task_id}")
# def todo_1(task_id: int) -> dict[str, int | str]:
#     if task_id < 1:
#         return {"error": "Task ID must be greater than 0"}
#     return {"id": task_id, "task": "Buy groceries"}

@app.get("/tasks/{task_id}")
def todo_1(task_id: int = 1, include_details: bool = False) -> dict[str, int | str]:
    if task_id < 0:
        return {"error": "Task ID must be greater than 0"}
    if include_details:
        return {"id": task_id, "task": "Buy groceries", "details":"details.."}
    return {"id": task_id, "task": "Buy groceries"}