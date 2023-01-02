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
ROCK_COUNT = 1000000000000
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


def fingerprint(tower: set[tuple[int, int]]) -> frozenset[tuple[int, int]]:
    highest_ys = [
        max(y for x, y in tower if x == i)
        for i in range(WIDTH)
    ]
    min_y = min(highest_ys)

    return frozenset((x, y - min_y) for x, y in tower if y >= min_y)


def compute(s: str) -> int:
    jet_patterns: Iterator[tuple[int, str]] = cycle(enumerate(s.strip()))
    height, tower, additional, rock = (
        0,
        {(x, 0) for x in range(WIDTH)},
        0,
        0,
    )
    seen: dict[
        tuple[int, int, frozenset[tuple[int, int]]],
        tuple[int, int],
    ] = {}

    while rock < ROCK_COUNT:
        pattern_id = rock % PATTERN_COUNT
        piece = Piece.get_type(pattern_id, height + 4)

        while 1:
            i, jet = next(jet_patterns)

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

                key = (i, pattern_id, fingerprint(tower))

                if key in seen:
                    (previous_rock, previous_y) = seen[key]
                    diff = rock - previous_rock
                    c = (ROCK_COUNT - rock) // diff
                    additional += c * (height - previous_y)
                    rock += c * diff

                seen[key] = (rock, height)

                break

        rock += 1

    return height + additional


INPUT_S = '''\
>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>
'''
EXPECTED = 1514285714288


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
