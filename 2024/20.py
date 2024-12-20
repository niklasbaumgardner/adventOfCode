import re
from pathlib import Path
from helpers import read_file, BaseGraph, Node, Point


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class Maze(BaseGraph):
    def parse(self):
        self.matrix = []
        for y, line in enumerate(self.string.split("\n")):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                node = Node(value, x, y)
                row.append(node)

                if node.value == "S":
                    self.start = node
                elif node.value == "E":
                    self.end = node

            self.matrix.append(row)

    def is_node_valid_edge(self, node):
        return node is not None and node.value != "#"

    def find_cheats(self):
        path = self.bfs(self.start, self.end)

        for i in range(len(path)):
            for j in range(i + 1, len(path)):
                # print(i, j, path[i], path[j])

                n1 = path[i]
                n2 = path[j]

                p1 = n1.point
                p2 = n2.point

                diff = p1.straight_distance_to(p2)
                if diff is None:
                    continue
                # print(diff, i, j, p1, p2)
                if diff.x != 0 and abs(diff.x) <= 2:
                    print(diff, p1, p2)
                elif diff.y != 0 and abs(diff.y) <= 2:
                    print(diff, p1, p2, i, j)


def part1():
    m = Maze(DATA)
    print(m)

    path = m.bfs(m.start, m.end)
    m.find_cheats()

    print(len(path), path)
    return


def part2():
    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
