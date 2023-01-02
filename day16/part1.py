from __future__ import annotations

import argparse
import os.path
import sys
from collections import deque
from functools import partial
from itertools import combinations
from typing import TypedDict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)

TIME = 30


class Valve(TypedDict):
    flow: int
    leads: list[str]


def compute(s: str) -> int:
    valves: dict[str, Valve] = {}
    positive_names = set()

    for line in s.splitlines():
        chars = support.parse_characters_upper(line)[1:]
        name = chars[0]
        flow = support.parse_numbers_all(line)[0]

        valves[name] = {'flow': flow, 'leads': chars[1:]}

        if flow > 0:
            positive_names.add(name)

    weights = {}
    edges = ['AA', *positive_names]

    for a, b in combinations(edges, r=2):
        q: deque[tuple[str, ...]] = deque([(a,)])

        while q:
            path = q.popleft()

            if path[-1] == b:
                break
            else:
                q.extend(
                    (*path, lead) for lead in valves[path[-1]]['leads']
                    if lead not in path
                )

        weights[(a, b)], weights[(b, a)] = len(path), len(path)

    res = 0
    search: list[tuple[int, int, str, set[str]]] = [
        (0, 0, 'AA', positive_names),
    ]

    while search:
        score, time, current, possible = search.pop()

        res = max(res, score)

        for p in possible:
            needed_time = time + weights[(current, p)]

            if needed_time < TIME:
                search.append(
                    (
                        score + (TIME - needed_time) * valves[p]['flow'],
                        needed_time,
                        p,
                        possible - {p},
                    ),
                )

    return res


INPUT_S = '''\
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
'''
EXPECTED = 1651


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
