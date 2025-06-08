from operator import call
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from app.keyboards.agreement import get_agreement_kb
from app.states.form import FormStates
from app.database.models import save_user_data

router = Router()


@router.callback_query(F.data == 'submit_form')
async def job_search_handler(callback: CallbackQuery, state: FSMContext):
    pdf = FSInputFile('static/agreement.pdf')
    await callback.answer()
    await callback.message.answer_document(pdf, caption='Вы согласны с политикой обработки данных?', reply_markup=get_agreement_kb())
    await state.set_state(FormStates.waiting_agreement)


@router.message(F.text.lower() == 'анкета')
async def ask_agreement(msg: Message, state: FSMContext):
    pdf = FSInputFile('static/agreement.pdf')
    await msg.answer_document(pdf, caption='Пожалуйста, ознакомьтесь и согласитесь')
    await msg.answer('Вы согласны с политикой обработки данных?', reply_markup=get_agreement_kb())
    await state.set_state(FormStates.waiting_agreement)

@router.callback_query(FormStates.waiting_agreement, F.data == 'agree')
async def agreed(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите ваше ФИО:')
    await state.set_state(FormStates.waiting_name)
    await call.answer()

@router.message(FormStates.waiting_name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('Введите номер телефона:')
    await state.set_state(FormStates.waiting_phone)

@router.message(FormStates.waiting_phone)
async def get_phone(msg: Message, state: FSMContext):
    data = await state.get_data()
    await save_user_data(msg.from_user.id, data['name'], msg.text)
    await msg.answer('Спасибо! Анкета заполнена.')
    await state.clear()
