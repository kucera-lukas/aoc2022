from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    grid: list[list[int]] = [[] for _ in range(len(lines))]

    for i, line in enumerate(lines):
        grid[i].extend(int(n) for n in line)

    def visible(value: int, x: int, y: int, d: str) -> bool:
        if x in (0, len(grid)-1) or y in (0, len(grid[0])-1):
            return True

        if d == 'up':
            c = (-1, 0)
        elif d == 'down':
            c = (1, 0)
        elif d == 'left':
            c = (0, -1)
        elif d == 'right':
            c = (0, 1)
        else:
            raise AssertionError

        new_x = x + c[0]
        new_y = y + c[1]

        if grid[new_x][new_y] >= value:
            return False

        return visible(value, new_x, new_y, d)

    data: defaultdict[tuple[int, int], bool] = defaultdict(bool)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            for d in ('up', 'down', 'left', 'right'):
                if not data[(x, y)] and visible(grid[x][y], x, y, d):
                    data[(x, y)] = True

    return sum(data.values())


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
