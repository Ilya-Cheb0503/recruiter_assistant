import asyncio

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.states.state_user_form import FormStates
from app.services.vacancy_service import get_vacancies_by_keyword_and_region
from utils.vacancy_sender import send_vacancy_batch


router = Router()


@router.message(F.text)
async def get_incoming_message(msg: Message, state: FSMContext):
    current_state = await state.get_state()

    if msg.text.lower() in ["/start", "главное меню"]:
        return
    elif current_state and current_state.startswith("FormStates"):
        return

    # Получаем сохранённый регион пользователя из FSM
    user_data = await state.get_data()
    user_region = user_data.get("region", "Москва")  # дефолт если нет данных

    vacancies = await get_vacancies_by_keyword_and_region(msg.text, user_region)
    await send_vacancy_batch(
    message=msg,
    vacancies=vacancies
    )
        