from __future__ import annotations

import argparse
import os.path
import sys
from collections import deque
from functools import partial
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)

COORDINATES = 1000, 2000, 3000
DECRYPTION_KEY = 811589153
CYCLES = 10


class Number(NamedTuple):
    value: int


def compute(s: str) -> int:
    numbers = [
        number * DECRYPTION_KEY for number in support.parse_numbers_split(s)
    ]
    stream: deque[tuple[int, int]] = deque(enumerate(numbers))
    length = len(stream)

    for _ in range(CYCLES):
        for i, number in enumerate(numbers):
            index = next(
                index for index, (idx, _)
                in enumerate(stream) if idx == i
            )
            stream.rotate(-index)
            stream.popleft()
            stream.rotate(-number)
            stream.appendleft((i, number))

    zero_index = next(
        index for index, (_, number)
        in enumerate(stream) if number == 0
    )

    return sum(
        stream[(zero_index + coordinate) % length][1]
        for coordinate in COORDINATES
    )


INPUT_S = '''\
1
2
-3
3
-2
0
4
'''
EXPECTED = 1623178306


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
