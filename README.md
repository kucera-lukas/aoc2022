# aoc2022

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/kucera-lukas/aoc2022/main.svg)](https://results.pre-commit.ci/latest/github/kucera-lukas/aoc2022/main)

My solutions to [Advent of Code 2022](https://adventofcode.com/2022)

## Installation

1. Setup python environment

```shell
# create venv
virtualenv venv

# install requirements
pip install -r requirements.txt
```

2. Copy and fill environment variables into .env file

```shell
cp .env.sample .env
```

### Dependencies

I'm using https://github.com/direnv/direnv to automatically drop me into the
Python virtual environment

## Usage

- solve each day in the correct directory
- `cp -r day00 $DAY` - create directory for a new problem
- `aoc-download-input` - download the input into `$DAY/input.txt`
- implement solution in the `compute` function
- `pytest part1.py` - run part1 tests
- `python part1.py input.txt` - run the part1 script directly
- `python part1.py input.txt | aoc-submit --part 1` - submit answer for part1
- `cp part1.py part2.py` - copy part1 script into part2

## Contributing

```shell
pre-commit install
```

## Credits

Inspired by https://github.com/anthonywritescode/aoc2022 and https://youtu.be/CZZLCeRya74

## License

Developed under the [MIT](https://github.com/kucera-lukas/aoc2022/blob/master/LICENSE) license.
