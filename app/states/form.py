from aiogram.fsm.state import StatesGroup, State

class FormStates(StatesGroup):
    waiting_agreement = State()
    waiting_name = State()
    waiting_phone = State()
