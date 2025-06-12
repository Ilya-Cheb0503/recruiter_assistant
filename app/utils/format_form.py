# app/utils/format_form.py


def format_user_form(data: dict) -> str:
    name = data.get("name", "—")
    phone = data.get("phone", "—")
    email = data.get("email", "—")
    region = data.get("region", "—")
    position = data.get("position", "—")
    experience = data.get("experience", "—")
    education = data.get("education", "—")

    return (
        f"📋 Ваша анкета:\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"✉️ Email: {email}\n"
        f"🌍 Регион поиска: {region}\n"
        f"💼 Должность: {position}\n"
        f"⏳ Стаж: {experience}\n"
        f"🎓 Образование: {education}\n\n"
        f"✅ Всё верно?"
        
    )
