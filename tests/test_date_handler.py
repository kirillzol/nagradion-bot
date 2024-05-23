import pytest
from src.date_handler import compare_dates


def test_compare_dates_exact_now():
    dt2 = 'Пн 20.05 15:00'
    dt1 = 'Вт 28.05 15:00'
    assert not compare_dates(dt2)
    assert compare_dates(dt1)
