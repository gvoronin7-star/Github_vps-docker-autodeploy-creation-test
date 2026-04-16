# ⏰ FastAPI Time Server API

**Продвинутый FastAPI бэкэнд для работы со временем и датами с автоматическим CI/CD деплоем**

| Статус | Описание |
|--------|----------|
| **Версия** | 1.0.3 |
| **Framework** | FastAPI + Uvicorn |
| **Container** | Docker (Python 3.11 slim) |
| **CI/CD** | GitHub Actions + GHCR |
| **Deploy** | SSH на VPS (Yandex Cloud) |
| **Статус** | ✅ production-ready |

---

## 📍 Быстрая навигация

- [🚀 Быстрый старт](#быстрый-старт)
- [📡 API Endpoints](#api-endpoints)
- [🐳 Docker и CI/CD](#docker--ci-cd)
- [🔧 Настройка](#настройка)
- [📁 Структура проекта](#структура-проекта)

---

## 🚀 Быстрый старт

### Локальная разработка

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Открыть Swagger UI
# http://localhost:8000/docs
```

### Через Docker

```bash
# Сборка образа
docker build -t fastapi-time-server .

# Запуск контейнера
docker run -d --name fastapi-time-server -p 8000:8000 fastapi-time-server

# Проверка
curl http://localhost:8000/time

# Остановка
docker stop fastapi-time-server && docker rm fastapi-time-server
```

### Через Docker Compose

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 📡 API Endpoints

### Время и дата

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/` | Текущее время сервера |
| `GET` | `/time` | Текущее время сервера (альтернативный) |
| `GET` | `/date` | Текущая дата и информация о дне |
| `GET` | `/date/tomorrow` | Завтрашняя дата |
| `GET` | `/date/diff?date1=&date2=` | Разница между датами |

### Конвертация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `POST` | `/convert/timestamp` | Unix timestamp → дата и время |
| `GET` | `/convert/datetime/{year}/{month}/{day}` | Дата → Unix timestamp |

---

## 📋 Примеры ответов

### GET /time
```json
{
  "current_time": "2026-04-16T22:27:58.112294",
  "timestamp": 1776378478.112294
}
```

### GET /date
```json
{
  "current_date": "2026-04-16",
  "day_of_week": 3,
  "day_of_year": 106,
  "week_number": 16
}
```

### GET /date/tomorrow
```json
{
  "current_date": "2026-04-17",
  "day_of_week": 4,
  "day_of_year": 107,
  "week_number": 16
}
```

### GET /date/diff?date1=2026-04-01&date2=2026-04-16
```json
{
  "days": 15,
  "weeks": 2,
  "months_approx": 0.49
}
```

### POST /convert/timestamp
**Запрос:**
```json
{"timestamp": 1713286338}
```

**Ответ:**
```json
{
  "datetime": "2024-04-16T19:52:18",
  "date": "2024-04-16",
  "time": "19:52:18"
}
```

### GET /convert/datetime/2024/04/16?hour=12&minute=30&second=0
```json
{
  "datetime": "2024-04-16T12:30:00",
  "timestamp": 1713272400.0,
  "date": "2024-04-16",
  "time": "12:30:00"
}
```

---

## 🐳 Docker & CI/CD

### Автоматический деплой через GitHub Actions

Каждый `git push` на ветку `main` автоматически:

1. **Собирает Docker образ**
2. **Запушивает в GitHub Container Registry (GHCR)**
3. **Подключается к серверу через SSH**
4. **Обновляет контейнер**
5. **Проверяет работоспособность**

### 🌐 Production доступ

```
http://89.169.169.92:8001/time
http://89.169.169.92:8001/docs        # Swagger UI
http://89.169.169.92:8001/redoc       # ReDoc
```

### Образ в GHCR

```
ghcr.io/gvoronin7-star/github_vps-docker-autodeploy-creation-test:latest
```

### Workflow статус

[![Build and Deploy](https://github.com/gvoronin7-star/Github_vps-docker-autodeploy-creation-test/actions/workflows/deploy.yml/badge.svg)](https://github.com/gvoronin7-star/Github_vps-docker-autodeploy-creation-test/actions)

---

## 🔧 Настройка

### Секреты GitHub

Перед первым деплоем настройте секреты в репозитории:

**Settings → Secrets and variables → Actions → New repository secret**

| Secret | Значение | Описание |
|--------|----------|----------|
| `SSH_HOST` | `89.169.169.92` | IP сервера |
| `SSH_USER` | `seahawk_gv_test1` | Пользователь SSH |
| `SSH_KEY` | (приватный ключ) | SSH-ключ для доступа |
| `SSH_PORT` | `22` | Порт SSH |

### Создание SSH-ключа

```bash
# Генерация ключа
ssh-keygen -t ed25519 -C "github-actions@deploy"

# Добавление публичного ключа на сервер
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Копирование приватного ключа в GitHub
cat ~/.ssh/id_ed25519
```

---

## 📁 Структура проекта

```
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD workflow
├── .dockerignore               # Исключения для Docker build
├── .gitignore                  # Исключения для Git
├── DEPLOY.md                   # Документация по деплою
├── Dockerfile                  # Конфигурация Docker образа
├── README.md                   # Основная документация
├── docker-compose.yml          # Docker Compose конфигурация
├── main.py                     # FastAPI приложение
└── requirements.txt            # Python зависимости
```

---

## 📊 Полезные команды

### Управление контейнером

```bash
# Статус контейнера
docker ps | grep fastapi-time-server

# Логи контейнера
docker logs -f fastapi-time-server

# Перезапуск
docker restart fastapi-time-server

# Остановка и удаление
docker stop fastapi-time-server && docker rm fastapi-time-server

# Обновление образа
docker pull ghcr.io/gvoronin7-star/github_vps-docker-autodeploy-creation-test:latest
```

### Проверка приложения

```bash
# Проверка времени
curl http://89.169.169.92:8001/time

# Проверка здоровья
curl http://89.169.169.92:8001/docs

# Проверка через Docker
docker exec fastapi-time-server python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/time').read().decode())"
```

---

## 🛠️ Технологии

| Технология | Версия | Назначение |
|------------|--------|------------|
| **Python** | 3.11 | Язык программирования |
| **FastAPI** | >=0.104.0 | Web framework |
| **Uvicorn** | >=0.24.0 | ASGI сервер |
| **Pydantic** | 2.x | Валидация данных |
| **Docker** | 28+ | Контейнеризация |
| **GitHub Actions** | - | CI/CD |

---

## 📚 Документация

- **Swagger UI:** `http://89.169.169.92:8001/docs`
- **ReDoc:** `http://89.169.169.92:8001/redoc`
- **GitHub Actions:** [Смотреть workflow](https://github.com/gvoronin7-star/Github_vps-docker-autodeploy-creation-test/actions)
- **GHCR Registry:** [Смотреть образы](https://github.com/gvoronin7-star/Github_vps-docker-autodeploy-creation-test/pkgs/container/github_vps-docker-autodeploy-creation-test)

---

## 📝 История версий

| Версия | Дата | Изменения |
|--------|------|-----------|
| 1.0.3 | 2026-04-16 | Финальная настройка CI/CD, полная документация |
| 1.0.2 | 2026-04-16 | Финальное тестирование CI/CD |
| 1.0.1 | 2026-04-16 | Тест автоматического деплоя |
| 1.0.0 | 2026-04-16 | Первый релиз |

---

## 🤝 Вклад

Приветствуются pull requests и issues!

---

## 📄 Лицензия

MIT License
