from __future__ import annotations

import argparse
import operator
import os.path
import sys
from functools import partial
from typing import Callable
from typing import cast
from typing import TypedDict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)


class Monkey(TypedDict):
    yelled: int | None
    first: str
    second: str
    op: Callable[[int, int], int]


def compute(s: str) -> int:
    monkeys: dict[str, Monkey] = {}

    for line in s.splitlines():
        split = line.split(':')
        name = split[0]

        numbers = support.parse_numbers_all(line)
        if numbers:
            # We don't care about other attributes since this a lone monkey.
            # Its job is to simply to yell that number. We will never access
            # other keys other than 'yelled' in this case (simplify typing).
            monkeys[name] = cast(Monkey, {'yelled': int(numbers[0])})
        else:
            job = split[1].strip()

            if '+' in job:
                job_dependencies = job.split(' + ')

                monkeys[name] = {
                    'yelled': None,
                    'first': job_dependencies[0],
                    'second': job_dependencies[1],
                    'op': operator.add,
                }
            elif '-' in job:
                job_dependencies = job.split(' - ')

                monkeys[name] = {
                    'yelled': None,
                    'first': job_dependencies[0],
                    'second': job_dependencies[1],
                    'op': operator.sub,
                }
            elif '*' in job:
                job_dependencies = job.split(' * ')

                monkeys[name] = {
                    'yelled': None,
                    'first': job_dependencies[0],
                    'second': job_dependencies[1],
                    'op': operator.mul,
                }
            elif '/' in job:
                job_dependencies = job.split(' / ')

                monkeys[name] = {
                    'yelled': None,
                    'first': job_dependencies[0],
                    'second': job_dependencies[1],
                    'op': operator.truediv,
                }

    def work(monkey: str) -> int:
        yelled: int | None = monkeys[monkey]['yelled']

        if yelled is None:
            first = work(monkeys[monkey]['first'])
            second = work(monkeys[monkey]['second'])

            monkeys[monkey]['yelled'] = monkeys[monkey]['op'](first, second)

            yelled = monkeys[monkey]['yelled']

        if yelled is None:
            raise AssertionError('yelled is None')

        return yelled

    return work('root')


INPUT_S = '''\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
'''
EXPECTED = 152


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
