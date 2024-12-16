import re
from pathlib import Path
from helpers import read_file


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


def part1():
    return


def part2():
    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
