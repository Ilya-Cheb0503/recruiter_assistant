from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_agreement_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Согласен', callback_data='agree')]
    ])
