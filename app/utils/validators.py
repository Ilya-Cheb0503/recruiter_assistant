import re

def is_valid_phone(phone: str) -> bool:
    pattern = r'^\+7-\d{3}-\d{3}-\d{2}-\d{2}$'
    return re.fullmatch(pattern, phone.strip()) is not None

def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    return re.fullmatch(pattern, email.strip()) is not None
