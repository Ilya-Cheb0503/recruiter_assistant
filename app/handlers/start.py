from aiogram import F, Router
from aiogram.types import Message
from bot_text.main_menu import welcome_message
from keyboards.inline.menu import get_main_menu

from app.utils.metrics import log_event

router = Router()

@router.message(lambda msg: msg.text.lower() in ["/start", "главное меню"])
async def start_cmd(msg: Message):
    await msg.answer(
        welcome_message,
        reply_markup=get_main_menu(msg.from_user.id)
    )
    await log_event(user_id=msg.from_user.id, event_type="start")

