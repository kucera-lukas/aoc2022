from __future__ import annotations

import argparse
import os.path
import sys
from collections.abc import Iterator
from functools import partial
from itertools import cycle
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)

WIDTH = 7
ROCK_COUNT = 2022
PATTERN_COUNT = 5


Pattern: TypeAlias = set[tuple[int, int]]


class Piece:
    def __init__(self, pattern: Pattern) -> None:
        self.pattern = pattern.copy()

    def left(self) -> None:
        if any(x == 0 for x, y in self.pattern):
            return

        self.pattern = {(x - 1, y) for x, y in self.pattern}

    def right(self) -> None:
        if any(x == 6 for x, y in self.pattern):
            return

        self.pattern = {(x + 1, y) for x, y in self.pattern}

    def down(self) -> None:
        self.pattern = {(x, y - 1) for x, y in self.pattern}

    def up(self) -> None:
        self.pattern = {(x, y + 1) for x, y in self.pattern}

    @classmethod
    def get_type(cls, pattern_id: int, y: int) -> Piece:
        pattern: Pattern

        if pattern_id == 0:
            pattern = {(2, y), (3, y), (4, y), (5, y)}
        elif pattern_id == 1:
            pattern = {(3, y + 2), (2, y + 1), (3, y + 1), (4, y + 1), (3, y)}
        elif pattern_id == 2:
            pattern = {(2, y), (3, y), (4, y), (4, y + 1), (4, y + 2)}
        elif pattern_id == 3:
            pattern = {(2, y), (2, y + 1), (2, y + 2), (2, y + 3)}
        elif pattern_id == 4:
            pattern = {(2, y + 1), (2, y), (3, y + 1), (3, y)}
        else:
            raise AssertionError('Unknown piece type')

        return cls(pattern)


def compute(s: str) -> int:
    jet_patterns: Iterator[str] = cycle(s.strip())
    height, tower = 0, {(x, 0) for x in range(WIDTH)}

    for rock in range(ROCK_COUNT):
        piece = Piece.get_type(rock % PATTERN_COUNT, height + 4)

        while 1:
            jet = next(jet_patterns)

            if jet == '>':
                move, back = piece.right, piece.left
            else:
                assert jet == '<'
                move, back = piece.left, piece.right

            move()

            if piece.pattern & tower:
                back()

            piece.down()

            if piece.pattern & tower:
                piece.up()

                tower |= piece.pattern
                height = max(y for x, y in tower)

                break

    return height


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 3068


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
