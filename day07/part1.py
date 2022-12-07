from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

SIZE_LIMIT = 100_000


def compute(s: str) -> int:
    sizes: defaultdict[str, int] = defaultdict(int)
    path: list[str] = []

    lines = s.splitlines()[1:]
    for line in lines:
        if line.startswith(('$ ls', 'dir ')):
            continue
        elif line == '$ cd /':
            path = []
        elif line == '$ cd ..':
            path.pop()
        elif line.startswith('$ cd '):
            path.append(line.replace('$ cd ', ''))
        else:
            size = support.parse_numbers_all(line)[0]
            for i in range(1, len(path)+1):
                sizes['/'.join(path[:i])] += size

    return sum(
        size for size in sizes.values()
        if size < SIZE_LIMIT
    )


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 95437


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
