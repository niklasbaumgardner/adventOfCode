import re
from pathlib import Path
from helpers import read_file, Matrix, Node


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class TreeNode(Node):
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
            if (n.value - self.value) == 1:
                valid.append(n)

        return valid


class Tree(Matrix):
    def parse(self):
        self.matrix = []
        self.trailheads = []
        for y, line in enumerate(self.string.split("\n")):
            row = []
            line_lst = list(map(int, line))
            for x, value in enumerate(line_lst):
                row.append(TreeNode(value=value, x=x, y=y))

            self.matrix.append(row)

        for x, row in enumerate(self.matrix):
            for y, node in enumerate(row):
                node.left = self.at(node.point.x - 1, node.point.y)
                node.up = self.at(node.point.x, node.point.y - 1)
                node.right = self.at(node.point.x + 1, node.point.y)
                node.down = self.at(node.point.x, node.point.y + 1)

                if node.value == 0:
                    self.trailheads.append(node)

    def get_scores(self):
        # trailhead node -> set(9 points)
        scores = dict()

        for start in self.trailheads:
            queue = [(start, [start])]
            # path = []
            visited = set()

            while queue:
                (node, path) = queue.pop(0)

                neighbors = node.get_valid_neighbors()
                # print(node, neighbors)
                for n in neighbors:
                    if n.point not in visited:
                        if n.value == 9:
                            # print("path", path, n)
                            if start.point in scores:
                                scores[start.point].add(n.point)
                            else:
                                scores[start.point] = set([n.point])
                            continue

                        queue.append((n, path + [n]))
                        visited.add(n.point)
            # print()
            # break

        # print(scores)
        total = 0
        for k, v in scores.items():
            # print(k, v)
            total += len(v)
        return total

    def get_ratings_v1(self):
        # trailhead node -> set(9 points)
        scores = dict()

        for start in self.trailheads:
            queue = [(start, [start])]
            # path = []
            visited = set()

            while queue:
                (node, path) = queue.pop(0)

                neighbors = node.get_valid_neighbors()
                # print(node, neighbors)
                for n in neighbors:
                    if n.point not in visited:
                        if n.value == 9:
                            # print("path", path, n)
                            if start.point in scores:
                                scores[start.point].append(n.point)
                            else:
                                scores[start.point] = [n.point]
                            continue

                        queue.append((n, path + [n]))
                        # visited.add(n.point)
            # print()
            # break

        # print(scores)
        total = 0
        for k, v in scores.items():
            # print(k, v)
            total += len(v)
        return total

    def get_ratings_v2(self):
        # trailhead node -> set(9 points)
        scores = dict()

        for start in self.trailheads:
            queue = [(start, [start])]
            # path = []
            visited = set()

            while queue:
                (node, path) = queue.pop()

                if node.point not in visited:
                    neighbors = node.get_valid_neighbors()
                    visited.add(node.point)

                neighbors = node.get_valid_neighbors()
                # print(node, neighbors)
                for n in neighbors:
                    if n.point not in visited:
                        if n.value == 9:
                            # print("path", path, n)
                            if start.point in scores:
                                scores[start.point].add(n.point)
                            else:
                                scores[start.point] = set([n.point])
                            continue

                        queue.append((n, path + [n]))
                        visited.add(n.point)
            # print()
            # break

            # q = [(start, [start])]
            # while q:
            #     (vertex, path) = q.pop()
            #     if self.id_map[vertex].visited is False:
            #         edges = self.get_edges(vertex)
            #         self.id_map[vertex].visit()
            #         for edge in edges:
            #             if edge == target:
            #                 return path + [edge]
            #             q.append((edge, path + [edge]))

        # print(scores)
        total = 0
        for k, v in scores.items():
            # print(k, v)
            total += len(v)
        return total
        # return path + [n]

        # if self.get_vertex(start):
        #     if start == target:
        #         return [start]
        #     q = [(start, [start])]
        #     while q:
        #         (vertex, path) = q.pop(0)
        #         edges = self.get_edges(vertex)
        #         for edge in edges:
        #             if self.id_map[edge].visited is False:
        #                 if edge == target:
        #                     return path + [edge]
        #                 q.append((edge, path + [edge]))
        #                 self.id_map[edge].visit()
        # return []


class Vertex:
    """
    Class representing a Vertex in the Graph
    """

    __slots__ = ["ID", "index", "visited"]

    def __init__(self, ID, index):
        """
        Class representing a vertex in the graph
        :param ID : Unique ID of this vertex
        :param index : Index of vertex edges in adjacency matrix
        """
        self.ID = ID
        self.index = index  # The index that this vertex is in the matrix
        self.visited = False

    def __repr__(self):
        return f"Vertex: {self.ID}"

    __str__ = __repr__

    def __eq__(self, other):
        """
        DO NOT EDIT THIS METHOD
        :param other: Vertex to compare
        :return: Bool, True if same, otherwise False
        """
        return self.ID == other.ID and self.index == other.index

    def out_degree(self, adj_matrix):
        """
        counts the number of outgoing edges for given vertex
        :param adj_matrix: adjacency matrix for the graph
        :return: number of outgoing edges
        """
        count = 0
        if adj_matrix:
            for ele in adj_matrix[self.index]:
                if ele is not None:
                    count += 1
        return count

    def in_degree(self, adj_matrix):
        """
        counts the number of incoming edges for given vertex
        :param adj_matrix:  adjacency matrix for the graph
        :return: number of incoming edges
        """
        count = 0
        if adj_matrix:
            for lst in adj_matrix:
                if lst[self.index] is not None:
                    count += 1
        return count

    def visit(self):
        """
        sets visited to true
        :return: None
        """
        self.visited = True


# Custom Graph error
class GraphError(Exception):
    pass


class Graph:
    """
    Graph Class ADT
    """

    def __init__(self, iterable=None):
        """
        DO NOT EDIT THIS METHOD
        Construct a random Directed Graph
        :param size: Number of vertices
        :param: iterable: iterable containing edges to use to construct the graph.
        """
        self.id_map = {}  # { vertex.ID: vertex }
        self.size = 0
        self.matrix = []
        self.iterable = iterable
        self.construct_graph()
        if hasattr(iterable, "close"):
            # iterable.close()
            pass

    def __eq__(self, other):
        """
        DO NOT EDIT THIS METHOD
        Determines if 2 graphs are Identical
        :param other: Graph Object
        :return: Bool, True if Graph objects are equal
        """
        return (
            self.id_map == other.id_map
            and self.matrix == other.matrix
            and self.size == other.size
        )

    def __str__(self):
        """
        function for printing graph in a visually pleasing way
        :return: string
        """
        string = "     "
        keys = []
        for k in self.id_map:
            string += "{0:>5s}".format(str(k))
            keys.append(str(k))
        string += "\n"
        i = 0
        for lst in self.matrix:
            string += "{0:>5s}".format(str(keys[i]))
            i += 1
            for item in lst:
                if item is None:
                    item = "_"
                string += "{0:>5s}".format(str(item))
            string += "\n"
        return string

    __repr__ = __str__

    def get_vertex(self, ID):
        """
        gets the vertex if ID is in the graph
        :param ID: vertex ID
        :return: vertex if found otherwise none
        """
        if ID in self.id_map:
            return self.id_map[ID]
        return None

    def get_edges(self, ID):
        """
        gets the outgoing edges for a given ID
        :param ID: vertex ID
        :return: set of edges if vertex exists and has edges otherwise empty set
        """
        edges = set()
        if ID in self.id_map:
            for vertex in self.matrix[self.id_map[ID].index]:
                if vertex is not None:
                    edges.add(vertex)
        return edges

    def construct_graph(self):
        """
        creates a graph with iterable object, throws GraphError if iterable is not iterable
        :return:
        """
        try:
            for e in self.iterable:
                s, d = e.split()
                self.insert_edge(int(s), int(d))
        except TypeError:
            raise GraphError

    def insert_edge(self, source, destination):
        """
        adds vertex edge to the graph
        :param source: first vertex
        :param destination: second vertex
        :return: None
        """
        s_index = self.get_vertex(source)
        if s_index is None:
            self.id_map[source] = Vertex(source, self.size)
            if self.size == 0:
                self.matrix = [[None]]
            else:
                for lst in self.matrix:
                    lst += [None]
                self.matrix.append([None for i in range(self.size + 1)])
            self.size += 1

        d_index = self.get_vertex(destination)
        if d_index is None:
            self.id_map[destination] = Vertex(destination, self.size)
            for lst in self.matrix:
                lst += [None]
            self.matrix.append([None for i in range(self.size + 1)])
            self.size += 1

        s_index = self.get_vertex(source).index
        d_index = self.get_vertex(destination).index
        self.matrix[s_index][d_index] = destination

    def bfs(self, start, target, path=None):
        """
        breadth first search from starting vertex to target vertex
        :param start: starting vertex
        :param target: ending vertex
        :param path: None
        :return: path from starting vertex to target vertex
        """
        if self.get_vertex(start):
            if start == target:
                return [start]
            q = [(start, [start])]
            while q:
                (vertex, path) = q.pop(0)
                edges = self.get_edges(vertex)
                for edge in edges:
                    if self.id_map[edge].visited is False:
                        if edge == target:
                            return path + [edge]
                        q.append((edge, path + [edge]))
                        self.id_map[edge].visit()
        return []

    def dfs(self, start, target, path=None):
        """
        depth first search from starting vertex to target vertex
        :param start: starting vertex
        :param target: ending vertex
        :param path: None
        :return: path from starting vertex to target vertex
        """
        if self.get_vertex(start):
            if start == target:
                return [start]
            q = [(start, [start])]
            while q:
                (vertex, path) = q.pop()
                if self.id_map[vertex].visited is False:
                    edges = self.get_edges(vertex)
                    self.id_map[vertex].visit()
                    for edge in edges:
                        if edge == target:
                            return path + [edge]
                        q.append((edge, path + [edge]))
        return []


def part1():
    # print(DATA)
    tree = Tree(DATA)

    # print(len(tree.trailheads), tree.trailheads)
    score = tree.get_scores()

    # 301 too low

    return score


def part2():
    tree = Tree(DATA)

    score = tree.get_ratings_v1()

    return score


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
