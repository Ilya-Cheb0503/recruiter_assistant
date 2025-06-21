from aiogram.fsm.state import State, StatesGroup

class FormStates(StatesGroup):
    waiting_agreement = State()          # Согласие на обработку
    waiting_name = State()               # Ввод ФИО
    waiting_phone = State()              # Ввод телефона
    waiting_email = State()              # Ввод email
    waiting_region = State()             # Ввод региона
    waiting_position = State()           # Ввод должности
    waiting_experience = State()         # Ввод опыта
    waiting_education_level = State()    # Ввод образования

    waiting_confirm = State()            # Подтверждение анкеты
    waiting_field_to_edit = State()      # Пользователь выбрал, что редактировать
    waiting_field_value = State()        # Пользователь вводит новое значение поля
    waiting_main_menu = State()          # Переход в главное меню после подтверждения верности анкеты

    waiting_for_new_content = State()    # Ожидание нового контента от администратора

    waiting_for_region = State()
    waiting_check_region = State()
    vacansies_transmission = State()