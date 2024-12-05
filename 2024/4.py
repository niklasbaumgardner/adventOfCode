import re
from pathlib import Path
from helpers import read_file, Matrix


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class xmasMatrix(Matrix):

    def get_adjacent_nodes(self, x, y):
        return {
            "top_left": self.at(x - 1, y - 1),
            "top": self.at(x, y - 1),
            "top_right": self.at(x + 1, y - 1),
            "right": self.at(x + 1, y),
            "bottom_right": self.at(x + 1, y + 1),
            "bottom": self.at(x, y + 1),
            "bottom_left": self.at(x - 1, y + 1),
            "left": self.at(x - 1, y),
        }

    def find_starting_nodes(self, ch):
        startings_nodes = []
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                node = self.at(c, r)
                if node.value == ch:
                    startings_nodes.append(node)

        return startings_nodes

    def find_words(self, word):
        count = 0
        starting_words = self.find_starting_nodes("X")
        for start_node in starting_words:

            adjacent = self.get_adjacent_nodes(start_node.point.x, start_node.point.y)

            for dir, adj_node in adjacent.items():

                if adj_node is None:
                    continue

                if start_node.value + adj_node.value == "XM":
                    is_xmas = self.check_for_word(start_node, dir)
                    if is_xmas:
                        count += 1

        return count

    def check_for_word(self, start_node, dir):
        adjacent = self.get_adjacent_nodes(start_node.point.x, start_node.point.y)
        m_node = adjacent[dir]

        adjacent = self.get_adjacent_nodes(m_node.point.x, m_node.point.y)
        a_node = adjacent[dir]
        if a_node is None or a_node.value != "A":
            return False

        adjacent = self.get_adjacent_nodes(a_node.point.x, a_node.point.y)
        s_node = adjacent[dir]
        if s_node is None or s_node.value != "S":
            return False

        return start_node.value + m_node.value + a_node.value + s_node.value == "XMAS"

    def count_x_mas(self):
        count = 0
        middle_a = self.find_starting_nodes("A")
        for a_node in middle_a:

            ajd = self.get_adjacent_nodes(a_node.point.x, a_node.point.y)

            top_left_node = ajd["top_left"]
            top_right_node = ajd["top_right"]
            bottom_left_node = ajd["bottom_left"]
            bottom_right_node = ajd["bottom_right"]

            if (
                top_left_node is None
                or top_right_node is None
                or bottom_left_node is None
                or bottom_right_node is None
            ):
                continue

            half_x = top_left_node.value + a_node.value + bottom_right_node.value
            other_half_x = top_right_node.value + a_node.value + bottom_left_node.value
            if (half_x == "MAS" or half_x == "SAM") and (
                other_half_x == "MAS" or other_half_x == "SAM"
            ):
                count += 1

        return count


def part1():

    matrix = xmasMatrix(DATA)
    # print(matrix)
    # temp = matrix.get_adjacent_nodes(0, 0)
    # ch, [x, y] = temp["right"]
    # print(temp)
    # print(ch, x, y)
    # print(matrix.find_starting_nodes("X"))

    count = matrix.find_words("XMAS")
    return count


def part2():
    matrix = xmasMatrix(DATA)

    count = matrix.count_x_mas()
    return count


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
