import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Впиши сюда свой реальный пароль от PostgreSQL
raw_password = "postgres"

# 2. Безопасное кодирование пароля
safe_password = urllib.parse.quote_plus(raw_password)

# 3. Формирование строки подключения
# Убедись, что 'postgres' - это твой юзернейм, а 'tasks_db' - имя созданной базы
DB_URL = f"postgresql://postgres:{safe_password}@localhost:5432/tasks_db"

# Engine - это "двигатель" для общения с БД
engine = create_engine(DB_URL)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс, от которого будут наследоваться все модели
Base = declarative_base()