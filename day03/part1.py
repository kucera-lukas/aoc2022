from __future__ import annotations

import argparse
import os.path
import string

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAP: dict[str, int] = dict(zip(string.ascii_lowercase, range(1, 27)))
MAP |= zip(string.ascii_uppercase, range(27, 53))


def compute(s: str) -> int:
    items_in_both: list[str] = []

    lines = s.splitlines()
    for line in lines:
        first_compartment, second_compartment = (
            line[:len(line) // 2], line[len(line) // 2:],
        )

        both = set(first_compartment) & set(second_compartment)

        items_in_both.extend(both)

    return sum(MAP[item] for item in items_in_both)


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 157


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
