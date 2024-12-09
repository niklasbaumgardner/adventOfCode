import re
from pathlib import Path
from helpers import read_file, Node, Matrix, Point
from copy import deepcopy
from itertools import combinations


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
            self.visited_nodes
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

    def make_rectangles(self):
        self.find_obstacles()

        looping_obstacles = set()
        looping_obstacles_tuple = set()
        seen = set()

        print(f"0%. {len(self.obstacles)} obstacles")
        coms = combinations(self.obstacles, 3)
        print(f"0%. {len(self.obstacles)**3} combinations")
        for i, n in enumerate(coms):

            # for i, n1 in enumerate(self.obstacles):
            #     for n2 in self.obstacles:
            #         for n3 in self.obstacles:
            n1, n2, n3 = n

            temp = [n1, n2, n3]
            nodes_sorted_x = sorted(temp, key=lambda n: n.point.x)
            nodes_sorted_y = sorted(temp, key=lambda n: n.point.y)
            temp = tuple(nodes_sorted_x)
            if n1 == n2 or n1 == n3 or n2 == n3 or temp in seen:
                continue

            x = None
            y = None
            # find top right
            # print(nodes_sorted_x)
            # print(nodes_sorted_y)
            if ((nodes_sorted_x[1].point.x - nodes_sorted_x[0].point.x) == 1) and (
                (nodes_sorted_y[2].point.y - nodes_sorted_y[1].point.y) == 1
            ):
                # print("top right")
                x = nodes_sorted_x[2].point.x + 1
                y = nodes_sorted_y[0].point.y + 1

            # find bottom right
            elif ((nodes_sorted_x[1].point.x - nodes_sorted_x[0].point.x) == 1) and (
                (nodes_sorted_y[1].point.y - nodes_sorted_y[0].point.y) == 1
            ):
                # print("bottom right")
                x = nodes_sorted_x[2].point.x - 1
                y = nodes_sorted_y[2].point.y + 1

            # find bottom left
            elif ((nodes_sorted_x[2].point.x - nodes_sorted_x[1].point.x) == 1) and (
                (nodes_sorted_y[1].point.y - nodes_sorted_y[0].point.y) == 1
            ):
                # print("bottom left")
                x = nodes_sorted_x[0].point.x - 1
                y = nodes_sorted_y[2].point.y - 1

            # find top left
            elif ((nodes_sorted_x[2].point.x - nodes_sorted_x[1].point.x) == 1) and (
                (nodes_sorted_y[2].point.y - nodes_sorted_y[1].point.y) == 1
            ):
                # print("top left")
                x = nodes_sorted_x[0].point.x + 1
                y = nodes_sorted_y[0].point.y - 1

            # print(x, y)

            if x is None or y is None:
                continue

            node = self.at(x, y)
            if node is None or self.guard.point == node.point or node.value == "#":
                continue

            # print("we got square?")
            # print(n1.point, n2.point, n3.point)
            # print(x, y)
            # print()
            pp = Point(x, y)

            if pp == self.guard.point:
                continue

            points = [n.point for n in nodes_sorted_x] + [pp]

            points_sorted = sorted(points, key=lambda p: p.y)
            points_sorted = sorted(points_sorted, key=lambda p: p.x)
            # print(points_sorted)
            # print()

            if self.check_path(points_sorted):
                looping_obstacles.add(pp)
                looping_obstacles_tuple.add(tuple([pp.x, pp.y]))

            # # seen.add(temp)
            # percent = round(100 * (i + 1) / (len(self.obstacles) ** 3), 2)
            # if percent > 1 and (int(percent) % 10) == 0:
            #     print(f"{round(100 * (i + 1) / (len(self.obstacles)**3), 2)}%")

        return looping_obstacles, looping_obstacles_tuple

    def check_path(self, points_sorted):
        bottom_left, top_left, bottom_right, top_right = points_sorted

        # top and bottom line
        for x in range(top_left.x, top_right.x):
            top_node = self.at(x, top_right.y)
            if top_node.value == "#":
                return False

            bottom_node = self.at(x, bottom_left.y)
            if bottom_node.value == "#":
                return False

        # right and left line
        for y in range(top_right.y, bottom_right.y):
            right_node = self.at(bottom_right.x, y)
            if right_node.value == "#":
                return False

            left_node = self.at(top_left.x, y)
            if left_node.value == "#":
                return False

        return True


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
    print(matrix.guard)
    # print(matrix)

    matrix.step_until_edge()
    # print(matrix)

    return len(matrix.get_visited_nodes())


def part2():
    matrix = PathMatrix(DATA)
    matrix.find_gaurd_node()
    # # print(matrix)
    # # print(matrix.find_gaurd_node())
    # print(matrix)

    # obstacles = matrix.find_obstacles()
    # for o in obstacles:
    #     print(o, o.point)

    looping_points, looping_points_tuple = matrix.make_rectangles()
    looping_points_list = list(looping_points)
    # print(looping_points)
    no_dupes = [
        p for i, p in enumerate(looping_points_list) if p not in looping_points_list[:i]
    ]

    dupes = [
        p for i, p in enumerate(looping_points_list) if p in looping_points_list[:i]
    ]
    print(dupes)

    # print(matrix.is_rectangle([Point(4, 0), Point(9, 1), Point(8, 7), Point(3, 6)]))
    # print(matrix.is_rectangle([Point(2, 3), Point(1, 6), Point(7, 4), Point(6, 7)]))
    # print(matrix.is_rectangle([Point(4, 4), Point(4, 0), Point(0, 4), Point(0, 0)]))

    # 4935 too high
    # 4717 too high

    return len(looping_points), len(looping_points_tuple), len(no_dupes)


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
