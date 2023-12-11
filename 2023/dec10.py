from loadFile import read_file


MATRIX_TEXT = read_file("dec10File.txt")
CONNECTERS = {
    "|": {"N": set(["|", "7", "F"]), "S": set(["|", "L", "J"])},
    "-": {"E": set(["-", "7", "J"]), "W": set(["-", "L", "F"])},
    # the rest need fixing
    "L": {"N": set(["|", "7", "F"]), "W": set(["|", "7", "F"])},
    "J": {"S": set(["|", "7", "F"]), "E": set(["|", "7", "F"])},
    "7": {"N": set(["|", "7", "F"]), "E": set(["|", "7", "F"])},
    "F": {"N": set(["|", "7", "F"]), "W": set(["|", "7", "F"])},
}

# CONNECTERS = {
#     "|": set(["N", "S"]),
#     "-": set(["E", "W"]),
#     "L": set(["N", "E"]),
#     "J": set(["N", "W"]),
#     "7": set(["S", "W"]),
#     "F": set(["S", "E"]),
# }


class Matrix:
    def __init__(self, matrixText):
        self.matrixFromString(matrixText=matrixText)

    def __str__(self):
        string = ""
        for lst in self.matrix:
            string += "".join(lst) + "\n"
        return string

    def matrixFromString(self, matrixText):
        self.matrix = []
        for line in matrixText.split("\n"):
            lst = list(line)
            self.matrix.append(lst)

    def maxX(self):
        return len(self.matrix[0])

    def maxY(self):
        return len(self.matrix)

    def at(self, x, y):
        if not (-1 < x < self.maxX()):
            return None

        if not (-1 < y < self.maxY()):
            return None

        return self.matrix[y][x]

    def getAdjacentCoords(self, x, y):
        maybeAdjCoords = [
            tuple([x, y - 1]),
            tuple([x + 1, y]),
            tuple([x, y + 1]),
            tuple([x - 1, y]),
        ]

        adjCoords = []

        for coord in maybeAdjCoords:
            xCoord, yCoord = coord
            if self.at(xCoord, yCoord):
                adjCoords.append(coord)

        return adjCoords

    def isStepValid(self, curr, next):
        currX, currY = curr
        nextX, nextY = next
        char = self.at(nextX, nextY)

        if char is None:
            return False, None

        dir = ""
        xDiff = nextX - currX
        yDiff = nextY - currY

        if xDiff == 1:
            dir = "E"
        elif xDiff == -1:
            dir = "W"
        elif yDiff == 1:
            dir = "S"
        elif yDiff == -1:
            dir = "N"

        print("direction:", dir, curr, next)

        if char not in CONNECTERS:
            return False

        print(dir in CONNECTERS[char], dir, CONNECTERS[char])
        return dir in CONNECTERS[char]
        transform = CONNECTERS[char].get(dir)
        # print("transform:", transform)

        if transform is None:
            return False

        return True

    def getSPosition(self):
        for yIndex, row in enumerate(self.matrix):
            for xIndex, char in enumerate(row):
                if char == "S":
                    return tuple([xIndex, yIndex])

    def createPath(self):
        start = self.getSPosition()
        print("start:", start)

        nextSteps = [start]
        # visited = dict()  # coord -> num times visited
        visited = set()
        path = dict()  # coord -> set(next coords)
        stepsAway = 0
        paths = dict()  # coord -> path

        print(nextSteps)

        while nextSteps:
            curr = nextSteps.pop(0)
            x, y = curr
            # print("current:", curr)
            visited.add(curr)
            # if curr in visited:
            #     visited[curr] += 1
            # else:
            #     visited[curr] = 1
            # print("visited:", visited)
            # if curr in path:
            #     path[curr] = min([path[curr], stepsAway])
            # else:
            #     path[curr] = stepsAway

            adjCoords = self.getAdjacentCoords(x, y)
            # print("adjacent:", adjCoords)
            for nextStep in adjCoords:
                stepIsValid = self.isStepValid(curr, nextStep)
                # numTimesVisited = visited.get(nextStep)
                # if (
                #     stepIsValid
                #     and numTimesVisited is None
                #     or (numTimesVisited is not None and numTimesVisited < 3)
                # ):
                if stepIsValid and nextStep not in path:
                    nextSteps.append(nextStep)

                    if path.get(curr):
                        print(
                            "more than 1 option",
                            self.matrix[y][x],
                            curr,
                            nextStep,
                            path.get(curr),
                        )
                        path[curr].add(nextStep)
                        stepsAway += 1
                        if stepsAway > 2:
                            return

                    else:
                        path[curr] = set([nextStep])

            print("next steps:", nextSteps)
            print()
            # stepsAway += 1
            # if stepsAway == 2:
            # return path
        for k in path.keys():
            path[k] = list(path[k])

        self.path = path
        self.start = start
        return path, start

    def walkMap(self, node):
        if node is None:
            return 0

        node = node[0]
        print("i am here", node)

        return 1 + self.walkMap(self.path.get(node))

    def countPath(self):
        nodes = self.path[self.start]

        allPathLengths = []
        for node in nodes:
            # print(node)
            allPathLengths.append(self.walkMap([node]))

        return max(allPathLengths)


def part1():
    matrix = Matrix(MATRIX_TEXT)
    # print(matrix)

    matrix.createPath()

    print("path:")
    for k, v in matrix.path.items():
        print(f"{k}: {v}")
    print(len(matrix.path))

    length = matrix.countPath()
    print("length of path:", length)

    # currNode = start
    # while currNode:
    #     nextNodes = path[currNode]

    #     for nNodes in nextNodes:


def part2():
    pass


def main():
    part1()

    part2()


main()
