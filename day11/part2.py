from __future__ import annotations

import argparse
import operator
import os.path
from functools import reduce
from math import prod
from typing import Any
from typing import Callable
from typing import TypedDict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
ROUNDS = 10_000


class Monkey(TypedDict):
    items: list[int]
    operation: str | int
    operator: Callable[[Any, Any], Any]
    test: int
    true: int
    false: int
    count: int


def compute(s: str) -> int:
    monkeys_strs = s.split('\n\n')
    monkeys: list[Monkey] = (
        [{} for _ in range(len(monkeys_strs))]  # type: ignore
    )

    for i, lines in enumerate(monkeys_strs):
        for line in lines.splitlines():
            line = line.strip()
            if line.startswith('Monkey'):
                monkeys[i] = {  # type: ignore
                    'monkey': support.parse_numbers_all(line)[0],
                }
            elif line.startswith('Starting'):
                monkeys[i]['items'] = support.parse_numbers_all(line)
            elif line.startswith('Operation'):
                if line.count('old') == 2:
                    monkeys[i]['operation'] = 'old'
                else:
                    monkeys[i]['operation'] = (
                        support.parse_numbers_all(line)[0]
                    )

                if '*' in line:
                    monkeys[i]['operator'] = operator.mul
                elif '+' in line:
                    monkeys[i]['operator'] = operator.add
                else:
                    raise AssertionError(i, line, monkeys)
            elif line.startswith('Test'):
                monkeys[i]['test'] = support.parse_numbers_all(line)[0]
            elif line.startswith('If true'):
                monkeys[i]['true'] = support.parse_numbers_all(line)[0]
            elif line.startswith('If false'):
                monkeys[i]['false'] = support.parse_numbers_all(line)[0]
            else:
                raise AssertionError(i, line, monkeys)

        monkeys[i]['count'] = 0

    mod = reduce(operator.mul, (m['test'] for m in monkeys))

    for _ in range(ROUNDS):
        for monkey in monkeys:
            for item in monkey['items']:
                monkey['count'] += 1

                item %= mod

                if monkey['operation'] == 'old':
                    worry_level = monkey['operator'](item, item)
                else:
                    worry_level = monkey['operator'](item, monkey['operation'])

                if worry_level % monkey['test'] == 0:
                    monkeys[monkey['true']]['items'].append(worry_level)
                else:
                    monkeys[monkey['false']]['items'].append(worry_level)

            monkey['items'] = []

    counts = [monkey['count'] for monkey in monkeys]
    counts.sort()

    return prod(counts[-2:])


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 2713310158


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
