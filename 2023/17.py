from helpers.loadFile import read_file
import sys

# import queue

HEATLOSS_MAP_TEXT = read_file("./2023/17.txt")

OPP_DIR = {"l": "r", "r": "l", "u": "d", "d": "u"}

OPP_SYM = {"l": ">", "r": "<", "u": "v", "d": "^"}


class Node:
    def __init__(self, heatLoss, x, y):
        self.x = x
        self.y = y
        self.heatLoss = int(heatLoss)
        self.stringVal = heatLoss

    def __str__(self):
        return f"{self.heatLoss} ({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        return self.x > other.x or self.y or other.y


class Map:
    def __init__(self, string, minStreak, maxStreak):
        self.string = string
        self.minStreak = minStreak
        self.maxStreak = maxStreak
        self.parse()
        self.constructGraph()
        self.endX = self.maxX() - 1
        self.endY = self.maxY() - 1

    def parse(self):
        self.matrix = []
        for y, row in enumerate(self.string.split("\n")):
            rowLst = []
            for x, ch in enumerate(row):
                node = Node(ch, x, y)
                rowLst.append(node)
            self.matrix.append(rowLst)

    def constructGraph(self):
        self.graph = {}
        for y, row in enumerate(self.matrix):
            for x, node in enumerate(row):
                l = self.get(x - 1, y)
                r = self.get(x + 1, y)
                u = self.get(x, y - 1)
                d = self.get(x, y + 1)
                neighbors = []
                if l:
                    neighbors.append((l, "r"))
                if r:
                    neighbors.append((r, "l"))
                if u:
                    neighbors.append((u, "d"))
                if d:
                    neighbors.append((d, "u"))
                self.graph[node] = neighbors

    def printPath(self, path):
        string = ""
        for row in self.matrix:
            stringRow = ""
            for n in row:
                if n in path:
                    stringRow += OPP_SYM[path[n]]
                else:
                    stringRow += n.stringVal
            string += stringRow + "\n"
        print(string)
        return "\n".join(["".join([str(n) for n in row]) for row in self.matrix])

    def maxX(self):
        return len(self.matrix[0])

    def maxY(self):
        return len(self.matrix)

    def __str__(self):
        return "\n".join(["".join([str(n) for n in row]) for row in self.matrix])

    def __repr__(self):
        return self.__str__()

    def get(self, x, y):
        if not -1 < x < self.maxX():
            return None
        if not -1 < y < self.maxY():
            return None
        return self.matrix[y][x]

    def distanceFromEnd(self, node):
        return abs(self.maxX() - 1 - node.x) + abs(self.maxY() - 1 - node.y)

    def doDijkstra2(self):
        # nodesToVisit = []
        visited = set()

        # open = [(self.get(0, 0), "dir", 0, 0)]
        # closed = []
        # frontier = queue.PriorityQueue()
        frontier = []

        cameFrom = {}
        costSoFar = {}

        temp = [(self.get(0, 0), "u", 0), (self.get(0, 0), "l", 0)]
        for n in temp:
            frontier.append(n)
            cameFrom[n] = None
            costSoFar[n] = 0

        # shortestPath = {}
        # prevNodes = {}

        while frontier:
            # What node is the correct node?
            # frontier.sort(key=lambda n: n[-1], reverse=True)
            # frontier.sort(key=lambda n: costSoFar[n])
            # frontier.sort(key=lambda n: n[0].x + n[0].y)
            frontier.sort(key=lambda n: n[0].x + n[0].y, reverse=True)
            frontier.sort(key=lambda n: costSoFar[n])
            # print(frontier[:10])
            # frontier.sort(key=lambda n: costSoFar[n])
            # currNode = frontier.get()
            currNode = frontier.pop(0)
            # print(f"checking node {currNode}")

            node, dir, step = currNode

            if node.x == self.endX and node.y == self.endY and step >= self.minStreak:
                print(currNode, costSoFar[currNode])
                # print("are we gettinng here?")
                break

            # print("current", currNode)
            neighbors = [(n, d) for n, d in self.graph[node]]
            for neighbor in neighbors:
                nNode, d = neighbor

                if d == OPP_DIR[dir]:
                    continue

                newStep = step + 1 if dir == d else 1
                if newStep > self.maxStreak:
                    continue

                if step < self.minStreak and dir != d:
                    continue

                next = (nNode, d, newStep)

                # print("next", next)

                newHeatLoss = costSoFar[currNode] + nNode.heatLoss

                if next not in costSoFar or newHeatLoss < costSoFar[next]:
                    costSoFar[next] = newHeatLoss
                    # priority = newHeatLoss + self.distanceFromEnd(nNode)
                    # frontier.put(next, priority)
                    frontier.append(next)
                    cameFrom[next] = currNode

                    # if nNode.x == self.endX and nNode.y == self.endY:
                    #     print(next, costSoFar[next])
                    #     print("neighbor node")
                    #     print()
                    #     break
                # if newStep <= 3:
                #     open.append((nNode, d, newStep, tempHeatLoss))
            # print()

        return cameFrom, costSoFar


def part1():
    print("Part 1")

    m = Map(HEATLOSS_MAP_TEXT, 1, 3)
    # print(m)

    cameFrom, costSoFar = m.doDijkstra2()
    # print(cameFrom)
    # # print(costSoFar)
    node = m.get(m.maxX() - 1, m.maxY() - 1)
    # # for ch in "ul":
    # #     print(costSoFar[(node, ch, 0)])
    pathNodes = []
    for k, v in costSoFar.items():
        n, d, s = k
        if n.x == node.x and n.y == node.y:
            pathNodes.append(((node, d, s), v))

    pathNodes.sort(key=lambda x: x[-1])
    # print(pathNodes)

    print(f"Min heat loss path is {pathNodes[0]}")

    path = {}
    n = pathNodes.pop(0)[0]
    while n:
        node, dir, s = n
        path[node] = dir
        n = cameFrom[n]
    m.printPath(path)


def part2():
    print()
    print("Part 2")

    m = Map(HEATLOSS_MAP_TEXT, 4, 10)

    cameFrom, costSoFar = m.doDijkstra2()
    # print(cameFrom)
    # print()
    # print(costSoFar)

    node = m.get(m.maxX() - 1, m.maxY() - 1)
    pathNodes = []
    for k, v in costSoFar.items():
        n, d, s = k
        if n.x == node.x and n.y == node.y and s >= 3:
            pathNodes.append(((node, d, s), v))

    pathNodes.sort(key=lambda x: x[-1])
    print(pathNodes)

    print(f"Min heat loss path is {pathNodes[0]}")

    path = {}
    n = pathNodes.pop(0)[0]
    while n:
        node, dir, s = n
        path[node] = dir
        n = cameFrom[n]
    m.printPath(path)

    # wrong: 1136 too high, 1113


def main():
    part1()

    part2()


main()
