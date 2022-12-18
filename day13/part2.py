from __future__ import annotations

import argparse
import os.path
import sys
from enum import Enum
from functools import cmp_to_key
from functools import partial
from math import prod
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)  # type: ignore[has-type]


Packet: TypeAlias = int | list['Packet']

DIVIDERS: tuple[Packet, ...] = ([[2]], [[6]])


class CMPResult(Enum):
    SMALLER = -1
    BIGGER = 1
    EQUAL = 0


def compare(
    left: Packet,
    right: Packet,
) -> CMPResult:
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return CMPResult.SMALLER
        elif left > right:
            return CMPResult.BIGGER
        return CMPResult.EQUAL

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    i = 0

    while i < len(left) and i < len(right):
        comparison = compare(left[i], right[i])
        if comparison in {CMPResult.SMALLER, CMPResult.BIGGER}:
            return comparison

        i += 1

    if len(left[i:]) < len(right[i:]):
        return CMPResult.SMALLER
    elif len(left[i:]) > len(right[i:]):
        return CMPResult.BIGGER
    return CMPResult.EQUAL


def compute(s: str) -> int:
    s = f"""{s}
[[2]]
[[6]]"""
    packet_pairs = s.split('\n\n')

    packets: list[Packet] = []

    for packet_pair in packet_pairs:
        packets.extend(eval(line) for line in packet_pair.splitlines())

    def cmp(left: Packet, right: Packet) -> int:
        return compare(left, right).value

    packets.sort(key=cmp_to_key(cmp))

    return prod(packets.index(divider) + 1 for divider in DIVIDERS)


INPUT_S = '''\
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
'''
EXPECTED = 140


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
