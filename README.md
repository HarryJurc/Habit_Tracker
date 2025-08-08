
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

---

## Как запустить проект через Docker Compose

1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/HarryJurc/Habit_Tracker.git
   cd Habit_Tracker
   ```

2. Создайте файл .env на основе .env.example и заполните переменные окружения:
   ```bash
   cp .env.example .env
   ```

3. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```

4. Открыть проект в браузере:
   - Backend API: http://localhost:8000/

## Как проверить работу сервисов

- **Backend**: откройте `http://localhost:8000/`, должны работать эндпоинты API.
- **PostgreSQL**: подключитесь к базе через pgAdmin или DBeaver (host: `localhost`, port: `5432`, логин и пароль из `.env`).
- **Redis**: проверьте подключение с помощью `redis-cli` или в логах контейнера.
- **Celery**: логи можно увидеть через:
  ```bash
  docker-compose logs -f celery
  ```
- **Celery Beat**: запустится планировщик периодических задач, можно смотреть через:
  ```bash
  docker-compose logs -f celery-beat
  ```

## Полезные команды
- Остановить проект:
  ```bash
  docker-compose down
  ```

- Выполнить миграции вручную:
  ```bash
  docker-compose exec backend python manage.py migrate
  ```

- попасть внутрь контейнера:
  ```bash
  docker-compose exec backend bash
  ```
