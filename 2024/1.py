from pathlib import Path
from helpers import read_file


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


def part1():
    # print(FILE_INPUT)

    left = []
    right = []

    for line in DATA.split("\n"):
        # print(f"|{line}|")
        l, r = line.strip().split()
        # print(f"|{l}|{r}|")
        left.append(int(l))
        right.append(int(r))

    left.sort()
    right.sort()

    diff = 0
    for i in range(len(left)):
        diff += abs(left[i] - right[i])

    return diff


def part2():
    left = []
    right = {}

    for line in DATA.split("\n"):
        # print(f"|{line}|")
        l, r = line.strip().split()

        left.append(int(l))

        r = int(r)

        if r in right:
            right[r] += 1
        else:
            right[r] = 1

    sim_score = 0
    for l in left:
        count = 0
        if l in right:
            count = right[l]

        sim_score += l * count

    return sim_score


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
