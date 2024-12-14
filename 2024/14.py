import re
from pathlib import Path
from helpers import read_file, Point, Matrix


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class Robot:
    def __init__(self, id, p, v):
        self.id = id
        self.point = Point(p[0], p[1])
        self.velocity = Point(v[0], v[1])

    def __str__(self):
        return f"{self.point}. {self.velocity}"

    def __repr__(self):
        return self.__str__()

    def matrix_repr(self):
        return "1"

    def __hash__(self):
        return hash(self.id)


class Bathroom(Matrix):
    def __init__(self, x, y):
        self.robots = []
        self.robots_points = dict()
        self.matrix = [["."] * x for _ in range(y)]

    def __str__(self):
        # return self.string
        string = ""
        for y, row in enumerate(self.matrix):
            row_string = ""
            for x, node in enumerate(row):
                robots_at_this_point = self.robots_points.get(Point(x, y))
                if robots_at_this_point:
                    row_string += f"{len(robots_at_this_point)}"
                else:
                    row_string += str(node)
            string += row_string + "\n"
        return string

    def set_robot_point(self, robot):
        self.robots.append(robot)
        if robot.point in self.robots_points:
            self.robots_points[robot.point].add(robot)
        else:
            self.robots_points[robot.point] = set([robot])

    def time_travel(self, time):
        for robot in self.robots:




def part1():
    bathroom = Bathroom(11, 7)

    for i, line in enumerate(DATA.strip().split("\n")):
        p1, p2, v1, v2 = re.findall("-?\d+", line)
        # print(p1, p2, v1, v2)
        r = Robot(i, list(map(int, [p1, p2])), list(map(int, [v1, v2])))
        bathroom.set_robot_point(r)



    print(bathroom)
    return


def part2():
    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
