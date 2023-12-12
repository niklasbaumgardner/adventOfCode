from loadFile import read_file


SPACE_TEXT = read_file("./2023/dec11File.txt")


class Matrix:
    def __init__(self, matrixText, space_growth=1):
        self.space_growth = space_growth
        print(self.space_growth)
        self.matrixFromString(matrixText=matrixText)
        self.checkForCosmicExpansion()
        self.findGalaxies()

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

    def getExpandedSpacePosition(self, pos):
        x, y = pos
        expandedX = (
            self.space_growth * len([col for col in self.insertSpaceColsAt if col < x])
            + x
        )

        expandedY = (
            self.space_growth * len([row for row in self.insertSpaceRowsAt if row < y])
            + y
        )

        return [expandedX, expandedY]

    def checkForCosmicExpansion(self):
        self.insertSpaceRowsAt = []
        self.insertSpaceColsAt = []
        colsContainerGalaxies = set()
        for y, row in enumerate(self.matrix):
            rowHasGalaxy = False
            for x, char in enumerate(row):
                if char == "#":
                    rowHasGalaxy = True
                    colsContainerGalaxies.add(x)
            if not rowHasGalaxy:
                self.insertSpaceRowsAt.append(y)

        for x in range(self.maxX()):
            if x in colsContainerGalaxies:
                continue

            self.insertSpaceColsAt.append(x)

        print(self.insertSpaceRowsAt)
        print(self.insertSpaceColsAt)

    def findGalaxies(self):
        self.galaxies = []
        for y, row in enumerate(self.matrix):
            for x, char in enumerate(row):
                if char == "#":
                    self.galaxies.append(tuple([x, y]))

    def getDistanceBetweenAllGalaxies(self):
        totalDistance = 0
        distanceChecked = set()  # [galaxy1, galaxy2]
        for galaxy1 in self.galaxies:
            for galaxy2 in self.galaxies:
                if (
                    galaxy1 == galaxy2
                    or tuple([galaxy1, galaxy2]) in distanceChecked
                    or tuple([galaxy2, galaxy1]) in distanceChecked
                ):
                    continue

                x1, y1 = self.getExpandedSpacePosition(galaxy1)
                x2, y2 = self.getExpandedSpacePosition(galaxy2)

                distance = abs(y2 - y1) + abs(x2 - x1)
                totalDistance += distance
                distanceChecked.add(tuple([galaxy1, galaxy2]))

        return totalDistance


def part1():
    SPACE = Matrix(SPACE_TEXT)
    # print(SPACE)
    # print(SPACE.galaxies, len(SPACE.galaxies))

    distance = SPACE.getDistanceBetweenAllGalaxies()

    print(f"Total distance between all galaxies is {distance}")

    # 9742154


def part2():
    SPACE = Matrix(SPACE_TEXT, 10)

    distance = SPACE.getDistanceBetweenAllGalaxies()

    print(f"Total distance between all galaxies is {distance}")


def main():
    part1()

    part2()


main()
