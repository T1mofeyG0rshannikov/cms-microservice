from datetime import datetime

months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]


def get_date_in_russian(date: datetime):
    month = date.month
    day = date.day
    year = date.year

    return f"{day} {months[month - 1]} {year}"
