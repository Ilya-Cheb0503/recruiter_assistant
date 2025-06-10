from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from keyboards.inline.menu import (get_job_by_categories_menu,
                                   get_job_seeking_menu, get_main_menu)

router = Router()


@router.callback_query(F.data == 'all_vacancies')
async def job_search_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Вакансии", reply_markup=get_job_seeking_menu())


@router.callback_query(F.data == 'vacancies_by_keywords')
async def vacancies_by_keywords_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Готово!")


@router.callback_query(F.data == 'vacancies_with_management')
async def vacancies_with_management_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Руководители", reply_markup=get_job_by_categories_menu())


@router.callback_query(F.data == 'vacancies_with_engineering')
async def vacancies_with_engineering_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Инженеры", reply_markup=get_job_by_categories_menu())


@router.callback_query(F.data == 'vacancies_with_workers')
async def vacancies_with_workers_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Рабочие", reply_markup=get_job_by_categories_menu())


@router.callback_query(F.data == 'vacancies_with_other')
async def vacancies_with_other_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Другое", reply_markup=get_job_by_categories_menu())


@router.callback_query(F.data == 'vacancies_no_experience')
async def vacancies_no_experience_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("О компании", reply_markup=get_job_seeking_menu())