from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

MAP = {
    'R': support.Direction4.RIGHT,
    'U': support.Direction4.UP,
    'L': support.Direction4.LEFT,
    'D': support.Direction4.DOWN,
}


def pull(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    if abs(head[0] - tail[0]) == 2 and abs(head[1] - tail[1]) == 2:
        # move one step diagonally to keep up
        return (head[0] + tail[0]) // 2, (head[1] + tail[1]) // 2
    elif abs(head[0] - tail[0]) == 2:
        # move one step in that direction, so it remains close enough
        return (head[0] + tail[0]) // 2, head[1]
    elif abs(head[1] - tail[1]) == 2:
        # move one step in that direction, so it remains close enough
        return head[0], (head[1] + tail[1]) // 2

    return tail


def compute(s: str) -> int:
    bridge = [(0, 0) for _ in range(10)]
    visited = {(bridge[-1])}

    lines = s.splitlines()
    for line in lines:
        direction, count = (
            support.parse_characters_all(line)[0],
            support.parse_numbers_all(line)[0],
        )

        for _ in range(count):
            head = bridge[0] = MAP[direction].apply(*bridge[0])

            for i in range(1, len(bridge)):
                head = bridge[i] = pull(head, bridge[i])

            visited.add(bridge[-1])

    return len(visited)


INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
