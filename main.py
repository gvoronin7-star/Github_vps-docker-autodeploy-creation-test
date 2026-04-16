from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(title="Time Server API")


class TimeResponse(BaseModel):
    current_time: str
    timestamp: float


@app.get("/", response_model=TimeResponse)
async def root():
    """Возвращает текущее время сервера"""
    now = datetime.now()
    return TimeResponse(
        current_time=now.isoformat(),
        timestamp=now.timestamp()
    )


@app.get("/time", response_model=TimeResponse)
async def get_time():
    """Эндпоинт для получения текущего времени сервера"""
    now = datetime.now()
    return TimeResponse(
        current_time=now.isoformat(),
        timestamp=now.timestamp()
    )
