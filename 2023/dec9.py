from loadFile import read_file


def getHistory():
    return [
        [int(char) for char in line.split(" ")]
        for line in read_file("dec9File.txt").split("\n")
    ]


def getDiffs(entry):
    entryDiffs = []
    for index, val in enumerate(entry):
        if index == 0:
            continue

        diff = val - entry[index - 1]
        entryDiffs.append(diff)
    return entryDiffs


def listContainsOnlyZeros(lst):
    for num in lst:
        if num != 0:
            return False
    return True


def part1():
    HISTORY = getHistory()
    total = 0
    for entry in HISTORY:
        entryDiffs = [entry]

        while not listContainsOnlyZeros(entryDiffs[-1]):
            entryDiffs.append(getDiffs(entryDiffs[-1]))
        # print(entryDiffs)

        entryDiffs[-1].append(0)
        for i in range(len(entryDiffs) - 1, 0, -1):
            val = entryDiffs[i][-1]
            prevVal = entryDiffs[i - 1][-1]
            result = val + prevVal
            entryDiffs[i - 1].append(result)

        predictedVal = entryDiffs[0][-1]
        print(f"predicted value is {predictedVal}")
        total += predictedVal
        # for e in entryDiffs:
        #     print(e)
        # print()

    print(f"Sum of predicted values is {total}")
    # 1964638360 wrong


def part2():
    HISTORY = getHistory()
    total = 0
    for entry in HISTORY:
        entryDiffs = [entry]

        while not listContainsOnlyZeros(entryDiffs[-1]):
            entryDiffs.append(getDiffs(entryDiffs[-1]))

        for lst in entryDiffs:
            lst.reverse()

        entryDiffs[-1].append(0)
        for i in range(len(entryDiffs) - 1, 0, -1):
            val = entryDiffs[i][-1]
            prevVal = entryDiffs[i - 1][-1]
            result = prevVal - val
            entryDiffs[i - 1].append(result)

        predictedVal = entryDiffs[0][-1]
        print(f"predicted value is {predictedVal}")
        total += predictedVal
        # for e in entryDiffs:
        #     print(e)
        # print()

    print(f"Sum of predicted values is {total}")


def main():
    part1()

    part2()


main()
