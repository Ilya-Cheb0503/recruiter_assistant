import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.hh_service import update_vacancies_db


async def daily_job():
    print("🔄 Загрузка вакансий с hh.ru...")
    vacancies = await update_vacancies_db()
    # print(f"✅ Загружено {len(vacancies)} вакансий.")

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_job, "interval", days=1)
    scheduler.start()