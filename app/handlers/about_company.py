from aiogram import F, Router
from aiogram.types import CallbackQuery
from bot_text.about_company import advantages_text, compnies_enterprises_text, main_directions_text
from keyboards.inline.menu import get_about_company_menu


router = Router()


@router.callback_query(F.data == 'advantages')
async def advantages_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(advantages_text, reply_markup=get_about_company_menu())


@router.callback_query(F.data == 'compnies_enterprises')
async def compnies_enterprises_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(compnies_enterprises_text, reply_markup=get_about_company_menu())


@router.callback_query(F.data == 'main_directions')
async def main_directions_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(main_directions_text, reply_markup=get_about_company_menu())