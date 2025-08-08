
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

# Инструкция по настройке удаленного сервера и деплоя проекта Habit Tracker

## Настройка удаленного сервера

1. Установите Docker и Docker Compose:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. Клонируйте проект и перейдите в директорию:
   ```bash
   git clone https://github.com/HarryJurc/Habit_Tracker.git
   cd Habit_Tracker
   ```

3. Скопируйте файл `.env` из шаблона `.env.example` и заполните переменные окружения:
   ```bash
   cp .env.example .env
   # Отредактируйте .env по вашим настройкам, особенно DATABASE_URL и другие секреты
   ```

4. Запустите проект через Docker Compose:
   ```bash
   docker compose up -d --build
   ```

5. Проверьте работу сервисов:
   - Backend API доступен по адресу: `http://localhost:8000/`
   - PostgreSQL: подключитесь через pgAdmin/DBeaver (host: localhost, port: 5432)
   - Redis: проверьте через `redis-cli` или логи контейнера
   - Celery и Celery Beat: просматривайте логи командой
     ```bash
     docker compose logs -f celery
     docker compose logs -f celery-beat
     ```

---

## GitHub Actions workflow (CI/CD)

### Описание workflow

- При каждом push в ветку `main` запускаются тесты проекта.
- После успешного прохождения тестов проект автоматически деплоится на удаленный сервер через SSH.

### Основные шаги workflow

- Checkout кода
- Установка Python 3.9 и зависимостей
- Запуск тестов (`python manage.py test`)
- Копирование проекта на сервер через rsync с использованием SSH ключа
- Создание и активация виртуального окружения на сервере
- Установка зависимостей на сервере
- Применение миграций и сбор статики
- Перезапуск сервиса через systemctl

---

## Переменные окружения для workflow

В настройках GitHub репозитория добавьте секреты:

| Название        | Описание                              |
|-----------------|-------------------------------------|
| REMOTE_HOST     | IP или доменное имя сервера          |
| REMOTE_PORT     | SSH порт сервера (обычно 22)         |
| REMOTE_USER     | SSH пользователь                     |
| REMOTE_SSH_KEY  | Приватный SSH ключ (без пароля)      |
| DEPLOY_DIR      | Путь к директории проекта на сервере |

---

## Запуск workflow вручную

1. Сделайте push в ветку `main`.
2. Перейдите во вкладку **Actions** в вашем GitHub репозитории.
3. Выберите workflow **CI/CD Pipeline** и наблюдайте за прогрессом.

---

## Команды для работы с сервером

- Чтобы зайти на сервер по SSH:
  ```bash
  ssh -p <REMOTE_PORT> <REMOTE_USER>@<REMOTE_HOST>
  ```

- Остановить проект:
  ```bash
  docker compose down
  ```

- Выполнить миграции вручную:
  ```bash
  docker compose exec backend python manage.py migrate
  ```

- Зайти внутрь контейнера backend:
  ```bash
  docker compose exec backend bash
  ```
