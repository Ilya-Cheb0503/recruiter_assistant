from aiogram import F, Router
from aiogram.types import CallbackQuery
from app.services.static_content import CONTENT
from keyboards.inline.menu import get_about_company_menu


router = Router()


@router.callback_query(F.data == 'advantages')
async def advantages_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(CONTENT.get('advantages'), reply_markup=get_about_company_menu())


@router.callback_query(F.data == 'company_enterprises')
async def company_enterprises_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(CONTENT.get('company_enterprises'), reply_markup=get_about_company_menu())


@router.callback_query(F.data == 'main_directions')
async def main_directions_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(CONTENT.get('main_directions'), reply_markup=get_about_company_menu())