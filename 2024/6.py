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

    def step_no_mark(self):
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
            # self.mark_visited(node)
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

    def try_every_spot(self):
        cycle_points = set()

        for row in self.matrix:
            for node in row:
                if node.point == self.guard.point or node.value != ".":
                    continue
                print(node, node.point)

                orig_value = deepcopy(node.value)
                node.value = "#"

                print(node, node.point)

                orig_guard_point = deepcopy(self.guard.point)

                if self.check_for_cycle():
                    cycle_points.add(node.point)

                self.guard.point = orig_guard_point

                print(self.guard.point)
                print()

                node.value = orig_value

        return cycle_points

    def check_for_cycle(self):
        path = dict()

        node = self.at_point(self.guard.point)
        while node:
            next_node = self.step_no_mark()
            if node.point in path and path[node.point] == next_node:
                return True

            path[node.point] = next_node

            node = next_node


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
    # print(matrix.guard)
    # print(matrix)

    matrix.step_until_edge()
    # print(matrix)

    return len(matrix.get_visited_nodes())


def part2():
    matrix = PathMatrix(DATA)
    matrix.find_gaurd_node()
    print(matrix.guard, matrix.guard.point)
    # # print(matrix)
    # # print(matrix.find_gaurd_node())
    # print(matrix)

    # obstacles = matrix.find_obstacles()
    # for o in obstacles:
    #     print(o, o.point)

    points = matrix.try_every_spot()
    # looping_points_list = list(looping_points)
    # print(looping_points)
    # no_dupes = [
    #     p for i, p in enumerate(looping_points_list) if p not in looping_points_list[:i]
    # ]

    # dupes = [
    #     p for i, p in enumerate(looping_points_list) if p in looping_points_list[:i]
    # ]
    # print(dupes)

    # print(matrix.is_rectangle([Point(4, 0), Point(9, 1), Point(8, 7), Point(3, 6)]))
    # print(matrix.is_rectangle([Point(2, 3), Point(1, 6), Point(7, 4), Point(6, 7)]))
    # print(matrix.is_rectangle([Point(4, 4), Point(4, 0), Point(0, 4), Point(0, 0)]))

    # 4935 too high
    # 4717 too high

    return len(points)


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
