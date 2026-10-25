import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import calculator  # noqa: E402


def test_add():
    assert calculator.add(2, 3) == 5


def test_subtract():
    assert calculator.subtract(5, 3) == 2


def test_multiply():
    assert calculator.multiply(4, 3) == 12


def test_divide():
    assert calculator.divide(8, 2) == 4


def test_divide_by_zero():
    import pytest
    with pytest.raises(ValueError):
        calculator.divide(1, 0)


def test_power():
    assert calculator.power(2, 3) == 8
