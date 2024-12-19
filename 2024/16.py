import re
from pathlib import Path
from helpers import read_file, Matrix, Node, Point, BaseGraph, PriorityQueue


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

    def __str__(self):
        # return self.string
        string = ""
        for row in self.matrix:
            row_string = ""
            for node in row:
                row_string += str(node.value)
            string += row_string + "\n"
        return string

    def find_best_path(self):
        self.paths = dict()
        for row in self.matrix:
            for n in row:
                if n.value != "#":
                    for dir in ["N", "S", "E", "W"]:

                        self.paths[n.point] = (INFINITY, None)

        starting_dir = "E"
        self.paths[self.start.point] = (0, None)
        queue = [(self.start, 0, starting_dir)]

        visited = set()

        while queue:
            (node, current_weight, dir) = queue.pop(0)
            # current_weight = self.paths[node.point][0]

            visited.add(node.point)

            neighbors = node.get_valid_neighbors(dir)
            # print(node, neighbors)
            # return
            for n, weight, n_dir in neighbors:
                if n.point not in visited:
                    new_weight = current_weight + weight
                    if new_weight < self.paths[n.point][0]:
                        self.paths[n.point] = (new_weight, node)

                        queue.append((n, new_weight, n_dir))

            queue = sorted(queue, key=lambda x: x[1])

            visited.add(n.point)
        # print(self.paths)
        # min_path = (INFINITY, "")
        # for dir in ["N", "S", "E", "W"]:
        #     path_len = self.paths[(self.end.point, dir)][0]
        #     if path_len < min_path[0]:
        #         min_path = (path_len, dir)

        print(len(visited))
        return self.paths[self.end.point][0]

    def find_best_path_v3(self):
        self.paths = dict()
        dist = dict()
        prev = dict()
        for row in self.matrix:
            for n in row:
                if n.value != "#":
                    self.paths[n.point] = [(INFINITY, None)]
                    dist[n.point] = INFINITY
                    prev[n.point] = None

        starting_dir = "E"
        self.paths[self.start.point] = [(0, None)]
        dist[self.start.point] = 0
        queue = [(self.start, 0, starting_dir)]

        visited = set()

        while queue:
            (node, current_weight, dir) = queue.pop(0)
            # current_weight = self.paths[node.point][0]
            if node.point in visited:
                continue

            neighbors = node.get_valid_neighbors(dir)
            # print(node, neighbors)
            # return
            for n, weight, n_dir in neighbors:
                if n == node:
                    continue
                # if n.point not in visited:
                # if n != node:
                new_weight = current_weight + weight
                current_weight_to_node = self.paths[n.point][0][0]

                if self.paths[n.point][0][1] is None:
                    self.paths[n.point].pop(0)

                # if (
                #     not len(self.paths[n.point])
                #     or new_weight <= self.paths[n.point][0][0]
                # ):
                self.paths[n.point].append((new_weight, node))
                # self.paths[n.point] = sorted(
                #     self.paths[n.point], key=lambda x: x[0]
                # )
                queue.append((n, new_weight, n_dir))

                # if new_weight < current_weight_to_node:
                #     # self.paths[n.point].pop(0)
                #     if self.paths[n.point][0][1] is None:
                #         self.paths[n.point].pop(0)
                #     self.paths[n.point].append((new_weight, node))
                #     queue.append((n, new_weight, n_dir))
                # elif new_weight == current_weight_to_node:
                #     self.paths[n.point].append((new_weight, node))
                #     queue.append((n, new_weight, n_dir))

            visited.add(node.point)
            queue = sorted(queue, key=lambda x: x[1])

        # print(self.paths)
        # for k, v in self.paths.items():
        #     print(k, v)
        # min_path = (INFINITY, "")
        # for dir in ["N", "S", "E", "W"]:
        #     path_len = self.paths[(self.end.point, dir)][0]
        #     if path_len < min_path[0]:
        #         min_path = (path_len, dir)

        # print(len(visited))
        return self.paths[self.end.point][0]

    def find_nodes_along_path_v3(self, best_path_weight):
        path = set()
        nodes = [(0, self.end)]
        # for k, v in self.paths.items():
        #     print(k, v)

        # for k, v in self.paths.items():
        #     for t in v:
        #         nodes.append(t)
        # nodes = sorted(nodes, key=lambda x: x[0])
        # print(nodes)
        visited = set()

        count = 0
        while nodes:
            weight, node = nodes.pop(0)
            if not node:
                continue

            if weight > best_path_weight:
                continue

            # if node.point in visited:
            #     continue

            if node == self.start:
                print("HIT STARTING POINT", len(path))
                count += 1
                # if count >= 3:
                break

            path.add(node.point)

            ns = self.paths[node.point]
            for w, n in ns:
                print(w, n)
                if n.point not in visited and w <= best_path_weight:
                    # if n == self.start:
                    #     print(len(path), path)
                    #     for p in path:
                    #         self.at_point(p).value = "O"
                    #     return
                    nodes.append((w, n))
                    visited.add(n.point)

            # node = self.
            # [node.point][1]
            # nodes = sorted(nodes, key=lambda x: x[0])
            print(nodes)

        print(len(path), path)
        print(self.paths[self.end.point])

        for p in path:
            self.at_point(p).value = "O"

        return len(path)


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
    m = WeightedMatrix(DATA)
    print(m)
    weight = m.find_best_path_v3()
    print(len(m.paths))
    for k, v in m.paths.items():
        print(k, v)
    print("done", weight)

    length = m.find_nodes_along_path_v3(weight[0])
    print(m)

    return length


def main():
    print(f"Part 1: {part1()}")
    # print(f"Part 2: {part2()}")


main()
