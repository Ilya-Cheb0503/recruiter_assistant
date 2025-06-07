from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv


load_dotenv()
ADMIN_IDS = list(map(int, os.getenv("ADMINS", "").split(",")))


def get_main_menu(user_id: int) -> InlineKeyboardMarkup:
    buttons =[
        [InlineKeyboardButton(text="Ищу работу", callback_data="job_search")],
        [InlineKeyboardButton(text="О компании", callback_data="about_company")],
        [InlineKeyboardButton(text="Отправь анкету", callback_data="submit_form")],
        [InlineKeyboardButton(text="Контактная информация", callback_data="contact_info")],
        [InlineKeyboardButton(text="Соц сети", callback_data="social_links")]
    ]

    if user_id in ADMIN_IDS:
        buttons.append([InlineKeyboardButton(text="Панель администратора", callback_data="admin_panel")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)