import re
from pathlib import Path
from helpers import read_file
import math
from functools import cache


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class Stone:
    def __init__(self, number, next=None):
        self.number = number
        self.next = next

    def __str__(self):
        return f"{self.number}"

    def __repr__(self):
        return self.__str__()

    def blink(self):
        if self.number == 0:
            self.number = 1
            return

        digits = int(math.log10(self.number)) + 1
        if digits % 2 == 0:
            n = digits / 2
            left = self.first_n_digits(n)
            right = self.last_n_digits(n)
            return [Stone(left), Stone(right)]

        self.number *= 2024

    def first_n_digits(self, n):
        return self.number // 10 ** (int(math.log10(self.number)) - n + 1)

    def last_n_digits(self, n):
        return self.number % 10**n

    def __hash__(self):
        return hash(self.number)


@cache
def blink(number):
    if number == 0:
        return tuple([1])

    split = maybe_split_number(number)
    if split:
        return tuple(split)

    return tuple([number * 2024])


@cache
def get_num_digits(number):
    return int(math.log10(number)) + 1


@cache
def maybe_split_number(number):
    digits = get_num_digits(number)
    if digits % 2 == 0:
        n = digits / 2
        left = first_n_digits(number, n)
        right = last_n_digits(number, n)
        return [left, right]

    return None


@cache
def first_n_digits(number, n):
    return number // 10 ** (int(math.log10(number)) - n + 1)


@cache
def last_n_digits(number, n):
    return number % 10**n


# @cache
def replace(stones, index, replacements):
    stones.pop(index)
    stones += list(replacements)
    return stones


def blink_n_times(stones, n):
    for _ in range(n):
        replacements = dict()
        for i, s in enumerate(stones):
            r = s.blink()
            if r:
                replacements[i] = r

        indexes = sorted(list(replacements.keys()), reverse=True)
        for i in indexes:
            stones = replace(stones, i, replacements[i])
        # print(stones)
        # print()
        print(f"Blink {_+1}")

    return stones


def blink_n_times2(stones, n):
    for _ in range(n):
        replacements = dict()
        for i, s in enumerate(stones):
            r = blink(s)
            if r:
                replacements[i] = r

        indexes = sorted(list(replacements.keys()), reverse=True)
        for i in indexes:
            stones = replace(stones, i, replacements[i])
        # print(stones)
        # print()
        print(f"Blink {_+1}")

    return stones


def part1():
    nums = list(map(int, DATA.strip().split(" ")))
    stones = []
    for n in nums:
        stones.append(Stone(n))

    stones = blink_n_times(stones, 25)

    # s = Stone(0)
    # s.blink()
    return len(stones)


def part2():
    stones = list(map(int, DATA.strip().split(" ")))

    stones = blink_n_times2(stones, 75)

    return len(stones)


def main():
    # print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
