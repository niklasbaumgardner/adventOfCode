import re
from pathlib import Path
from helpers import read_file, Matrix, Node, Point, BaseGraph, PriorityQueue
from collections import deque


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


MOVEMENT = {"N": Point(0, -1), "E": Point(1, 0), "S": Point(0, 1), "W": Point(-1, 0)}
POINT_TO_DIR = {
    Point(0, -1): "N",
    Point(1, 0): "E",
    Point(0, 1): "S",
    Point(-1, 0): "W",
}
CURRENT_DIR_TO_NEXT_POINTS = {
    "N": [(Point(0, -1), 1), (Point(1, 0), 1001), (Point(-1, 0), 1001)],
    "E": [(Point(1, 0), 1), (Point(0, 1), 1001), (Point(0, -1), 1001)],
    "S": [(Point(0, 1), 1), (Point(1, 0), 1001), (Point(-1, 0), 1001)],
    "W": [(Point(-1, 0), 1), (Point(0, 1), 1001), (Point(0, -1), 1001)],
}
DIR_TO_OPPOSITE_POINT = {
    "S": Point(0, -1),
    "W": Point(1, 0),
    "N": Point(0, 1),
    "E": Point(-1, 0),
}

INFINITY = 99999999999999999999


class WeightedNode(Node):
    def __init__(self, value, x, y):
        super().__init__(value, x, y)
        self.up = None
        self.right = None
        self.down = None
        self.left = None

    def __str__(self):
        return f"{self.value} at ({self.point})"

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
            neighbors.append([self.left, 1001 ** abs(dir_point.y), "W"])

        return neighbors


class WM2(BaseGraph):
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

    def __str__(self):
        # return self.string
        string = ""
        for row in self.matrix:
            row_string = ""
            for node in row:
                row_string += str(node.value)
            string += row_string + "\n"
        return string

    def is_node_valid_edge(self, node):
        return node is not None and node.value != "#"

    def get_edges(self, node, current_dir):
        next_points = CURRENT_DIR_TO_NEXT_POINTS[current_dir]

        edges = []
        for p, cost in next_points:
            n = self.at_point(node.point + p)
            if self.is_node_valid_edge(n):
                # cost = self.get_cost(p, current_dir)
                edges.append((cost, n, POINT_TO_DIR[p]))
        return edges

    def get_cost(self, dir_point, current_dir):
        if dir_point == current_dir:
            return 1

        return 1001

    def dijkstra(self, start_node):
        dist = {}
        prev = {}

        for row in self.matrix:
            for node in row:
                if self.is_node_valid_edge(node):
                    for dir in "NSEW":
                        dist[(node.point, dir)] = INFINITY if node != self.start else 0
                        prev[(node.point, dir)] = None

        pq = PriorityQueue([(0, start_node, "E")])

        while pq.size:
            cost, node, current_dir = pq.pop()

            edges = self.get_edges(node, current_dir)
            for c, edge, e_dir in edges:
                new_cost = cost + c
                prev_cost = dist[(edge.point, e_dir)]

                if new_cost < prev_cost:
                    dist[(edge.point, e_dir)] = new_cost
                    prev[(edge.point, e_dir)] = node

                    pq.push((new_cost, edge, e_dir))

        return dist, prev

    def dijkstra_all_paths(self, start_node):
        dist = {}
        prev = {}

        for row in self.matrix:
            for node in row:
                if self.is_node_valid_edge(node):
                    for dir in "NSEW":
                        dist[(node.point, dir)] = INFINITY if node != self.start else 0
                        prev[(node.point, dir)] = []

        pq = PriorityQueue([(0, start_node, "E")])

        while pq.size:
            cost, node, current_dir = pq.pop()

            edges = self.get_edges(node, current_dir)
            for c, edge, e_dir in edges:
                new_cost = cost + c
                prev_cost = dist[(edge.point, e_dir)]

                if new_cost < prev_cost:
                    dist[(edge.point, e_dir)] = new_cost
                    prev[(edge.point, e_dir)] = [(node, current_dir)]
                    pq.push((new_cost, edge, e_dir))
                elif new_cost == prev_cost:
                    prev[(edge.point, e_dir)].append((node, current_dir))
                    # pq.push((new_cost, edge, e_dir))

        return dist, prev


def part1():
    m = WM2(DATA)
    print(m)
    d, p = m.dijkstra(m.start)
    # print(d, p)
    min_path = INFINITY
    for dir in "NSEW":
        cost = d[(m.end.point, dir)]
        # print(cost)
        if cost < min_path:
            min_path = cost
        # print(d[(m.end.point, dir)])

    # 127484 too high
    return min_path


def part2():
    m = WM2(DATA)
    # print(m)
    d, path = m.dijkstra_all_paths(m.start)
    # print(d, p)
    min_path = INFINITY
    for dir in "NSEW":
        cost = d[(m.end.point, dir)]
        # print(cost)
        if cost < min_path:
            min_path = cost
            min_prev = path[(m.end.point, dir)]

    # 127484 too high

    # print(min_prev)

    # pq = PriorityQueue(min_prev)
    q = deque(min_prev)

    visited = set()
    while q:
        node, dir = q.popleft()

        if (node.point, dir) not in visited:
            prev_edges = path[(node.point, dir)]

            visited.add((node.point, dir))
            for edge, new_dir in prev_edges:
                # if edge == end_node:
                #     return path + [edge]
                q.append((edge, new_dir))

    # print(len(visited))
    for p, _ in visited:
        m.at_point(p).value = "O"

    print(m)

    # for (point, dir), v in path.items():
    #     if len(v) > 1:
    #         print(point, dir, v)

    return m.count_values("O") + 1


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
