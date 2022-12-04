from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    dupes = 0

    lines = s.splitlines()
    for line in lines:
        first, second = line.split(',')

        first_start, first_end = map(int, first.split('-'))
        second_start, second_end = map(int, second.split('-'))

        first_range, second_range = (
            list(assignment_range) for assignment_range in
            (
                range(first_start, first_end + 1),
                range(second_start, second_end + 1),
            )
        )

        if any(f in second_range for f in first_range):
            dupes += 1
        elif any(s in first_range for s in second_range):
            dupes += 1

    return dupes


INPUT_S = '''\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
'''
EXPECTED = 4


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
