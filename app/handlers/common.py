from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from keyboards.inline.menu import (get_admin_dashboard, get_job_seeking_menu,
                                   get_main_menu)

router = Router()

@router.message(F.text == '/help')
async def help_cmd(msg: Message):
    await msg.answer('Доступные команды: /start /help')


@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Привет! Я помощник рекрутера.',
        reply_markup=get_main_menu(callback.from_user.id)
    )


@router.callback_query(F.data == 'job_search')
async def job_search_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Вакансии", reply_markup=get_job_seeking_menu())


@router.callback_query(F.data == 'about_company')
async def about_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("О компании", reply_markup=get_about_company_menu())

@router.callback_query(F.data == 'advantages')
async def about_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Преимущества", reply_markup=get_about_company_menu())

@router.callback_query(F.data == 'compnies_enterprises')
async def about_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Предприяттия", reply_markup=get_about_company_menu())\


@router.callback_query(F.data == 'main_directions')
async def about_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Действительно основные", reply_markup=get_about_company_menu())


@router.callback_query(F.data == 'contact_info')
async def contact_info_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Контакты", reply_markup=get_main_menu(callback.from_user.id))


@router.callback_query(F.data == 'social_links')
async def social_links_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Соц сети", reply_markup=get_main_menu(callback.from_user.id))
