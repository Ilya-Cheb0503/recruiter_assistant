from aiogram.fsm.state import State, StatesGroup


class FormStates(StatesGroup):
    waiting_agreement = State()
    waiting_name = State()
    waiting_phone = State()
