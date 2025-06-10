from aiogram import F, Router
from aiogram.types import CallbackQuery, InputFile, Message
from keyboards.inline.menu import get_admin_dashboard

from app.config import load_config

router = Router()
config = load_config()
admin_ids = list(map(int, config['ADMINS'].split(',')))



@router.callback_query(F.data == 'admin_panel')
async def admin_panel_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Панель администратора", reply_markup=get_admin_dashboard())


@router.callback_query(F.data == 'send_broadcast')
async def admin_panel_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Рассылка *пока не подключена", reply_markup=get_admin_dashboard())


@router.callback_query(F.data == 'metrics')
async def admin_panel_handler(callback: CallbackQuery):
    await callback.answer()
    if callback.from_user.id not in admin_ids:
        return await callback.answer('Нет доступа')
    path = 'reports/metrics.txt'
    await callback.message.edit_text("Метрика разрабатывается гномами по ночам", reply_markup=get_admin_dashboard())
