import asyncio

from aiogram import Bot, Dispatcher

from app.config import load_config
from app.handlers import admin, common, job_seeking, start, user_form


async def main():
    config = load_config()
    bot = Bot(token=config['BOT_TOKEN'])
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(common.router)
    dp.include_router(user_form.router)
    dp.include_router(job_seeking.router)

    await dp.start_polling(bot)
