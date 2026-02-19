from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from starlette import status
import asyncio
from sqlalchemy.orm import Session

from database import SessionLocal
from repository import TaskRepository


app = FastAPI()

# --- Модели данных (Pydantic) ---
class Task(BaseModel):
    title: str
    description: str | None = None

class TaskPublic(BaseModel):
    id: int
    title: str
    description: str | None = None

    class Config:
        from_attributes = True # Позволяет Pydantic читать данные

class User(BaseModel):
    username: str
    email: str

# Временные хранилища (users пока оставляем в памяти, задачи переносим в БД)
users = []

# --- Зависимость для работы с БД ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Эндпоинты для задач (CRUD через PostgreSQL) ---

@app.post("/tasks", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
async def create_task(task: Task, db: Session = Depends(get_db)):
    # Имитация асинхронности
    await asyncio.sleep(1)

    repo = TaskRepository(db)
    # Создаем задачу через репозиторий
    new_task = repo.add(title=task.title, description=task.description)
    # Сохраняем изменения в базу (Unit of Work)
    db.commit()
    # Обновляем объект, чтобы получить ID, сгенерированный базой
    db.refresh(new_task)
    return new_task


@app.get("/tasks/{task_id}", response_model=TaskPublic)
async def get_single_task(task_id: int, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    success = repo.delete(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    db.commit()  # Не забываем зафиксировать удаление в БД
    return None


# --- Эндпоинты для пользователей (пока без БД, как и было) ---

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
