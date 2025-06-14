from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.inline.menu import (get_job_by_categories_menu,
                                   get_job_seeking_menu)
from services.vacancy_service import get_all_vacancies
from utils.vacancy_sender import send_vacancy_batch
from services.vacancy_service import get_vacancies_by_keywords_list, get_vacancies_no_experience
from app.keywords.categories_keywords import keywords
from aiogram.fsm.context import FSMContext


router = Router()


@router.callback_query(F.data.startswith("region_"))
async def region_selected_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    region = callback.data.replace("region_", "")
    await state.update_data(region=region)  # сохраняем регион в FSM

    await callback.message.edit_text(
        f"Выбран регион: {region}\nТеперь выберите, как искать вакансии:",
        reply_markup=get_job_seeking_menu()
    )


# @router.callback_query(F.data == 'job_search_with_current_region')
# async def job_search_handler(callback: CallbackQuery, state: FSMContext):
#     data = state.get_data()
#     region = data["region"]
#     print(region)

#     await callback.answer()
#     await callback.message.edit_text(
#         f"Выбран регион: {region}\nТеперь выберите, как искать вакансии:",
#         reply_markup=get_job_seeking_menu()
#     )

    
@router.callback_query(F.data == 'categories_vacancies')
async def vacancies_by_keywords_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Выберите подраздел", reply_markup=get_job_by_categories_menu())


@router.callback_query(F.data.startswith("vacancies_"))
async def vacancy_pagination_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split("_")

    if len(parts) < 2:
        await callback.message.answer("Некорректная команда.")
        return

    category = parts[1]  # all, noexp, keywords и т.п.
    offset = int(parts[2]) if len(parts) >= 3 and parts[2].isdigit() else 0

    # Получаем сохранённый регион пользователя из FSM
    user_data = await state.get_data()
    user_region = user_data.get("region", "Москва")  # дефолт если нет данных

    if category == "all":
        vacancies = await get_all_vacancies(user_region)

    elif category == "management":
        vacancies = await get_vacancies_by_keywords_list(keywords['Руководители'], user_region)

    elif category == "engineering":
        vacancies = await get_vacancies_by_keywords_list(keywords['ИТР'], user_region)

    elif category == "workers":
        vacancies = await get_vacancies_by_keywords_list(keywords['Рабочие'], user_region)

    elif category == "other":
        vacancies = await get_vacancies_by_keywords_list(keywords['Другие категории'], user_region)

    elif category == "noexp":
        vacancies = await get_vacancies_no_experience(user_region)

    elif category == "keywords":
        user_keywords = user_data.get("keywords", ["инженер", "конструктор"])  # если задаётся вручную
        vacancies = await get_vacancies_by_keywords_list(user_keywords, user_region)

    else:
        await callback.message.answer("Ошибка: неизвестная категория.")
        print(f"Unknown category: {category}")
        return

    await send_vacancy_batch(
        callback.message,
        vacancies,
        start_index=offset,
        category=category
    )