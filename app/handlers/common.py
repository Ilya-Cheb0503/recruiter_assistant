from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from bot_text.about_company import (about_company_text, advantages_text)
from bot_text.contacts import contact_info_text
from bot_text.main_menu import welcome_message
from keyboards.inline.menu import (get_about_company_menu, get_admin_dashboard,
                                   get_job_seeking_menu, get_main_menu,
                                   get_region_selection_keyboard)

router = Router()

@router.message(F.text == '/help')
async def help_cmd(msg: Message):
    await msg.answer('Доступные команды: /start /help')


@router.callback_query(F.data == 'main_menu')
async def main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        welcome_message,
        reply_markup=get_main_menu(callback.from_user.id)
    )


@router.callback_query(F.data == 'job_search')
async def job_search_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Выберите регион для поиска вакансий:",
        reply_markup=get_region_selection_keyboard()
    )


@router.callback_query(F.data.startswith("region_"))
async def region_selected_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    region = callback.data.replace("region_", "")
    await state.update_data(region=region)  # сохраняем регион в FSM

    await callback.message.edit_text(
        f"Выбран регион: {region}\nТеперь выберите, как искать вакансии:",
        reply_markup=get_job_seeking_menu()
    )


@router.callback_query(F.data == 'about_company')
async def about_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(about_company_text, reply_markup=get_about_company_menu())

@router.callback_query(F.data == 'advantages')
async def about_company_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(advantages_text, reply_markup=get_about_company_menu())

# @router.callback_query(F.data == 'compnies_enterprises')
# async def about_company_handler(callback: CallbackQuery):
#     await callback.answer()
#     await callback.message.edit_text(compnies_enterprises_text, reply_markup=get_about_company_menu())


# @router.callback_query(F.data == 'main_directions')
# async def about_company_handler(callback: CallbackQuery):
#     await callback.answer()
#     await callback.message.edit_text(main_directions_text, reply_markup=get_about_company_menu())


@router.callback_query(F.data == 'contact_info')
async def contact_info_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(contact_info_text, reply_markup=get_main_menu(callback.from_user.id))


# @router.callback_query(F.data == 'social_links')
# async def social_links_handler(callback: CallbackQuery):
#     await callback.answer()
#     await callback.message.edit_text(social_links_text, reply_markup=get_main_menu(callback.from_user.id))
