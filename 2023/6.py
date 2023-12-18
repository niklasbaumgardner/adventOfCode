from loadFile import read_file


TIMES_AND_DISTANCES = read_file("./2023/6.txt")


def parse(string):
    times = []
    distances = []

    for i, line in enumerate(string.split("\n")):
        if i == 0:
            times = [int(ch) for ch in line.split(" ") if ch.isdigit()]
        elif i == 1:
            distances = [int(ch) for ch in line.split(" ") if ch.isdigit()]

    td = []
    for i, t in enumerate(times):
        td.append([t, distances[i]])

    return td


def parse2(string):
    times = []
    distances = []

    for i, line in enumerate(string.split("\n")):
        if i == 0:
            times = int("".join([ch for ch in line.split(" ") if ch.isdigit()]))
        elif i == 1:
            distances = int("".join([ch for ch in line.split(" ") if ch.isdigit()]))

    return [[times, distances]]


def getDistance(s, time):
    return s * time


def howManyWins(t, dtb):
    timesThatWon = 0
    for i in range(1, t):
        d = getDistance(i, t - i)
        if d > dtb:
            timesThatWon += 1
    return timesThatWon


def part1():
    td = parse(TIMES_AND_DISTANCES)
    print(td)

    total = 1
    for t, d in td:
        total *= howManyWins(t, d)

    print(f"Total wins multiplied together is {total}")


def part2():
    td = parse2(TIMES_AND_DISTANCES)
    print(td)

    total = 1
    for t, d in td:
        total *= howManyWins(t, d)

    print(f"Total wins multiplied together is {total}")


def main():
    part1()

    part2()


main()
