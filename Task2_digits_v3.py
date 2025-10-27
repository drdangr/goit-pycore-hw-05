import re
from typing import Callable, Iterator

# Number: optional sign, integer part, optional fractional part after a period
# Edge restrictions: no non-whitespace characters before/after (i.e., space or line boundary)

#Regulator for searching for valid numbers in the text:

#(?<!\S) — negative lookback: no non-whitespace character on the left ⇒ either a space or the beginning of a line on the left.
#[+-]? — optional + or - sign
#\d+ — one or more digits (integer part)
#(?:\.\d+)? — optional non-capturing group: a period and one or more digits (fractional part). Non-capturing (?:) — to avoid creating numbered groups; we will take the entire match.
#(?!\S) — negative lookahead: no non-whitespace character to the right ⇒ either a space or the end of the line to the right.


_NUMBER_RE = re.compile(r'(?<!\S)[+-]?\d+(?:\.\d+)?(?!\S)')

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
