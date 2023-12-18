from helpers.loadFile import read_file
from functools import reduce

LAYOUT_TEXT = read_file("./2023/14.txt")


class Matrix:
    def __init__(self, string):
        self.string = string.strip()
        self.parse()

    def parse(self):
        self.rowsMatrix = (
            []
        )  # [ [ [rows] ] ] split at '#' [ [ [ O, O, O, . ], #, [O, ., O] ] ]
        self.colsMatrix = []  # [ cols ] split at '#'
        self.matrix = []

        for line in self.string.split("\n"):
            row = line.split("#")
            # print(row)
            rowList = tuple([tuple(list(a)) for a in row])
            # print(rowList)
            self.rowsMatrix.append(rowList)

            self.matrix.append(tuple(list(line)))

        # print(self.matrix)

        for i in range(self.getMaxY()):
            colString = ""
            for row in self.matrix:
                colString += row[i]
            col = colString.split("#")
            colList = tuple([tuple(list(a)) for a in col])
            # print(colList)
            self.colsMatrix.append(colList)

        self.matrix = tuple(self.matrix)
        self.rowsMatrix = tuple(self.rowsMatrix)
        self.colsMatrix = tuple(self.colsMatrix)

    def getMaxX(self):
        return len(self.matrix[0])

    def getMaxY(self):
        return len(self.rowsMatrix)

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()

    def tiltedColsToMatrix(self, tiltedCols):
        mLst = []
        for i in range(self.getMaxX()):
            rowString = ""
            for col in tiltedCols:
                colString = "#".join(["".join(lst) for lst in col])
                # print(colString)
                rowString += colString[i]
            mLst.append(rowString)

        mString = "\n".join(mLst)
        return Matrix(mString)

    def tiltedRowsToMatrix(self, tiltedRows):
        mString = "\n".join(
            ["#".join(["".join(lst) for lst in row]) for row in tiltedRows]
        )
        return Matrix(mString)

    def tiltNorthOrSouth(self, dir):
        sortedMatrix = []
        for col in self.colsMatrix:
            newCol = []
            for lst in col:
                sortedLst = sorted(lst, reverse=True if dir == "N" else False)
                newCol.append(tuple(sortedLst))
            sortedMatrix.append(tuple(newCol))
        return self.tiltedColsToMatrix(tuple(sortedMatrix))

    def tiltEastOrWest(self, dir):
        sortedMatrix = []
        for row in self.rowsMatrix:
            newRow = []
            for lst in row:
                sortedLst = sorted(lst, reverse=True if dir == "W" else False)
                newRow.append(tuple(sortedLst))
            sortedMatrix.append(tuple(newRow))
        return self.tiltedRowsToMatrix(tuple(sortedMatrix))

    def tiltLayout(self, dir="N"):
        tiltedMatrix = None

        if dir == "N" or dir == "S":
            tiltedMatrix = self.tiltNorthOrSouth(dir)
            # print(tiltedMatrix)
            # tiledString = "\n".join(["#".join(lst) for lst in tiltedMatrix])
            # for col in tiltedMatrix:
            #     print(col)
            # print(tiledString)
            # for
        elif dir == "E" or dir == "W":
            tiltedMatrix = self.tiltEastOrWest(dir)

        return tiltedMatrix

    def NorSLoad(self, dir="N"):
        load = 0
        for i, row in enumerate(self.matrix):
            numRocks = row.count("O")
            multiplier = self.getMaxY() - (i if dir == "N" else self.getMaxY() - i - 1)
            # print(row, numRocks, multiplier)
            load += numRocks * multiplier
        return load

    def calculateLoad(self, dir):
        if dir == "N" or dir == "S":
            return self.NorSLoad(dir)

        return 0


def createLayout():
    m = Matrix(LAYOUT_TEXT)

    return m


cache = {}


def cycle(stringLayout):
    if stringLayout in cache:
        return cache[stringLayout]

    layout = Matrix(stringLayout)
    nLayout = layout.tiltLayout("N")
    # print("finished tiliting north")
    wLayout = nLayout.tiltLayout("W")
    # print("finished tiliting west")
    sLayout = wLayout.tiltLayout("S")
    # print("finished tiliting south")
    eLayout = sLayout.tiltLayout("E")
    # print("finished tiliting east")

    del layout
    del nLayout
    del wLayout
    del sLayout

    cache[stringLayout] = eLayout

    return eLayout


def part1():
    print("Part 1")

    m = createLayout()
    tiltedM = m.tiltLayout()

    load = tiltedM.calculateLoad("N")

    print(f"Load for layout tilted north is {load}")


def part2():
    print()
    print("Part 2")

    m = createLayout()
    curr = m
    # print(m.getMaxX(), m.getMaxX())
    # return

    temp = {}

    for i in range(1, 1000000001):
        # load = curr.calculateLoad("N")
        # if load == 64:
        #     print(f"load for cycle {i} is 64")

        next = cycle(curr.string)
        curr = next
        if i % 100000000 == 0:
            print(f"cycle {i}:")
        # print(curr)
        # print()

        # load = curr.calculateLoad("N")
        # tup = (curr.string, load)
        # if tup in temp:
        #     temp[tup].append(i)
        #     # print(f"cylce {i} already exists", temp[curr.string])
        # else:
        #     temp[tup] = [i]

    load = curr.calculateLoad("N")
    print(f"Load after 1000000000 cycles is {load}")

    # print(len(temp))
    # cyclicCount = 0
    # for k, v in temp.items():
    #     print(k[1], v[:10])
    #     if len(v) > 1:
    #         cyclicCount += 1

    # print()
    # cyc = 1000000000 % cyclicCount
    # print(f"cycle repeats every {cyclicCount} cycles")

    # for k, v in temp.items():
    #     if len(v) > 1 and v[0] % cyclicCount == cyc:
    #         print(f"load: {k[1]}. cycle:  {v[0]}")

    # for k, v in temp.items():
    #     for c, load in v:
    #         if c == 1000000000 % len(temp):
    #             print(1000000000 % len(temp))
    #             print(v)
    #             print()
    #         elif c == 100:
    #             print(c)
    #             print(v)
    #             print()

    # 112432, 112540,


def main():
    part1()

    part2()


main()
