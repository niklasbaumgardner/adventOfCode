from loadFile import read_file
import re

MATRIX_TEXT = read_file("./2023/3.txt")
SYMBOLS = set(["/", "@", "=", "%", "&", "*", "$", "-", "+", "#"])


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
            # TODO: need to separate line not by every char because numbers should not be split
            # lst = re.findall(r"(\d+|\@|\#|\$|\%|\&|\*|\.)", line)
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
        coords = []
        for xAdj in [x - 1, x, x + 1]:
            for yAdj in [y - 1, y, y + 1]:
                if (
                    xAdj == x
                    and yAdj == y
                    or xAdj < 0
                    or yAdj < 0
                    or xAdj >= self.maxX()
                    or yAdj >= self.maxY()
                ):
                    continue
                coords.append((xAdj, yAdj))
        return coords

    def getAdjacentChars(self, x, y):
        adjacentChars = []

        for coord in self.getAdjacentCoords(x, y):
            xCoord, yCoord = coord
            val = self.at(xCoord, yCoord)
            if val is None:
                continue

            adjacentChars.append(val)
        return adjacentChars

    def getNumberStartingAt(self, x, y):
        row = self.matrix[y]
        numString = ""

        while x < self.maxX():
            char = row[x]

            if char.isdigit():
                numString += char
                x += 1
            else:
                break

        num = None
        if numString != "":
            num = int(numString)
        return num, x

    def getNumberAt(self, x, y):
        row = self.matrix[y]
        currX = x

        if not row[currX].isdigit():
            return None, x, x
        # while -1 < currX < self.maxX():
        #     char = row[currX]

        #     if char.isdigit():
        #         numString = char + numString
        #         currX -= 1
        #     else:
        #         break
        while row[currX].isdigit():
            currX -= 1
        # the current position is no longer a digit so go back to last know digit
        currX += 1

        # print("trying to get number starting at", currX, y)

        num, endX = self.getNumberStartingAt(currX, y)
        # print("got num from num starting at", num, currX, x, endX)

        return num, currX, endX


MATRIX = Matrix(MATRIX_TEXT)
# towSet = set()
# for row in MATRIX.matrix:
#     print(len(row))
#     towSet.add(len(row))
# print(towSet)


def isSymbolInList(lst):
    for ele in lst:
        if ele in SYMBOLS:
            return True
    return False


# def isDigitInList(lst):
#     for ele in lst:
#         if


def part1():
    total = 0
    for yIndex, lst in enumerate(MATRIX.matrix):
        xIndex = 0
        while xIndex < len(lst):
            char = lst[xIndex]
            if char.isdigit():
                num, xEnd = MATRIX.getNumberStartingAt(xIndex, yIndex)
                # print(num, xIndex, xEnd, lst[xIndex:xEnd])
                # adjCoordsSet = set()
                # for x in range(xIndex, xEnd):
                #     for coord in MATRIX.getAdjacentCoords(x, yIndex):
                #         adjCoordsSet.add(coord)

                # adjSymbolsList = []
                # for coord in adjCoordsSet:
                #     x, y = coord
                #     adjSymbolsList += MATRIX.getAdjacentChars(x, y)
                adjSymbolsList = []
                for x in range(xIndex, xEnd):
                    adjSymbolsList += MATRIX.getAdjacentChars(x, yIndex)

                if isSymbolInList(adjSymbolsList):
                    print(f"number is next to symbol. {num}")
                    total += num
                # return
                xIndex = xEnd
            else:
                xIndex += 1

        # for xIndex, char in enumerate(lst):
        #     if char.isdigit():
        #         # print(f"({xIndex}, {yIndex})", char)
        #         adjs = MATRIX.getAdjacentChars(xIndex, yIndex)
        #         # print(adjs)
        #         if isSymbolInList(adjs):
        #             num = int(char)
        #             total += num

    print(f"The total of all part numbers is {total}")


def part2():
    total = 0
    excludedCoords = set()
    symbolCoords = []
    for yIndex, lst in enumerate(MATRIX.matrix):
        for xIndex, char in enumerate(lst):
            if char == "*":
                print(f"got symbol at {xIndex}, {yIndex}")
                adjCoords = MATRIX.getAdjacentCoords(xIndex, yIndex)
                adjNumSet = set()
                for coord in adjCoords:
                    x, y = coord
                    # adjNumSet.add(MATRIX.getNumberAt(x, y))
                    # print(temp)
                    num, startX, endX = MATRIX.getNumberAt(x, y)
                    if num is None:
                        continue
                    # print(f"got number {num} from {x}, {y}")

                    adjNumSet.add(tuple([num, tuple([startX, endX]), y]))

                # print(adjNumSet)
                if len(adjNumSet) == 2:
                    multple = 1
                    for tup in adjNumSet:
                        num, xCoords, yCoord = tup
                        multple *= num

                        # for x in range(xCoords[0], xCoords[1]):
                        #     excludedCoords.add(tuple([x, yCoord]))
                    print(f"multiple is {multple}")
                    total += multple
                # print()
                # if yIndex == 1 and xIndex > 20:
                #     return
                else:
                    symbolCoords.append(tuple([tuple([xIndex, yIndex]), adjNumSet]))

    # print(symbolCoords)
    print(f"The sum of all gear ratios is {total}")
    for i in range(len(symbolCoords)):
        if i > -1 and i < 10:
            print(symbolCoords[i])
    # 77495589 is too low
    # 78642389 wrong
    print(len(symbolCoords))


def main():
    part1()

    part2()


main()
