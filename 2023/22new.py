import re
from pathlib import Path
from helpers import read_file, Point
import numpy as np
from copy import deepcopy


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class Brick:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return str(self.p1) + " " + str(self.p2)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(self.p1)

    def overlaps(self, other):
        return max(self.p1.x, other.p1.x) <= min(self.p2.x, other.p2.x) and max(
            self.p1.y, other.p1.y
        ) <= min(self.p2.y, other.p2.y)


class Grid:
    def __init__(self, data):
        self.string = data
        self.parse()
        # self.settle_bricks()

    def __str__(self):
        string = ""
        for a in reversed(self.grid):
            string += str(a) + "\n"
        return string

    def __repr__(self):
        return str(self)

    def parse(self):
        coords = []
        max_x = 0
        max_y = 0
        max_z = 0
        for line in self.string.split("\n"):
            c1, c2 = line.split("~")
            x1, y1, z1 = list(map(int, c1.split(",")))
            x2, y2, z2 = list(map(int, c2.split(",")))

            max_x = max(max_x, x1, x2)
            max_y = max(max_y, y1, y2)
            max_z = max(max_z, z1, z2)

            coords.append(((x1, y1, z1), (x2, y2, z2)))

        # self.nodes = []

        self.grid = [np.zeros((max_x + 1, max_y + 1)) for _ in range(max_z + 1)]

        for i, coord in enumerate(coords):
            c1, c2 = coord
            x1, y1, z1 = c1
            x2, y2, z2 = c2

            p1 = Point(x1, y1)
            p2 = Point(x2, y2)
            node = Brick(p1, p2)

            # self.nodes[i + 1] = node
            # self.nodes.append(i + 1)

            if x2 - x1 != 0:
                self.grid[z1][x1 : x2 + 1, y1] = i + 1
            elif y2 - y1 != 0:
                self.grid[z1][x1, y1 : y2 + 1] = i + 1
            elif z2 - z1 != 0:
                for z in range(z1, z2 + 1):
                    self.grid[z][x1, y1] = i + 1
            else:
                self.grid[z1][x1, y1] = i + 1

    def combine_layers(self, layer1, layer2, z):
        new_layer = layer1 + layer2
        self.grid = self.grid[:z] + [new_layer] + self.grid[z + 2 :]

    def settle_bricks(self):
        bricks_settled = True
        while bricks_settled:
            bricks_settled = False

            z = 0
            max_z = len(self.grid) - 1
            while z < max_z:
                layer1 = deepcopy(self.grid[z])
                layer2 = deepcopy(self.grid[z + 1])

                multiplied = layer1 * layer2

                if not np.any(multiplied):
                    # this settles an entire layer
                    bricks_settled = True
                    self.combine_layers(layer1, layer2, z)
                    max_z -= 1
                    continue
                else:
                    # this settles parts of a layer
                    self.maybe_settle_partial_layer(self.grid[z], self.grid[z + 1])

                    # Layer 1
                    # [[3. 0. 4.]
                    #  [3. 0. 4.]
                    #  [3. 0. 4.]]

                    # Layer 2
                    # [[6. 6. 6.]
                    #  [0. 5. 0.]
                    #  [0. 0. 0.]]

                    # Multiplied
                    # [[18.  0. 24.]
                    #  [ 0.  0.  0.]
                    #  [ 0.  0.  0.]]

                    # Added
                    # [[ 9.  6. 10.]
                    #  [ 3.  5.  4.]
                    #  [ 3.  0.  4.]]

                z += 1

    def maybe_settle_partial_layer(self, layer1, layer2):
        settleable_numbers = {}
        for r, row in enumerate(layer2):
            for c, num in enumerate(row):
                if num > 0 and layer1[r][c] == 0:
                    # can settle
                    # print(num, layer1[r][c])
                    if num in settleable_numbers:
                        settleable_numbers[num]["count"] += 1
                        settleable_numbers[num]["indices"].append(tuple([r, c]))
                    else:
                        settleable_numbers[num] = {
                            "count": 1,
                            "indices": [tuple([r, c])],
                        }

        unique, counts = np.unique(layer2, return_counts=True)
        unique_counts = dict(zip(unique, counts))
        # print(settleable_numbers)
        for num, dct in settleable_numbers.items():
            count = dct["count"]
            if count < unique_counts[num]:
                continue
            else:
                # print(f"{num} can be settled")
                for r, c in dct["indices"]:
                    # print(r, c)
                    layer1[r][c], layer2[r][c] = layer2[r][c], layer1[r][c]

        # multiplied = layer1 * layer2
        # added = layer1 + layer2

        # unique2, count2 = np.unique(layer2, return_counts=True)
        # unique_multiplied = np.unique_all(multiplied)
        # print(unique_multiplied)

        # set2 = set([(u, count2[i]) for i, u in enumerate(unique2)])

        # print(layer1)
        # print(layer2)
        # added = layer1 + layer2

        # print(multiplied)
        # print(added)

        # print()
        # print()
        # print()
        # print()

    def create_support_maps(self):
        self.nodes = set(np.unique(self.grid))
        self.nodes.remove(np.float64(0.0))

        self.brick_supports = dict()
        self.brick_supported_by = dict()

        for num in self.nodes:
            self.brick_supports[num] = set()
            self.brick_supported_by[num] = set()

        for z in range(len(self.grid) - 1):
            layer1 = self.grid[z]
            layer2 = self.grid[z + 1]

            for r, row in enumerate(layer2):
                for c, supported_brick in enumerate(row):
                    support_brick = layer1[r][c]
                    if (
                        supported_brick > 0
                        and support_brick > 0
                        and support_brick != supported_brick
                    ):
                        # print(support_brick, supported_brick)
                        if support_brick in self.brick_supports:
                            self.brick_supports[support_brick].add(supported_brick)
                        else:
                            self.brick_supports[support_brick] = set([supported_brick])

                        if supported_brick in self.brick_supported_by:
                            self.brick_supported_by[supported_brick].add(support_brick)
                        else:
                            self.brick_supported_by[supported_brick] = set(
                                [support_brick]
                            )

        # last_layer = self.grid[-1]
        # for r, row in enumerate(last_layer):
        #     for c, brick in enumerate(row):
        #         if brick > 0:
        #             print("DID WE GET HERE????", self.brick_supports[brick])
        #             self.brick_supports[brick] = set()

        # print(self.brick_supports)
        # print(self.brick_supported_by)
        # print()

    def find_bricks_that_can_be_removed(self):
        self.create_support_maps()
        # print()

        bricks_that_can_be_removed = set()

        for brick, supported_bricks in self.brick_supports.items():
            # print(brick, supported_bricks)
            can_be_rmeoved = True
            for s_brick in supported_bricks:
                if len(self.brick_supported_by[s_brick]) < 2:
                    can_be_rmeoved = False

            if can_be_rmeoved:
                # print(f"adding {brick}")
                bricks_that_can_be_removed.add(brick)

        for brick, supported_bricks in self.brick_supports.items():
            if not len(supported_bricks):
                bricks_that_can_be_removed.add(brick)

        # print(bricks_that_can_be_removed)
        return len(bricks_that_can_be_removed)

    def find_chain_reactions(self):
        self.create_support_maps()

        for k, v in self.brick_supports.items():
            print(k, v)
        print()
        for k, v in self.brick_supported_by.items():
            print(k, v)
        print()
        # print(self.brick_supports)
        # print(self.brick_supported_by)

        first_layer = self.grid[0]
        floor_bricks = set()
        for row in first_layer:
            for brick in row:
                if brick > 0:
                    floor_bricks.add(brick)

        # print(floor_bricks)

        count = 0
        prev_count = 0

        temp = []
        for fb in floor_bricks:
            temp.append(fb)

        while len(temp):
            copied_supported_by = deepcopy(self.brick_supported_by)
            # del copied_supported_by[k]
            deleted_brick = temp.pop(0)
            for b in self.brick_supports[deleted_brick]:
                if b not in temp:
                    temp.append(b)

            print(deleted_brick, temp)
            for brick, supports in self.brick_supported_by.items():
                # print(brick, supports)
                if deleted_brick in supports:
                    copied_supported_by[brick].remove(deleted_brick)
                else:
                    for s_brick in supports:

                        if not len(copied_supported_by[s_brick]) and len(
                            self.brick_supported_by[s_brick]
                        ):
                            copied_supported_by[brick].remove(s_brick)

            # print("start")
            # print(self.brick_supported_by)
            # for key, v in self.brick_supported_by.items():
            #     print(key, v)
            # print()
            for key, v in copied_supported_by.items():
                # print(k, v)
                if key not in floor_bricks and len(v) == 0:
                    print(key, v, self.brick_supported_by[key], count)
                    count += 1
            # print("end")
            # print()
            print(
                f"brick {deleted_brick} would cause {count - prev_count} bricks to fall"
            )
            prev_count = count

        return count


def part1():
    grid = Grid(DATA)

    # print(grid)
    grid.settle_bricks()
    # print()
    # print("Settled:")
    # print(grid)

    # print(grid.brick_supports[grid.nodes[0]])
    # print()
    # print()
    # print()
    count = grid.find_bricks_that_can_be_removed()
    return count


def part2():
    grid = Grid(DATA)
    grid.settle_bricks()
    print(grid)
    # 1966 too low
    count = grid.find_chain_reactions()
    return count


# 1 -> 2
# 2 -> 1
# 3 -> 0
# 4 -> 2
# 5 -> 1
# 6 -> 0


def main():
    print(f"Part 1: {part1()}")  # 471
    print(f"Part 2: {part2()}")
    # 1966 too low


main()
