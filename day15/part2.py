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

MAX_COORD = 4000000


def compute(s: str, *, high: int = MAX_COORD) -> int:
    points = []

    for line in s.splitlines():
        sensor_x, sensor_y, beacon_x, beacon_y = support.parse_numbers_all(
            line,
            minus=True,
        )

        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        points.append((sensor_x, sensor_y, distance))

    result = -1

    for y in range(high + 1):
        ranges: list[tuple[int, int]] = []

        for point_x, point_y, distance in points:
            diff = distance - abs(y - point_y)

            if diff >= 0:
                ranges.extend(
                    (
                        (-diff + point_x, -1),
                        (diff + 1 + point_x, 1),
                    ),
                )

        curr = 0
        for first, second in sorted(ranges):
            curr += second

            if curr == 0 and 0 <= first <= high:
                result = first * MAX_COORD + y
                break

    return result


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 56000011


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, high=20) == expected


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
