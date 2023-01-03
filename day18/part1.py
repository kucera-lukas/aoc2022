from __future__ import annotations

import argparse
import os.path
import sys
from functools import partial

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)


SIDES = 6
DIRS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def compute(s: str) -> int:
    cubes = {tuple(support.parse_numbers_all(line)) for line in s.splitlines()}
    sides = 0

    for cube in cubes:
        adj = 0

        for x, y, z in DIRS:
            moved = (cube[0] + x, cube[1] + y, cube[2] + z)

            if moved in cubes:
                adj += 1

        sides += SIDES - adj

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
EXPECTED = 64


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
