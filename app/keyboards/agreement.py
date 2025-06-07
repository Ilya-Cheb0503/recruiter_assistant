from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_agreement_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Согласен', callback_data='agree')]
    ])
