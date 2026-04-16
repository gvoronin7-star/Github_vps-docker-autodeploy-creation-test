# Time Server API

Простой FastAPI бэкэнд, возвращающий текущее время сервера.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn main:app --reload
```

## API Endpoints

### Время
- `GET /` — возвращает текущее время сервера
- `GET /time` — альтернативный эндпоинт для получения времени

### Дата
- `GET /date` — возвращает текущую дату сервера
- `GET /date/tomorrow` — возвращает дату завтрашнего дня
- `GET /date/diff?date1=YYYY-MM-DD&date2=YYYY-MM-DD` — разница между двумя датами

### Конвертация
- `POST /convert/timestamp` — конвертирует Unix timestamp в дату и время
- `GET /convert/datetime/{year}/{month}/{day}?hour=0&minute=0&second=0` — конвертирует дату в timestamp

## Пример ответа

### GET /time
```json
{
  "current_time": "2024-01-15T14:30:45.123456",
  "timestamp": 1705329045.123456
}
```

### GET /date
```json
{
  "current_date": "2024-01-15",
  "day_of_week": 0,
  "day_of_year": 15,
  "week_number": 3
}
```

### GET /date/diff?date1=2024-01-01&date2=2024-01-15
```json
{
  "days": 14,
  "weeks": 2,
  "months_approx": 0.46
}
```

## Swagger документация

После запуска откройте:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚀 CI/CD Автоматический деплой

### Как это работает

Каждый push на ветку `main` автоматически:
1. **Собирает Docker образ**
2. **Запушивает в GitHub Container Registry (GHCR)**
3. **Подключается к серверу через SSH**
4. **Запускает новый контейнер на порту 8001**

### Настройка секретов

В репозитории GitHub настрой следующие секреты:

| Secret | Значение |
|--------|----------|
| `SSH_HOST` | `89.169.169.92` |
| `SSH_USER` | `seahawk_gv_test1` |
| `SSH_KEY` | Приватный SSH-ключ |
| `SSH_PORT` | `22` |

### Просмотр workflow

```
https://github.com/gvoronin7-star/Github_vps-docker-autodeploy-creation-test/actions
```

### Доступ к приложению

После деплоя приложение доступно по адресу:
```
http://89.169.169.92:8001/time
http://89.169.169.92:8001/docs
```
