from aiogram import F, Router
from aiogram.types import Message
from keyboards.inline.menu import get_main_menu
from bot_text.main_menu import welcome_message

router = Router()

@router.message(lambda msg: msg.text.lower() in ["/start", "главное меню"])
async def start_cmd(msg: Message):
    await msg.answer(
        welcome_message,
        reply_markup=get_main_menu(msg.from_user.id)
    )
