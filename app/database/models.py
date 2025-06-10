import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

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
        user = User(tg_id=tg_id, name=name, phone=phone)
        session.add(user)
        await session.commit()




class Vacancy(Base):
    __tablename__ = "vacancies"

    id = Column(Integer, primary_key=True, unique=True)
    company = Column(String, nullable=True)
    region = Column(String, nullable=True)
    title = Column(String, nullable=False)
    salary_from = Column(String, nullable=True)
    salary_to = Column(String, nullable=True)
    requirements = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    schedule = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    employment = Column(String, nullable=True)
    metro = Column(String, nullable=True)  # Сохраняем как строку, можно сериализовать список
    url = Column(String, nullable=False)
    employer_url = Column(String, nullable=True)
