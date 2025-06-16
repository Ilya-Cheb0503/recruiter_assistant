import json
from pathlib import Path

CONTENT_PATH = Path("static/static_content.json")

# Шаблон со всеми ключами, но пустыми строками
DEFAULT_TEMPLATE = {

    "welcome_message": "Приветственный текст",

    "about_company": "Текст о компании",
    "advantages": "Текст о преимуществах компании",
    "main_directions": "Текст об основных направлениях",
    "company_enterprises": "Текст о компаниях и предприятиях",

    "contact_info": "Контактная информация",
    "social_links": "Социальные ссылки",
}

def load_content() -> dict:
    if not CONTENT_PATH.exists():
        # Файл не существует — создаём с пустыми значениями
        save_content(DEFAULT_TEMPLATE)
        return DEFAULT_TEMPLATE.copy()

    try:
        with open(CONTENT_PATH, encoding="utf-8") as f:
            content = json.load(f)
    except json.JSONDecodeError:
        # Если файл повреждён — перезаписываем шаблоном
        save_content(DEFAULT_TEMPLATE)
        return DEFAULT_TEMPLATE.copy()

    # Добавим недостающие ключи (если вдруг файл был неполный)
    for key in DEFAULT_TEMPLATE:
        if key not in content:
            content[key] = ""

    return content

def save_content(data: dict):
    # Обеспечим наличие всех ключей при сохранении
    for key in DEFAULT_TEMPLATE:
        data.setdefault(key, "")
    with open(CONTENT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
