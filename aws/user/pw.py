import random
import string
from typing import List


def get_pw(length: int = 10, symbols: str = string.punctuation,
           digit_ratio: float = 0.2, symbol_ratio: float = 0.2) -> str:
    assert(digit_ratio + symbol_ratio <= 1)

    def get_chars(l: int, candidates: str) -> List[str]:
        return list(random.choice(candidates) for i in range(l))

    digit_num = int(length * digit_ratio)
    symbol_num = int(length * symbol_ratio)
    letter_num = length - digit_num - symbol_num

    chars = get_chars(digit_num, string.digits) \
        + get_chars(symbol_num, symbols) \
        + get_chars(letter_num, string.ascii_letters)

    random.shuffle(chars)
    return ''.join(chars)


print(get_pw(symbols='-!@', symbol_ratio=0.2, length=12))
