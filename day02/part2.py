from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


opponent_to_score = {
    'A': 1,  # rock
    'B': 2,  # paper
    'C': 3,  # scissors
}

outcome_to_score = {
    'X': 0,  # lose
    'Y': 3,  # draw
    'Z': 6,  # win
}


def compute(s: str) -> int:
    res = 0

    lines = s.splitlines()
    for line in lines:
        opponent, outcome = line.strip().split(' ')

        res += outcome_to_score[outcome]

        if outcome == 'Y':
            res += opponent_to_score[opponent]
        elif outcome == 'X':
            if opponent == 'A':
                res += opponent_to_score['C']
            elif opponent == 'B':
                res += opponent_to_score['A']
            elif opponent == 'C':
                res += opponent_to_score['B']
            else:
                raise AssertionError
        elif outcome == 'Z':
            if opponent == 'A':
                res += opponent_to_score['B']
            elif opponent == 'B':
                res += opponent_to_score['C']
            elif opponent == 'C':
                res += opponent_to_score['A']
            else:
                raise AssertionError
        else:
            raise AssertionError

    return res


INPUT_S = '''\
A Y
B X
C Z
'''
EXPECTED = 12


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
