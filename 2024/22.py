import re
import os
from turtle import st
from typing import Sequence
from helpers import read_file


FILENAME = os.path.basename(__file__)
YEAR = os.path.basename(os.path.dirname(__file__))
TEXT_FILE_PATH = os.path.join(".", YEAR, FILENAME.split(".")[0] + ".txt")
DATA = read_file(TEXT_FILE_PATH)


class SecretNumber:
    def __init__(self, number) -> None:
        self.number = number

    def mix(self, number) -> None:
        self.number = number ^ self.number

    def prune(self) -> None:
        self.number = self.number % 16777216

    def step_one(self) -> None:
        self.mix(self.number * 64)
        self.prune()

    def step_two(self) -> None:
        self.mix(self.number // 32)
        self.prune()

    def step_three(self) -> None:
        self.mix(self.number * 2048)
        self.prune()

    def calculate_secret_number(self):
        self.step_one()
        self.step_two()
        self.step_three()

        return self.number

    def do_calculate_n_times(self, n):
        for _ in range(n):
            self.number = self.calculate_secret_number()

        return self.number

    def do_calculate_n_times_with_changes(self, n):
        result = []
        last_price = 0
        for _ in range(n):
            current_price = self.number % 10
            result.append((self.number, current_price, current_price - last_price))
            last_price = current_price

            self.number = self.calculate_secret_number()

        return result


def get_max_bananas(all_prices):
    # sequence = [None] * 4
    data = {}

    for buyer, prices in enumerate(all_prices):
        for i in range(4, len(prices)):
            tup = prices[i]
            tup1 = prices[i - 1]
            tup2 = prices[i - 2]
            tup3 = prices[i - 3]
            # seq = (tup[2], tup1[2], tup2[2], tup3[2])
            seq = (tup3[2], tup2[2], tup1[2], tup[2])
            if seq in data:
                if buyer in data[seq]:
                    # data[seq][buyer] = tup[1]
                    continue
                    # pass
                else:
                    data[seq][buyer] = tup[1]
            else:
                data[seq] = {}
                data[seq][buyer] = tup[1]

    # print(data)
    # print(data.values())
    lst = [(k, v) for k, v in data.items()]
    lst.sort(reverse=True, key=lambda v: sum(v[1].values()))
    # print()
    # values = sorted(
    #     data.values(), reverse=True, key=lambda d: d["count"] * d["bananas"]
    # )
    # print(lst[0], sum(lst[0][1].values()))

    # bananas = sorted([v[1] for v in data.values()], reverse=True)
    # counts = sorted([v[0] for v in data.values()], reverse=True)
    # print(bananas)
    # print(counts)

    # for k, v in data.items():
    #     print(k, v)
    # print(seq)
    return sum(lst[0][1].values())


def part1():
    initial_numbers = []
    for initial in DATA.strip().split("\n"):
        start = int(initial)
        initial_numbers.append((start, SecretNumber(start)))

    total = 0
    for tup in initial_numbers:
        start, sn = tup
        sn.do_calculate_n_times(2000)
        # print(f"{start}: {sn.number}")
        total += sn.number

    return total


def part2():
    initial_numbers = []
    for initial in DATA.strip().split("\n"):
        start = int(initial)
        initial_numbers.append((start, SecretNumber(start)))

    seqs = []
    for tup in initial_numbers:
        start, sn = tup
        seq = sn.do_calculate_n_times_with_changes(2000)
        seqs.append(seq)
        # print(f"{start}: {sn.number}")

    # print(seqs)
    # for seq in seqs:

    # 1638 too high
    # 1614 too low

    return get_max_bananas(seqs)


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
