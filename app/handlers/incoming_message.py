import asyncio

from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.states.state_user_form import FormStates
from app.services.vacancy_service import get_vacancies_by_keyword_and_region
from app.keyboards.reply.form_keyboard import region_button

from utils.vacancy_sender import send_vacancy_batch


router = Router()


@router.message(FormStates.waiting_for_region)
async def get_first_region(msg: Message, state: FSMContext):
    print(f"Функция {get_first_region.__name__}")
    user_data = await state.get_data()
    keyword = user_data.get("user_keyword")

    await state.update_data(region=msg.text)
    await vacansies_transmission(msg, user_keyword=keyword, region=msg.text)


@router.message(F.text)
async def get_incoming_message(msg: Message, state: FSMContext):
    print(f"Функция {get_incoming_message.__name__}")
    current_state = await state.get_state()

    if msg.text.lower() in ["/start", "главное меню"]:
        return
    elif current_state and current_state.startswith("FormStates"):
        return
    await check_region(msg, state)
    print(f"Функция {get_incoming_message.__name__} завершилась")
    

async def check_region(msg: Message, state: FSMContext):
    print(f"Функция {check_region.__name__}")

    # Получаем сохранённый регион пользователя из FSM
    user_data = await state.get_data()
    user_region = user_data.get("region")
    await state.update_data(user_keyword=msg.text)

    if user_region is None:
        await msg.answer(text="Вы не указали регион для поиска вакансий❌\nВыберет регион из предложенных вариантов.", reply_markup=region_button())
        await state.set_state(FormStates.waiting_for_region)
        print(f"Функция {check_region.__name__} перед return")
        return
    
    await vacansies_transmission(msg, user_keyword=msg.text, region=user_region)


async def vacansies_transmission(msg: Message, user_keyword: str, region: str):
    print(f"Функция {vacansies_transmission.__name__}")

    vacancies = await get_vacancies_by_keyword_and_region(user_keyword, region)
    await send_vacancy_batch(
    message=msg,
    vacancies=vacancies
    )