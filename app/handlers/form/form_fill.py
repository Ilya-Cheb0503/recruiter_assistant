import asyncio

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.models import save_user_data
from app.keyboards.inline.form_keyboard import confim_button
from app.keyboards.inline.menu import get_main_menu
from app.keyboards.reply.form_keyboard import (education_level_button,
                                               experience_button,
                                               get_edit_fields_keyboard,
                                               region_button)
from app.services.static_content import load_content
from app.states.state_user_form import FormStates
from app.utils.format_form import format_user_form
from app.utils.metrics import log_event
from app.utils.validators import is_valid_email, is_valid_phone

router = Router()


@router.message(FormStates.waiting_name)
async def get_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer('Ваш контактный номер телефона:')
    await state.set_state(FormStates.waiting_phone)


@router.message(FormStates.waiting_phone)
async def get_phone_number(msg: Message, state: FSMContext):
    if not is_valid_phone(msg.text):
        await msg.answer("❗️Неверный формат номера телефона.\nПожалуйста, укажите Ваш контактный номер телефона в формате +7-***-***-**-**")
        return
    await state.update_data(phone=msg.text)
    await msg.answer("Пожалуйста, укажите Ваш электронный адрес в формате ivanov.ivan@mail.ru")
    await state.set_state(FormStates.waiting_email)


@router.message(FormStates.waiting_email)
async def get_email(msg: Message, state: FSMContext):
    if not is_valid_email(msg.text):
        await msg.answer("❗️Неверный формат электронного адреса.\nПожалуйста, укажите email в формате ivanov.ivan@mail.ru")
        return
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

    # Фильтрация только нужных полей
    allowed_fields = {
        "name", "phone", "email", "region",
        "position", "experience", "education"
    }
    filtered_data = {k: v for k, v in data.items() if k in allowed_fields}

    await save_user_data(callback.from_user.id, **filtered_data)
    await callback.message.edit_text("Спасибо! Анкета заполнена ✅\nВозвращаем вас в Главное меню.")
    await asyncio.sleep(2)
    content = load_content()
    await callback.message.edit_text(content.get('welcome_message')[0], reply_markup=get_main_menu(callback.from_user.id))
    await state.clear()
    await callback.answer()
    await log_event(user_id=callback.from_user.id, event_type="form_submit")


@router.callback_query(F.data == "form_edit", FormStates.waiting_confirm)
async def edit_form(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Что вы хотите изменить?", reply_markup=get_edit_fields_keyboard())
    await state.set_state(FormStates.waiting_field_to_edit)
    await callback.answer()


@router.callback_query(F.data.startswith("edit_"), FormStates.waiting_field_to_edit)
async def handle_field_choice(callback: CallbackQuery, state: FSMContext):
    field_key = callback.data.removeprefix("edit_")

    field_map = {
        "name": ("name", "Введите ваше ФИО:", None, "inline"),
        "phone": ("phone", "Введите номер телефона:", None, "inline"),
        "email": ("email", "Введите email:", None, "inline"),
        "region": ("region", "Введите предпочтительный регион:", region_button(), "reply"),
        "position": ("position", "Введите вашу должность:", None, "inline"),
        "experience": ("experience", "Введите опыт работы:", experience_button(), "reply"),
        "education": ("education", "Введите уровень образования:", education_level_button(), "reply")
    }

    if field_key not in field_map:
        return await callback.answer("Ошибка выбора.")

    field_name, prompt, keyboard, keyboard_type = field_map[field_key]

    await state.update_data(current_edit_field=field_name)

    if keyboard_type == "reply":
        # Удаляем inline-сообщение и отправляем новое с reply-клавиатурой
        await callback.message.delete()
        await callback.message.answer(prompt, reply_markup=keyboard)
    else:
        # Редактируем inline-сообщение
        await callback.message.edit_text(prompt, reply_markup=keyboard)

    await state.set_state(FormStates.waiting_field_value)
    await callback.answer()



@router.message(FormStates.waiting_field_value)
async def receive_new_value(msg: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get("current_edit_field")

    if not field:
        return await msg.answer("Произошла ошибка. Попробуйте снова.")

    # Валидация email и телефона при редактировании
    if field == "phone" and not is_valid_phone(msg.text):
        return await msg.answer("❗️Неверный формат номера телефона.\nПожалуйста, укажите номер в формате +7-***-***-**-**")

    if field == "email" and not is_valid_email(msg.text):
        return await msg.answer("❗️Неверный формат email.\nПожалуйста, укажите адрес в формате ivanov.ivan@mail.ru")

    await state.update_data({field: msg.text})
    updated_data = await state.get_data()
    await msg.answer(format_user_form(updated_data), reply_markup=confim_button())
    await state.set_state(FormStates.waiting_confirm)


@router.callback_query(F.data == "back_to_confirm", FormStates.waiting_field_to_edit)
async def back_to_confirmation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(format_user_form(data), reply_markup=confim_button())
    await state.set_state(FormStates.waiting_confirm)
    await callback.answer()