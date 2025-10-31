import re
import os
from helpers import read_file


FILENAME = os.path.basename(__file__)
YEAR = os.path.basename(os.path.dirname(__file__))
TEXT_FILE_PATH = os.path.join(".", YEAR, FILENAME.split(".")[0] + ".txt")
DATA = read_file(TEXT_FILE_PATH)


def gate_and(a, b):
    return a and b


def gate_or(a, b):
    return a or b


def gate_xor(a, b):
    return a ^ b


def parse_data(data):
    first, second = data.split("\n\n")
    starting = {}

    for line in first.split("\n"):
        name, val = line.split(": ")
        starting[name] = int(val)

    rules = []
    for line in second.split("\n"):
        logic, end_name = line.split(" -> ")
        a, gate, b = logic.split(" ")
        if gate == "AND":
            gate = gate_and
        elif gate == "OR":
            gate = gate_and
        else:
            gate = gate_xor
        rules.append([a, gate, b, end_name])

    # print(starting)
    # print(rules)
    # print(first)
    # print(second)
    return starting, rules


# def do_rule()
def do_logic(starting, rules):
    known_rules = set(starting.keys())
    unknown_rules = set()
    for rule in rules:
        a, gate, b, end_name = rule
        if a not in known_rules:
            unknown_rules.add(a)
        if b not in known_rules:
            unknown_rules.add(b)
        if end_name not in known_rules:
            unknown_rules.add(end_name)

    nums = {}
    # for rule in rules:
    i = 0
    while unknown_rules:
        rule = rules[i % len(rules)]

        a, gate, b, end_name = rule
        if a in starting and b in starting:
            answer = gate(starting[a], starting[b])
            nums[end_name] = answer
            starting[end_name] = answer
            unknown_rules.discard(end_name)

        i += 1
    print(nums)

    nums_sorted = sorted(nums.keys())
    actual_nums = [nums[n] for n in nums_sorted]
    print(actual_nums)
    return int("".join(actual_nums), 2)


def part1():
    # print(DATA)
    starting, rules = parse_data(DATA)
    nums = do_logic(starting, rules)

    return


def part2():
    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
