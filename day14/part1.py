from __future__ import annotations

import argparse
import os.path
import sys
from functools import partial
from typing import cast

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)

SAND_START = (500, 0)


def is_blocked(sand: tuple[int, int], rocks: set[tuple[int, int]]) -> bool:
    return (
        (sand[0], sand[1] + 1) in rocks
        and (sand[0] - 1, sand[1] + 1) in rocks
        and (sand[0] + 1, sand[1] + 1) in rocks
    )


def is_done(
    sand: tuple[int, int],
    rocks: set[tuple[int, int]],
    max_y: int,
) -> bool:
    while not is_blocked(sand, rocks):
        if (sand[0], sand[1] + 1) not in rocks:
            sand = (sand[0], sand[1] + 1)
        elif (sand[0] - 1, sand[1] + 1) not in rocks:
            sand = (sand[0] - 1, sand[1] + 1)
        elif (sand[0] + 1, sand[1] + 1) not in rocks:
            sand = (sand[0] + 1, sand[1] + 1)
        else:
            raise AssertionError

        if sand[1] > max_y:
            return True
    return False


def compute(s: str) -> int:
    rocks: set[tuple[int, int]] = set()

    lines = s.splitlines()
    for line in lines:
        coords: list[tuple[int, int]] = [
            cast(tuple[int, int], tuple(support.parse_numbers_all(coord)))
            for coord in line.split(' -> ')
        ]
        last = coords[0]

        for rock_line in coords[1:]:
            if rock_line[0] == last[0]:
                rocks.update((last[0], y) for y in range(
                    min(last[1], rock_line[1]), max(last[1], rock_line[1]) + 1,
                ))
            elif rock_line[1] == last[1]:
                rocks.update((x, last[1]) for x in range(
                    min(last[0], rock_line[0]), max(last[0], rock_line[0]) + 1,
                ))
            elif rock_line == last:
                rocks.add(rock_line)
            else:
                raise AssertionError

            last = rock_line

    current_sand, resting = SAND_START, 0
    max_y = max(r[1] for r in rocks)

    while not is_done(current_sand, rocks, max_y):
        if is_blocked(current_sand, rocks):
            resting += 1
            rocks.add(current_sand)
            current_sand = SAND_START
        elif (current_sand[0], current_sand[1] + 1) not in rocks:
            current_sand = (current_sand[0], current_sand[1] + 1)
        elif (current_sand[0] - 1, current_sand[1] + 1) not in rocks:
            current_sand = (current_sand[0] - 1, current_sand[1] + 1)
        elif (current_sand[0] + 1, current_sand[1] + 1) not in rocks:
            current_sand = (current_sand[0] + 1, current_sand[1] + 1)
        else:
            raise AssertionError

    return resting


INPUT_S = '''\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
'''
EXPECTED = 24


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
        # Make sure answer goes to stdout
        print(compute(f.read()), file=sys.stdout)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
