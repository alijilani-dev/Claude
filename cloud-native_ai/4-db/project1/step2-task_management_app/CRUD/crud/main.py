import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, select, create_engine, Session      # Session is important for db interaction.
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo = True)

class TodoItem(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key= True, index= True)       # API, DB <-> We will send it none and DB will set it.
    task: str                                                       # is required, so cannot be set to none
    time_estimate: int | None = Field(default = None)               # in minutes, Not required and None by default

class TodoItemResponse(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key= True)       # API, DB <-> We will send it none and DB will set it.
    task: str                                                       # is required, so cannot be set to none
    time_estimate: int | None = Field(default = None)               # in minutes, Not required and None by default
    completed: bool = Field(default = False)                        # Not required and False by default

def get_session():
    with Session(engine) as session:                                # maintains session memory and database connection at the same time.
        yield session

# Migration Command: How to create table?
def create_tables():
    print("Trying to create tables")
    SQLModel.metadata.create_all(engine)        # create tables in our DB where table = True for any class elements
    print("Tables function completed")

create_tables()

# How to actually interact with tables?
app = FastAPI(title="Task Management API..")


@app.get("/")
def read_root():
    """Root endpoint returning a Hello World message."""
    return {"message": "Hello World"}

@app.get("/todo")
def todo(session: Session = Depends(get_session)) -> list[TodoItemResponse]:    # using dependency injection to get db connection
    expected = session.exec(select(TodoItem)).all()
    return expected

@app.post("/todo", response_model=TodoItemResponse)
def add_todo(todo: TodoItem, session: Session = Depends(get_session)) -> TodoItemResponse: # using dependency injection to get db connection
    # 1. Convert the input schema to the Database Table Model
    # The database will automatically assign the next available ID
    db_todo = TodoItem.model_validate(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    todo = session.get(TodoItem, todo_id)                                       # 1. Find the item in the database by ID
    if not todo:                                                                # 2. If the item doesn't exist, raise a 404 error
        raise HTTPException(status_code=404, detail="Todo item not found")
    session.delete(todo)                                                        # 3. Delete the item from the session
    session.commit()                                                            # 4. Commit the transaction to the database
    return {"message": f"Todo item {todo_id} deleted successfully"}             # 5. Return a success message

@app.put("/todo/{todo_id}", response_model=TodoItemResponse)
def update_todo(todo_id: int, todo_data: TodoItem, session: Session = Depends(get_session)):
    db_todo = session.get(TodoItem, todo_id)                                    # 1. Fetch the existing item from the database
    if not db_todo:                                                             # 2. Check if it exists
        raise HTTPException(status_code=404, detail="Todo item not found")
    # We use exclude_unset=True so we don't accidentally overwrite 
    # data with None if the user didn't provide every field.
    update_data = todo_data.model_dump(exclude_unset=True)                      # 3. Extract the data sent by the user as a dictionary
    for key, value in update_data.items():                                      # 4. Update the database object with the new data
        setattr(db_todo, key, value)                                            # db_todo.key = value
    session.add(db_todo)                                                        # 5. Add
    session.commit()                                                            # 6. Save
    session.refresh(db_todo)                                                    # 7. Refresh
    return db_todo                                                              # 8. Return the updated item

@app.patch("/todo/{item_id}", response_model=TodoItemResponse)
def patch_todo(item_id: int, todo_data: TodoItem, session: Session = Depends(get_session)): # Using the model as a schema
    db_todo = session.get(TodoItem, item_id)                                    # 1. Fetch the existing record from the DB
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo item not found")      # 2. Raise 404 if not found
    update_data = todo_data.model_dump(exclude_unset=True)                      # 3. model_dump(exclude_unset=True) is the "secret sauce" for PATCH
                                                                                # It creates a dictionary of ONLY the fields the user actually sent
    for key, value in update_data.items():                                      # 4. Update only the provided fields
        setattr(db_todo, key, value)

    session.add(db_todo)                                                        # 5. Save the changes
    session.commit()
    session.refresh(db_todo)
    return db_todo                                                                                

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)