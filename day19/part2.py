from __future__ import annotations

import argparse
import os.path
import sys
from collections import deque
from copy import deepcopy
from functools import partial
from math import prod
from typing import get_args
from typing import Literal
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Answer is read via stdin when submitting. To avoid
# accidentally reading a value from a debugging print
# let's re-assign 'print' to always write to stderr.
print = partial(print, file=sys.stderr, flush=True)

Robot: TypeAlias = Literal['ore', 'clay', 'obsidian', 'geode']

ROBOTS: tuple[Robot, ...] = get_args(Robot)
MINUTES = 32


def can_buy(
    robot: Robot,
    inventory: dict[Robot, int],
    costs: dict[Robot, dict[Robot, int]],
) -> bool:
    return all(
        inventory[resource] >= amount
        for resource, amount in costs[robot].items()
    )


def buy(
    robot: Robot,
    inventory: dict[Robot, int],
    robots: dict[Robot, int],
    costs: dict[Robot, dict[Robot, int]],
) -> tuple[dict[Robot, int], dict[Robot, int]]:
    new_robots = deepcopy(robots)

    for resource, amount in costs[robot].items():
        inventory[resource] -= amount

    new_robots[robot] += 1

    return inventory, new_robots


def get_costs(blueprint: str) -> dict[Robot, dict[Robot, int]]:
    numbers: list[int] = support.parse_numbers_all(blueprint)[1:]

    return {
        'ore': {'ore': numbers[0]},
        'clay': {'ore': numbers[1]},
        'obsidian': {'ore': numbers[2], 'clay': numbers[3]},
        'geode': {'ore': numbers[4], 'obsidian': numbers[5]},
    }


def update_inventory(
    inventory: dict[Robot, int],
    robots: dict[Robot, int],
) -> dict[Robot, int]:
    new_inventory = deepcopy(inventory)

    for robot, amount in robots.items():
        new_inventory[robot] += amount

    return new_inventory


def quality(blueprint: str) -> int:
    inventory: dict[Robot, int] = dict.fromkeys(ROBOTS, 0)

    robots: dict[Robot, int] = dict.fromkeys(ROBOTS, 0)
    robots['ore'] = 1

    costs = get_costs(blueprint)

    ore_max = max(cost['ore'] for cost in costs.values())
    clay_max = costs['obsidian']['clay']
    obsidian_max = costs['geode']['obsidian']

    best = -1
    seen: set[
        tuple[
            int,
            tuple[tuple[Robot, int], ...],
            tuple[tuple[Robot, int], ...],
        ]
    ] = set()
    q: deque[tuple[int, dict[Robot, int], dict[Robot, int]]] = deque()
    q.append((0, inventory, robots))

    while q:
        minute, inventory, robots = q.popleft()

        remaining_minutes = MINUTES - minute

        inventory['ore'], inventory['clay'], inventory['obsidian'] = (
            min(remaining_minutes * ore_max, inventory['ore']),
            min(remaining_minutes * clay_max, inventory['clay']),
            min(remaining_minutes * obsidian_max, inventory['obsidian']),
        )

        robots['ore'], robots['clay'], robots['obsidian'] = (
            min(robots['ore'], ore_max),
            min(robots['clay'], clay_max),
            min(robots['obsidian'], obsidian_max),
        )

        key = (minute, tuple(robots.items()), tuple(inventory.items()))

        if key in seen:
            continue

        seen.add(key)

        best = max(best, inventory['geode'])

        if minute == MINUTES:
            continue

        minute += 1

        robot: Robot
        for robot in ROBOTS:
            if can_buy(robot, inventory, costs):
                new_inventory = update_inventory(inventory, robots)
                new_inventory, new_robots = buy(
                    robot,
                    new_inventory,
                    robots,
                    costs,
                )
                q.append((minute, new_inventory, new_robots))

                if robot == 'geode':
                    break
        else:
            q.append((minute, update_inventory(inventory, robots), robots))

    return best


def compute(s: str) -> int:
    lines = s.splitlines()[:3]

    return prod(quality(line) for line in lines)


INPUT_S = '''\
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
'''  # noqa: E501
EXPECTED = 56 * 62


@pytest.mark.slow
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
