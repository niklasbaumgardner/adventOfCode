from loadFile import read_file


MATRIX_TEXT = read_file("./2023/dec10File.txt")
CONNECTIONS = {
    "S": {
        "N": set(["|", "7", "F"]),
        "S": set(["|", "L", "J"]),
        "E": set(["-", "7", "J"]),
        "W": set(["-", "L", "F"]),
    },
    "|": {"N": set(["|", "7", "F"]), "S": set(["|", "L", "J"])},
    "-": {"E": set(["-", "7", "J"]), "W": set(["-", "L", "F"])},
    "L": {"N": set(["|", "7", "F"]), "E": set(["-", "7", "J"])},
    "J": {"N": set(["|", "7", "F"]), "W": set(["-", "L", "F"])},
    "7": {"S": set(["|", "L", "J"]), "W": set(["-", "L", "F"])},
    "F": {"S": set(["|", "L", "J"]), "E": set(["-", "7", "J"])},
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
        currChar = self.at(currX, currY)
        nextChar = self.at(nextX, nextY)

        if nextChar is None:
            return False

        if nextChar not in CONNECTIONS:
            return False

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

        # print("direction:", dir, currChar, nextChar)

        if dir not in CONNECTIONS[currChar]:
            return False

        # print(nextChar in CONNECTIONS[currChar][dir])
        return nextChar in CONNECTIONS[currChar][dir]

    def getSPosition(self):
        for yIndex, row in enumerate(self.matrix):
            for xIndex, char in enumerate(row):
                if char == "S":
                    return tuple([xIndex, yIndex])

    def createPath(self):
        start = self.getSPosition()

        nextSteps = [start]
        path = dict()  # coord -> set(next coords)

        while nextSteps:
            curr = nextSteps.pop(0)
            x, y = curr
            char = self.at(x, y)

            adjCoords = self.getAdjacentCoords(x, y)
            for nextStep in adjCoords:
                stepIsValid = self.isStepValid(curr, nextStep)
                if stepIsValid and nextStep not in path:
                    nextSteps.append(nextStep)

                    if char == "S" and path.get(curr):
                        path[curr].append(nextStep)
                    else:
                        path[curr] = [nextStep]

        for k in path.keys():
            path[k] = list(path[k])

        self.path = path
        self.start = start
        return path, start

    def walkMap(self, node):
        depth = 0
        while node is not None:
            if node is None:
                break

            depth += 1

            nextNode = self.path.get(node[0])
            node = nextNode

        return depth

    def countPath(self):
        nodes = self.path[self.start]

        allPathLengths = []
        for node in nodes:
            # print(node)
            allPathLengths.append(self.walkMap([node]))

        return max(allPathLengths)

    def countTilesInsidePath(self):
        # if there is two paths on a col, then all tiles inbetween are inside
        # if more than two paths on col, then the its the tiles between 0 and 1, 2 and 3, 4 and 5, etc
        count = 0
        for yIndex, row in enumerate(self.matrix):
            pathsInRow = []
            for xIndex in range(len(row)):
                coord = tuple([xIndex, yIndex])
                char = self.at(xIndex, yIndex)

                if coord in self.path and (
                    "N" in CONNECTIONS[char] or "S" in CONNECTIONS[char]
                ):
                    pathsInRow.append(xIndex)

            if (len(pathsInRow) - 1) == pathsInRow[-1] - pathsInRow[0]:
                print(
                    "No non path tiles in this row",
                    len(pathsInRow) - 1,
                    pathsInRow[-1] - pathsInRow[0],
                )
                print()
                continue
            countForRow = 0
            print(f"found {len(pathsInRow)} paths in row {yIndex}")
            for i in range(0, len(pathsInRow) - 1, 2):
                print("searching", pathsInRow[i], pathsInRow[i + 1])
                for x in range(pathsInRow[i], pathsInRow[i + 1]):
                    coord = tuple([x, yIndex])
                    if coord in self.path:
                        continue
                    countForRow += 1
                # numTiles = pathsInRow[i + 1] - pathsInRow[i] - 1
            print(f"Found {countForRow} non path tiles")
            print()

            count += countForRow

        return count


def part1():
    matrix = Matrix(MATRIX_TEXT)
    # print(matrix)

    matrix.createPath()

    # print("path:")
    # for k, v in matrix.path.items():
    #     print(f"{k}: {v}")
    print(len(matrix.path))

    length = matrix.countPath()
    print("length of path:", length)

    # correct number is 6951


def part2():
    matrix = Matrix(MATRIX_TEXT)

    matrix.createPath()

    count = matrix.countTilesInsidePath()

    print(f"There are {count} tiles inside the path")


def main():
    part1()

    part2()


main()
