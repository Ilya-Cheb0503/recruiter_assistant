# app/handlers/form/agreement.py
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from app.keyboards.agreement import get_agreement_kb
from app.states.state_user_form import FormStates
from app.utils.metrics import log_event

router = Router()

@router.callback_query(F.data == 'submit_form')
async def job_search_handler(callback: CallbackQuery, state: FSMContext):
    pdf = FSInputFile('static/agreement.pdf')
    await callback.answer()
    await log_event(user_id=callback.from_user.id, event_type="send_contact")
    await callback.message.answer_document(
        pdf,
        caption='Вы согласны с политикой обработки данных?',
        reply_markup=get_agreement_kb()
    )
    await state.set_state(FormStates.waiting_agreement)


@router.callback_query(FormStates.waiting_agreement, F.data == 'agree')
async def agreed(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Для начала укажите в сообщении ваши ФИО:')
    await state.set_state(FormStates.waiting_name)
    await call.answer()
    await log_event(user_id=call.from_user.id, event_type="agreed_to_terms")