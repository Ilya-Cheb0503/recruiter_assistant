from aiogram import F, Router
from aiogram.types import InputFile, Message

from app.config import load_config

router = Router()
config = load_config()
admin_ids = list(map(int, config['ADMIN_IDS'].split(',')))

@router.message(F.text.lower() == 'метрика')
async def metrics(msg: Message):
    if msg.from_user.id not in admin_ids:
        return await msg.answer('Нет доступа')
    path = 'reports/metrics.txt'
    with open(path, 'w', encoding='utf-8') as f:
        f.write('Пользователи: 123\nЗапросы: 456\nКлючевые слова: resume, python, sales')
    await msg.answer_document(InputFile(path))
