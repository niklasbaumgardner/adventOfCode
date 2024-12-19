import re
from pathlib import Path
from helpers import read_file

from itertools import permutations, product
from copy import deepcopy


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


# COLORS: {}
PATTERN_TO_TOWELS = dict()
PATTERN_TO_COUNT = dict()


def check_design(towels, pattern):
    if len(pattern) == 0:
        return True

    for t in towels:
        if pattern.startswith(t):
            if check_design(towels, pattern[len(t) :]):
                return True
    return False


def check_design_count(towels, pattern, cache):
    if len(pattern) == 0:
        return 1

    if pattern in cache:
        return cache[pattern]

    count = 0
    for t in towels:
        if pattern.startswith(t):
            count += check_design_count(towels, pattern[len(t) :], cache)

    cache[pattern] = count
    return cache[pattern]


def part1():
    towels, patterns = DATA.strip().split("\n\n")
    towels = towels.strip().split(", ")
    patterns = patterns.strip().split("\n")

    for pattern in patterns:
        for t in towels:
            if t in pattern:
                if pattern in PATTERN_TO_TOWELS:
                    PATTERN_TO_TOWELS[pattern].add(t)
                else:
                    PATTERN_TO_TOWELS[pattern] = set([t])

    #######################################################

    designs_possible = 0
    # for pattern in patterns:
    for k, v in PATTERN_TO_TOWELS.items():
        if check_design(v, k):
            designs_possible += 1

    return designs_possible


def part2():
    towels, patterns = DATA.strip().split("\n\n")
    towels = towels.strip().split(", ")
    patterns = patterns.strip().split("\n")

    for pattern in patterns:
        for t in towels:
            if t in pattern:
                if pattern in PATTERN_TO_TOWELS:
                    PATTERN_TO_TOWELS[pattern].add(t)
                else:
                    PATTERN_TO_TOWELS[pattern] = set([t])

    #######################################################

    designs_possible = 0
    cache = dict()
    # for pattern in patterns:
    for k, v in PATTERN_TO_TOWELS.items():
        designs_possible += check_design_count(v, k, cache)

    # for k, v in PATTERN_TO_COUNT.items():
    #     designs_possible += v
    #     print(k, v)

    return designs_possible


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
