from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def confim_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Все верно", callback_data="form_confirm")],
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data="form_edit")],
    ])


def get_edit_fields_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📛 ФИО", callback_data="edit_name")],
        [InlineKeyboardButton(text="📞 Телефон", callback_data="edit_phone")],
        [InlineKeyboardButton(text="📧 Email", callback_data="edit_email")],
        [InlineKeyboardButton(text="📍 Регион", callback_data="edit_region")],
        [InlineKeyboardButton(text="💼 Должность", callback_data="edit_position")],
        [InlineKeyboardButton(text="🧰 Опыт работы", callback_data="edit_experience")],
        [InlineKeyboardButton(text="🎓 Образование", callback_data="edit_education")],
        [InlineKeyboardButton(text="🔙 Вернуться", callback_data="back_to_confirm")],
    ])