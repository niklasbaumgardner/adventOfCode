import re
import os
from helpers import read_file


FILENAME = os.path.basename(__file__)
YEAR = os.path.basename(os.path.dirname(__file__))
TEXT_FILE_PATH = os.path.join(".", YEAR, FILENAME.split(".")[0] + ".txt")
DATA = read_file(TEXT_FILE_PATH)


def parse_pin_heights(chunk):
    pin_heights = [0] * 5
    lock_list = chunk.split("\n")[1:-1]

    for row in lock_list:
        for i, col in enumerate(row):
            if col == "#":
                pin_heights[i] += 1

    return pin_heights


def check_locks_and_keys(locks, keys):
    valid_combos = 0
    for lock in locks:
        for key in keys:
            zipped = [x + y for x, y in zip(lock, key)]
            if max(zipped) < 6:
                valid_combos += 1

    return valid_combos


def parse_to_locks_and_keys(data):
    locks = []
    keys = []

    for chunk in data.strip().split("\n\n"):
        # print(chunk)
        pin_heights = parse_pin_heights(chunk)
        if chunk.startswith("#####"):
            locks.append(pin_heights)
        if chunk.startswith("....."):
            keys.append(pin_heights)
    # print(keys)
    # print(locks)

    return check_locks_and_keys(locks, keys)


def part1():
    # print(DATA)
    return parse_to_locks_and_keys(DATA)


def part2():
    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
