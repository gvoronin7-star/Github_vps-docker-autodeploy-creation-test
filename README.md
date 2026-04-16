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

- `GET /` — возвращает текущее время сервера
- `GET /time` — альтернативный эндпоинт для получения времени

## Пример ответа

```json
{
  "current_time": "2024-01-15T14:30:45.123456",
  "timestamp": 1705329045.123456
}
```

## Swagger документация

После запуска откройте:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
