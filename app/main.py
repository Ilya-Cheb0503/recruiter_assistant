import asyncio
from aiogram import Bot, Dispatcher
from app.config import load_config
from app.handlers import start, common, form


async def main():
    config = load_config()
    bot = Bot(token=config['BOT_TOKEN'])
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(common.router)
    dp.include_router(form.router)

    await dp.start_polling(bot)
