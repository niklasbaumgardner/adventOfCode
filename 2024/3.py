import re
from pathlib import Path
from loadFile import read_file


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


def parse_mul(string):
    a, b = re.findall("\d+", string)
    return int(a) * int(b)


def part1():
    mul_match = re.findall("mul\(\d{1,3},\d{1,3}\)", DATA)
    # print(mul_match)
    total = 0
    for m in mul_match:
        total += parse_mul(m)
    return total


def part2():
    mul_match = re.findall("mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)", DATA)
    # print(mul_match)
    total = 0
    doing = True
    for m in mul_match:
        if m == "do()":
            doing = True
        elif m == "don't()":
            doing = False
        elif doing:
            # print(m)
            total += parse_mul(m)
    return total


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
