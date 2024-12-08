from pathlib import Path
from helpers import read_file
from itertools import product
import time


PATH = Path(__file__)
YEAR = str(PATH).split("/")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


def eval_line(total, nums, operatins):
    for op in operatins:
        # equation = [None] * (len(nums) + len(op))
        # equation[::2] = nums
        # equation[1::2] = op
        # print(equation)
        temp = nums[::1]
        temp_ops = op[::1]
        # print(temp)
        equation = []
        a = 0
        equation.append(temp.pop(0))
        equation.append(temp_ops.pop(0))
        equation.append(temp.pop(0))
        a = eval("".join(equation))
        while temp:
            n = temp.pop(0)
            o = temp_ops.pop(0)
            a = eval(f"{a}{o}{n}")

        if total == a:
            return True
    return False


def part1():
    # print(DATA)
    lines = []
    max_nums = 0
    for line in DATA.split("\n"):
        total, nums = line.split(": ")
        total = int(total)
        # print(total, nums)
        # nums = list(map(int, nums.split()))
        nums = nums.split()
        # print(nums)
        lines.append([total, nums])
        max_nums = max(max_nums, len(nums))

    operations = ["+", "*"]
    possible_operations = {}
    for i in range(1, max_nums):
        possible_operations[i] = [list(p) for p in product(operations, repeat=i)]
    # print(possible_operations[3])

    total_sum = 0
    for line in lines:
        total, nums = line
        if eval_line(total, nums, possible_operations[len(nums) - 1]):
            # print(f"{total}, {nums}")
            total_sum += total

    return total_sum


def part2():
    lines = []
    max_nums = 0
    for line in DATA.split("\n"):
        total, nums = line.split(": ")
        total = int(total)
        nums = nums.split()
        lines.append([total, nums])
        max_nums = max(max_nums, len(nums))

    operations = ["+", "*", ""]
    possible_operations = {}
    for i in range(1, max_nums):
        possible_operations[i] = [list(p) for p in product(operations, repeat=i)]

    total_sum = 0
    for line in lines:
        total, nums = line
        if eval_line(total, nums, possible_operations[len(nums) - 1]):
            total_sum += total

    return total_sum


def main():
    start = time.time()
    answer = part1()
    end = time.time()
    print(f"Part 1: {answer}. (Completed in {end - start} seconds)")

    start = time.time()
    answer = part2()
    end = time.time()
    print(f"Part 2: {answer}. (Completed in {end - start} seconds)")


main()
