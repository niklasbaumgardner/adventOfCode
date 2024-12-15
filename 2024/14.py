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

    def add_robot(self, robot):
        self.robots.append(robot)
        self.set_robot_point(robot)

    def set_robot_point(self, robot):
        if robot.point in self.robots_points:
            self.robots_points[robot.point].add(robot)
        else:
            self.robots_points[robot.point] = set([robot])

    def update_robot_points(self):
        self.robots_points.clear()

        for r in self.robots:
            self.set_robot_point(r)

    def time_travel(self, time):
        time_multiplier = Point(time, time)
        for robot in self.robots:
            travled = time_multiplier * robot.velocity
            # print(robot.point, travled)
            robot.point = robot.point + travled
            # print(robot.point, self.x, self.y)
            robot.point.x = robot.point.x % self.x
            robot.point.y = robot.point.y % self.y
            # print(robot.point)
            # print()

        self.update_robot_points()

    def multiply_robots(self):
        one, two, three, four = 0, 0, 0, 0
        middle_x = self.x // 2
        middle_y = self.y // 2
        for point, robot_set in self.robots_points.items():
            if point.x < middle_x and point.y < middle_y:
                one += len(robot_set)
            elif point.x > middle_x and point.y < middle_y:
                two += len(robot_set)
            elif point.x < middle_x and point.y > middle_y:
                three += len(robot_set)
            elif point.x > middle_x and point.y > middle_y:
                four += len(robot_set)

        print(one, two, three, four)
        return one * two * three * four

    def robots_in_a_line(self):
        robots_sorted = sorted(self.robots, key=lambda r: r.point.x)
        robots_sorted = sorted(robots_sorted, key=lambda r: r.point.y)

        in_a_row = 0

        for i in range(len(robots_sorted) - 1):
            robot = robots_sorted[i]
            next_robot = robots_sorted[i + 1]

            diff = next_robot.point.x - robot.point.x
            if diff == 1 or diff == 0:
                in_a_row += 1
                # if in_a_row > 5:
                # print(f"number in a row {in_a_row}")
            else:
                in_a_row = 0

            if in_a_row >= 9:
                return in_a_row

        return 0


def test_input():
    bathroom = Bathroom(11, 7)

    for i, line in enumerate(DATA.strip().split("\n")):
        p1, p2, v1, v2 = re.findall("-?\d+", line)
        # print(p1, p2, v1, v2)
        r = Robot(i, list(map(int, [p1, p2])), list(map(int, [v1, v2])))
        bathroom.add_robot(r)

    # print(bathroom)
    # print(bathroom.robots)
    bathroom.time_travel(100)

    # print(bathroom)
    # print(bathroom.robots)

    # 218618400 too low
    return bathroom.multiply_robots()


def part1():
    bathroom = Bathroom(101, 103)

    for i, line in enumerate(DATA.strip().split("\n")):
        p1, p2, v1, v2 = re.findall("-?\d+", line)
        # print(p1, p2, v1, v2)
        r = Robot(i, list(map(int, [p1, p2])), list(map(int, [v1, v2])))
        bathroom.add_robot(r)

    # print(bathroom)
    # print(bathroom.robots)
    bathroom.time_travel(100)

    # print(bathroom)
    # print(bathroom.robots)

    # 218618400 too low
    return bathroom.multiply_robots()


def part2():
    bathroom = Bathroom(101, 103)

    for i, line in enumerate(DATA.strip().split("\n")):
        p1, p2, v1, v2 = re.findall("-?\d+", line)
        # print(p1, p2, v1, v2)
        r = Robot(i, list(map(int, [p1, p2])), list(map(int, [v1, v2])))
        bathroom.add_robot(r)

    # print(bathroom)
    # print(bathroom.robots)
    bathroom.time_travel(7753)
    print(bathroom)
    # for i in range(1, 99999):
    #     bathroom.time_travel(1)
    #     if bathroom.robots_in_a_line() > 0:
    #         print(bathroom)
    #         print(i)
    # input()

    # print(bathroom)
    # print(bathroom.robots)
    # 816, 831, 919, 934, 95


def main():
    # print(f"Test input: {test_input()}")
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
