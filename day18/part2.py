from __future__ import annotations

import argparse
import os.path
import sys
from collections import deque
from functools import partial
from typing import cast
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)

Cube: TypeAlias = tuple[int, int, int]


SIDES = 6
DIRS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))

# should be large enough to indicate outside reach
OUT_THRESHOLD = 1000

OUT = set()
IN = set()


def is_trapped(cube: Cube, cubes: set[Cube]) -> bool:
    if cube in OUT:
        return False
    if cube in IN:
        return True

    q = deque((cube,))
    seen = set()

    def bfs() -> bool:
        while q:
            nxt = q.popleft()

            if nxt in cubes:
                continue

            if nxt in seen:
                continue

            seen.add(nxt)

            for d in DIRS:
                dx, dy, dz = nxt[0] + d[0], nxt[1] + d[1], nxt[2] + d[2]
                q.append((dx, dy, dz))

            if len(q) > OUT_THRESHOLD:
                for c in seen:
                    OUT.add(c)

                return False

        for c in seen:
            IN.add(c)

        return True

    return bfs()


def compute(s: str) -> int:
    cubes = cast(
        set[Cube],
        {tuple(support.parse_numbers_all(line)) for line in s.splitlines()},
    )
    sides = 0

    for cube in cubes:
        adj = SIDES

        for d in DIRS:
            moved = (cube[0] + d[0], cube[1] + d[1], cube[2] + d[2])

            if is_trapped(moved, cubes):
                adj -= 1

        sides += adj

    return sides


INPUT_S = '''\
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
'''
EXPECTED = 58


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
