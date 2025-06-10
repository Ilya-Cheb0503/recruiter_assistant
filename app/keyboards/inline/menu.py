import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
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


def get_job_seeking_menu() -> InlineKeyboardMarkup:
    buttons =[
        [InlineKeyboardButton(text="Все вакансии", callback_data="all_vacancies")],
        [InlineKeyboardButton(text="Вакансии по направлениям деятельности", callback_data="vacancies_by_keywords")],
        [InlineKeyboardButton(text="Без опыта работы", callback_data="vacancies_no_experience")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_job_by_categories_menu() -> InlineKeyboardMarkup:
    buttons =[
        [InlineKeyboardButton(text="Руководители", callback_data="vacancies_with_management")],
        [InlineKeyboardButton(text="ИТР", callback_data="vacancies_with_engineering")],
        [InlineKeyboardButton(text="Рабочие", callback_data="vacancies_with_workers")],
        [InlineKeyboardButton(text="Другие категории", callback_data="vacancies_with_other")],
        [InlineKeyboardButton(text="Назад", callback_data="job_search")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)