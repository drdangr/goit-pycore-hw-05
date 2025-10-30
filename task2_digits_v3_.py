import re
from typing import Callable, Iterator

_NUMBER_RE = re.compile(r'(?<= )[+-]?\d+(?:\.\d+)?(?= )')  # (?<= ), (?= ) — перевірка вперед та назад на " "


def generator_numbers(text: str) -> Iterator[float]:
    """find all numbers in the text and return them one by one as floats."""
    for m in _NUMBER_RE.finditer(text):
        yield float(m.group()) 

def sum_profit(text: str, func: Callable) -> float:
    """We sum up all the numbers found in the text using the transferred generator function."""
    return sum(func(text))


# рабочий код
if __name__ == "__main__": # for testing
    text = ("Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів.")
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")  # => 1351.46
