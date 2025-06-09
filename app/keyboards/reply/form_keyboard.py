from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



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