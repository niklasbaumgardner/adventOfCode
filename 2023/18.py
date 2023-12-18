from helpers.loadFile import read_file
import math

INSTRUCTIONS = read_file("./2023/18.txt")

INT_TO_DIR = {"0": "R", "1": "D", "2": "L", "3": "U"}


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

    def distanceTo(self, other):
        xSquared = (other.x - self.x) ** 2
        ySquared = (other.y - self.y) ** 2
        return math.sqrt(xSquared + ySquared)


def getNextPoint(currentPoint, dir, dist):
    match dir:
        case "R":
            return currentPoint + Point(dist, 0)
        case "L":
            return currentPoint + Point(-int(dist), 0)
        case "D":
            return currentPoint + Point(0, dist)
        case "U":
            return currentPoint + Point(0, -int(dist))


class Node:
    def __init__(self, dir, point, color):
        self.dir = dir
        self.point = point
        self.color = color

    def __str__(self):
        return str(self.point)

    def __repr__(self):
        return str(self)


class Polygon:
    def __init__(self, string):
        self.string = string
        self.parse()

    def parse(self):
        self.nodes = []
        currentPoint = Point(0, 0)
        for line in self.string.split("\n"):
            dir, dist, color = line.split()

            nextPoint = getNextPoint(currentPoint, dir, dist)

            self.nodes.append(Node(dir, nextPoint, color))

            currentPoint = nextPoint

    def perimeter(self):
        perimeter = 0
        for i in range(len(self.nodes)):
            pointI = self.nodes[i].point
            pointI1 = self.nodes[(i + 1) % len(self.nodes)].point
            perimeter += pointI.distanceTo(pointI1)
        return perimeter

    def areaIncludingPerimeter(self):
        sumOfPoints = 0
        for i in range(len(self.nodes)):
            pointI = self.nodes[i].point
            pointI1 = self.nodes[(i + 1) % len(self.nodes)].point

            npI = pointI
            npI1 = pointI1

            thisIter = ((npI.x) * (npI1.y)) - ((npI.y) * (npI1.x))

            # print(
            #     f"point{i} {nodeI.point}. point{(i + 1) % len(self.nodes)} {nodeI1.point} = {thisIter}"
            # )

            sumOfPoints += thisIter
        area = abs(sumOfPoints + self.perimeter()) / 2
        return area + 1


class HexPolygon(Polygon):
    def parseHex(self, colorString):
        hexString = colorString.strip("(#)")
        hex_, dir = hexString[:-1], hexString[-1]

        return INT_TO_DIR[dir], int(hex_, 16)

    def parse(self):
        self.nodes = []
        currentPoint = Point(0, 0)
        for line in self.string.split("\n"):
            _, _, color = line.split()

            dir, dist = self.parseHex(color)

            nextPoint = getNextPoint(currentPoint, dir, dist)

            self.nodes.append(Node(dir, nextPoint, color))

            currentPoint = nextPoint


def part1():
    print("Part 1")

    grid = Polygon(INSTRUCTIONS)

    perimeter = grid.perimeter()
    print(f"Perimeter of grid is {perimeter}")

    area = grid.areaIncludingPerimeter()
    print(f"Area of grid is {area}")


def part2():
    print()
    print("Part 2")

    grid = HexPolygon(INSTRUCTIONS)

    perimeter = grid.perimeter()
    print(f"Perimeter of grid is {perimeter}")

    area = grid.areaIncludingPerimeter()
    print(f"Area of grid is {area}")


def main():
    part1()

    part2()


main()
