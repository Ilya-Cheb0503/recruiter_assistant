from aiogram.fsm.state import State, StatesGroup


class FormStates(StatesGroup):
    waiting_agreement = State()
    waiting_name = State()
    waiting_phone = State()
    waiting_email = State()
    waiting_region = State()
    waiting_position = State()
    waiting_experience = State()
    waiting_education_level = State()
    waiting_confirm = State()
