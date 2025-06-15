from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile

from app.services.static_content import CONTENT
from keyboards.inline.menu import (get_about_company_menu, get_main_menu,
                                   get_region_selection_keyboard)
from states.state_user_form import FormStates
from keyboards.agreement import get_agreement_kb



router = Router()


# Обработчик кнопки "Ищу работу"
@router.callback_query(F.data == 'job_search')
async def job_search_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Выберите регион для поиска вакансий:",
        reply_markup=get_region_selection_keyboard()
    )


# Обработчик кнопки "О компании"
@router.callback_query(F.data == 'about_company')
async def about_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(CONTENT.get('about_company'), reply_markup=get_about_company_menu())


# Обработчик кнопки "Частые вопросы"
@router.callback_query(F.data == 'social_links')
async def frequent_questions_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(CONTENT.get('social_links'), reply_markup=get_main_menu(callback.from_user.id))


# Обработчик кнопки "Отправить анкету"
@router.callback_query(F.data == 'submit_form')
async def job_search_handler(callback: CallbackQuery, state: FSMContext):
    pdf = FSInputFile('static/agreement.pdf')
    await callback.answer()
    await callback.message.answer_document(
        pdf,
        caption='Вы согласны с политикой обработки данных?',
        reply_markup=get_agreement_kb()
    )
    await state.set_state(FormStates.waiting_agreement)


# Обработчик кнопки "Контактная информация"
@router.callback_query(F.data == 'contact_info')
async def contact_info_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(CONTENT.get('contact_info'), reply_markup=get_main_menu(callback.from_user.id))