from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Task API")

# Models
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    status: str | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
