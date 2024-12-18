from pathlib import Path
from helpers import read_file, Point, Matrix, Node
import time

PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class Matrix18(Matrix):
    def __init__(self, points, width, height):
        # super().__init__(data)
        self.points = set(points)
        self.create(width, height)

    def __str__(self):
        # return self.string
        string = ""
        for row in self.matrix:
            row_string = ""
            for node in row:
                row_string += str(node.value)
            string += row_string + "\n"
        return string

    def create(self, width, height):
        self.matrix = []
        for y in range(height + 1):
            row = []
            for x in range(width + 1):
                node = Node(".", x, y)
                if node.point in self.points:
                    node.value = "#"

                row.append(node)
            self.matrix.append(row)

    def get_neightbors(self, node):
        neighbors = []
        for p in [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]:
            n = self.at_point(node.point + p)
            if n and n.value == ".":
                neighbors.append(n)
        return neighbors

    def shortest_path(self):
        self.start = self.at(0, 0)
        self.end = self.at(self.x - 1, self.y - 1)

        visited = set()

        q = [(self.start, [self.start])]
        while q:
            node, path = q.pop(0)
            edges = self.get_neightbors(node)
            for edge in edges:
                if edge not in visited:
                    if edge == self.end:
                        return path + [edge]
                    q.append((edge, path + [edge]))
                    visited.add(edge)
        return []


def part1():
    points = []
    for line in DATA.strip().split("\n"):
        x, y = list(map(int, line.strip().split(",")))
        points.append(Point(x, y))
        if len(points) > 1024:
            break
    # print(len(points), points)

    m = Matrix18(points[:1024], 70, 70)
    print(m)
    path = m.shortest_path()
    # print(path)
    for n in path:
        n.value = "O"
    print(m)

    # 323 too high
    return len(path) - 1


def part2():
    points = []
    for line in DATA.strip().split("\n"):
        x, y = list(map(int, line.strip().split(",")))
        points.append(Point(x, y))

    # print(len(points), points)

    start = time.time()

    point = None

    for i in range(1, len(points)):
        temp_points = points[:i]
        m = Matrix18(temp_points, 70, 70)
        # print(m)
        path = m.shortest_path()
        if len(path) == 0:
            point = temp_points[-1]
            break
    end = time.time()

    print(f"Completed Part 2 in {end - start} seconds")
    return point


def main():
    # print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
