from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from app.services.hh_api import get_vacancies
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text.lower().startswith('вакансии'))
async def show_vacancies(msg: Message, state: FSMContext):
    data = await get_vacancies('')
    await msg.answer(f'Найдено {len(data)} вакансий. Показываю первые 5:')
    for item in data[:5]:
        await msg.answer(f'{item}')
    await msg.answer('Вы просмотрели 5 вакансий.', reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text='Ещё 5', callback_data='more'),
            InlineKeyboardButton(text='Достаточно', callback_data='enough')
        ]]))
