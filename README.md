# Task manager

Проект **task manager** — это backend-приложение, разработанное с использованием FastAPI, SQLAlchemy и Dishka (внедрение зависимостей).
Он спроектирован с чистой архитектурой, акцентом на модульность и тестируемость компонентов.

---

## 🚀 Технологии

- **FastAPI** — асинхронный веб-фреймворк для создания REST API
- **SQLAlchemy** — ORM для работы с PostgreSQL
- **Dishka** — библиотека для внедрения зависимостей
- **Pytest** — фреймворк для тестирования

---

## 📁 Структура проекта

```bash
task-manager/
├── backend/
│   └── api/
│       └── v1/
│           ├── handlers/             # Обработка запросов, маршруты, HTTP-интерфейс
│           ├── application/          # Бизнес-логика и сценарии использования
│           │   └── task/             # Компонент пользователя
│           │       ├── dto.py
│           │       ├── exceptions.py
│           │       ├── interactors.py
│           │       ├── interfaces.py
│           │       └── validators.py
│           ├── domen/                # Доменные сущности (чистые Python-классы)
│           ├── infrastructure/       # Работа с БД, файлами и внешними сервисами
│           │   ├── db/
│           │   │   ├── database.py
│           │   │   ├── exceptions.py
│           │   │   ├── models.py
│           │   │   └── repositories.py
│           ├── config.py             # Конфигурация FastAPI, PostgreSQL
│           ├── ioc.py                # DI-контейнеры Dishka
│           ├── main.py               # Точка входа FastAPI
│           ├── migrations/           # Миграции (если есть)
│           └── test_handlers.py      # Интеграционные тесты через HTTP-клиент
├── requirements.txt
└── README.md
```

---

## ⚙ Конфигурация

```python
class Config(BaseModel):
    postgres: PostgresConfig
    fastapi: FastApiConfig

  
```

Каждая секция конфигурируется через переменные окружения. Пример `.env`:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=postgres

```

---

## 🧪 Тестирование

```bash
pytest
```

---

## 🧱 Архитектура

Проект построен по принципам **чистой архитектуры**:

- **handlers** — внешний слой, взаимодействующий с клиентом (HTTP).
- **application** — прикладная бизнес-логика, разделённая по доменным компонентам.
- **domen** — ядро с доменными сущностями.
- **infrastructure** — адаптеры к базе данных, файлам и другим технологиям.
- **ioc** — конфигурация внедрения зависимостей.

---

## 📦 Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Запуск

```bash
uvicorn backend.api.v1.main:app --reload
```

---

## 🐳 Запуск через Docker Compose

Требуется Docker и Docker Compose.

1. (Опционально) Создайте `.env` с нужными значениями (совпадают с дефолтами в config.py).
2. Соберите и запустите:
   ```bash
   docker compose up --build
   ```
3. Приложение: http://localhost:8000/docs
4. Postgres: порт 5432 (user: postgres / password: password / db: postgres)

Остановка:

```bash
docker compose down
```

Очистка данных:

```bash
docker compose down -v
```

Горячих перезапусков кода нет (образ собирается заново). Для разработки можно убрать :ro у volume в backend.
