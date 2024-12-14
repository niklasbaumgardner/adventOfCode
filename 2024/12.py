import re
from pathlib import Path
from helpers import read_file, Matrix, Node, Point


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

    def get_valid_neighbors_dict(self):
        neighbors = {"up": None, "right": None, "left": None, "down": None}
        if self.up and self.up.value == self.value:
            neighbors["up"] = self.up
        if self.right and self.right.value == self.value:
            neighbors["right"] = self.right
        if self.down and self.down.value == self.value:
            neighbors["down"] = self.down
        if self.left and self.left.value == self.value:
            neighbors["left"] = self.left

        return neighbors


class Region:
    def __init__(self, garden):
        self.garden = garden
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

    def exterior_sides(self):
        # print(f"counting num sides for region {self.region}")
        num_sides = 0
        nodes = sorted(self.nodes, key=lambda n: n.point.x)
        nodes = sorted(nodes, key=lambda n: n.point.y)
        starting_node = nodes[0]

        point = Point(starting_node.point.x, starting_node.point.y)
        node = None

        walking_point = Point(starting_node.point.x, starting_node.point.y - 1)
        step = Point(1, 0)
        # print("starting node", starting_node)
        while True:
            # print()
            if point == starting_node.point and step == Point(1, 0) and num_sides > 0:
                # print(f"{self.region}: num_sides is {num_sides}!!")
                return num_sides

            walking_point = walking_point + step
            point = point + step

            node = self.garden.at_point(point)
            walking_node = self.garden.at_point(walking_point)

            # if node is None and walking_node is None:
            #     print(f"num_sides is {num_sides}!!")
            #     return num_sides

            # print(f"step: {step}")
            # print(f"walking_point: {walking_point}, point: {point}")
            # print(f"walking_node: {walking_node}, node: {node}")

            if (
                node is not None
                and node.value == self.region
                and (walking_node is None or walking_node.value != self.region)
            ):
                # keep going straight
                # print("continue straight")
                continue

            if walking_node is not None and walking_node.value == self.region:
                walking_point = walking_point - step
                # turn left
                # print("turning left")
                if step.x == 0:
                    if step.y == 1:
                        step.x = 1
                    else:
                        step.x = -1
                    step.y = 0
                else:
                    if step.x == 1:
                        step.y = -1
                    else:
                        step.y = 1
                    step.x = 0

                # i think theres more here
                walking_point = walking_point - step

                num_sides += 1
                continue

            if node is None or (node is not None and node.value != self.region):
                point = point - step
                # turn right
                # print("turning right")
                if step.x == 0:
                    if step.y == 1:
                        step.x = -1
                    else:
                        step.x = 1
                    step.y = 0
                else:
                    if step.x == 1:
                        step.y = 1
                    else:
                        step.y = -1
                    step.x = 0

                walking_point = walking_point + step

                # i think more here

                num_sides += 1
                continue

    def interior_sides(self):
        # print(f"counting num sides for region {self.region}")
        num_sides = 0
        nodes = sorted(self.nodes, key=lambda n: n.point.x)
        nodes = sorted(nodes, key=lambda n: n.point.y)
        starting_node = nodes[0]

        point = Point(starting_node.point.x, starting_node.point.y)
        node = None

        walking_point = Point(starting_node.point.x, starting_node.point.y - 1)
        step = Point(1, 0)
        # print("starting node", starting_node)
        while True:
            # print()
            if point == starting_node.point and step == Point(1, 0) and num_sides > 0:
                # print(f"{self.region}: num_sides is {num_sides}!!")
                return num_sides

            walking_point = walking_point + step
            point = point + step

            node = self.garden.at_point(point)
            walking_node = self.garden.at_point(walking_point)

            # if node is None and walking_node is None:
            #     print(f"num_sides is {num_sides}!!")
            #     return num_sides

            # print(f"step: {step}")
            # print(f"walking_point: {walking_point}, point: {point}")
            # print(f"walking_node: {walking_node}, node: {node}")

            if (
                node is not None
                and node.value == self.region
                and (walking_node is None or walking_node.value != self.region)
            ):
                # keep going straight
                # print("continue straight")
                continue

            if walking_node is not None and walking_node.value == self.region:
                walking_point = walking_point - step
                # turn left
                # print("turning left")
                if step.x == 0:
                    if step.y == 1:
                        step.x = 1
                    else:
                        step.x = -1
                    step.y = 0
                else:
                    if step.x == 1:
                        step.y = -1
                    else:
                        step.y = 1
                    step.x = 0

                # i think theres more here
                walking_point = walking_point - step

                num_sides += 1
                continue

            if node is None or (node is not None and node.value != self.region):
                point = point - step
                # turn right
                # print("turning right")
                if step.x == 0:
                    if step.y == 1:
                        step.x = -1
                    else:
                        step.x = 1
                    step.y = 0
                else:
                    if step.x == 1:
                        step.y = 1
                    else:
                        step.y = -1
                    step.x = 0

                walking_point = walking_point + step

                # i think more here

                num_sides += 1
                continue

    def count_all_sides(self):
        num_sides = 0
        # nodes = sorted(self.nodes, key=lambda n: n.point.x)
        # nodes = sorted(nodes, key=lambda n: n.point.y)
        top_sides = dict()
        bottom_sides = dict()
        for n in self.nodes:
            top_fence = n.point.y - 0.5
            bottom_fence = n.point.y + 0.5
            neighs = n.get_valid_neighbors_dict()
            if neighs["up"] is None:
                if top_fence in top_sides:
                    top_sides[top_fence].append(n)
                else:
                    top_sides[top_fence] = [n]

            if neighs["down"] is None:
                if bottom_fence in bottom_sides:
                    bottom_sides[bottom_fence].append(n)
                else:
                    bottom_sides[bottom_fence] = [n]

        for sides in [top_sides, bottom_sides]:
            for k, v in sides.items():
                sorted_v = sorted(v, key=lambda n: n.point.x)
                # print(k, sorted_v)
                length = len(sorted_v)
                temp = 0
                for i in range(len(sorted_v) - 1):
                    node = sorted_v[i]
                    next = sorted_v[i + 1]
                    # print(i, i + 1, length)
                    if (next.point.x - node.point.x) == 1:
                        temp += 1

                # print(length, temp)
                num_sides += length - temp

        # print(f"Num row sides: {num_sides}")
        # print()

        left_sides = dict()
        right_sides = dict()
        for n in self.nodes:
            left_fence = n.point.x - 0.5
            right_fence = n.point.x + 0.5
            neighs = n.get_valid_neighbors_dict()
            if neighs["left"] is None:
                if left_fence in left_sides:
                    left_sides[left_fence].append(n)
                else:
                    left_sides[left_fence] = [n]

            if neighs["right"] is None:
                if right_fence in right_sides:
                    right_sides[right_fence].append(n)
                else:
                    right_sides[right_fence] = [n]

        for sides in [left_sides, right_sides]:
            for k, v in sides.items():
                sorted_v = sorted(v, key=lambda n: n.point.y)
                # print(k, sorted_v)
                length = len(sorted_v)
                temp = 0
                for i in range(len(sorted_v) - 1):
                    node = sorted_v[i]
                    next = sorted_v[i + 1]
                    # print(i, i + 1, length)
                    if (next.point.y - node.point.y) == 1:
                        temp += 1

                # print(length, temp)
                num_sides += length - temp

        # print(f"Num row sides: {num_sides}")
        # print()

        return num_sides

    def num_sides(self):
        return self.count_all_sides()
        ###########################
        e_s = self.exterior_sides()
        i_s = self.interior_sides()

        return e_s + i_s

    def bulk_cost(self):
        a = self.area()
        s = self.num_sides()

        # print(f"{self.region}: {a}, {s}, {a*s}")
        # print("\n\n\n\n\n")
        return a * s


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
        new_region = Region(self)
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

    # too low 882270
    # too low 900368

    return cost


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
