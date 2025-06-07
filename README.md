Вот обновлённый `README.md` для твоего проекта Telegram-бота на `Aiogram 3` с использованием `SQLite` и `Alembic`:

---

````markdown
# 🤖 Telegram Recruiter Assistant Bot

Асинхронный Telegram-бот на `Aiogram 3`, предназначенный для автоматизации рекрутинга. Поддерживает FSM-анкету, работу с базой данных, админ-панель и миграции через Alembic.

---

## 📦 Стек технологий

- Python 3.11+
- Aiogram 3.x
- SQLAlchemy (async)
- Alembic
- SQLite (по умолчанию)
- python-dotenv

---

## ⚙️ Установка и запуск проекта

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
````

### 2. Создайте виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Настройте `.env`

Создайте файл `.env` в корне и укажите:

```env
BOT_TOKEN=your_telegram_bot_token
ADMINS=123456789,987654321
DB_URL=sqlite+aiosqlite:///./dev.db
```

* `BOT_TOKEN` — токен вашего Telegram-бота.
* `ADMINS` — Telegram ID администраторов через запятую.
* `DB_URL` — строка подключения к БД (по умолчанию SQLite).

---

## 🛠️ Работа с базой данных

### 1. Инициализация Alembic (уже выполнена)

Если нужно переинициализировать:

```bash
alembic init alembic
```

### 2. Генерация миграции

```bash
alembic revision --autogenerate -m "Initial"
```

### 3. Применение миграции

```bash
alembic upgrade head
```

После этого создастся `dev.db` с таблицей `users`.

---

## 🚀 Запуск бота

```bash
python run.py
```

---

## 🧪 Проверка функционала

* Напишите `/start` боту.
* Введите команду `анкета` — запустится FSM для ввода имени и телефона.
* Введённые данные сохраняются в БД (`users`).

---

## 📁 Структура проекта

```
├── app/
│   ├── main.py
│   ├── handlers/
│   ├── database/
│   └── ...
├── alembic/
│   ├── versions/
│   └── env.py
├── .env
├── dev.db
├── run.py
├── README.md
└── requirements.txt
```

---

## 📌 Дополнительно

* Можно легко переключиться на PostgreSQL, заменив `DB_URL` и установив `asyncpg`.
* Поддержка админов встроена: проверка `tg_id` из `.env`.

---

## 🧼 TODO

* [ ] Подключение к hh.ru API
* [ ] Админ-панель через inline-кнопки
* [ ] Рассылка метрик и логов
* [ ] Поддержка MySQL/PostgreSQL на сервере
