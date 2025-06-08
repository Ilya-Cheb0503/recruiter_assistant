from aiogram.fsm.state import StatesGroup, State

class FormStates(StatesGroup):
    waiting_agreement = State()
    waiting_name = State()
    waiting_phone = State()
    waiting_email = State()
    waiting_region = State()
    waiting_position = State()
    waiting_experience = State()
    waiting_study_level = State()
    waiting_confirm = State()
