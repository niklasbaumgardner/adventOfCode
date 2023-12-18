from loadFile import read_file
import sys
import queue

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
    def __init__(self, string):
        self.string = string
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

    def move(self, x, y, dir, heatLoss, currentStraight):
        node = self.get(x, y)
        if node is None:
            return 0

    def distanceFromEnd(self, node):
        return abs(self.maxX() - 1 - node.x) + abs(self.maxY() - 1 - node.y)

    def doDijkstra2(self):
        # nodesToVisit = []
        visited = set()

        # open = [(self.get(0, 0), "dir", 0, 0)]
        # closed = []
        frontier = queue.PriorityQueue()

        cameFrom = {}
        costSoFar = {}

        temp = [(self.get(0, 0), "r", 0), (self.get(0, 0), "d", 0)]
        for n in temp:
            frontier.put(n, 0)
            cameFrom[n] = None
            costSoFar[n] = 0

        # shortestPath = {}
        # prevNodes = {}

        while not frontier.empty():
            # What node is the correct node?
            # frontier.sort(key=lambda n: n[-1])
            currNode = frontier.get()
            # print(f"checking node {currNode}")

            node, dir, step = currNode

            if node.x == self.endX and node.y == self.endY:
                break

            neighbors = [(n, d) for n, d in self.graph[node]]
            for neighbor in neighbors:
                nNode, d = neighbor
                newStep = step + 1 if dir == d else 0
                if newStep > 2:
                    continue

                next = (nNode, d, newStep)

                newHeatLoss = costSoFar[currNode] + nNode.heatLoss

                if next not in costSoFar or newHeatLoss < costSoFar[next]:
                    costSoFar[next] = newHeatLoss
                    priority = newHeatLoss + self.distanceFromEnd(nNode)
                    frontier.put(next, priority)
                    cameFrom[next] = currNode
                # if newStep <= 3:
                #     open.append((nNode, d, newStep, tempHeatLoss))

        return cameFrom, costSoFar

    def doDijkstra(self):
        # unvisitedNodes = [
        #     (n, dir) for row in self.matrix for n in row for dir in "lrud"
        # ]
        unvisitedNodes = []
        for k, v in self.graph.items():
            unvisitedNodes += v

        # print("HERE", unvisitedNodes)
        # unvisitedNodes.sort(key=lambda n: n[0].x)
        # unvisitedNodes.sort(key=lambda n: n[0].y)
        # print(unvisitedNodes[:20])

        shortestPath = {}
        prevNodes = {}
        for node in unvisitedNodes:
            shortestPath[node] = 999999999999999999

        startingNode = self.get(0, 0)
        for dir in "rd":
            shortestPath[(startingNode, dir)] = 0
        count = 0
        while unvisitedNodes:
            currMinNode, dir = None, None
            for node, d in unvisitedNodes:
                if currMinNode is None:
                    currMinNode = node
                    dir = d
                elif shortestPath[(node, d)] < shortestPath[(currMinNode, dir)]:
                    currMinNode = node
                    dir = d

            # if node == self.get(self.maxX(), self.maxY()):
            #     break

            pNodeTup = prevNodes.get((currMinNode, dir))
            # print(pNode)
            p2Node = prevNodes.get(pNodeTup)
            p3NodeTup = prevNodes.get(p2Node)
            p3Node, p3Dir = p3NodeTup if p3NodeTup else (None, None)

            neighbors = [(n, d) for n, d in self.graph[currMinNode]]
            # print(neighbors, p3Node)

            if pNodeTup in neighbors:
                neighbors.remove(pNodeTup)

            if p3Node and (abs(currMinNode.x - p3Node.x) > 2):
                numInlineX = currMinNode.x - p3Node.x
                nextNodeInlineX = self.get(
                    currMinNode.x + (1 if numInlineX > 0 else -1), currMinNode.y
                )
                # if nextNodeInlineX:
                #     print(currMinNode, nextNodeInlineX, numInlineX, neighbors)
                temp = (nextNodeInlineX, "l" if numInlineX > 0 else "r")
                if temp in neighbors:
                    neighbors.remove(temp)

            if p3Node and (abs(currMinNode.y - p3Node.y) > 2):
                numInlineY = currMinNode.y - p3Node.y
                nextNodeInlineY = self.get(
                    currMinNode.x, currMinNode.y + (1 if numInlineY > 0 else -1)
                )
                # print(nextNodeInlineY, neighbors)
                temp = (nextNodeInlineY, "u" if numInlineY > 0 else "d")
                if temp in neighbors:
                    neighbors.remove(temp)

            for neighbor, d in neighbors:
                # if pNodeTup:
                #     print(pNodeTup[0], pNodeTup[1])
                # print(currMinNode, dir, "|", neighbor, d)
                tempHeatLoss = shortestPath[(currMinNode, dir)] + neighbor.heatLoss
                if tempHeatLoss < shortestPath[(neighbor, d)]:
                    shortestPath[(neighbor, d)] = tempHeatLoss

                    prevNodes[(neighbor, d)] = (currMinNode, dir)
            # print()
            # if count > 4:
            #     return None, None
            # count += 1
            unvisitedNodes.remove((currMinNode, dir))
        return prevNodes, shortestPath


def part1():
    print("Part 1")

    m = Map(HEATLOSS_MAP_TEXT)
    # print(m)

    cameFrom, costSoFar = m.doDijkstra2()
    # print(cameFrom)
    # # print(costSoFar)
    node = m.get(m.maxX() - 1, m.maxY() - 1)
    # # for ch in "ul":
    # #     print(costSoFar[(node, ch, 0)])
    for k, v in costSoFar.items():
        n, d, s = k
        if n.x == node.x and n.y == node.y:
            print(node, d, s, v)

    print()
    path = {}
    n = (node, "u", 2)
    while n:
        node, dir, s = n
        path[node] = dir
        n = cameFrom[n]
    # 3 (12, 12) u 2 101
    m.printPath(path)

    node = m.get(m.maxX() - 1, m.maxY() - 1)

    path = {}
    n = (node, "l", 0)
    while n:
        node, dir, s = n
        path[node] = dir
        n = cameFrom[n]
    # 3 (12, 12) l 0 102
    m.printPath(path)

    # prevNodes, shortestPath = m.doDijkstra()

    # path = []
    # node = nodes[m.get(12, 12)]
    # while node:
    #     path.append(node)
    #     # print(node)
    #     node = nodes.get(node)

    # path.reverse()
    # print(" -> ".join([str(n) for n in path]))

    # print(nodes)
    # print(shortestPath)
    # for dir in "lu":
    #     print(f"{dir}, {shortestPath[(m.get(m.maxX() - 1, m.maxY() - 1), dir)]}")
    # # print(m.graph)
    # for k, v in m.graph.items():
    #     print(k, v)


def main():
    part1()


main()
