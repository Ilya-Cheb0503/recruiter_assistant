from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.types import CallbackQuery, InputFile, Message
from keyboards.inline.menu import get_admin_dashboard
from sqlalchemy import distinct, func, select

from app.config import load_config
from app.database.models import Metric
from app.database.session import async_session

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
