import logging

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError

from app.database.models import Vacancy
from app.database.session import async_session

logger = logging.getLogger(__name__)


async def get_all_vacancies(region: str = "Москва") -> list[Vacancy]:
    """
    Возвращает список всех вакансий.
    """
    async with async_session() as session:
        stmt = select(Vacancy).where(
            Vacancy.region.ilike(f"%{region}%"),
        )
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_vacancies_by_keyword_and_region(keyword: str, region: str):
    async with async_session() as session:
        filters = or_(
            *[func.lower(func.coalesce(Vacancy.title, '')).like(f"%{keyword.lower()}%")],
            *[func.lower(func.coalesce(Vacancy.requirements, '')).like(f"%{keyword.lower()}%")],
            *[func.lower(func.coalesce(Vacancy.responsibilities, '')).like(f"%{keyword.lower()}%")],
        )

        stmt = select(Vacancy).where(
            Vacancy.region.ilike(f"%{region}%"),
            filters
        )
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_vacancies_by_keywords_list(keywords: list[str], region: str):
    async with async_session() as session:
        filters = or_(
            *[func.lower(func.coalesce(Vacancy.title, '')).like(f"%{kw.lower()}%") for kw in keywords],
            *[func.lower(func.coalesce(Vacancy.requirements, '')).like(f"%{kw.lower()}%") for kw in keywords],
            *[func.lower(func.coalesce(Vacancy.responsibilities, '')).like(f"%{kw.lower()}%") for kw in keywords],
        )

        stmt = select(Vacancy).where(
            Vacancy.region.ilike(f"%{region}%"),
            filters
        )

        result = await session.execute(stmt)
        return result.scalars().all()


async def get_vacancies_no_experience(region: str):
    async with async_session() as session:

        filters = or_(
            Vacancy.experience.ilike("%Нет%опыта%"),
            Vacancy.requirements.ilike("%без опыта%"),
            Vacancy.requirements.ilike("%без опыта работы%"),
            Vacancy.requirements.ilike("%стажировка%"),
            Vacancy.requirements.ilike("%стажер%"),
            Vacancy.requirements.ilike("%стажировка/стажер%"),
            Vacancy.requirements.ilike("%обучение%"),
        )

        stmt = select(Vacancy).where(
            Vacancy.region.ilike(f"%{region}%"),
            filters
        )
        result = await session.execute(stmt)
        return result.scalars().all()
