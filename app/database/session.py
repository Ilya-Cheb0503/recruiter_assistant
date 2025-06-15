import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DB_URL")  # Убедись, что в .env есть DB_URL, например:
# DB_URL=sqlite+aiosqlite:///./db.sqlite3

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)
