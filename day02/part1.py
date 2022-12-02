from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


player_to_score = {
    'X': 1,  # rock
    'Y': 2,  # paper
    'Z': 3,  # scissors
}

player_to_opponent = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C',
}


def compute(s: str) -> int:
    score = 0

    lines = s.splitlines()
    for line in lines:
        opponent, player = line.strip().split(' ')

        score += player_to_score[player]

        if opponent == player_to_opponent[player]:
            score += 3
        elif opponent == 'A' and player_to_opponent[player] == 'B':
            score += 6
        elif opponent == 'A' and player_to_opponent[player] == 'C':
            score += 0
        elif opponent == 'B' and player_to_opponent[player] == 'A':
            score += 0
        elif opponent == 'B' and player_to_opponent[player] == 'C':
            score += 6
        elif opponent == 'C' and player_to_opponent[player] == 'A':
            score += 6
        elif opponent == 'C' and player_to_opponent[player] == 'B':
            score += 0
        else:
            raise AssertionError

    return score


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 15


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
