from pathlib import Path
from loadFile import read_file
import numpy as np
import math
from copy import deepcopy

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
        return math.sqrt(self.x**2 + self.y**2) > math.sqrt(other.x**2 + other.y**2)

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
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def __str__(self):
        return str(self.point1) + " " + str(self.point2)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.point1)

    def overlaps(self, other):
        return max(self.point1.x, other.point1.x) <= min(
            self.point2.x, other.point2.x
        ) and max(self.point1.y, other.point1.y) <= min(self.point2.y, other.point2.y)


def canSettleBricks(layer1, layer2, nodes):
    if not np.any(layer1 * layer2):
        return True

    layer3 = layer1 + layer2
    unique2, count2 = np.unique(layer2, return_counts=True)
    unique3, count3 = np.unique(layer3, return_counts=True)

    set2 = set([(u, count2[i]) for i, u in enumerate(unique2)])
    set3 = set([(u, count3[i]) for i, u in enumerate(unique3)])

    # print(set2)
    # print(set3)

    for tup in set2:
        u, c = tup
        if u == 0:
            continue

        if tup not in set3:
            continue

        n = nodes[u]
        p1 = n.point1
        p2 = n.point2

        subLayer1 = layer1[p1.x : p2.x + 1, p1.y : p2.y + 1]
        if np.any(subLayer1):
            continue

        # brick is not suported anymore
        print(f"{tup} brick is not supported so it will fall now")
        return True

    return False

    # set(unique non zeros in, count) np.unique(layer1, return_counts=True)
    # check diff between set(layer3) and set(layer2)
    # return number of non zero diffs
    # do i care about layer1 ?


class Grid:
    def __init__(self, string):
        self.string = string
        self.supports = {}
        self.supportedBy = {}
        self.parse()
        # print(self)
        self.settleBricks()
        self.createSupportMaps()

    def __str__(self):
        return str(self.matrix)

    def __repr__(self):
        return str(self)

    def parse(self):
        coords = []
        maxX = 0
        maxY = 0
        maxZ = 0
        for line in self.string.split("\n"):
            c1, c2 = line.split("~")
            x1, y1, z1 = list(map(int, c1.split(",")))
            x2, y2, z2 = list(map(int, c2.split(",")))

            maxX = max(maxX, x1, x2, maxX)
            maxY = max(maxY, y1, y2, maxY)
            maxZ = max(maxZ, z1, z2, maxZ)

            coords.append(((x1, y1, z1), (x2, y2, z2)))

        self.nodes = {}

        # print((maxX + 1, maxY + 1, maxZ + 1))
        # print(coords)
        self.matrix = np.zeros((maxX + 1, maxY + 1, maxZ + 1))
        for i, coord in enumerate(coords):
            c1, c2 = coord
            x1, y1, z1 = c1
            x2, y2, z2 = c2

            p1 = Point(x1, y1)
            p2 = Point(x2, y2)
            node = Node(p1, p2)

            self.nodes[i + 1] = node

            if x2 - x1 != 0:
                self.matrix[x1 : x2 + 1, y1, z1] = i + 1
            elif y2 - y1 != 0:
                self.matrix[x1, y1 : y2 + 1, z1] = i + 1
            elif z2 - z1 != 0:
                self.matrix[x1, y1, z1 : z2 + 1] = i + 1
            else:
                self.matrix[x1, y1, z1] = i + 1

    def settleBricks(self):
        bricksSettled = True
        while bricksSettled:
            bricksSettled = False

            z = 1
            maxZ = self.matrix.shape[2] - 1
            while z < maxZ:
                layer1 = deepcopy(self.matrix[:, :, z])
                layer2 = deepcopy(self.matrix[:, :, z + 1])

                mulLayer = layer1 * layer2

                if not np.any(mulLayer):
                    # we can settle this layer
                    # print(layer1)
                    # print(layer2)
                    bricksSettled = True
                    newLayer = layer1 + layer2
                    self.matrix = np.delete(self.matrix, z + 1, 2)
                    self.matrix[:, :, z] = newLayer
                    maxZ -= 1

                else:
                    # print(layer1)
                    # print(layer2)
                    # we still might be able to settle some bricks on this layer
                    layer3 = layer1 + layer2
                    unique2, count2 = np.unique(layer2, return_counts=True)
                    unique3, count3 = np.unique(layer3, return_counts=True)

                    set2 = set([(u, count2[i]) for i, u in enumerate(unique2)])
                    set3 = set([(u, count3[i]) for i, u in enumerate(unique3)])

                    for tup in set2:
                        u, c = tup
                        if u == 0.0:
                            continue

                        if tup not in set3:
                            continue

                        n = self.nodes[u]
                        p1 = n.point1
                        p2 = n.point2

                        subLayer1 = self.matrix[p1.x : p2.x + 1, p1.y : p2.y + 1, z]
                        if np.any(subLayer1):
                            continue

                        # print(f"swapping {u} from {z+1} to {z}")

                        subLayer2 = deepcopy(
                            self.matrix[p1.x : p2.x + 1, p1.y : p2.y + 1, z + 1]
                        )

                        zerosLayer = np.zeros(subLayer2.shape)
                        fallingLayer = np.full(subLayer2.shape, u)

                        # print(subLayer1, fallingLayer)
                        # print(subLayer2, zerosLayer)

                        self.matrix[p1.x : p2.x + 1, p1.y : p2.y + 1, z] = fallingLayer
                        self.matrix[p1.x : p2.x + 1, p1.y : p2.y + 1, z + 1] = (
                            zerosLayer
                        )
                        bricksSettled = True
                        continue
                z += 1

    # def findBricksToDisintegrate(self):
    #     count = 0
    #     for z in range(1, self.matrix.shape[2] - 1):
    #         layer1 = deepcopy(self.matrix[:, :, z])
    #         layer2 = deepcopy(self.matrix[:, :, z + 1])

    #         for nodeInt in np.unique(layer1):
    #             if nodeInt == 0:
    #                 continue

    #             node = self.nodes[nodeInt]
    #             if (
    #                 self.matrix[node.point1.x, node.point1.y, z]
    #                 == self.matrix[node.point1.x, node.point1.y, z + 1]
    #             ):
    #                 # print(nodeInt)
    #                 # print(layer1)
    #                 # print(layer2)
    #                 # print(node, z, z + 1)
    #                 # print()
    #                 continue

    #             tempLayer = deepcopy(layer1)
    #             tempLayer[
    #                 node.point1.x : node.point2.x + 1,
    #                 node.point1.y : node.point2.y + 1,
    #             ] = np.zeros(
    #                 (
    #                     1 + node.point2.x - node.point1.x,
    #                     1 + node.point2.y - node.point1.y,
    #                 )
    #             )
    #             # print(nodeInt)
    #             # print(layer1)
    #             # print(tempLayer)
    #             # print(layer2)
    #             # print(tempLayer * layer2)

    #             # if np.any(tempLayer * layer2):
    #             # check more here
    #             # fix me
    #             if not canSettleBricks(tempLayer, layer2, self.nodes):
    #                 print("can remove, adding to count")
    #                 count += 1

    #             # print()
    #     # print(np.count_nonzero(np.unique(self.matrix[:, :, -1])), self.matrix[:, :, -1])
    #     count += np.count_nonzero(np.unique(self.matrix[:, :, -1]))
    #     return count


class Tower:
    def __init__(self, string):
        self.string = string
        self.supports = {}
        self.supportedBy = {}
        self.parse()
        # print(self)
        self.settleBricks()
        self.createSupportMaps()

    def parse(self):
        coords = []
        maxX = 0
        maxY = 0
        maxZ = 0
        for line in self.string.split("\n"):
            c1, c2 = line.split("~")
            x1, y1, z1 = list(map(int, c1.split(",")))
            x2, y2, z2 = list(map(int, c2.split(",")))

            maxX = max(maxX, x1, x2)
            maxY = max(maxY, y1, y2)
            maxZ = max(maxZ, z1, z2)

            coords.append(((x1, y1, z1), (x2, y2, z2)))

        self.nodes = {}

        # print((maxX + 1, maxY + 1, maxZ + 1))
        # print(coords)
        self.matrix = [np.zeros((maxX + 1, maxY + 1)) for _ in range(maxZ + 1)]
        for i, coord in enumerate(coords):
            c1, c2 = coord
            x1, y1, z1 = c1
            x2, y2, z2 = c2

            p1 = Point(x1, y1)
            p2 = Point(x2, y2)
            node = Node(p1, p2)

            self.nodeList.append(node)

            self.nodes[i + 1] = node

            if x2 - x1 != 0:
                self.matrix[z1][x1 : x2 + 1, y1] = i + 1
            elif y2 - y1 != 0:
                self.matrix[z1][x1, y1 : y2 + 1] = i + 1
            elif z2 - z1 != 0:
                for z in range(z1, z2 + 1):
                    self.matrix[z][x1, y1] = i + 1
            else:
                self.matrix[z1][x1, y1] = i + 1

    def __str__(self):
        string = ""
        for a in reversed(self.matrix):
            string += str(a) + "\n"
        return string

    def __repr__(self):
        return str(self)

    def settleBricks(self):
        bricksSettled = True
        while bricksSettled:
            bricksSettled = False

            z = 1
            maxZ = len(self.matrix) - 1
            while z < maxZ:
                layer1 = deepcopy(self.matrix[z])
                layer2 = deepcopy(self.matrix[z + 1])

                mulLayer = layer1 * layer2

                if not np.any(mulLayer):
                    # we can settle this layer
                    # print(layer1)
                    # print(layer2)
                    bricksSettled = True
                    newLayer = layer1 + layer2
                    self.matrix = self.matrix[:z] + [newLayer] + self.matrix[z + 2 :]
                    maxZ -= 1
                    continue

                else:
                    # print(layer1)
                    # print(layer2)
                    # we still might be able to settle some bricks on this layer
                    unique2, count2 = np.unique(layer2, return_counts=True)

                    set2 = set([(u, count2[i]) for i, u in enumerate(unique2)])

                    for tup in set2:
                        u, c = tup
                        if u == 0.0:
                            continue

                        n = self.nodes[u]
                        p1 = n.point1
                        p2 = n.point2

                        subLayer1 = layer1[p1.x : p2.x + 1, p1.y : p2.y + 1]
                        if np.any(subLayer1):
                            continue

                        # print(f"swapping {u} from {z+1} to {z}")

                        subLayer2 = deepcopy(layer2[p1.x : p2.x + 1, p1.y : p2.y + 1])

                        zerosLayer = np.zeros(subLayer2.shape)
                        fallingLayer = np.full(subLayer2.shape, u)

                        # print(subLayer1, fallingLayer)
                        # print(subLayer2, zerosLayer)

                        self.matrix[z][p1.x : p2.x + 1, p1.y : p2.y + 1] = fallingLayer
                        self.matrix[z + 1][
                            p1.x : p2.x + 1, p1.y : p2.y + 1
                        ] = zerosLayer
                        bricksSettled = True
                z += 1

    def findBricksToDisintegrate(self):
        bricksThatCanBeRemoved = []
        for nodeInt, supportedBy in self.supportedBy.items():
            if len(supportedBy) > 1:
                bricksThatCanBeRemoved.append(nodeInt)
        for nodeInt, supports in self.supports.items():
            if not supports:
                bricksThatCanBeRemoved.append(nodeInt)

        # print(bricksThatCanBeRemoved)
        return len(bricksThatCanBeRemoved)

    def createSupportMaps(self):
        for nI in self.nodes.keys():
            self.supports[nI] = set()
            self.supportedBy[nI] = set()

        zLength = len(self.matrix)
        for z in range(2, zLength):
            layer = self.matrix[z]

            for nodeInt in np.unique(layer):
                if nodeInt == 0:
                    continue

                node = self.nodes[nodeInt]
                if (
                    self.matrix[z][node.point1.x, node.point1.y]
                    == self.matrix[z - 1][node.point1.x, node.point1.y]
                ):
                    continue

                for x in range(node.point1.x, node.point2.x + 1):
                    for y in range(node.point1.y, node.point2.y + 1):
                        supportInt = self.matrix[z - 1][x, y]
                        if supportInt == 0.0:
                            continue

                        self.supports[supportInt].add(nodeInt)
                        self.supportedBy[nodeInt].add(supportInt)

        print(self.supports)
        print(self.supportedBy)
        print(len(self.supportedBy), len(self.supports))


def part1():
    print("Part 1")
    grid = Tower(DATA)
    # print(grid.matrix.shape)
    print(grid)
    numBricks = grid.findBricksToDisintegrate()

    print()
    # print(grid)
    # 1547 too high
    # 1543 too high
    # 324 wrong
    # 1306 wrong
    # 563 wrong
    # 1243 wrong
    # 87 wrong
    # 453 wrong
    # 873 wrong
    # 474 wrong
    # 480 wrong
    # 483 wrong
    # 250 wrong
    print(f"The number of bricks that can be disintegrated is {numBricks}")


def part2():
    print()
    print("Part 2")


def main():
    part1()
    part2()


main()
