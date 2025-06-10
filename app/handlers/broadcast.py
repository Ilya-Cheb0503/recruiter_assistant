from aiogram import F, Router
from aiogram.types import Message

from app.config import load_config

router = Router()
config = load_config()
admin_ids = list(map(int, config['ADMIN_IDS'].split(',')))
users = [10001, 10002, 10003]  # Мок список пользователей

@router.message(F.text.lower().startswith('рассылка:'))
async def broadcast(msg: Message):
    if msg.from_user.id not in admin_ids:
        return await msg.answer('Нет доступа')
    text = msg.text[9:].strip()
    for uid in users:
        try:
            await msg.bot.send_message(uid, text)
        except Exception:
            pass
    await msg.answer('Рассылка завершена')
