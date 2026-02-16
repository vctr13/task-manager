import asyncio
import asyncpg

async def create_tables():
    # Подключаемся к твоей базе данных [6]
    conn = await asyncpg.connect(
        host='127.0.0.1',
        port=5432,
        user='postgres',
        password='postgres',
        database='tasks_db'
    )

    # SQL запрос на создание таблицы [3]
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        is_completed BOOLEAN DEFAULT FALSE
    );
    """

    print("Создание таблицы tasks...")
    await conn.execute(create_table_query) # Выполняем запрос [7]
    print("Таблица успешно создана!")

    # Закрываем соединение [6]
    await conn.close()

if __name__ == "__main__":
    asyncio.run(create_tables())