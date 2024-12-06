import re
from pathlib import Path
from helpers import read_file, LinkedNode


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


def parse_part1():
    order, updates = DATA.split("\n\n")

    rules = {}

    for line in order.split("\n"):
        first, second = line.split("|")
        first = int(first)
        second = int(second)
        if first in rules:
            rules[first].append(second)
        else:
            rules[first] = [second]

        # second = LinkedNode(second)
        # first = LinkedNode(first, second)

        # print(first)
    # print(rules)

    total = 0
    for line in updates.split("\n"):
        update = list(map(int, line.split(",")))

        is_valid = check_rule_violation(rules, update)
        if is_valid:
            middle_num = update[len(update) // 2]
            # print(middle_num)
            total += middle_num

    return total


def parse_part2():
    order, updates = DATA.split("\n\n")

    rules = {}

    for line in order.split("\n"):
        first, second = line.split("|")
        first = int(first)
        second = int(second)
        if first in rules:
            rules[first].append(second)
        else:
            rules[first] = [second]

        # second = LinkedNode(second)
        # first = LinkedNode(first, second)

        # print(first)
    # print(rules)

    total = 0
    for line in updates.split("\n"):
        update = list(map(int, line.split(",")))

        is_valid = check_rule_violation(rules, update)
        if is_valid:
            continue
        else:
            make_update_valid(rules, update)
            middle_num = update[len(update) // 2]
            # print(middle_num)
            total += middle_num

    return total


def check_rule_violation(rules, update):
    # print(update)

    update_map = dict()
    for i, num in enumerate(update):
        update_map[num] = i

    for num in update:
        if num not in rules:
            continue

        for rule in rules[num]:
            # print(num, rule)
            if rule not in update_map:
                continue

            if update_map[num] > update_map[rule]:
                return False

        # print()
    return True


def make_update_valid(rules, update):
    # print(update)
    update_map = dict()
    index_map = dict()
    for i, num in enumerate(update):
        update_map[num] = i
        index_map[i] = num

    # print(update_map)
    # print(index_map)

    i = 0
    while not check_rule_violation(rules, update):

        num = update[i]

        if num not in rules:
            i += 1
            i = i % len(update)
            continue

        for rule in rules[num]:
            # print(num, rule)
            if rule not in update_map:
                # print("here?")
                continue

            if update_map[num] > update_map[rule]:
                # print(i, num)
                # print(f"swapping {update[i]} and {update[update_map[rule]]}")
                update[i], update[update_map[rule]] = (
                    update[update_map[rule]],
                    update[i],
                )

                # print(update_map)
                update_map[num] = update_map[rule]
                update_map[rule] = i
                # print(update_map)
                # print(update)

                is_update_now_valid = check_rule_violation(rules, update)
                # print(is_update_now_valid)

                if is_update_now_valid:
                    # print(update)
                    return

                break

        # print(needs_fixing)

        i += 1
        i = i % len(update)

    # print(update)
    is_update_now_valid = check_rule_violation(rules, update)
    # print(is_update_now_valid)
    # print()


def part1():
    total = parse_part1()
    return total


def part2():
    total = parse_part2()
    return total


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
