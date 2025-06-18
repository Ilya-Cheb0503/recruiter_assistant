import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.config import load_config


config = load_config()
ADMIN_IDS = list(map(int, config['ADMINS'].split(',')))


def get_main_menu(user_id: int) -> InlineKeyboardMarkup:
    buttons =[
        [InlineKeyboardButton(text="Ищу работу", callback_data="job_search")],
        [InlineKeyboardButton(text="О компании", callback_data="about_company")],
        [InlineKeyboardButton(text="Отправь анкету", callback_data="submit_form")],
        [InlineKeyboardButton(text="Контактная информация", callback_data="contact_info")],
        [InlineKeyboardButton(text="Социальные сети", callback_data="social_links")]
    ]

    if user_id in ADMIN_IDS:
        buttons.append([InlineKeyboardButton(text="Панель администратора", callback_data="admin_panel")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_job_seeking_menu() -> InlineKeyboardMarkup:
    buttons =[
        [InlineKeyboardButton(text="Все вакансии", callback_data="vacancies_all")],
        [InlineKeyboardButton(text="Вакансии по направлениям деятельности", callback_data="categories_vacancies")],
        [InlineKeyboardButton(text="Без опыта работы", callback_data="vacancies_noexp")],
        [InlineKeyboardButton(text="Главное меню", callback_data="main_menu")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_job_by_categories_menu() -> InlineKeyboardMarkup:
    buttons =[
        [InlineKeyboardButton(text="Руководители", callback_data="vacancies_management")],
        [InlineKeyboardButton(text="ИТР", callback_data="vacancies_engineering")],
        [InlineKeyboardButton(text="Рабочие", callback_data="vacancies_workers")],
        [InlineKeyboardButton(text="Другие категории", callback_data="vacancies_other")],
        [InlineKeyboardButton(text="Назад", callback_data="job_search")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_about_company_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Преимущества", callback_data="advantages")],
        [InlineKeyboardButton(text="Предприятия ГЭХИА", callback_data="company_enterprises")],
        [InlineKeyboardButton(text="Основные направления деятельности", callback_data="main_directions")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")]
    ])


def get_admin_dashboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Рассылка", callback_data="send_broadcast")],
        [InlineKeyboardButton(text="Метрика", callback_data="metrics")],
        [InlineKeyboardButton(text="Редакция содержания", callback_data="edit_static_text")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")]
    ])


def get_region_selection_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Санкт-Петербург", callback_data="region_Санкт-Петербург")],
        [InlineKeyboardButton(text="Москва", callback_data="region_Москва")],
        [InlineKeyboardButton(text="Московская Область", callback_data="region_Московская Область")],
        [InlineKeyboardButton(text="Тюмень", callback_data="region_Тюмень")],
        [InlineKeyboardButton(text="Брянск", callback_data="region_Брянск")],
        [InlineKeyboardButton(text="Щекино, Тульская обл.", callback_data="region_Щекино")],
        [InlineKeyboardButton(text="Камышин, Волгоградская обл.", callback_data="region_Камышин")],
        [InlineKeyboardButton(text="Екатеринбург", callback_data="region_Екатеринбург")],
        [InlineKeyboardButton(text="Узловая", callback_data="region_Узловая")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")]
    ])