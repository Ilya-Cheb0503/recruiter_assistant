import logging

from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError

from app.database.models import Vacancy
from app.database.session import async_session

logger = logging.getLogger(__name__)


async def get_all_vacancies():
    """
    Возвращает список всех вакансий.
    """
    async with async_session() as session:
        result = await session.execute(select(Vacancy))
        return result.scalars().all()


async def get_vacancies_by_keyword_and_region(keyword: str, region: str):
    async with async_session() as session:
        stmt = select(Vacancy).where(
            func.lower(Vacancy.region).like(f"%{region.lower()}%"),
            or_(
                func.lower(Vacancy.title).like(f"%{keyword.lower()}%"),
                func.lower(Vacancy.requirements).like(f"%{keyword.lower()}%"),
                func.lower(Vacancy.responsibilities).like(f"%{keyword.lower()}%")
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_vacancies_by_keywords_and_region(keywords: list[str], region: str):
    async with async_session() as session:
        filters = [
            or_(
                func.lower(Vacancy.title).like(f"%{kw.lower()}%"),
                func.lower(Vacancy.requirements).like(f"%{kw.lower()}%"),
                func.lower(Vacancy.responsibilities).like(f"%{kw.lower()}%")
            )
            for kw in keywords
        ]

        stmt = select(Vacancy).where(
            func.lower(Vacancy.region).like(f"%{region.lower()}%"),
            or_(*filters)
        )
        result = await session.execute(stmt)
        return result.scalars().all()


async def get_vacancies_no_experience(region: str):
    async with async_session() as session:
        stmt = select(Vacancy).where(
            func.lower(Vacancy.region).like(f"%{region.lower()}%"),
            func.lower(Vacancy.experience) == "нет опыта"
        )
        result = await session.execute(stmt)
        return result.scalars().all()
