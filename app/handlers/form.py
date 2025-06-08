from operator import call
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from app.keyboards.agreement import get_agreement_kb
from app.states.form import FormStates
from app.database.models import save_user_data

from app.keyboards.reply.form_keyboard import region_button, experience_button, study_level_button, confim_button

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
    await call.message.answer('Для начала укажите в сообщении ваши ФИО:')
    await state.set_state(FormStates.waiting_name)
    await call.answer()

@router.message(FormStates.waiting_name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('Ваш контактный номер телефона:')
    await state.set_state(FormStates.waiting_phone)

@router.message(FormStates.waiting_phone)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(number=msg.text)
    await msg.answer('Ваш электронный адрес:')
    await state.set_state(FormStates.waiting_email)

@router.message(FormStates.waiting_email)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(email=msg.text)
    await msg.answer('Выбранный регион поиска:', reply_markup=region_button())
    await state.set_state(FormStates.waiting_region)

@router.message(FormStates.waiting_region)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(region=msg.text)
    await msg.answer('Желаемая должность:')
    await state.set_state(FormStates.waiting_position)

@router.message(FormStates.waiting_position)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(position=msg.text)
    await msg.answer('Ваш стаж:', reply_markup=experience_button())
    await state.set_state(FormStates.waiting_experience)

@router.message(FormStates.waiting_experience)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(experience=msg.text)
    await msg.answer('Ваш уровень образования:', reply_markup=study_level_button())
    await state.set_state(FormStates.waiting_study_level)

@router.message(FormStates.waiting_study_level)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(study_level=msg.text)
    data = await state.get_data()

    await msg.answer(
        text= f'''
ФИО:   
{data['name']}

Номер телефона:
{data['number']}

Email:
{data['email']}

Регион поиска:
{data['region']}

Должность:
{data['position']}

Опыт работы:
{data['experience']}

Образование:
{data['study_level']}
    ''',
    reply_markup=confim_button()
    )
    await state.set_state(FormStates.waiting_confirm)

@router.message(FormStates.waiting_phone)
async def get_phone(msg: Message, state: FSMContext):
    data = await state.get_data()
    await save_user_data(msg.from_user.id, data['name'], msg.text)
    await msg.answer('Спасибо! Анкета заполнена.')
    await state.clear()
