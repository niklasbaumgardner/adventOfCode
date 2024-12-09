import re
from pathlib import Path
from helpers import read_file, Matrix
from itertools import combinations


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class AntenaMatrix(Matrix):
    def __init__(self, data):
        super().__init__(data)
        self.antenas = dict()
        self.antinodes = set()
        self.find_antenas()

    def find_antenas(self):
        for row in self.matrix:
            for node in row:
                if node.value != ".":
                    if node.value in self.antenas:
                        self.antenas[node.value].append(node)
                    else:
                        self.antenas[node.value] = [node]

    def find_all_antinodes(self):
        for a, nodes in self.antenas.items():
            self.find_antinodes_for_antena(nodes)

    def find_antinodes_for_antena(self, nodes):
        coms = combinations(nodes, 2)
        for ns in coms:
            n1, n2 = ns
            if n1 == n2:
                continue

            left_node = None
            right_node = None
            if n1.point.x < n2.point.x:
                left_node = n1
                right_node = n2
            elif n1.point.x > n2.point.x:
                left_node = n2
                right_node = n1
            elif n1.point.y < n2.point.y:
                left_node = n1
                right_node = n2
            else:
                left_node = n2
                right_node = n1

            # print(left_node, right_node)
            diff1 = left_node.point - right_node.point
            diff2 = right_node.point - left_node.point

            a1 = left_node.point + diff1
            a2 = right_node.point + diff2
            # print(a1, a2)

            if self.at_point(a1) is not None:
                self.antinodes.add(a1)

            if self.at_point(a2) is not None:
                self.antinodes.add(a2)
            # print()

    def find_all_antinodes_part2(self):
        for a, nodes in self.antenas.items():
            self.find_antinodes_in_line_for_antena(nodes)

    def find_antinodes_in_line_for_antena(self, nodes):
        coms = combinations(nodes, 2)

        for ns in coms:
            n1, n2 = ns
            if n1 == n2:
                continue

            left_node = None
            right_node = None
            if n1.point.x < n2.point.x:
                left_node = n1
                right_node = n2
            elif n1.point.x > n2.point.x:
                left_node = n2
                right_node = n1
            elif n1.point.y < n2.point.y:
                left_node = n1
                right_node = n2
            else:
                left_node = n2
                right_node = n1

            # self.antinodes.add(left_node.point)
            # self.antinodes.add(right_node.point)

            # print(left_node, right_node)
            diff1 = left_node.point - right_node.point
            diff2 = right_node.point - left_node.point

            a1 = left_node.point
            a1_node = self.at_point(a1)
            while a1_node is not None:
                self.antinodes.add(a1)

                a1 = a1 + diff1
                a1_node = self.at_point(a1)

            a2 = right_node.point
            a2_node = self.at_point(a2)
            while a2_node is not None:
                self.antinodes.add(a2)

                a2 = a2 + diff2
                a2_node = self.at_point(a2)


def part1():
    matrix = AntenaMatrix(DATA)
    # print(matrix)
    # print(matrix.antenas)
    matrix.find_all_antinodes()
    # print(len(matrix.antinodes), matrix.antinodes)
    return len(matrix.antinodes)


def part2():
    matrix = AntenaMatrix(DATA)
    # print(matrix)
    # print(matrix.antenas)
    matrix.find_all_antinodes_part2()
    # print(len(matrix.antinodes), matrix.antinodes)
    return len(matrix.antinodes)


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
