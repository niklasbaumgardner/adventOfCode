import re
from pathlib import Path
from helpers import read_file, Matrix, Node, Point


MOVEMENT = {"N": Point(0, -1), "E": Point(1, 0), "S": Point(0, 1), "W": Point(-1, 0)}
PATH = Path(__file__)
YEAR = str(PATH).split("/")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class WeightedNode(Node):
    def __init__(self, value, x, y):
        super().__init__(value, x, y)
        self.up = None
        self.right = None
        self.down = None
        self.left = None

    def __str__(self):
        return f"{self.value}"

    def get_neighbors(self):
        neighbors = []
        if self.up:
            neighbors.append(self.up)
        if self.right:
            neighbors.append(self.right)
        if self.down:
            neighbors.append(self.down)
        if self.left:
            neighbors.append(self.left)

        return neighbors

    def get_valid_neighbors(self, dir):
        dir_point = MOVEMENT[dir]
        neighbors = []
        if self.up and self.up.value != "#":
            neighbors.append([self.up, 1001 ** abs(dir_point.x), "N"])
        if self.right and self.right.value != "#":
            neighbors.append([self.right, 1001 ** abs(dir_point.y), "E"])
        if self.down and self.down.value != "#":
            neighbors.append([self.down, 1001 ** abs(dir_point.x), "S"])
        if self.left and self.left.value != "#":
            neighbors.append([self.left, 1001 ** abs(dir_point.x), "W"])

        return neighbors


class WeightedMatrix(Matrix):
    def parse(self):
        self.matrix = []
        for y, line in enumerate(self.string.split("\n")):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                node = WeightedNode(value, x, y)
                row.append(node)

                if node.value == "S":
                    self.start = node
                elif node.value == "E":
                    self.end = node

            self.matrix.append(row)

        for row in self.matrix:
            for node in row:
                node.left = self.at(node.point.x - 1, node.point.y)
                node.up = self.at(node.point.x, node.point.y - 1)
                node.right = self.at(node.point.x + 1, node.point.y)
                node.down = self.at(node.point.x, node.point.y + 1)

    def find_best_path(self):
        paths = dict()
        for row in self.matrix:
            for n in row:
                if n.value != "#":
                    paths[n.point] = (999999999, None)

        paths[self.start.point] = (0, None)
        starting_dir = "E"
        queue = [(self.start, 0, starting_dir)]

        visited = set()

        while queue:
            (node, current_weight, dir) = queue.pop(0)
            current_weight = paths[node.point][0]

            # if node == self.end:
            #     print(queue)
            #     return current_weight

            # visited.add((node.point, dir))

            neighbors = node.get_valid_neighbors(dir)
            # print(node, neighbors)
            # return
            for n, weight, n_dir in neighbors:
                if (n.point, dir) not in visited:
                    new_weight = paths[node.point][0] + weight
                    if new_weight < paths[n.point][0]:
                        paths[n.point] = (new_weight, node)

                        queue.append((n, new_weight, n_dir))

            queue = sorted(queue, key=lambda x: x[1])
            print(queue)
            return

            # visited.add(n.point)
        return paths[self.end.point][0]


def part1():
    m = WeightedMatrix(DATA)
    print(m)
    weight = m.find_best_path()

    # 127484 too high
    return weight


def part2():
    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
