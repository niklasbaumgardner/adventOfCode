from loadFile import read_file
from functools import cache
import sys


sys.setrecursionlimit(10**6)

MIRRORS_TEXT = read_file("./2023/16.txt")


class Node:
    def __init__(self, symbol, x, y):
        self.x = x
        self.y = y
        self.symbol = symbol
        self.energized = 0

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.__str__()


class Map:
    def __init__(self, string):
        self.string = string
        self.parse()
        self.path = set()
        self.nextNodes = []

    def parse(self):
        self.matrix = []
        for y, row in enumerate(self.string.split("\n")):
            rowLst = []
            for x, ch in enumerate(row):
                node = Node(ch, x, y)
                rowLst.append(node)
            self.matrix.append(rowLst)

    def maxX(self):
        return len(self.matrix[0])

    def maxY(self):
        return len(self.matrix)

    def __str__(self):
        return "\n".join(["".join([n.symbol for n in row]) for row in self.matrix])

    def __repr__(self):
        return self.__str__()

    def printEnergized(self):
        return "\n".join(
            [
                "".join(["#" if n.energized > 0 else "." for n in row])
                for row in self.matrix
            ]
        )

    def get(self, x, y):
        if not -1 < x < self.maxX():
            return None
        if not -1 < y < self.maxY():
            return None
        return self.matrix[y][x]

    def moveWhile(self, x, y, dir):
        currNode = self.get(x, y)
        self.nextNodes.append(tuple([x, y, dir]))
        while self.nextNodes:
            x, y, dir = self.nextNodes.pop(0)
            currNode = self.get(x, y)

            # print(f"checking node {currNode} at {x}, {y}")
            if currNode is None:
                continue

            if tuple([x, y, dir]) in self.path:
                continue

            self.path.add(tuple([x, y, dir]))
            currNode.energized = 1

            symbol = currNode.symbol

            if symbol == "|":
                if dir in "LR":
                    self.nextNodes.append(tuple([x, y - 1, "U"]))
                    self.nextNodes.append(tuple([x, y + 1, "D"]))
                    continue

            if symbol == "-":
                if dir in "UD":
                    self.nextNodes.append(tuple([x - 1, y, "L"]))
                    self.nextNodes.append(tuple([x + 1, y, "R"]))
                    continue

            if symbol == "\\":
                if dir == "R":
                    self.nextNodes.append(tuple([x, y + 1, "D"]))
                    continue
                if dir == "U":
                    self.nextNodes.append(tuple([x - 1, y, "L"]))
                    continue
                if dir == "D":
                    self.nextNodes.append(tuple([x + 1, y, "R"]))
                    continue
                if dir == "L":
                    self.nextNodes.append(tuple([x, y - 1, "U"]))
                    continue

            if symbol == "/":
                if dir == "R":
                    self.nextNodes.append(tuple([x, y - 1, "U"]))
                    continue
                if dir == "U":
                    self.nextNodes.append(tuple([x + 1, y, "R"]))
                    continue
                if dir == "D":
                    self.nextNodes.append(tuple([x - 1, y, "L"]))
                    continue
                if dir == "L":
                    self.nextNodes.append(tuple([x, y + 1, "D"]))
                    continue

            if dir == "L":
                self.nextNodes.append(tuple([x - 1, y, dir]))
                continue
            if dir == "R":
                self.nextNodes.append(tuple([x + 1, y, dir]))
                continue
            if dir == "U":
                self.nextNodes.append(tuple([x, y - 1, dir]))
                continue
            if dir == "D":
                self.nextNodes.append(tuple([x, y + 1, dir]))
                continue

    def countEnergized(self):
        count = 0
        for row in self.matrix:
            for node in row:
                count += node.energized

        return count

    def reset(self):
        for row in self.matrix:
            for node in row:
                node.energized = 0
        self.path = set()
        self.nextNodes = []


def part1():
    print("Part 1")

    m = Map(MIRRORS_TEXT)
    # print(m)
    m.moveWhile(0, 0, "R")

    energized = m.countEnergized()
    print(f"After the light move through, the number of energized is {energized}")
    # print(m.printEnergized())


def part2():
    print()
    print("Part 2")

    m = Map(MIRRORS_TEXT)

    startingPoints = []
    for y in [0, m.maxY() - 1]:
        for x in range(m.maxX()):
            if y == 0:
                dir = "D"
            else:
                dir = "U"
            startingPoints.append((x, y, dir))

    for x in [0, m.maxX() - 1]:
        for y in range(m.maxY()):
            if x == 0:
                dir = "R"
            else:
                dir = "L"
            startingPoints.append((x, y, dir))

    eList = []
    for start in startingPoints:
        x, y, dir = start

        m.moveWhile(x, y, dir)

        energized = m.countEnergized()
        # print(f"Starting at ({x}, {y}, {dir}); the number of energized is {energized}")
        eList.append(energized)

        m.reset()

    eMax = max(eList)
    print(f"The max engergized is {eMax}")


def main():
    part1()

    part2()


main()
