from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards.inline.menu import get_main_menu

router = Router()

@router.message(F.text == '/help')
async def help_cmd(msg: Message):
    await msg.answer('Доступные команды: /start /help')


@router.callback_query(F.data == 'job_search')
async def job_search_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Вакансии", reply_markup=get_main_menu(callback.from_user.id))


@router.callback_query(F.data == 'about_company')
async def about_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("О компании", reply_markup=get_main_menu(callback.from_user.id))


@router.callback_query(F.data == 'submit_form')
async def submit_form_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Анкета", reply_markup=get_main_menu(callback.from_user.id))


@router.callback_query(F.data == 'contact_info')
async def contact_info_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Контакты", reply_markup=get_main_menu(callback.from_user.id))


@router.callback_query(F.data == 'social_links')
async def social_links_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Соц сети", reply_markup=get_main_menu(callback.from_user.id))


@router.callback_query(F.data == 'admin_panel')
async def admin_panel_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Панель администратора", reply_markup=get_main_menu(callback.from_user.id))