# app/handlers/form/agreement.py
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.states.state_user_form import FormStates


router = Router()


@router.callback_query(FormStates.waiting_agreement, F.data == 'agree')
async def agreed(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Для начала укажите в сообщении ваши ФИО:')
    await state.set_state(FormStates.waiting_name)
    await call.answer()