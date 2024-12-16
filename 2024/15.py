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
        return self.value == "O"

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
        total_gps = 0
        for ch in self.directions:
            self.move_robot(ch)
            print(f"After move {ch}: ")
            print(self)
            print()

        return total_gps


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
                    node1 = LanterNode(value, 2 * x, y)
                    row.append(node1)
                    row.append(node1)

            self.matrix.append(row)

    def __str__(self):
        # return self.string
        string = ""
        for y, row in enumerate(self.matrix):
            row_string = ""
            for x, node in enumerate(row):
                if node.is_box:
                    string_val = "["
                    if node.point.x != x:
                        string_val = "]"

                    row_string += string_val
                else:
                    row_string += str(node)
            string += row_string + "\n"
        return string

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

        if node1.is_box or node2.is_box:
            print("before swap", node1.point_str(), node2.point_str())

        x1 = node1.point.x
        y1 = node1.point.y
        x2 = node2.point.x
        y2 = node2.point.y

        self.matrix[y1][x1], self.matrix[y2][x2] = (
            self.matrix[y2][x2],
            self.matrix[y1][x1],
        )

        if node1.is_box:
            # x1 and x1 + 1 are the box

            self.matrix[y1][x1 + 1], self.matrix[y1][x1] = (
                self.matrix[y1][x1],
                self.matrix[y1][x1 + 1],
            )

        # if node2.is_box:
        #     self.matrix[y2][x2], self.matrix[y2][x2 + 1] = (
        #         self.matrix[y2][x2 + 1],
        #         self.matrix[y2][x2],
        #     )

        node1.point, node2.point = node2.point, node1.point

        print("after swap", self.at(x1, y1).point_str(), self.at(x2, y2).point_str())

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
        total_gps = 0
        for ch in self.directions:
            self.move_robot(ch)
            print(f"After move {ch}: ")
            print(self)
            print()

        return total_gps


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

    total_gps = w.follow_directions()

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

    total_gps = w.follow_directions()

    # print("After all moves: ")
    # print(w)
    # print()
    # return w.gps()


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
