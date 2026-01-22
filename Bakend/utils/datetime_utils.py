"""Utilidades de fecha y hora.
Funciones para manipulación y formateo de fechas y horas."""
from datetime import date, datetime, timedelta

def is_future_date(date: datetime) -> bool:
    return date > datetime.now()

def Datetime_to_Date_and_Date(day: datetime) -> tuple:
    """Convierte un datetime a una tupla de (fecha, hora)."""
    start = datetime.combine(day, datetime.min.time())
    end = start + timedelta(days=1)
    return start, end