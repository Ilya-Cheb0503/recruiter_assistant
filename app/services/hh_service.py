import asyncio
import logging
import re

import aiohttp
from sqlalchemy import select

from app.config import load_config
from app.database.models import Vacancy
from app.database.session import async_session

config = load_config()

EMPLOYER_IDS = [5436353, 10696710, 3147445, 538640, 2763248]
HH_API_URL = "https://api.hh.ru/vacancies"
ACCESS_TOKEN = config['ACCESS_TOKEN']  # желательно вынести в .env

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}


def strip_tags(text):
    return re.sub(r"<[^>]+>", "", text) if text else None


def parse_vacancy(data: dict) -> Vacancy:
    salary = data.get("salary") or {}

    salary_from = salary.get("from")
    salary_to = salary.get("to")
    currency = salary.get("currency", "")

    def format_salary(value):
        if value is not None and currency:
            return f"{value} {currency}"
        return None

    metro_stations = []
    try:
        metro_stations = [station["station_name"] for station in data.get("address", {}).get("metro_stations", [])]
    except Exception:
        pass

    return Vacancy(
        id=int(data["id"]),
        company=data["employer"]["name"],
        region=data["area"]["name"],
        title=data["name"],
        salary_from=format_salary(salary_from),
        salary_to=format_salary(salary_to),
        requirements=(data.get("snippet", {}).get("requirement") or "").strip(),
        responsibilities=(data.get("snippet", {}).get("responsibility") or "").strip(),
        schedule=data.get("schedule", {}).get("name"),
        experience=data.get("experience", {}).get("name"),
        employment=data.get("employment", {}).get("name"),
        metro=", ".join(metro_stations),
        url=data.get("alternate_url"),
        employer_url=data["employer"].get("alternate_url")
    )



async def update_vacancies_db(per_page=100):
    async with aiohttp.ClientSession() as session:
        for employer_id in EMPLOYER_IDS:
            page = 0
            logging.info(f"Загрузка вакансий для работодателя: {employer_id}")
            while True:
                params = {"employer_id": employer_id, "page": page, "per_page": per_page}
                async with session.get(HH_API_URL, headers=HEADERS, params=params) as response:
                    if response.status != 200:
                        logging.error(f"Ошибка получения вакансий {employer_id}: {response.status}")
                        break
                    data = await response.json()
                    items = data.get("items", [])
                    if not items:
                        break

                async with async_session() as db:
                    for item in items:
                        exists = await db.scalar(select(Vacancy).where(Vacancy.id == int(item["id"])))
                        if exists:
                            continue
                        parsed = parse_vacancy(item)
                        db.add(parsed)

                    await db.commit()

                if page >= data.get("pages", 1) - 1:
                    break
                page += 1



if __name__ == '__main__':
    asyncio.run(update_vacancies_db()) # Если нужно протестировать процесс получения вакансий и выгрузку их в БД
    # То используй команду python -m app.services.hh_service