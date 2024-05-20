from datetime import datetime
import locale


def compare_dates(date_str):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    now = datetime.now()
    date_obj = datetime.strptime(date_str, "%a %d.%m %H:%M")
    date_obj = date_obj.replace(year=now.year)

    if date_obj >= now:
        return True
    else:
        return False
