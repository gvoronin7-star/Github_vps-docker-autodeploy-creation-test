from fastapi import FastAPI, Query
from datetime import datetime, date, timedelta
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Time Server API")


class TimeResponse(BaseModel):
    current_time: str
    timestamp: float


class DateResponse(BaseModel):
    current_date: str
    day_of_week: int
    day_of_year: int
    week_number: int


class DateDiffResponse(BaseModel):
    days: int
    weeks: int
    months_approx: float


class ConvertRequest(BaseModel):
    timestamp: float


class ConvertResponse(BaseModel):
    datetime: str
    date: str
    time: str


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


@app.get("/date", response_model=DateResponse)
async def get_date():
    """Возвращает текущую дату сервера"""
    today = date.today()
    now = datetime.now()
    return DateResponse(
        current_date=today.isoformat(),
        day_of_week=now.weekday(),
        day_of_year=now.timetuple().tm_yday,
        week_number=now.isocalendar()[1]
    )


@app.get("/date/tomorrow", response_model=DateResponse)
async def get_tomorrow():
    """Возвращает дату завтрашнего дня"""
    tomorrow = date.today() + timedelta(days=1)
    return DateResponse(
        current_date=tomorrow.isoformat(),
        day_of_week=tomorrow.weekday(),
        day_of_year=tomorrow.timetuple().tm_yday,
        week_number=tomorrow.isocalendar()[1]
    )


@app.get("/date/diff")
async def date_diff(
    date1: str = Query(..., description="Первая дата в формате YYYY-MM-DD"),
    date2: str = Query(..., description="Вторая дата в формате YYYY-MM-DD")
):
    """Вычисляет разницу между двумя датами"""
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d").date()
        d2 = datetime.strptime(date2, "%Y-%m-%d").date()
        
        diff = abs((d2 - d1).days)
        
        return DateDiffResponse(
            days=diff,
            weeks=diff // 7,
            months_approx=diff / 30.44
        )
    except ValueError as e:
        return {"error": f"Неверный формат даты. Используйте YYYY-MM-DD: {str(e)}"}


@app.post("/convert/timestamp", response_model=ConvertResponse)
async def convert_timestamp(request: ConvertRequest):
    """Конвертирует Unix timestamp в дату и время"""
    dt = datetime.fromtimestamp(request.timestamp)
    return ConvertResponse(
        datetime=dt.isoformat(),
        date=dt.date().isoformat(),
        time=dt.time().isoformat()
    )


@app.get("/convert/datetime/{year}/{month}/{day}")
async def convert_datetime(
    year: int,
    month: int,
    day: int,
    hour: int = Query(0, ge=0, le=23),
    minute: int = Query(0, ge=0, le=59),
    second: int = Query(0, ge=0, le=59)
):
    """Конвертирует дату и время в timestamp"""
    try:
        dt = datetime(year, month, day, hour, minute, second)
        return {
            "datetime": dt.isoformat(),
            "timestamp": dt.timestamp(),
            "date": dt.date().isoformat(),
            "time": dt.time().isoformat()
        }
    except ValueError as e:
        return {"error": f"Неверная дата: {str(e)}"}
