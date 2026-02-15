from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from dotenv import load_dotenv
import os
load_dotenv()

app = FastAPI(title="Task API")

class Task(BaseModel):
    id: int | None = None
    title: str
    completed: bool = False

tasks: list[Task] = []
next_id = 1

@app.post("/tasks", response_model=Task)
def create_task(task: Task) -> Task:
    global next_id
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task

@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return tasks

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")
    
@app.get("/health")
def health_check() -> dict:
    print("Health check endpoint called", os.getenv("LOGS"))
    return {"status": "healthy"}