# app/handlers/form/form_fill.py
import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.states.state_user_form import FormStates
from app.keyboards.reply.form_keyboard import (
    region_button,
    experience_button,
    education_level_button,
    get_edit_fields_keyboard
)
from app.keyboards.inline.form_keyboard import confim_button
from app.keyboards.inline.menu import get_main_menu
from app.utils.format_form import format_user_form
from app.database.models import save_user_data
from app.bot_text.main_menu import welcome_message


router = Router()


@router.message(FormStates.waiting_name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('Ваш контактный номер телефона:')
    await state.set_state(FormStates.waiting_phone)


@router.message(FormStates.waiting_phone)
async def get_phone_number(msg: Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await msg.answer('Ваш электронный адрес:')
    await state.set_state(FormStates.waiting_email)


@router.message(FormStates.waiting_email)
async def get_email(msg: Message, state: FSMContext):
    await state.update_data(email=msg.text)
    await msg.answer('Выбранный регион поиска:', reply_markup=region_button())
    await state.set_state(FormStates.waiting_region)


@router.message(FormStates.waiting_region)
async def get_user_region(msg: Message, state: FSMContext):
    await state.update_data(region=msg.text)
    await msg.answer('Желаемая должность:')
    await state.set_state(FormStates.waiting_position)


@router.message(FormStates.waiting_position)
async def get_position(msg: Message, state: FSMContext):
    await state.update_data(position=msg.text)
    await msg.answer('Ваш стаж:', reply_markup=experience_button())
    await state.set_state(FormStates.waiting_experience)


@router.message(FormStates.waiting_experience)
async def get_experience(msg: Message, state: FSMContext):
    await state.update_data(experience=msg.text)
    await msg.answer('Ваш уровень образования:', reply_markup=education_level_button())
    await state.set_state(FormStates.waiting_education_level)


@router.message(FormStates.waiting_education_level)
async def check_user_form(msg: Message, state: FSMContext):
    await state.update_data(education=msg.text)
    data = await state.get_data()
    await msg.answer(format_user_form(data), reply_markup=confim_button())
    await state.set_state(FormStates.waiting_confirm)


@router.callback_query(F.data == "form_confirm", FormStates.waiting_confirm)
async def confirm_form(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await save_user_data(callback.from_user.id, **data)
    await callback.message.edit_text("Спасибо! Анкета заполнена ✅\nВозвращаем вас в Главное меню.")
    await asyncio.sleep(2)
    await callback.message.edit_text(welcome_message, reply_markup=get_main_menu(callback.from_user.id))
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "form_edit", FormStates.waiting_confirm)
async def edit_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Что вы хотите изменить?", reply_markup=get_edit_fields_keyboard())
    await state.set_state(FormStates.waiting_field_to_edit)
    await callback.answer()


@router.callback_query(F.data.startswith("edit_"), FormStates.waiting_field_to_edit)
async def handle_field_choice(callback: CallbackQuery, state: FSMContext):
    field_map = {
        "edit_name": ("name", "Введите ваше ФИО:"),
        "edit_phone": ("phone", "Введите номер телефона:"),
        "edit_email": ("email", "Введите email:"),
        "edit_region": ("region", "Введите предпочтительный регион:"),
        "edit_position": ("position", "Введите вашу должность:"),
        "edit_experience": ("experience", "Введите опыт работы:"),
        "edit_education": ("education", "Введите уровень образования:"),
    }

    field_key = callback.data
    if field_key not in field_map:
        await callback.answer("Ошибка выбора.")
        return

    field_name, prompt = field_map[field_key]
    await state.update_data(current_edit_field=field_name)

    # Удаляем предыдущее сообщение
    await callback.message.delete()

    # Добавляем клавиатуру с регионами
    if field_key == "edit_region":
        await callback.message.answer(prompt, reply_markup=region_button())
        await state.set_state(FormStates.waiting_field_value)
    elif field_key == "edit_experience":
        # await callback.message.delete()
        await callback.message.answer(prompt, reply_markup=experience_button())
        await state.set_state(FormStates.waiting_field_value)
        # await callback.message.delete()
    elif field_key == "edit_education":
        await callback.message.answer(prompt, reply_markup=education_level_button())
        await state.set_state(FormStates.waiting_field_value)
    else:
        await callback.message.edit_text(prompt)
        await state.set_state(FormStates.waiting_field_value)

    await callback.answer()


@router.message(FormStates.waiting_field_value)
async def receive_new_value(msg: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("current_edit_field")

    if field:
        await state.update_data({field: msg.text})

    data = await state.get_data()
    await msg.answer(format_user_form(data), reply_markup=confim_button())
    await state.set_state(FormStates.waiting_confirm)


@router.callback_query(F.data == "back_to_confirm", FormStates.waiting_field_to_edit)
async def back_to_confirmation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(format_user_form(data), reply_markup=confim_button())
    await state.set_state(FormStates.waiting_confirm)
    await callback.answer()