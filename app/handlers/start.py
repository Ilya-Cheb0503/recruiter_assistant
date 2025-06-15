from aiogram import F, Router
from aiogram.types import Message
from aiogram.types import Message, CallbackQuery
from keyboards.inline.menu import get_main_menu
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



@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        welcome_message,
        reply_markup=get_main_menu(callback.from_user.id)
    )


@router.message(F.text == '/help')
async def help_cmd(msg: Message):
    await msg.answer('Доступные команды: /start /help')
