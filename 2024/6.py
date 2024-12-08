import re
from pathlib import Path
from helpers import read_file, Node, Matrix, Point
from copy import deepcopy


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class PathMatrix(Matrix):
    def find_gaurd_node(self):
        for r, row in enumerate(self.matrix):
            for c, node in enumerate(row):
                if node.value in set(["^", ">", "v", "<"]):
                    new_node = Node("x", node.point.x, node.point.y)
                    self.matrix[r][c] = new_node
                    self.guard = node
                    return self.guard

    def mark_visited(self, node):
        try:
            if self.visited_nodes:
                return self.visited_nodes
        except:
            self.visited_nodes = set()

        node.value = "x"
        self.visited_nodes.add(node)

    def get_visited_nodes(self):
        return self.visited_nodes

    def step(self):
        # step until obstacle

        # get node at next step
        x = self.guard.point.x
        y = self.guard.point.y

        if self.guard.value == "^":
            y -= 1
        elif self.guard.value == ">":
            x += 1
        elif self.guard.value == "v":
            y += 1
        elif self.guard.value == "<":
            x -= 1

        node = self.at(x, y)
        if node is None:
            # print(f"Reached edge at {self.guard.point}")
            return

        # print(f"At node {node}. {node.point}")
        if node.value == "#":
            # print("hit obstacle. rotating gaurd")
            self.rotate_gaurd_90()
            return node

        else:
            self.guard.point.x = x
            self.guard.point.y = y
            self.mark_visited(node)
            return node

    def step_until_edge(self):
        node = self.at_point(self.guard.point)
        print(node)
        while node:
            node = self.step()

    def rotate_gaurd_90(self):
        if self.guard.value == "^":
            self.guard.value = ">"
        elif self.guard.value == ">":
            self.guard.value = "v"
        elif self.guard.value == "v":
            self.guard.value = "<"
        elif self.guard.value == "<":
            self.guard.value = "^"

    # part 2
    def find_obstacles(self):
        try:
            if self.obstacles:
                return self.obstacles
        except:
            self.obstacles = []

        for row in self.matrix:
            for node in row:
                if node.value == "#":
                    self.obstacles.append(node)

        return self.obstacles

    # def make_node(self, left_node, right_node, top_node, bottom_node):
    #     if

    def get_counts(self, nodes_dict):
        counts = {}
        for k, n in nodes_dict.items():
            if n in counts:
                counts[n]["edge"].append(k)
                counts[n]["count"] += 1
            else:
                counts[n] = {"edge": [k], "count": 1}
        return counts

    def is_rectangle(self, points):
        sorted_points = sorted(points, key=lambda p: p.x)
        sorted_points = sorted(sorted_points, key=lambda p: p.y)
        print("HERTERERE", sorted_points)

        #####################################
        p1, p2, p3, p4 = sorted_points
        cx = (p1.x + p2.x + p3.x + p4.x) / 4
        cy = (p1.y + p2.y + p3.y + p4.y) / 4

        print(cx, cy)
        center = Point(cx, cy)
        print(center)

        print(
            p1.distance_to(center),
            p2.distance_to(center),
            p3.distance_to(center),
            p4.distance_to(center),
        )
        return p1.distance_to(center) == p3.distance_to(center) and p2.distance_to(
            center
        ) == p4.distance_to(center)

    def make_rectangles(self):
        self.find_obstacles()

        seen = set()

        for n1 in self.obstacles:
            for n2 in self.obstacles:
                for n3 in self.obstacles:

                    temp = tuple([n1, n2, n3])
                    if n1 == n2 or n1 == n3 or n2 == n3 or temp in seen:
                        continue

                    xs = set()
                    for x in [n1.point.x, n2.point.x, n3.point.x]:
                        for diff in [-1, 0, 1]:
                            if x + diff < 0:
                                continue
                            xs.add(x + diff)

                    ys = set()
                    for y in [n1.point.y, n2.point.y, n3.point.y]:
                        for diff in [-1, 0, 1]:
                            if y + diff < 0:
                                continue
                            ys.add(y + diff)

                    potential_points = []
                    for x in xs:
                        for y in ys:
                            p = Point(x, y)
                            potential_points.append(p)

                    print(potential_points)

                    # for

                    #####################################################

                    print(n1.point, n2.point, n3.point)
                    left_edge = min(n1.point.x, n2.point.x, n3.point.x)
                    right_edge = max(n1.point.x, n2.point.x, n3.point.x)
                    top_edge = min(n1.point.y, n2.point.y, n3.point.y)
                    bottom_edge = max(n1.point.y, n2.point.y, n3.point.y)

                    # print(left_edge, right_edge, top_edge, bottom_edge)

                    # top_left = Node("#", left_edge, top_edge)
                    # top_right = Node("#", right_edge, top_edge)
                    # bottom_right = Node("#", right_edge, bottom_edge)
                    # bottom_left = Node("#", left_edge, bottom_edge)
                    # test = set()
                    # for n in [
                    #     top_left,
                    #     top_right,
                    #     bottom_right,
                    #     bottom_left,
                    #     n1,
                    #     n2,
                    #     n3,
                    # ]:
                    #     test.add(tuple([n.point.x, n.point.y]))

                    # print(test, len(test))
                    nodes = [n1, n2, n3]
                    left_node = find_node(left_edge, "x", nodes)
                    right_node = find_node(right_edge, "x", nodes)
                    top_node = find_node(top_edge, "y", nodes)
                    bottom_node = find_node(bottom_edge, "y", nodes)

                    counts = self.get_counts(
                        {
                            "left": left_node,
                            "right": right_node,
                            "top": top_node,
                            "bottom": bottom_node,
                        }
                    )
                    print(counts)
                    print()

                    seen.add(temp)
                    if len(seen) > 20:
                        return

                # find position for each node


def find_node(edge, xOrY, nodes):
    for node in nodes:
        if xOrY == "x":
            if edge == node.point.x:
                return node
        else:
            if edge == node.point.y:
                return node


def part1():
    matrix = PathMatrix(DATA)
    matrix.find_gaurd_node()
    # print(matrix)
    # print(matrix.find_gaurd_node())
    print(matrix)

    matrix.step_until_edge()
    print(matrix)

    return len(matrix.get_visited_nodes())


def part2():
    matrix = PathMatrix(DATA)
    # matrix.find_gaurd_node()
    # # print(matrix)
    # # print(matrix.find_gaurd_node())
    # print(matrix)

    # obstacles = matrix.find_obstacles()
    # for o in obstacles:
    #     print(o, o.point)

    # matrix.make_rectangles()

    print(matrix.is_rectangle([Point(4, 0), Point(9, 1), Point(8, 7), Point(3, 6)]))
    print(matrix.is_rectangle([Point(2, 3), Point(1, 6), Point(7, 4), Point(6, 7)]))
    print(matrix.is_rectangle([Point(4, 4), Point(4, 0), Point(0, 4), Point(0, 0)]))

    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
