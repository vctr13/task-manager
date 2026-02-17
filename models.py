from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class TaskModel(Base):
    __tablename__ = "tasks" # Должно совпадать с именем в БД

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String)
    is_completed = Column(Boolean, default=False)