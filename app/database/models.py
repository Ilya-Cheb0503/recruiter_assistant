from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DB_URL')

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)
    name = Column(String)
    phone = Column(String)

async def save_user_data(tg_id: int, name: str, phone: str):
    async with async_session() as session:
        # Поиск пользователя по tg_id
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()

        if user:
            # Пользователь найден — обновляем
            user.name = name
            user.phone = phone
        else:
            # Пользователь не найден — создаём нового
            user = User(tg_id=tg_id, name=name, phone=phone)
            session.add(user)

        await session.commit()
