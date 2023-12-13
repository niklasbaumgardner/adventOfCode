from loadFile import read_file
import re
import sys
from functools import cache

# sys.setrecursionlimit(99999)


SPRINGS_TEXT = read_file("./2023/dec12File.txt")


def findAllInString(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def createRows(string):
    lst = []
    for line in string.split("\n"):
        springs, grouping = line.split(" ")
        grouping = [int(g) for g in grouping.split(",")]
        lst.append([springs, grouping])
    return lst


@cache
def isRowValid(springs, grouping):
    brokenSprings = re.findall(r"(#+)", springs)
    if len(brokenSprings) != len(grouping):
        return False

    for index, bs in enumerate(brokenSprings):
        if len(bs) != grouping[index]:
            return False

    return True


def bruteForce(row):
    springs, grouping = row
    missing = findAllInString(springs, "?")

    count = recursiveBrute(springs, tuple(grouping), tuple(missing), len(missing))
    # for i in range(len(grouping)):
    #     count += recursiveBrute(springs, grouping, missing)

    # print("Total count:", count)

    # for i in missing:
    #     for j in missing:
    #         if i == j:
    #             continue
    return count


@cache
def recursiveBrute(springs, grouping, missing, number, count=0):
    if number > 0:
        i = missing[0]
        tempSpringsBroken = springs[:i] + "#" + springs[i + 1 :]
        tempSpringsWorking = springs[:i] + "." + springs[i + 1 :]

        brokenCount = recursiveBrute(
            tempSpringsBroken, grouping, missing[1:], number - 1
        )
        count += brokenCount

        workingCount = recursiveBrute(
            tempSpringsWorking, grouping, missing[1:], number - 1
        )
        count += workingCount

    else:
        # print("checking if row valid", springs, grouping)
        if isRowValid(springs, grouping):
            # print("Spring is valid", springs)
            return 1

    return count


@cache
def otherMethod(s, g):
    if len(s) == 0:
        if len(g) == 0:
            return 1
        return 0

    if len(g) == 0:
        if "#" in s:
            return 0
        return 1

    count = 0
    ch = s[0]
    if ch in ".?":
        count += otherMethod(s[1:], g)

    if (
        ch in "#?"
        and g[0] <= len(s)
        and "." not in s[: g[0]]
        and (g[0] == len(s) or s[g[0]] != "#")
    ):
        # expectedLength = g[0]
        # actual = re.findall(r"(#+)", s)

        # if not actual or len(actual[0]) != expectedLength:
        #     return 0
        # for i in range(expectedLength):
        #     if s[i] == ".":
        #         return 0
        # if len(s) > expectedLength and s[expectedLength] == "#":
        #     return 0

        # print(len(actual[0]), expectedLength, s[expectedLength:], g[1:])
        # print("found match", actual[0], expectedLength, s[expectedLength:], g[1:])
        count += otherMethod(s[g[0] + 1 :], g[1:])

    # if ch == "?":
    #     return otherMethod("#" + s[1:], g) + otherMethod(s[1:], g)

    return count


def part1():
    rows = createRows(SPRINGS_TEXT)
    totalArrangements = 0
    for i, row in enumerate(rows):
        possibleArrangements = bruteForce(row)
        totalArrangements += possibleArrangements
        print(
            f"Part 1: Finished row {i} out of {len(rows)}. Count for this row is {possibleArrangements}"
        )

    print(f"Possible arrangments count is {totalArrangements}")
    # return


def p1():
    rows = createRows(SPRINGS_TEXT)
    totalArrangements = 0
    for i, row in enumerate(rows):
        s, g = row
        # print(s, g)
        possibleArrangements = otherMethod(s, tuple(g))
        totalArrangements += possibleArrangements
        print(
            f"Part 1: Finished row {i} out of {len(rows)}. Count for this row is {possibleArrangements}"
        )
        # return

    print(f"Possible arrangments count is {totalArrangements}")


# return


def part2():
    rows = createRows(SPRINGS_TEXT)
    rows = [["?".join([springs] * 5), grouping * 5] for springs, grouping in rows]
    totalArrangements = 0
    for i, row in enumerate(rows):
        print(row.split("."))
        possibleArrangements = bruteForce(row)
        totalArrangements += possibleArrangements
        print(
            f"Part 2: Finished row {i} out of {len(rows)}. Count for this row is {possibleArrangements}"
        )

    print(f"Possible arrangments count is {totalArrangements}")


def p2():
    rows = createRows(SPRINGS_TEXT)
    rows = [["?".join([springs] * 5), grouping * 5] for springs, grouping in rows]
    totalArrangements = 0
    for i, row in enumerate(rows):
        s, g = row
        possibleArrangements = otherMethod(s, tuple(g))
        totalArrangements += possibleArrangements
        print(
            f"Part 2: Finished row {i} out of {len(rows)}. Count for this row is {possibleArrangements}"
        )

    print(f"Possible arrangments count is {totalArrangements}")


def main():
    # part1()
    p1()

    # part2()
    p2()


main()
