from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(
    title="Golden Path API",
    description="A high-performance, stateless API following DevOps best practices.",
    version="1.0.0"
)

# In-memory database for demonstration (Statelessness maintained by not persisting across restarts)
todos = {}

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: str

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/todos", response_model=List[Todo])
async def list_todos():
    """List all TODO items."""
    return list(todos.values())

@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_in: TodoCreate):
    """Create a new TODO item."""
    todo_id = str(uuid.uuid4())
    new_todo = Todo(id=todo_id, **todo_in.dict())
    todos[todo_id] = new_todo
    return new_todo

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str):
    """Retrieve a specific TODO item."""
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str):
    """Delete a TODO item."""
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return None
