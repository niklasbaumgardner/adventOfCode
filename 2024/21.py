import os
from helpers import read_file, BaseGraph, Node, Point, PriorityQueue


FILENAME = os.path.basename(__file__)
YEAR = os.path.basename(os.path.dirname(__file__))
TEXT_FILE_PATH = os.path.join(".", YEAR, FILENAME.split(".")[0] + ".txt")
DATA = read_file(TEXT_FILE_PATH)


POINT_TO_ARROW = {
    Point(-1, 0): "<",
    Point(1, 0): ">",
    Point(0, -1): "^",
    Point(0, 1): "v",
}
CURRENT_DIR_TO_NEXT_POINTS_NUMPAD = {
    "N": [(Point(0, -1), 3), (Point(0, 1), 11), (Point(1, 0), 9), (Point(-1, 0), 6)],
    "E": [(Point(1, 0), 4), (Point(-1, 0), 11), (Point(0, 1), 7), (Point(0, -1), 8)],
    "S": [(Point(0, 1), 2), (Point(0, -1), 11), (Point(1, 0), 9), (Point(-1, 0), 6)],
    "W": [(Point(-1, 0), 1), (Point(1, 0), 11), (Point(0, 1), 7), (Point(0, -1), 8)],
    None: [(Point(-1, 0), 1), (Point(1, 0), 4), (Point(0, 1), 2), (Point(0, -1), 3)],
}
CURRENT_DIR_TO_NEXT_POINTS_ARROWPAD = {
    "N": [(Point(0, -1), 3), (Point(0, 1), 11), (Point(1, 0), 9), (Point(-1, 0), 6)],
    "E": [(Point(1, 0), 4), (Point(-1, 0), 11), (Point(0, 1), 7), (Point(0, -1), 8)],
    "S": [(Point(0, 1), 2), (Point(0, -1), 11), (Point(1, 0), 9), (Point(-1, 0), 6)],
    "W": [(Point(-1, 0), 1), (Point(1, 0), 11), (Point(0, 1), 7), (Point(0, -1), 8)],
    None: [(Point(-1, 0), 1), (Point(1, 0), 4), (Point(0, 1), 2), (Point(0, -1), 3)],
}
POINT_TO_DIR = {
    Point(0, -1): "N",
    Point(1, 0): "E",
    Point(0, 1): "S",
    Point(-1, 0): "W",
}
DIR_TO_OPPOSITE_POINT = {
    "S": Point(0, -1),
    "W": Point(1, 0),
    "N": Point(0, 1),
    "E": Point(-1, 0),
}
DIR_TO_OPPOSITE_DIR = {"N": "S", "E": "W", "S": "N", "W": "E"}
DIR_STRAIGHT_COST = {"N": 1, "E": 1, "S": 1, "W": 0.5}
DIR_TURN_COST = {}

INFINITY = 99999999999999999999


class Numpad(BaseGraph):
    def __init__(self):
        self.parse()

    def parse(self):
        self.matrix = []
        for y, line in enumerate([[7, 8, 9], [4, 5, 6], [1, 2, 3], [None, 0, "A"]]):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                node = Node(value, x, y)
                row.append(node)

                if node.value == "A":
                    self.start = node
                # elif node.value == "E":
                #     self.end = node

            self.matrix.append(row)

    @property
    def num7(self):
        return self.at(0, 0)

    @property
    def num8(self):
        return self.at(1, 0)

    @property
    def num9(self):
        return self.at(2, 0)

    @property
    def num4(self):
        return self.at(0, 1)

    @property
    def num5(self):
        return self.at(1, 1)

    @property
    def num6(self):
        return self.at(2, 1)

    @property
    def num1(self):
        return self.at(0, 2)

    @property
    def num2(self):
        return self.at(1, 2)

    @property
    def num3(self):
        return self.at(2, 2)

    @property
    def num0(self):
        return self.at(1, 3)

    @property
    def numA(self):
        return self.at(2, 3)

    def char_to_node(self, ch):
        match ch:
            case 0:
                return self.num0
            case 1:
                return self.num1
            case 2:
                return self.num2
            case 3:
                return self.num3
            case 4:
                return self.num4
            case 5:
                return self.num5
            case 6:
                return self.num6
            case 7:
                return self.num7
            case 8:
                return self.num8
            case 9:
                return self.num9
            case "A":
                return self.numA
        return None

    def get_edges(self, node, current_dir):
        next_points = CURRENT_DIR_TO_NEXT_POINTS_NUMPAD[current_dir]

        edges = []
        for p, cost in next_points:
            n = self.at_point(node.point + p)
            if self.is_node_valid_edge(n):
                # cost = self.get_cost(p, current_dir)
                edges.append((cost, n, POINT_TO_DIR[p]))
        return edges

    def get_cost(self, dir_point, current_dir):
        if dir_point == current_dir:
            return 1

        return 10

    def dijkstra(self, start_node, end_node, start_dir):
        if start_node.point == end_node.point:
            return [], start_dir

        dist = {}
        prev = {}

        for row in self.matrix:
            for node in row:
                if self.is_node_valid_edge(node):
                    for dir in "NSEW":
                        dist[(node.point, dir)] = INFINITY if node != start_node else 0
                        prev[(node.point, dir)] = (None, None)

        pq = PriorityQueue([(0, start_node, start_dir)])

        while pq.size:
            cost, node, current_dir = pq.pop()

            edges = self.get_edges(node, current_dir)
            for c, edge, e_dir in edges:
                new_cost = cost + c
                prev_cost = dist[(edge.point, e_dir)]

                if new_cost < prev_cost:
                    dist[(edge.point, e_dir)] = new_cost
                    prev[(edge.point, e_dir)] = (node, current_dir)

                    pq.push((new_cost, edge, e_dir))

        # for k, v in prev.items():
        #     print(k, v)

        return self.reconstruct_path_with_dir(dist, prev, end_node)


class Arrowpad(BaseGraph):
    def __init__(self):
        self.parse()

    def parse(self):
        self.matrix = []
        for y, line in enumerate([[None, "^", "A"], ["<", "v", ">"]]):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                node = Node(value, x, y)
                row.append(node)

                if node.value == "A":
                    self.start = node
                # elif node.value == "E":
                #     self.end = node

            self.matrix.append(row)

    @property
    def left(self):
        return self.at(0, 1)

    @property
    def down(self):
        return self.at(1, 1)

    @property
    def right(self):
        return self.at(2, 1)

    @property
    def up(self):
        return self.at(1, 0)

    @property
    def numA(self):
        return self.at(2, 0)

    def char_to_node(self, ch):
        match ch:
            case "<":
                return self.left
            case "^":
                return self.up
            case ">":
                return self.right
            case "v":
                return self.down
            case "A":
                return self.numA

        return None

    def get_edges(self, node, current_dir):
        next_points = CURRENT_DIR_TO_NEXT_POINTS_ARROWPAD[current_dir]

        edges = []
        for p, cost in next_points:
            n = self.at_point(node.point + p)
            if self.is_node_valid_edge(n):
                # cost = self.get_cost(p, current_dir)
                edges.append((cost, n, POINT_TO_DIR[p]))
        return edges

    def get_cost(self, dir_point, current_dir):
        if dir_point == current_dir:
            return 1

        return 10

    def dijkstra(self, start_node, end_node, start_dir):
        if start_node.point == end_node.point:
            return [], start_dir

        dist = {}
        prev = {}

        for row in self.matrix:
            for node in row:
                if self.is_node_valid_edge(node):
                    for dir in "NSEW":
                        dist[(node.point, dir)] = INFINITY if node != start_node else 0
                        prev[(node.point, dir)] = (None, None)

        pq = PriorityQueue([(0, start_node, start_dir)])

        while pq.size:
            cost, node, current_dir = pq.pop()

            edges = self.get_edges(node, current_dir)
            for c, edge, e_dir in edges:
                new_cost = cost + c
                prev_cost = dist[(edge.point, e_dir)]

                if new_cost < prev_cost:
                    dist[(edge.point, e_dir)] = new_cost
                    prev[(edge.point, e_dir)] = (node, current_dir)

                    pq.push((new_cost, edge, e_dir))

        return self.reconstruct_path_with_dir(dist, prev, end_node)


def path_to_arrows(path):
    string = ""
    for i in range(len(path) - 1):
        node = path[i]
        next = path[i + 1]
        string += POINT_TO_ARROW[next.point - node.point]
    return string


def parse_data():
    lst = []
    for line in DATA.strip().split("\n"):
        # print(line)
        temp = []
        for ch in line:
            if ch.isdigit():
                temp.append(int(ch))
            else:
                temp.append(ch)
        lst.append(temp)

    return lst


def struct_to_int(struct):
    split = struct.split("A")
    num = split[0]
    if num.isdigit():
        return int(num)

    return 0


def part1():
    m = Numpad()
    print(m)

    arrow1 = Arrowpad()
    print(arrow1)
    arrow2 = Arrowpad()

    def get_arrow2_path(path):
        prev = arrow2.start
        string_path = ""
        dir = None
        for end in path:
            end_node = arrow2.char_to_node(end)
            a2_path, dir = arrow2.dijkstra(prev, end_node, None)
            string_path += path_to_arrows(a2_path) + "A"
            prev = end_node

        return string_path

    def get_arrow1_path(path):
        prev = arrow1.start
        string_path = ""
        dir = None
        for end in path:
            end_node = arrow1.char_to_node(end)
            a1_path, dir = arrow1.dijkstra(prev, end_node, None)
            string_path += path_to_arrows(a1_path) + "A"
            # print(string_path)
            prev = end_node
        # v<<A>>^A<A>AvA<^AA>A<vAAA>^A

        return string_path

    paths_dict = dict()

    instructions = parse_data()
    # print(instructions)
    for struct in instructions:
        prev = m.start
        string_path = ""
        dir = None
        print(struct)
        for end in struct:
            end_node = m.char_to_node(end)
            # print(prev, "->", end_node)
            path, dir = m.dijkstra(prev, end_node, None)
            # print(path)
            string_path += path_to_arrows(path) + "A"
            # print(string_path)

            # print(path, path_to_arrows(path) + "A")
            prev = end_node
            # print()
            # print()
        print(string_path)
        # print()
        # return
        a1_path = get_arrow1_path(string_path)
        print(a1_path)
        whole_path = get_arrow2_path(a1_path)
        print(whole_path)
        print()

        s = "".join(map(str, struct))
        paths_dict[s] = whole_path
        # break

        # break

    # path = m.bfs(m.start, m.end)
    total = 0
    for k, v in paths_dict.items():
        print(k, struct_to_int(k), len(v), v)
        total += struct_to_int(k) * len(v)

    # 173472 too high
    # 176156 too high
    return total


def part2():
    return


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()

# <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
# <v<A>A<A>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
