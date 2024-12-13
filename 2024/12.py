import re
from pathlib import Path
from helpers import read_file, Matrix, Node


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class GardenNode(Node):
    def __init__(self, value, x, y):
        super().__init__(value, x, y)
        self.up = None
        self.right = None
        self.down = None
        self.left = None

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

    def get_valid_neighbors(self):
        neighbors = self.get_neighbors()

        valid = []
        for n in neighbors:
            if n.value == self.value:
                valid.append(n)

        return valid


class Region:
    def __init__(self):
        self.nodes = []
        self.region = None

    def __str__(self):
        string = f"{self.region}: ["
        for n in self.nodes:
            string += f"{n}, "
        return string + "]"

    def __repr__(self):
        return self.__str__()

    def add_node(self, node):
        if self.region is None and not self.nodes:
            self.region = node.value
            self.nodes.append(node)
            return True

        if self.region != node.value:
            return False

        if node in self.nodes:
            return False

        for n in self.nodes:
            if node in n.get_valid_neighbors():
                self.nodes.append(node)
                return True

        return False

    def area(self):
        return len(self.nodes)

    def perimeter(self):
        perimeter = 0
        for n in self.nodes:
            perimeter += 4 - len(n.get_valid_neighbors())

        return perimeter

    def cost(self):
        return self.area() * self.perimeter()

    def num_sides(self):
        if self.area() == 1:
            return 4

        corners = 0
        for n in self.nodes:
            neighbors = n.get_valid_neighbors()
            if len(neighbors) == 1:
                corners += 2
            if len(neighbors) == 2:
                corners += 2
            if len(neighbors) == 3:
                corners += 2

        return corners

    def bulk_cost(self):
        return self.area() * self.num_sides()


class Garden(Matrix):
    def __init__(self, data):
        super().__init__(data)
        self.node_values = dict()

    def parse(self):
        self.matrix = []
        self.regions = dict()
        for y, line in enumerate(self.string.strip().split("\n")):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                row.append(GardenNode(value=value, x=x, y=y))

            self.matrix.append(row)

        for x, row in enumerate(self.matrix):
            for y, node in enumerate(row):
                node.left = self.at(node.point.x - 1, node.point.y)
                node.up = self.at(node.point.x, node.point.y - 1)
                node.right = self.at(node.point.x + 1, node.point.y)
                node.down = self.at(node.point.x, node.point.y + 1)

    def create_and_add_new_region(self, node):
        new_region = Region()
        new_region.add_node(node)
        if node.value in self.regions:
            self.regions[node.value].append(new_region)
        else:
            self.regions[node.value] = [new_region]

    def create_regions(self):
        visited = set()

        for row in self.matrix:
            for node in row:
                if node in visited:
                    continue

                q = [node]

                while q:
                    current_node = q.pop(0)
                    if current_node in visited:
                        continue
                    visited.add(current_node)

                    if current_node.value in self.regions:
                        node_added = False
                        for r in self.regions[current_node.value]:
                            node_added = r.add_node(current_node)
                            if node_added:
                                break
                        if not node_added:
                            self.create_and_add_new_region(current_node)
                    else:
                        self.create_and_add_new_region(current_node)

                    q += current_node.get_valid_neighbors()

    def get_fence_cost(self):
        cost = 0

        for k, v in self.regions.items():
            for r in v:
                cost += r.cost()

        return cost

    def get_bulk_fence_cost(self):
        cost = 0

        for k, v in self.regions.items():
            for r in v:
                cost += r.bulk_cost()

        return cost


def part1():
    # print(DATA)
    matrix = Garden(DATA)
    # print(matrix)
    matrix.create_regions()
    cost = matrix.get_fence_cost()
    return cost


def part2():
    matrix = Garden(DATA)
    # print(matrix)
    matrix.create_regions()
    cost = matrix.get_bulk_fence_cost()
    return cost


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
