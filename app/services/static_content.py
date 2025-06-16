import json
from pathlib import Path

CONTENT_PATH = Path("static/static_content.json")

# Шаблон со всеми ключами, но пустыми строками
DEFAULT_TEMPLATE = {
  "welcome_message": ["Работает!", "Приветственный текст"], 
  "about_company": ["о", "О компании"],
  "advantages": ["Текст о преимуществах компании", "Преимущества компании"],
  "main_directions": ["Текст об основных направлениях", "Основные направления деятельности"],
  "company_enterprises": ["Текст о компаниях и предприятиях", "Компании и предприятия"],
  "contact_info": ["информация о доступных контактах", "Контактная информация"],
  "social_links": ["сети", "Социальные сети"]
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


CONTENT = load_content()