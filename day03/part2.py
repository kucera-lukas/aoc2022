from __future__ import annotations

import argparse
import os.path
import string

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAP: dict[str, int] = dict(zip(string.ascii_lowercase, range(1, 27)))
MAP |= dict(zip(string.ascii_uppercase, range(27, 53)))


def compute(s: str) -> int:
    badges = []

    lines = s.splitlines()

    for start, end in zip(range(0, len(lines), 3), range(3, len(lines)+3, 3)):
        group = lines[start:end]

        sets = [set(line) for line in group]

        badge = (sets[0] & sets[1] & sets[2]).pop()

        badges.append(badge)

    return sum(MAP[item] for item in badges)


INPUT_S = '''\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''
EXPECTED = 70


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
