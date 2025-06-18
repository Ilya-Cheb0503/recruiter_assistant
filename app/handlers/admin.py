from datetime import datetime, timedelta
import asyncio

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from keyboards.inline.menu import get_admin_dashboard
from sqlalchemy import distinct, func, select

from app.config import load_config
from app.database.models import Metric
from app.database.session import async_session
from app.services.static_content import load_content, save_content
from app.states.state_user_form import FormStates



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
    await callback.message.edit_text("Временно недоступна в связи с рефакторингом проекта", reply_markup=get_admin_dashboard())


@router.callback_query(F.data == 'metrics')
async def admin_panel_handler(callback: CallbackQuery):
    await callback.answer()
    if callback.from_user.id not in admin_ids:
        return await callback.answer('Нет доступа ❌')

    one_month_ago = datetime.utcnow() - timedelta(days=30)

    async with async_session() as session:
        # Уникальные обращения
        result = await session.execute(
            select(func.count(distinct(Metric.user_id))).where(Metric.timestamp >= one_month_ago)
        )
        unique_users = result.scalar()

        # Все действия
        result = await session.execute(
            select(func.count()).where(Metric.timestamp >= one_month_ago)
        )
        total_actions = result.scalar()

        # Целевые действия (отклик, анкета, контакты)
        result = await session.execute(
            select(Metric.event_type).where(
                Metric.timestamp >= one_month_ago,
                Metric.event_type.in_(['form_submit', 'respond_click', 'send_contact'])
            )
        )
        target_actions = result.scalars().all()
        form_count = target_actions.count('form_submit')
        respond_count = target_actions.count('respond_click')
        contact_count = target_actions.count('send_contact')
        total_target = len(target_actions)

        # Удержание
        result = await session.execute(
            select(Metric.user_id, func.count(distinct(func.date(Metric.timestamp))))
            .where(Metric.timestamp >= one_month_ago)
            .group_by(Metric.user_id)
        )
        multi_day_users = [user_id for user_id, days in result.fetchall() if days > 1]
        retention_percent = round(len(multi_day_users) / unique_users * 100, 2) if unique_users else 0

        # Переходы на внешние сайты
        result = await session.execute(
            select(func.count()).where(
                Metric.timestamp >= one_month_ago,
                Metric.event_type.like('external_click%')
            )
        )
        external_clicks = result.scalar()

    metrics_text = f"""📊 Метрика за 30 дней:

👤 Уникальные пользователи: {unique_users}
⚡️ Всего действий: {total_actions}

🎯 Целевые действия:
• Анкет заполнено: {form_count}
• Откликов на вакансии: {respond_count}
• Контактов отправлено: {contact_count}
• Всего целевых: {total_target}

🔁 Удержание:
• Вернулись снова: {len(multi_day_users)} пользователей
• Удержание: {retention_percent}%

🌐 Переходы на внешние сайты: {external_clicks}
"""

    await callback.message.edit_text(metrics_text, reply_markup=get_admin_dashboard())


@router.callback_query(F.data == "edit_static_text")
async def choose_content_to_edit(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id not in admin_ids:
        return await callback.answer("Нет доступа")
    
    content = load_content()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=value[1], callback_data=f"edit_content_{key}")]
            for key, value in list(content.items())
        ]
    )
    await callback.message.edit_text("Что редактируем?", reply_markup=keyboard)


@router.callback_query(F.data.startswith("edit_content_"))
async def ask_new_value(callback: CallbackQuery, state: FSMContext):
    key = callback.data.replace("edit_content_", "")

    content = load_content()
    key_name = content[key][1]

    await state.update_data(edit_key=key)
    await callback.message.edit_text(f"Введите новое значение для «{key_name}»")
    await state.set_state(FormStates.waiting_for_new_content)


@router.message(FormStates.waiting_for_new_content)
async def update_content_text(msg: Message, state: FSMContext):
    data = await state.get_data()
    key = data["edit_key"]
    content = load_content()
    content[key][0] = msg.text
    key_name = content[key][1]
    save_content(content)
    await msg.answer(f"Содержимое «{key_name}» обновлено ✅")
    await asyncio.sleep(2)
    await msg.answer("Панель администратора", reply_markup=get_admin_dashboard())
    await state.clear()