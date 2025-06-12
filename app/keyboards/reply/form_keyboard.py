from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)


def region_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Санкт-Петербург")],
            [KeyboardButton(text="Москва")],
            [KeyboardButton(text="Московская Область")],
            [KeyboardButton(text="Тюмень")],
            [KeyboardButton(text="Брянск")],
            [KeyboardButton(text="Щекино, Тульская обл.")],
            [KeyboardButton(text="Камышин, Волгоградская обл.")],
            [KeyboardButton(text="Екатеринбург")],
            [KeyboardButton(text="Узловая")]
        ],
        resize_keyboard=True,  # кнопки адаптируются по ширине
        one_time_keyboard=True  # клавиатура не исчезает после нажатия
    )

def experience_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Менее 1 года")],
            [KeyboardButton(text="1-2 года")],
            [KeyboardButton(text="2-3 года")],
            [KeyboardButton(text="3+ лет")]
        ],
        resize_keyboard=True,  # кнопки адаптируются по ширине
        one_time_keyboard=True  # клавиатура не исчезает после нажатия
    )

def education_level_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Высшее образование")],
            [KeyboardButton(text="Среднее образование")],
            [KeyboardButton(text="Школьное")]
        ],
        resize_keyboard=True,  # кнопки адаптируются по ширине
        one_time_keyboard=True  # клавиатура не исчезает после нажатия
    )

def confim_button() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Все верно!")],
            [KeyboardButton(text="Редактировать")]
        ],
        resize_keyboard=True,  # кнопки адаптируются по ширине
        one_time_keyboard=True  # клавиатура не исчезает после нажатия
    )


def get_edit_fields_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ФИО", callback_data="edit_name")],
        [InlineKeyboardButton(text="Телефон", callback_data="edit_phone")],
        [InlineKeyboardButton(text="Email", callback_data="edit_email")],
        [InlineKeyboardButton(text="Регион", callback_data="edit_region")],
        [InlineKeyboardButton(text="Должность", callback_data="edit_position")],
        [InlineKeyboardButton(text="Стаж", callback_data="edit_experience")],
        [InlineKeyboardButton(text="Образование", callback_data="edit_education")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_confirm")],
    ])
    return keyboard