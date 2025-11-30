from app import parse_number, calculate
from decimal import Decimal
import pytest


def test_parse_ok():
    assert parse_number(" 3.5 ") == Decimal("3.5")


def test_parse_bad():
    with pytest.raises(ValueError):
        parse_number("abc")


def test_calc_basic():
    assert calculate(Decimal("2"), Decimal("3"), "+") == Decimal("5")


def test_divide_zero():
    with pytest.raises(ZeroDivisionError):
        calculate(Decimal("1"), Decimal("0"), "/")
        