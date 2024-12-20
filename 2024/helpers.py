import math
import heapq


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
        return self.__str__()

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def distance_to(self, other):
        xSquared = (other.x - self.x) ** 2
        ySquared = (other.y - self.y) ** 2
        return math.sqrt(xSquared + ySquared)

    def straight_distance_to(self, other):
        diff = other - self
        if diff.x == 0 or diff.y == 0:
            return diff

        return None


class Node:
    def __init__(self, value, x, y):
        self.value = value
        self.point = Point(x, y)

    def __str__(self):
        return f"{self.value} at {self.point}"

    # def __str__(self):
    #     return f"{self.value}"

    def __repr__(self):
        return self.__str__()

    def matrix_repr(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.point)

    def __eq__(self, other):
        return self.value == other.value and self.point == other.point

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return True


class Matrix:
    def __init__(self, data):
        self.string = data.strip()
        self.parse()

    def __str__(self):
        # return self.string
        string = ""
        for row in self.matrix:
            row_string = ""
            for node in row:
                row_string += str(node)
            string += row_string + "\n"
        return string

    def __repr__(self):
        return self.__str__()

    def parse(self):
        self.matrix = []
        for y, line in enumerate(self.string.split("\n")):
            row = []
            line_lst = list(line)
            for x, value in enumerate(line_lst):
                row.append(Node(value, x, y))

            self.matrix.append(row)

    @property
    def num_cols(self):
        return self.x

    @property
    def x(self):
        return len(self.matrix[0])

    @property
    def num_rows(self):
        return self.y

    @property
    def y(self):
        return len(self.matrix)

    def at_point(self, point):
        return self.at(point.x, point.y)

    def at(self, x, y):
        if not (-1 < x < self.num_cols):
            return None

        if not (-1 < y < self.num_rows):
            return None

        return self.matrix[y][x]

    def set_point(self, point, value):
        self.set(point.x, point.y, value)

    def set(self, x, y, value):
        if not (-1 < x < self.num_cols):
            return False

        if not (-1 < y < self.num_rows):
            return False

        self.matrix[y][x] = value
        return True


class PriorityQueue:
    def __init__(self, initial_queue):
        self.heap = initial_queue

    def push(self, tup):
        heapq.heappush(self.heap, tup)

    def pop(self):
        return heapq.heappop(self.heap)

    @property
    def size(self):
        return len(self.heap)


class BaseGraph(Matrix):
    def count_values(self, value):
        count = 0
        for row in self.matrix:
            for node in row:
                if node.value == value:
                    count += 1

        return count

    def __str__(self):
        # return self.string
        string = ""
        for row in self.matrix:
            row_string = ""
            for node in row:
                row_string += str(node.value)
            string += row_string + "\n"
        return string

    def is_node_valid_edge(self, node):
        # overwrite this
        return node is not None

    def get_edges(self, node):
        edges = []
        for p in [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]:
            n = self.at_point(node.point + p)
            if self.is_node_valid_edge(n):
                edges.append(n)
        return edges

    def bfs(self, start_node=None, end_node=None):
        if start_node == end_node:
            return [start_node]

        visited = set()
        q = [(start_node, [start_node])]
        while q:
            node, path = q.pop(0)
            edges = self.get_edges(node)
            for edge in edges:
                if edge.point not in visited:
                    if edge == end_node:
                        return path + [edge]

                    q.append((edge, path + [edge]))
                    visited.add(edge.point)
        return []

    def dfs(self, start_node, end_node):
        if start_node == end_node:
            return [start_node]

        visited = set()
        q = [(start_node, [start_node])]
        while q:
            node, path = q.pop()
            if edge.point not in visited:
                edges = self.get_edges(node)
                visited.add(node.point)
                for edge in edges:
                    if edge == end_node:
                        return path + [edge]
                    q.append((edge, path + [edge]))
        return []

    def get_cost(self, node):
        return 1

    def dijkstra(self, start_node):
        dist = {}
        prev = {}

        for row in self.matrix:
            for node in row:
                if self.is_node_valid_edge(node):
                    dist[node.point] = 999999999
                    prev[node.point] = None

        dist[start_node.point] = 0

        pq = PriorityQueue([(0, start_node)])

        while pq.size:
            cost, node = pq.pop()

            edges = self.get_edges(node)
            for edge in edges:
                new_cost = cost + self.get_cost(node)

                if new_cost < dist[edge.point]:
                    dist[edge.point] = new_cost
                    prev[edge.point] = node

                    pq.push((new_cost, edge))

        return dist, prev


class LinkedNode:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __str__(self):
        if self.next is not None:
            return f"{self.value} -> {self.next}"

        return f"{self.value}"

    def __repr__(self):
        return self.__str__()


class TreeNode:
    __slots__ = "value", "parent", "left", "right", "height"

    def __init__(self, value, parent=None, left=None, right=None):
        """
        Initialization of a node
        :param value: value stored at the node
        :param parent: the parent node
        :param left: the left child node
        :param right: the right child node
        """
        self.value = value
        self.parent = parent
        self.left = left
        self.right = right
        self.height = 0

    def __eq__(self, other):
        """
        Determine if the two nodes are equal
        :param other: the node being compared to
        :return: true if the nodes are equal, false otherwise
        """
        if type(self) is not type(other):
            return False
        return self.value == other.value

    def __str__(self):
        """String representation of a node by its value"""
        return str(self.value)

    def __repr__(self):
        """String representation of a node by its value"""
        return str(self.value)

    def is_leaf(self):
        return self.height == 0


class AVLTree:
    def __init__(self):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Initializes an empty Binary Search Tree
        """
        self.root = None  # The root Node of the tree
        self.size = 0  # The number of Nodes in the tree

    def __eq__(self, other):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Describe equality comparison for BSTs ('==')
        :param other: BST being compared to
        :return: True if equal, False if not equal
        """
        if self.size != other.size:
            return False
        if self.root != other.root:
            return False
        if self.root is None or other.root is None:
            return True  # Both must be None

        if self.root.left is not None and other.root.left is not None:
            r1 = self._compare(self.root.left, other.root.left)
        else:
            r1 = self.root.left == other.root.left
        if self.root.right is not None and other.root.right is not None:
            r2 = self._compare(self.root.right, other.root.right)
        else:
            r2 = self.root.right == other.root.right

        result = r1 and r2
        return result

    def _compare(self, t1, t2):
        # DO NOT MODIFY THIS FUNCTION #
        """
        Recursively compares two trees, used in __eq__.
        :param t1: root node of first tree
        :param t2: root node of second tree
        :return: True if equal, False if nott
        """
        if t1 is None or t2 is None:
            return t1 == t2
        if t1 != t2:
            return False
        result = self._compare(t1.left, t2.left) and self._compare(t1.right, t2.right)
        return result

    def visual(self):
        """
        Returns a visual representation of the AVL Tree in terms of levels
        :return: None
        """
        root = self.root
        if not root:
            print("Empty tree.")
            return
        bfs_queue = []
        track = {}
        bfs_queue.append((root, 0, root.parent))
        h = self.height(self.root)
        for i in range(h + 1):
            track[i] = []
        while bfs_queue:
            node = bfs_queue.pop(0)
            track[node[1]].append(node)
            if node[0].left:
                bfs_queue.append((node[0].left, node[1] + 1, node[0]))
            if node[0].right:
                bfs_queue.append((node[0].right, node[1] + 1, node[0]))
        for i in range(h + 1):
            print(f"Level {i}: ", end="")
            for node in track[i]:
                print(tuple([node[0], node[2]]), end=" ")
            print()

    ### Implement/Modify the functions below ###

    def insert(self, node, value):
        """
        Inserts a node into the sorted spot in the tree. Rebalances if needed
        :param node: root node
        :param value: value to be inserted
        :return: nothing
        """
        if not self.root:
            self.root = TreeNode(value)
            self.size += 1
            return

        else:
            if value == node.value:
                return

            if value < node.value:
                if node.left is None:
                    node.left = TreeNode(value, parent=node)
                    self.size += 1
                else:
                    self.insert(node.left, value)

            elif value > node.value:
                if node.right is None:
                    node.right = TreeNode(value, parent=node)
                    self.size += 1
                else:
                    self.insert(node.right, value)
        self.rebalance(node)

    def remove(self, node, value):
        """
        Removes the node with value value. Does nothing if value isn't found
        :param node: root node
        :param value: value to be removed
        :return: root of subtree
        """
        if node is None:
            return
        new_node = node
        found = self.search(node, value)
        if found is None or found.value != value:
            return
        node = found
        parent = node.parent

        if self.size == 1 and self.root.value == value:
            self.root = None
            self.size = 0
            return
        if self.size == 2:
            if self.root.left and self.root.value == value:
                self.root.value = self.root.left.value
                self.root.left = None
                self.root.height = 0
                self.size -= 1
                return self.root
            elif self.root.right and self.root.value == value:
                self.root.value = self.root.right.value
                self.root.right = None
                self.root.height = 0
                self.size -= 1
                return self.root

        if node.left is not None and node.right is not None:
            succ = self.max(node.left)
            self.remove(new_node, succ.value)
            found.value = succ.value
            return new_node

        elif node == new_node:
            if found.left is not None:
                new_node = node.left
            else:
                new_node = node.right
            if new_node:
                new_node.parent = None
            self.size -= 1
            return new_node
        elif node.left is not None:
            self.replace_child(parent, node, node.left)
            self.size -= 1
        else:
            self.replace_child(parent, node, node.right)
            self.size -= 1

        node = parent
        while node:
            self.rebalance(node)
            node = node.parent
        return node

    def search(self, node, value):
        """
        searches the tree for node with value value
        :param node: root node
        :param value: value to be found
        :return: node if found, else possible parent
        """
        cur = self.root
        while cur:
            if value == cur.value:
                return cur
            elif value < cur.value:
                if cur.left is None:
                    return cur
                cur = cur.left
            else:
                if cur.right is None:
                    return cur
                cur = cur.right
        return cur

    def inorder(self, node):
        """
        Returns a generator object of the tree traversed using the inorder method of traversal starting at node
        :param node: root node
        :return: generator object
        """
        if node is None:
            return
        else:
            yield from self.inorder(node.left)
            yield node
            yield from self.inorder(node.right)

    def preorder(self, node):
        """
        Returns a generator object of the tree traversed using the preorder method of traversal starting at node
        :param node: root node
        :return: generator object
        """
        if node is None:
            return
        else:
            yield node
            yield from self.preorder(node.left)
            yield from self.preorder(node.right)

    def postorder(self, node):
        """
        Returns a generator object of the tree traversed using the postorder method of traversal starting at node
        :param node: root node
        :return: generator object
        """
        if node is None:
            return
        else:
            yield from self.postorder(node.left)
            yield from self.postorder(node.right)
            yield node

    def depth(self, value):
        """
        Finds depth of node with given value
        :param value: value of depth to be found
        :return: depth
        """
        node = self.root
        dep = 0
        while node is not None:
            if node.value == value:
                return dep
            elif value < node.value:
                node = node.left
                dep += 1
            elif value > node.value:
                node = node.right
                dep += 1
        return -1

    def height(self, node):
        """
        Returns height of node
        :param node: node of height to be found
        :return: height
        """
        if node is None:
            return -1
        return node.height

    def min(self, node):
        """
        Finds the minimum value of the tree
        :param node: root node
        :return: minimum node
        """
        if node is None:
            return None
        if node.left is None:
            return node
        else:
            return self.min(node.left)

    def max(self, node):
        """
        Finds the maximum value of the tree
        :param node: root node
        :return: maximum node
        """
        if node is None:
            return None
        if node.right is None:
            return node
        else:
            return self.max(node.right)

    def get_size(self):
        """
        Number of nodes in the tree
        :return: size
        """
        return self.size

    def get_balance(self, node):
        """
        Finds the balance factor of the given node
        :param node: node of balance factor to be found
        :return: balance factor
        """
        if node is None:
            return 0
        left = -1
        if node.left is not None:
            left = node.left.height
        right = -1
        if node.right is not None:
            right = node.right.height
        return left - right

    def left_rotate(self, root):
        """
        Performs an AVL left rotation of the tree
        :param root: root node
        :return: root of rotated tree
        """
        right_left = root.right.left
        if root.parent is not None:
            self.replace_child(root.parent, root, root.right)
        else:
            self.root = root.right
            self.root.parent = None
        self.set_child(root.right, "left", root)
        self.set_child(root, "right", right_left)
        self.update_height(root)

    def right_rotate(self, root):
        """
        Performs and AVL right rotation of the tree
        :param root: root node
        :return: root of rotated tree
        """
        left_right = root.left.right
        if root.parent is not None:
            self.replace_child(root.parent, root, root.left)
        else:
            self.root = root.left
            self.root.parent = None
        self.set_child(root.left, "right", root)
        self.set_child(root, "left", left_right)
        self.update_height(root)

    def rebalance(self, node):
        """
        Rebalances the tree at node
        :param node: node that needs to be rebalanced
        :return: balanced node
        """
        self.update_height(node)
        if self.get_balance(node) == -2:
            if self.get_balance(node.right) == 1:
                self.right_rotate(node.right)
            return self.left_rotate(node)
        elif self.get_balance(node) == 2:
            if self.get_balance(node.left) == -1:
                self.left_rotate(node.left)
            return self.right_rotate(node)
        return node

    def set_child(self, parent, which_child, child):
        """
        sets the node as the parents left of right
        :param parent: parent node
        :param which_child: left or right
        :param child: child node
        :return: True or false
        """
        if which_child != "left" and which_child != "right":
            return False
        if which_child == "left":
            parent.left = child
        else:
            parent.right = child
        if child is not None:
            child.parent = parent
        self.update_height(child)
        return True

    def replace_child(self, parent, current, new_child):
        """
        Replaces current node with a new value
        :param parent: parent node
        :param current: node to be changed
        :param new_child: new node
        :return: True of false
        """
        if parent.left == current:
            return self.set_child(parent, "left", new_child)
        elif parent.right == current:
            return self.set_child(parent, "right", new_child)
        return False

    def update_height(self, node):
        """
        Updates the height of the node
        :param node: node of height to be found
        :return: nothing
        """
        if node is None:
            return
        left = -1
        if node.left is not None:
            left = node.left.height
        right = -1
        if node.right is not None:
            right = node.right.height
        node.height = 1 + max(right, left)


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
            raise TypeError

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
