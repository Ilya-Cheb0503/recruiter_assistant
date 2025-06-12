import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.database.session import async_session

load_dotenv()
DATABASE_URL = os.getenv('DB_URL')

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class User(Base):
    __tablename__ = 'users'

    tg_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)  # ФИО
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    region = Column(String, nullable=True)  # Предпочтительный регион поиска
    position = Column(String, nullable=True)  # Должность
    experience = Column(String, nullable=True)  # Опыт работы
    education = Column(String, nullable=True)  # Образование

async def save_user_data(
    
    tg_id: int,
    name: str = None,
    phone: str = None,
    email: str = None,
    region: str = None,
    position: str = None,
    experience: str = None,
    education: str = None
):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        user = result.scalar_one_or_none()
        print(f"User found: {user}")
        # Если пользователь уже существует, обновляем его данные
        print(f'user_phone: {phone}, user_email: {email}, user_region: {region}, user_position: {position}, user_experience: {experience}, user_education: {education}')
        print(f"Updating user {tg_id} with data: {name}, {phone}, {email}, {region}, {position}, {experience}, {education}")
        if user:
            user.name = name or user.name
            user.phone = phone or user.phone
            user.email = email or user.email
            user.region = region or user.region
            user.position = position or user.position
            user.experience = experience or user.experience
            user.education = education or user.education
        else:
            user = User(
                tg_id=tg_id,
                name=name,
                phone=phone,
                email=email,
                region=region,
                position=position,
                experience=experience,
                education=education
            )
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
