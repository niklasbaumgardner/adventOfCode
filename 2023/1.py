from loadFile import read_file
import re

FILE_INPUT = read_file("./2023/1.txt")

STRING_TO_NUM = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part1():
    # print(FILE_INPUT)
    fileLines = FILE_INPUT.split("\n")
    numsList = []
    for line in fileLines:
        # print(line)
        nums = re.findall(r"\d", line)
        first = nums[0]
        last = nums[-1]
        num = int(first + last)
        # print(first, last, num)
        numsList.append(num)
        # print(nums)
    total = sum(numsList)
    print(f"Total of all lines is {total}")


def part2():
    fileLines = FILE_INPUT.split("\n")
    numsList = []
    for line in fileLines:
        # print(line)
        nums = re.findall(
            r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line
        )
        # print(nums)
        first = nums[0]
        last = nums[-1]

        # print(first, last, line)
        if first in STRING_TO_NUM:
            # print(first)
            first = STRING_TO_NUM[first]
        if last in STRING_TO_NUM:
            # print(last)
            last = STRING_TO_NUM[last]

        num = int(first + last)
        print(first, last, num, nums, line)
        numsList.append(num)
        # print(nums)
        # print()
    total = sum(numsList)
    print(f"Total of all lines is {total}")


def main():
    part1()

    part2()


main()
