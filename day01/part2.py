from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    elves = s.strip().split('\n\n')

    calories_per_elf = []

    for elf in elves:
        items = [num.strip() for num in elf.split('\n') if num != '']

        calories_per_elf.append(sum(map(int, items)))

    top_three_calories = 0

    for _ in range(3):
        mx = max(calories_per_elf)

        calories_per_elf.pop(calories_per_elf.index(mx))

        top_three_calories += mx

    return top_three_calories


INPUT_S = '''\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''
EXPECTED = 45000


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
