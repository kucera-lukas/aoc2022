from __future__ import annotations

import argparse
import math
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    grid: list[list[int]] = [[] for _ in range(len(lines))]

    for i, line in enumerate(lines):
        numbers = [int(n) for n in line]
        grid[i].extend(numbers)

    def score(x: int, y: int) -> int:
        if x in (0, len(grid[0]) - 1) or y in (0, len(grid[0]) - 1):
            return -1

        value = grid[x][y]

        mx: defaultdict[str, int] = defaultdict(int)

        for d in ('up', 'down', 'left', 'right'):
            if d == 'up':
                r = range(x - 1, -1, -1)
            elif d == 'down':
                r = range(x + 1, len(grid))
            elif d == 'left':
                r = range(y - 1, -1, -1)
            elif d == 'right':
                r = range(y + 1, len(grid[0]))
            else:
                raise AssertionError(d)

            for i in r:
                mx[d] += 1

                x_i = i if d in ('up', 'down') else x
                y_i = i if d in ('left', 'right') else y

                if grid[x_i][y_i] >= value:
                    break

        return math.prod(mx.values())

    res = 0

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            res = max(res, score(x, y))

    return res


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
