from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy import select

from app.database.models import User
from app.database.session import async_session
from app.states.state_user_form import FormStates

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
            await state.clear()
            await state.set_state(FormStates.waiting_name)
            await callback.message.answer("Введите ваше ФИО:")
            return

        # Здесь логика успешного отклика
        await callback.message.answer("Вы успешно откликнулись на вакансию ✅")
        await callback.answer()
