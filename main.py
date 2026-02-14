from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status

app = FastAPI()

class Task(BaseModel):
    title: str
    description: str | None = None

class TaskPublic(BaseModel):
    title: str

class User(BaseModel):
    username: str
    email: str

tasks = []
users =[]

@app.post("/tasks")
async def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task created successfully", "task": task}

@app.post("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    if not (0 <= task_id < len(tasks)):
        raise HTTPException(status_code=404, detail="Task not found")
    current_task = tasks[task_id]
    if not current_task.title.startswith("[DONE] "):
        current_task.title = f"[DONE] {current_task.title}"
    return {"message": "Task marked as completed", "task": current_task}

@app.post("/users")
async def great_user(user: User):
    users.append(user)
    return {"message": f"Hello, {user.username}!"}

@app.get("/users/{username}")
async def get_user(username: str):
    for user in users:
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/tasks")
async def get_tasks():
    return {"tasks": tasks}

@app.get("/tasks/titles", response_model=list[TaskPublic])
async def get_task_titles():
    return tasks

@app.get("/tasks/{task_id}")
async def get_single_task(task_id: int):
    if task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    if task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    if task_id >= len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.pop(task_id)
    return None