import asyncio

from aiogram import Bot, Dispatcher

from app.config import load_config
from app.handlers import admin, job_seeking, start, main_menu, about_company
from app.handlers.form import form_fill, agreement  # Импорт твоего роутера

async def main():
    config = load_config()
    bot = Bot(token=config['BOT_TOKEN'])
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(main_menu.router)
    dp.include_router(job_seeking.router)
    dp.include_router(form_fill.router)
    dp.include_router(agreement.router)
    dp.include_router(about_company.router)

    await dp.start_polling(bot)
