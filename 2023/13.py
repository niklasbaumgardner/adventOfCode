from loadFile import read_file
import numpy as np

# from functools import cache


PUZZLE_TEXT = read_file("./2023/13.txt")


class Matrix:
    def __init__(self, string):
        self.parse(string)

    def parse(self, string):
        self.rowsMatrix = []  # [ rows ]
        self.colsMatrix = []  # [ cols ]
        self.rows = {}  # string of row to [ row index ]
        self.cols = {}  # string of col to [ col index ]
        for i, line in enumerate(string.strip().split("\n")):
            if line in self.rows:
                self.rows[line].append(i)
            else:
                self.rows[line] = [i]
            self.rowsMatrix.append(line)

        for i in range(len(self.rowsMatrix[0])):
            colString = ""
            for row in self.rowsMatrix:
                colString += row[i]
            if colString in self.cols:
                self.cols[colString].append(i)
            else:
                self.cols[colString] = [i]
            self.colsMatrix.append(colString)

        # print(self.rowsMatrix)
        # print(self.colsMatrix)
        # print(self.rows)
        # print(self.cols)

    def findHorizontalMirror(self):
        # for k, v in self.rows.items():
        mirror = -1
        for i in range(1, len(self.rowsMatrix)):
            if self.recurseRows(i - 1, i):
                mirror = i
                return i
        # print(mirror)
        return mirror

    # @cache
    def recurseRows(self, left, right):
        if left < 0 or right >= len(self.rowsMatrix):
            return False

        if left == 0 and self.rowsMatrix[left] == self.rowsMatrix[right]:
            return True

        if (
            right == len(self.rowsMatrix) - 1
            and self.rowsMatrix[left] == self.rowsMatrix[right]
        ):
            return True

        if self.rowsMatrix[left] != self.rowsMatrix[right]:
            return False

        return self.recurseRows(left - 1, right + 1)

    def findVerticalMirror(self):
        # for k, v in self.rows.items():
        mirror = -1
        for i in range(1, len(self.colsMatrix)):
            # print(self.recurseCols(i - 1, i), i - 1, i)
            if self.recurseCols(i - 1, i):
                mirror = i
                return i
        # print(mirror)
        return mirror

    # @cache
    def recurseCols(self, left, right):
        if left < 0 or right >= len(self.colsMatrix):
            return False

        # print(
        #     "comparing",
        #     left,
        #     right,
        #     self.colsMatrix[left],
        #     self.colsMatrix[right],
        #     "here",
        # )

        if left == 0 and self.colsMatrix[left] == self.colsMatrix[right]:
            return True

        if (
            right == len(self.colsMatrix) - 1
            and self.colsMatrix[left] == self.colsMatrix[right]
        ):
            # print("GOT HERE", self.colsMatrix[right], self.colsMatrix[-1])
            return True

        if self.colsMatrix[left] != self.colsMatrix[right]:
            return False

        return self.recurseCols(left - 1, right + 1)

    def vDiffsRecurse(self, left, right):
        if left < 0 or right >= len(self.colsMatrix):
            return 0
        return counDiffs(
            self.colsMatrix[left], self.colsMatrix[right]
        ) + self.vDiffsRecurse(left - 1, right + 1)

    def findVerticalDiffs(self, diffs=0):
        mirror = -1
        for i in range(1, len(self.colsMatrix)):
            c = self.vDiffsRecurse(i - 1, i)
            # print(c, i - 1, i)
            if c == diffs:
                mirror = i

        # print(mirror)
        return mirror

    def hDiffsRecurse(self, left, right):
        if left < 0 or right >= len(self.rowsMatrix):
            return 0
        return counDiffs(
            self.rowsMatrix[left], self.rowsMatrix[right]
        ) + self.hDiffsRecurse(left - 1, right + 1)

    def findHorizontalDiffs(self, diffs=0):
        mirror = -1
        for i in range(1, len(self.rowsMatrix)):
            c = self.hDiffsRecurse(i - 1, i)
            # print(c, i - 1, i)
            if c == diffs:
                mirror = i

        # print(mirror)
        return mirror


def createAllPossibleSmudges():
    a = []
    for g in PUZZLE_TEXT.split("\n\n"):
        group = []
        rows = g.split("\n")
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                ch = rows[i][j]
                if ch == ".":
                    newRow = rows[i][:j] + "#" + rows[i][j + 1 :]
                else:
                    newRow = rows[i][:j] + "." + rows[i][j + 1 :]
                # temp = [r if idx != i else newRow for idx,r in enumerate(rows)]
                newG = "\n".join(
                    [r if idx != i else newRow for idx, r in enumerate(rows)]
                )
                group.append(newG)
        a.append(group)
    return a


def createGStrings():
    s = []
    for g in PUZZLE_TEXT.split("\n\n"):
        s.append(g)
    return s


def part1():
    print("Part 1")
    total = 0
    lst = createGStrings()
    for g in lst:
        m = Matrix(g)
        hIndex = m.findHorizontalMirror()
        vIndex = m.findVerticalMirror()
        # return
        # print(hIndex, vIndex)

        hSum = hIndex * 100 if hIndex >= 0 else 0
        vSum = vIndex if vIndex >= 0 else 0

        print(f"Total sum for graph is {vSum + hSum}")
        total += vSum + hSum

    print()
    print(f"Total for all graphs is {total}")


def part2():
    print()
    print("Part 2")
    orig = createGStrings()
    origIndex = {}  # graph index to [hIndex, vIndex]
    for i, g in enumerate(orig):
        m = Matrix(g)
        hIndex = m.findHorizontalMirror()
        vIndex = m.findVerticalMirror()

        origIndex[i] = [hIndex, vIndex]
    # print(origIndex)
    # for k, v in origIndex.items():
    #     print(k, v)
    # return
    allPossss = createAllPossibleSmudges()
    total = 0
    temp = {}
    for i, group in enumerate(allPossss):
        # print(len(group))
        for j, g in enumerate(group):
            m = Matrix(g)
            # print(m.rowsMatrix[0])
            # print("try number", j)
            hIndex = m.findHorizontalMirror()
            vIndex = m.findVerticalMirror()
            # return
            # print(hIndex, vIndex)

            # if hIndex != -1 or vIndex != -1:
            #     print(origIndex[i], hIndex, vIndex)
            if origIndex[i] == [hIndex, vIndex]:
                # print(g)
                # return
                # print(origIndex[i], hIndex, vIndex)
                continue

            hSum = 0
            if hIndex > 0:
                hSum = hIndex * 100
            # hSum = hIndex * 100 if hIndex >= 0 else 0
            vSum = 0
            if vIndex > 0:
                vSum = vIndex

            # vSum = vIndex if vIndex >= 0 else 0
            # if
            # print(f"Total sum for graph {i+1}, try {j+1} is {vSum}, {hSum}")
            # if hSum > 0 and vSum > 0:
            #     origH, origV = origIndex[i]
            #     # print(origH, hIndex, origV, vIndex)
            #     if hIndex == origH:
            #         # print(origH, hIndex, vSum)
            #         total += vSum
            #         # break
            #     elif vIndex == origV:
            #         # print(origV, vIndex, hSum)
            #         total += hSum
            #         # break
            if hSum > 0 or vSum > 0:
                print(
                    f"Total sum for graph {i+1}, try {j+1} is {vSum}, {hSum}. {vIndex}, {hIndex}"
                )
                origH, origV = origIndex[i]
                # print(origH, hIndex, origV, vIndex)
                # print("HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", vSum, hSum)
                # print(g)
                # print()
                total += vSum + hSum
                if i in temp:
                    temp[i].add(
                        tuple(
                            [
                                tuple([hSum, vSum]),
                                tuple([hIndex, vIndex]),
                                tuple([origH, origV]),
                            ]
                        )
                    )
                else:
                    temp[i] = set()
                    temp[i].add(
                        tuple(
                            [
                                tuple([hSum, vSum]),
                                tuple([hIndex, vIndex]),
                                tuple([origH, origV]),
                            ]
                        )
                    )
                # break

                # print(g)
                # if hIndex in origIndex[i] or vIndex in origIndex[i]:
                #     print(
                #         f"Total sum for graph {i+1}, try {j+1} is {vSum + hSum}",
                #         origIndex[i],
                #         hIndex in origIndex[i],
                #         vIndex in origIndex[i],
                #     )
                # else:
                #     print(
                #         "###################################################################################################"
                #     )

    print()
    print(f"Total for all graphs with smudge is {total}")

    # for k, v in temp.items():
    #     # if len(v) == 1:
    #     print(k, v)
    #     print()
    # 40374 wrong


def counDiffs(a, b):
    # print(a, b)
    a = np.array(list(a))
    b = np.array(list(b))
    return np.count_nonzero(a != b)


def p2():
    print("Part 2")
    total = 0
    lst = createGStrings()
    for g in lst:
        m = Matrix(g)
        # print(g)
        hIndex = m.findHorizontalDiffs(diffs=1)
        vIndex = m.findVerticalDiffs(diffs=1)
        # return
        # print(hIndex, vIndex)

        hSum = hIndex * 100 if hIndex >= 0 else 0
        vSum = vIndex if vIndex >= 0 else 0

        print(f"Total sum for graph is {vSum + hSum}")
        total += vSum + hSum

    print()
    print(f"Total for all graphs is {total}")


def main():
    part1()

    part2()
    p2()


main()
