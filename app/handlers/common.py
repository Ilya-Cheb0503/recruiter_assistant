from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == '/help')
async def help_cmd(msg: Message):
    await msg.answer('Доступные команды: /start /help')
