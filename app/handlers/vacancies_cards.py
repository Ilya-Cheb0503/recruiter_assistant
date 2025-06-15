import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select

from app.database.models import User
from app.database.session import async_session
from app.states.state_user_form import FormStates
from app.utils.vacancy_sender import get_redirect_keyboard
from app.utils.metrics import log_event

router = Router()


@router.callback_query(F.data == "respond_direct")
async def handle_direct_response(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id

    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        if not user or not all([
            user.name,
            user.phone,
            user.email,
            user.region,
            user.position,
            user.experience,
            user.education
        ]):
            await callback.message.answer(
                "Перед откликом на вакансию, пожалуйста, заполните анкету."
            )
            await callback.answer()
            await log_event(user_id=callback.from_user.id, event_type="respond_direct_no_form")

            await state.clear()
            await state.set_state(FormStates.waiting_name)
            await callback.message.answer("Введите ваше ФИО:")
            return

        # Здесь логика успешного отклика
        await callback.message.answer("Вы успешно откликнулись на вакансию ✅")
        await log_event(user_id=callback.from_user.id, event_type="respond_click")
        await callback.answer()


@router.callback_query(F.data.startswith("go_to_site"))
async def handle_redirect_to_site(callback: CallbackQuery):
    parts = callback.data.split("|")
    if len(parts) != 2:
        await callback.answer("Ошибка ссылки", show_alert=True)
        return

    url = parts[1]

    # Логируем/сохраняем переход
    user_id = callback.from_user.id
    # await save_click(user_id, "external_site", url)

    # Редактируем клавиатуру сообщения на ссылку
    await callback.message.edit_reply_markup(reply_markup=get_redirect_keyboard(url))
    await callback.answer("Обновление клавиатуры")
    await log_event(user_id=callback.from_user.id, event_type="external_click")
