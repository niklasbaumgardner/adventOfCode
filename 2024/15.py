import re
from pathlib import Path
from helpers import read_file, Matrix, Node, Point

MOVEMENT = {"^": Point(0, -1), ">": Point(1, 0), "v": Point(0, 1), "<": Point(-1, 0)}


class LanterNode(Node):
    @property
    def is_wall(self):
        return self.value == "#"

    @property
    def is_empty(self):
        return self.value == "."

    @property
    def is_box(self):
        return self.value == "O" or self.value in ["[", "]"]

    @property
    def is_robot(self):
        return self.value == "@"

    @property
    def can_move(self):
        return not self.is_wall

    def point_str(self):
        return f"{self.value} at {self.point}"

    def __str__(self):
        return f"{self.value}"

    def gps(self):
        return (self.point.y * 100) + self.point.x


class Warehouse(Matrix):
    def __init__(self, data, directions):
        super().__init__(data)
        self.directions = directions

    def parse(self):
        self.matrix = []
        for y, line in enumerate(self.string.split("\n")):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                node = LanterNode(value, x, y)
                row.append(node)

                if node.value == "@":
                    self.robot = node

            self.matrix.append(row)

    def gps(self):
        total = 0
        for row in self.matrix:
            for node in row:
                if node.is_box:
                    total += node.gps()

        return total

    def maybe_swap_nodes(self, node1, node2):
        if not node1.can_move or not node2.can_move:
            return False

        self.__swap_nodes__(node1, node2)
        return True

    def maybe_push_node(self, node, dir):
        move_dir = MOVEMENT[dir]
        point = node.point + move_dir

        next_node = self.at_point(point)

        if next_node.is_empty:
            self.__swap_nodes__(node, next_node)
            return True
        elif next_node.is_box:
            if self.maybe_push_node(next_node, dir):
                self.__swap_nodes__(node, self.at_point(point))
                return True
        elif next_node.is_wall:
            return False

    def __swap_nodes__(self, node1, node2):
        x1 = node1.point.x
        y1 = node1.point.y
        x2 = node2.point.x
        y2 = node2.point.y
        self.matrix[y1][x1], self.matrix[y2][x2] = (
            self.matrix[y2][x2],
            self.matrix[y1][x1],
        )
        node1.point, node2.point = node2.point, node1.point

    def move_robot(self, dir):
        move_dir = MOVEMENT[dir]
        move_point = self.robot.point + move_dir
        move_node = self.at_point(move_point)

        if move_node.is_empty:
            self.__swap_nodes__(self.robot, move_node)

        elif move_node.is_box:
            if self.maybe_push_node(move_node, dir):
                self.__swap_nodes__(self.robot, self.at_point(move_point))

    def follow_directions(self):
        for ch in self.directions:
            self.move_robot(ch)
            # print(f"After move {ch}: ")
            # print(self)
            # print()


class Warehouse2(Warehouse):
    def parse(self):
        self.matrix = []
        for y, line in enumerate(self.string.split("\n")):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                if value == "#" or value == ".":
                    node1 = LanterNode(value, 2 * x, y)
                    row.append(node1)
                    node2 = LanterNode(value, (2 * x) + 1, y)
                    row.append(node2)
                elif value == "@":
                    node1 = LanterNode(value, 2 * x, y)
                    row.append(node1)
                    node2 = LanterNode(".", (2 * x) + 1, y)
                    row.append(node2)
                    self.robot = node1
                elif value == "O":
                    node1 = LanterNode("[", 2 * x, y)
                    row.append(node1)
                    node2 = LanterNode("]", (2 * x) + 1, y)
                    row.append(node2)

            self.matrix.append(row)

    def __str__(self):
        # return self.string
        string = ""
        for y, row in enumerate(self.matrix):
            row_string = ""
            for x, node in enumerate(row):
                row_string += str(node)
            string += row_string + "\n"
        return string

    def maybe_push_points_vertically(self, points, dir):
        move_dir = MOVEMENT[dir]

        all_empty = True
        empty_or_box_only = False
        for point in points:
            next_point = point + move_dir
            next_node = self.at_point(next_point)

            if next_node.is_wall:
                return False

            elif next_node.is_box:
                empty_or_box_only = True
                all_empty = False

        did_swap = False
        if empty_or_box_only:
            next_points = set()
            for point in points:
                next_point = point + move_dir
                next_node = self.at_point(next_point)

                if next_node.is_box:
                    other_box_point = Point(next_point.x, next_point.y)
                    if next_node.value == "[":
                        other_box_point.x += 1
                    else:
                        other_box_point.x -= 1
                    next_points.add(next_point)
                    next_points.add(other_box_point)
            did_swap = self.maybe_push_points_vertically(list(next_points), dir)

        if all_empty or did_swap:
            for point in points:
                next_point = point + move_dir
                next_node = self.at_point(next_point)
                self.__swap_points__(point, next_point)
            return True

    def maybe_push_node(self, point, dir):
        move_dir = MOVEMENT[dir]
        next_point = point + move_dir

        node = self.at_point(point)

        next_node = self.at_point(next_point)

        if next_node.is_empty:
            self.__swap_points__(point, next_point)
            return True
        elif next_node.is_box:
            if self.maybe_push_node(next_point, dir):
                self.__swap_points__(point, next_point)
                return True
        elif next_node.is_wall:
            return False

    def __swap_points__(self, p1, p2):
        node1 = self.at_point(p1)
        node2 = self.at_point(p2)

        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y

        self.matrix[y1][x1], self.matrix[y2][x2] = (
            self.matrix[y2][x2],
            self.matrix[y1][x1],
        )

        node1.point, node2.point = node2.point, node1.point

    def move_robot(self, dir):
        move_dir = MOVEMENT[dir]
        move_point = self.robot.point + move_dir
        move_node = self.at_point(move_point)

        if move_node.is_empty:
            self.__swap_points__(self.robot.point, move_point)

        elif move_node.is_box:
            if move_dir.y != 0:
                other_box_point = Point(move_point.x, move_point.y)
                if move_node.value == "[":
                    other_box_point.x += 1
                else:
                    other_box_point.x -= 1

                if self.maybe_push_points_vertically(
                    [move_point, other_box_point], dir
                ):
                    self.__swap_points__(self.robot.point, move_point)
            else:
                if self.maybe_push_node(move_point, dir):
                    self.__swap_points__(self.robot.point, move_point)

    def follow_directions(self):
        for ch in self.directions:
            self.move_robot(ch)
            # print(f"After move {ch}: ")
            # print(self)
            # print()

    def gps(self):
        total = 0
        for row in self.matrix:
            for node in row:
                if node.value == "[":
                    total += node.gps()

        return total


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


def part1():
    mtrx, directions = DATA.strip().split("\n\n")
    directions = directions.replace("\n", "")

    w = Warehouse(mtrx, directions)

    print("Initial state: ")
    print(w)
    print()

    w.follow_directions()

    print("After all moves: ")
    print(w)
    print()
    return w.gps()


def part2():
    mtrx, directions = DATA.strip().split("\n\n")
    directions = directions.replace("\n", "")

    w = Warehouse2(mtrx, directions)

    print("Initial state: ")
    print(w)
    print()

    w.follow_directions()

    print("After all moves: ")
    print(w)
    print()
    return w.gps()


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
