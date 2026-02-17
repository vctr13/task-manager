from sqlalchemy.orm import Session
from models import TaskModel

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, title: str, description: str = None) -> TaskModel:
        # Создаем объект модели
        new_task = TaskModel(title=title, description=description)
        # Добавляем в сессию (но еще не сохраняем в БД!)
        self.session.add(new_task)
        return new_task

    def get_all(self):
        return self.session.query(TaskModel).all()

    def get_by_id(self, task_id: int):
        # return self.session.query(TaskModel).filter(TaskModel.id == task_id).first()
        return self.session.get(TaskModel, task_id)

    def delete(self, task_id: int):
        task = self.get_by_id(task_id)
        if task:
            self.session.delete(task)
            return True
        return False