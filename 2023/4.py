from loadFile import read_file
import re

CARDS_TEXT = read_file("./2023/4.txt")


def createsCardsList(text):
    cLst = []
    for line in text.split("\n"):
        cardString, numbers = line.split(": ")
        winningNumsStr, pickedNumsString = numbers.split(" | ")
        winningNumbersSet = set(
            [int(num) for num in winningNumsStr.strip().split(" ") if num]
        )
        pickNumbersSet = set(
            [int(num) for num in pickedNumsString.strip().split(" ") if num]
        )
        # print(cardNum, winningNumbersSet, pickNumbersSet)

        cLst.append(tuple([winningNumbersSet, pickNumbersSet]))
    return cLst


CARDS_LIST = createsCardsList(CARDS_TEXT)


def part1():
    total = 0

    for tup in CARDS_LIST:
        winningNums, pickedNums = tup
        numWinningNumbers = len(winningNums.intersection(pickedNums))

        points = 0
        if numWinningNumbers > 0:
            points = 2 ** (numWinningNumbers - 1)
        print(f"this card had {points} points")

        total += points

    print(f"The total number of points is {total}")


def part2():
    CARDS_TUPLE_LIST = createsCardsList(CARDS_TEXT)
    CARDS_TUPLE_LIST = [[card, 1] for card in CARDS_TUPLE_LIST]
    totalCount = 0
    for i in range(len(CARDS_TUPLE_LIST)):
        count = CARDS_TUPLE_LIST[i][1]

        tup = CARDS_TUPLE_LIST[i][0]
        winningNums, pickedNums = tup
        numWinningNumbers = len(winningNums.intersection(pickedNums))
        totalCount += count

        print(
            f"this card had {numWinningNumbers} winning numbers and a count of {count}"
        )

        for j in range(numWinningNumbers):
            CARDS_TUPLE_LIST[i + j + 1][1] += 1 * count

    print(f"The total number of winning cards is {totalCount}")


def main():
    part1()
    part2()


main()
