from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from alembic import context
import os
import sys
from dotenv import load_dotenv

# Добавляем путь к приложению, чтобы импортировать модели
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Загружаем переменные из .env
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Импорт моделей
from app.database.models import Base

# Конфигурация Alembic
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    """Миграции в offline-режиме"""
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Миграции в online-режиме с использованием async engine"""
    connectable = create_async_engine(
        DB_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        def do_migrations(sync_connection):
            context.configure(
                connection=sync_connection,
                target_metadata=target_metadata,
            )
            with context.begin_transaction():
                context.run_migrations()

        await connection.run_sync(do_migrations)

    await connectable.dispose()

# Запуск
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
