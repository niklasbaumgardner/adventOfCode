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

    rules = {}
    zs = []
    for line in second.split("\n"):
        logic, end_name = line.split(" -> ")
        a, gate, b = logic.split(" ")
        if gate == "AND":
            gate = gate_and
        elif gate == "OR":
            gate = gate_or
        else:
            gate = gate_xor
        rules[end_name] = dict(a=a, gate=gate, b=b, end_name=end_name, answer=None)
        if end_name.startswith("z"):
            zs.append(end_name)

    zs.sort(reverse=True)
    # print(zs)
    # print(starting)
    # print(rules)
    # print(first)
    # print(second)
    return starting, rules, zs


def solve_rule(rule, initial_values, rules_map):
    a, gate, b, end_name, answer = (
        rule["a"],
        rule["gate"],
        rule["b"],
        rule["end_name"],
        rule["answer"],
    )

    if answer is not None:
        return answer

    if a not in initial_values and rules_map[a]["answer"] is None:
        solve_rule(rules_map[a], initial_values, rules_map)

    if b not in initial_values and rules_map[b]["answer"] is None:
        solve_rule(rules_map[b], initial_values, rules_map)

    a_val = None
    if a in initial_values:
        a_val = initial_values[a]
    else:
        a_val = rules_map[a]["answer"]

    b_val = None
    if b in initial_values:
        b_val = initial_values[b]
    else:
        b_val = rules_map[b]["answer"]

    rule["answer"] = gate(a_val, b_val)


def find_all_z(initial_values, rules_map, zs):
    for z in zs:
        # print(z)
        rule_dict = rules_map[z]
        solve_rule(rule_dict, initial_values, rules_map)

    nums = [
        [r["end_name"], r["answer"]]
        for r in rules_map.values()
        if r["answer"] is not None and r["end_name"].startswith("z")
    ]
    nums.sort(key=lambda x: x[0], reverse=True)
    # print(nums)
    bin_num = "".join([str(x[1]) for x in nums])

    # print(bin_num)

    return int(bin_num, 2)


def part1():
    # print(DATA)
    starting, rules, zs = parse_data(DATA)

    return find_all_z(starting, rules, zs)


def part2():
    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
