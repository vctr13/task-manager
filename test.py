from database import SessionLocal
from repository import TaskRepository

# 1. Открываем сессию
db = SessionLocal()

# 2. Инициализируем репозиторий
repo = TaskRepository(db)

# 3. Добавляем задачу
#repo.add(title="Изучить Pydantic", description="Это основа Backend на Python")

search_result = repo.get_by_id(2)
if search_result is not None:
    print(f"Задача найдена: {search_result.title} - {search_result.description}")
else:
    print("Задача с таким ID не найдена.")

# del_result = repo.delete(2)
# if del_result:
#     print("Задача удалена успешно!")
# else:
#     print("Задача не найдена для удаления.")

# 4. ФИКСИРУЕМ изменения (Unit of Work)

db.commit()

# 5. Закрываем сессию
db.close()