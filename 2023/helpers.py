import math


def read_file(filename):
    fp = open(filename)
    file = fp.read().strip()
    return file


def parse_to_matrix(data):
    return Matrix(data=data)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if type(x) == str:
            x = int(x)
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if type(y) == str:
            y = int(y)
        self._y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return math.sqrt(self.x**2 + self.y**2) > math.sqrt(other.x**2 + other.y**2)

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other):
        return not self.__gt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def distanceTo(self, other):
        xSquared = (other.x - self.x) ** 2
        ySquared = (other.y - self.y) ** 2
        return math.sqrt(xSquared + ySquared)


class Node:
    def __init__(self, value, x, y):
        self.value = value
        self.point = Point(x, y)


class Matrix:
    def __init__(self, data):
        self.string = data.strip()
        self.parse()

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()

    def parse(self):
        self.matrix = []
        for y, line in enumerate(self.string.split("\n")):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                row.append(Node(value=value, x=x, y=y))

            self.matrix.append(row)

    @property
    def num_cols(self):
        return len(self.matrix[0])

    @property
    def num_rows(self):
        return len(self.matrix)

    def at(self, x, y):
        if not (-1 < x < self.num_cols):
            return None

        if not (-1 < y < self.num_rows):
            return None

        return self.matrix[y][x]
