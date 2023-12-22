from pathlib import Path
from loadFile import read_file
import math
from functools import cache


PATH = Path(__file__)
DATA = read_file(f"./2023/{PATH.name.split('.')[0]}.txt")


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if type(x) == str:
            x = int(x)
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if type(y) == str:
            y = int(y)
        self._y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return math.sqrt(self.x**2 + self.y**2) > math.sqrt(
            other.x**2 + other.y**2
        )

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other):
        return not self.__gt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def distanceTo(self, other):
        xSquared = (other.x - self.x) ** 2
        ySquared = (other.y - self.y) ** 2
        return math.sqrt(xSquared + ySquared)


class Node:
    def __init__(self, char, point):
        self.char = char
        self.point = point

    def __str__(self):
        return self.char + " " + str(self.point)

    def __repr__(self):
        return str(self)


class Grid:
    def __init__(self, string):
        self.string = string
        self.parse()
        self.currentStep = 0
        self.currentStepNodes = set()

    @property
    def rows(self):
        return len(self.grid)

    @property
    def cols(self):
        return len(self.grid[0])

    @property
    def size(self):
        return (self.cols, self.rows)

    def parse(self):
        self.grid = []
        for y, line in enumerate(self.string.split("\n")):
            row = []
            for x, ch in enumerate(list(line)):
                point = Point(x, y)
                if ch == "S":
                    self.startPoint = point

                node = Node(ch, point)
                row.append(node)
            self.grid.append(row)

    def _at(self, x, y):
        if not (-1 < x < self.cols):
            return None

        if not (-1 < y < self.rows):
            return None

        return self.grid[y][x]

    def at(self, point):
        return self._at(point.x, point.y)

    def __getitem__(self, key):
        if type(key) == tuple:
            if len(key) == 1:
                return self.grid[key]
            elif len(key) == 2:
                return self._at(key[1], key[0])

    def __str__(self):
        return self.string

    def __repr__(self):
        return str(self)

    def getAllNeighbors(self, point):
        points = [
            point + Point(-1, 0),
            point + Point(0, 1),
            point + Point(1, 0),
            point + Point(0, -1),
        ]

        neighbors = []
        for p in points:
            node = self.at(p)
            if node:
                neighbors.append(node)
        return neighbors

    @cache
    def getValidNeighborPoints(self, point):
        validNeighbors = []
        for node in self.getAllNeighbors(point):
            if node.char != "#":
                validNeighbors.append(node.point)
        return validNeighbors

    @cache
    def getValidNeighbors(self, point):
        validNeighbors = []
        for node in self.getAllNeighbors(point):
            if node.char != "#":
                validNeighbors.append(node)
        return validNeighbors

    def takeStep(self):
        if self.currentStep == 0 and not self.currentStepNodes:
            self.currentStepNodes.add(self.startPoint)

        nextStepNodes = set()
        for point in self.currentStepNodes:
            nextStepNodes.update(self.getValidNeighborPoints(point))
            # nextStepNodes |= self.getValidNeighborPoints(point)

        self.currentStep += 1
        self.currentStepNodes = nextStepNodes
        return self.currentStepNodes


class InfiniteGrid(Grid):
    def __init__(self, string):
        super().__init__(string)
        self.cache = {}
        self.currentStepNodes = dict()

    def _at(self, x, y):
        x = x % self.cols
        y = y % self.rows
        if not (-1 < x < self.cols):
            return None

        if not (-1 < y < self.rows):
            return None

        return self.grid[y][x]

    def getAllNeighborPoints(self, point):
        points = [
            point + Point(-1, 0),
            point + Point(0, 1),
            point + Point(1, 0),
            point + Point(0, -1),
        ]

        return points

    @cache
    def getValidNeighborPoints(self, point):
        validNeighbors = []
        for p in self.getAllNeighborPoints(point):
            node = self.at(p)
            if node.char != "#":
                validNeighbors.append(p)
        return validNeighbors

    # def takeStep(self):
    #     if self.currentStep == 0 and not self.currentStepNodes:
    #         self.currentStepNodes[self.startPoint] = 1

    #     # print(f"{self.currentStep}: {self.currentStepNodes}")

    #     nextStepNodes = dict()
    #     for point in self.currentStepNodes:
    #         for n in self.getValidNeighbors(point):
    #             if n.point in nextStepNodes:
    #                 nextStepNodes[n.point] += self.currentStepNodes[point]
    #             else:
    #                 nextStepNodes[n.point] = self.currentStepNodes[point]

    #         # nextStepNodes.update(self.getValidNeighborPoints(point))
    #         # nextStepNodes |= self.getValidNeighborPoints(point)

    #     self.currentStep += 1
    #     self.currentStepNodes = nextStepNodes
    #     return self.currentStepNodes

    def takeStep(self):
        if self.currentStep == 0 and not self.currentStepNodes:
            self.currentStepNodes[self.currentStep] = set([self.startPoint])

        # print(f"{self.currentStep}: {self.currentStepNodes}")

        nextStepNodes = set()
        for point in self.currentStepNodes[self.currentStep]:
            nextStepNodes.update(self.getValidNeighborPoints(point))
            # for p in self.getValidNeighborPoints(point):
            #     if p in nextStepNodes:
            #         nextStepNodes[p] += 1
            #     else:
            #         nextStepNodes[p] = 1

            # nextStepNodes.update(self.getValidNeighborPoints(point))
            # nextStepNodes |= self.getValidNeighborPoints(point)

        self.currentStep += 1
        self.currentStepNodes[self.currentStep] = nextStepNodes
        return self.currentStepNodes

    def func(self, point):
        pass

    def getNumberOfPlotsForStep(step):
        pass


def part1():
    print("Part 1")

    grid = Grid(DATA)
    # print(grid)

    # print(grid.startPoint)
    STEPS = 5
    for _ in range(1, STEPS + 1):
        currentNodes = grid.takeStep()
        print(f"Step {_}: {len(currentNodes)}, {currentNodes}")
    print(
        f"The number of starting nodes after {STEPS} steps is {len(grid.currentStepNodes)}"
    )


def part2():
    print()
    print("Part 2")

    grid = InfiniteGrid(DATA)
    print(grid)
    print(grid.size)
    print(grid.at(Point(-1, -1)), grid.at(Point(-2, -2)))

    print(grid.startPoint)
    STEPS = 333
    lst = []
    for i in range(1, STEPS + 1):
        currentNodes = grid.takeStep()
        lst.append(currentNodes)
        print(f"Step {i}: {len(currentNodes[i])}")
        # print(f"Step {i}: {len(currentNodes[i])}, {currentNodes[i]}")

    print(grid.currentStepNodes[2], grid.currentStepNodes[3])
    print(grid.currentStepNodes[2].union(grid.currentStepNodes[3]))
    print(grid.currentStepNodes[4])
    # print(len(lst), len(lst[2].union(lst[3])))

    lst = []
    for k, v in grid.currentStepNodes.items():
        lst.append(len(v))
        if k > 1:
            print(f"Step {k}: {len(v)}, {len(v) - len(grid.currentStepNodes[k - 2])}")
        else:
            print(f"Step {k}: {len(v)}")
    # print(lst)

    print(grid.size)
    size = grid.size[0]

    print((size // 2), (size // 2) + size, (size // 2) + (2 * size))
    l1 = len(grid.currentStepNodes[size // 2])
    l2 = len(grid.currentStepNodes[size // 2 + size])
    l3 = len(grid.currentStepNodes[size // 2 + 2 * size])

    a = (l3 - (2 * l2) + l1) // 2
    b = l2 - l1 - a
    c = l1

    f = lambda n: a * n**2 + b * n + c

    t = (26501365 - size // 2) // size

    # 5 16 27
    # 65 196 327
    # 93684864250 too low

    print(f(t))
    # total = 0
    # for k, v in grid.currentStepNodes[STEPS].items():
    #     print(k, v)
    #     total += v
    # print(len(grid.currentStepNodes))
    # print(f"The number of starting nodes after {STEPS} steps is {total}")


def main():
    part1()
    part2()


main()
