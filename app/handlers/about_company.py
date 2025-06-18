from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.services.static_content import load_content
from keyboards.inline.menu import get_about_company_menu


router = Router()


@router.callback_query(F.data == 'advantages')
async def advantages_handler(callback: CallbackQuery):
    await callback.answer()
    content = load_content()
    await callback.message.edit_text(content.get('advantages')[0], reply_markup=get_about_company_menu())


@router.callback_query(F.data == 'company_enterprises')
async def company_enterprises_handler(callback: CallbackQuery):
    await callback.answer()
    content = load_content()
    await callback.message.edit_text(content.get('company_enterprises')[0], reply_markup=get_about_company_menu())


@router.callback_query(F.data == 'main_directions')
async def main_directions_handler(callback: CallbackQuery):
    await callback.answer()
    content = load_content()
    await callback.message.edit_text(content.get('main_directions')[0], reply_markup=get_about_company_menu())