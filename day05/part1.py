from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    start, end = s.split('\n\n')

    stack_count = start.splitlines()[-2].count('[')
    stacks: list[deque[str]] = [deque() for _ in range(stack_count)]

    for line in start.splitlines()[:-1]:
        for i, c in enumerate(line[1::4]):
            if not c.isspace():
                stacks[i].appendleft(c)

    for line in end.splitlines():
        move, from_, to = support.parse_numbers_all(line)

        for _ in range(move):
            stacks[to - 1].append(stacks[from_ - 1].pop())

    return ''.join(stack[-1] for stack in stacks if stack)


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'CMZ'


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
