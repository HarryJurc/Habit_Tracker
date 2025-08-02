
# Habit Tracker Backend

Backend API для приложения трекера привычек, реализованное на Django и Django REST Framework.

## Описание

Этот сервис позволяет пользователям создавать, читать, обновлять и удалять свои привычки. Есть возможность делать привычки публичными, чтобы другие пользователи могли их видеть. Поддерживается пагинация и проверка прав доступа.

---

## Установка и запуск

### Требования

- Python 3.8+
- Poetry (рекомендуется) или pip
- PostgreSQL (или любая другая БД, которую используешь)

### Установка через Poetry

```bash
poetry install
poetry shell
python manage.py migrate
python manage.py runserver
```

### Установка через pip

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## Использование API

- **GET /habits/** — получить список своих привычек
- **GET /habits/?public=true** — получить список публичных привычек
- **POST /habits/** — создать новую привычку
- **PATCH /habits/{id}/** — обновить привычку (только свои)
- **DELETE /habits/{id}/** — удалить привычку (только свои)

---

## Тестирование

Запуск тестов:

```bash
python manage.py test habits
```

---

## Линтеры

Для проверки кода используется flake8.

Запуск линтера:

```bash
flake8
```