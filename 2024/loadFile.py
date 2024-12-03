def read_file(filename):
    fp = open(filename)
    file = fp.read().strip()
    return file


def parse_to_matrix(data):
    return Matrix(data=data)


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
        for line in self.string.split("\n"):
            lst = list(map(int, line.split()))
            self.matrix.append(lst)

    def max_x(self):
        return len(self.matrix[0])

    def max_y(self):
        return len(self.matrix)

    def at(self, x, y):
        if not (-1 < x < self.maxX()):
            return None

        if not (-1 < y < self.maxY()):
            return None

        return self.matrix[y][x]
