from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from app.database.models import Vacancy

VACANCIES_PER_PAGE = 5

def get_vacancy_keyboard(url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
        InlineKeyboardButton(text="Откликнуться", callback_data="respond_direct"),
        ],
        [
        InlineKeyboardButton(text="Через сайт", url=url)
        ]
])

def get_pagination_keyboard(current: int, total: int, category: str) -> InlineKeyboardMarkup:
    buttons = []

    if current < total:
        buttons.append([InlineKeyboardButton(text="Еще 5", callback_data=f"vacancies_{category}_{current}")])

    buttons.append([InlineKeyboardButton(text="Достаточно", callback_data="main_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)



async def send_vacancy_batch(
    message: Message | CallbackQuery,
    vacancies: list[Vacancy],
    start_index: int = 0,
    category: str = "all"
) -> None:
    if not vacancies:
        await message.answer("По вашему запросу вакансий не найдено.")
        return

    batch = vacancies[start_index:start_index + VACANCIES_PER_PAGE]
    total = len(vacancies)

    for v in batch:
        text = (
            f"📌 <b>{v.title}</b>\n"
            f"🏢 {v.company or '-'}\n"
            f"📍 {v.region or '-'}\n"
            f"💰 {v.salary_from or 'от —'} — {v.salary_to or 'до —'}\n\n"
            f"<b>Требования:</b>\n{v.requirements or '—'}\n\n"
            f"<b>Обязанности:</b>\n{v.responsibilities or '—'}"
        )
        await message.answer(text, reply_markup=get_vacancy_keyboard(v.url), parse_mode="HTML")

    viewed = start_index + len(batch)
    text = (
        f"Всего вакансий: {total}\n"
        f"Вы просмотрели {viewed} из них"
    )

    if viewed < total:
        text += "\nПоказать ещё вакансии или остановиться?"
    else:
        text += "\nВы просмотрели все доступные вакансии."

    await message.answer(
        text,
        reply_markup=get_pagination_keyboard(viewed, total, category=category)
    )
