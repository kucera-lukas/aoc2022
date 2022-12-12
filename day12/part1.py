from __future__ import annotations

import argparse
import os.path
import string
import sys
from collections import deque
from functools import partial

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)


MAP = dict(
    zip(
        string.ascii_lowercase, range(
            len(string.ascii_lowercase),
        ),
    ), S=0, E=25,
)
DIRS = (
    support.Direction4.RIGHT,
    support.Direction4.UP,
    support.Direction4.LEFT,
    support.Direction4.DOWN,
)


def compute(s: str) -> int:
    S = E = (-1, -1)

    lines = s.strip().splitlines()
    grid: list[list[str]] = [[] for _ in range(len(lines))]

    for i, line in enumerate(lines):
        grid[i].extend(list(line))

        if 'S' in line:
            S = (i, line.index('S'))

        if 'E' in line:
            E = (i, line.index('E'))

    seen = {S}
    queue: deque[tuple[int, int]] = deque((S,))

    def bfs() -> int:
        steps = -1

        while queue:
            steps += 1

            for _ in range(len(queue)):
                old_x, old_y = queue.popleft()

                if (old_x, old_y) == E:
                    return steps

                for d in DIRS:
                    new_x, new_y = d.apply(old_x, old_y)

                    if (new_x, new_y) in seen:
                        continue

                    if (
                        new_x < 0
                        or new_x >= len(grid)
                        or new_y < 0
                        or new_y >= len(grid[0])
                    ):
                        continue

                    if (
                        MAP[grid[old_x][old_y]] - MAP[grid[new_x][new_y]]
                    ) <= -2:
                        continue

                    seen.add((new_x, new_y))
                    queue.append((new_x, new_y))

        return 0

    return bfs()


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 31


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
