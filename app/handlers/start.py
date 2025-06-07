from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == '/start')
async def start_cmd(msg: Message):
    await msg.answer('Привет! Я помощник рекрутера.')
