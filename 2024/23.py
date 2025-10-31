import re
import os
from helpers import parse_to_list
from itertools import combinations


FILENAME = os.path.basename(__file__)
YEAR = os.path.basename(os.path.dirname(__file__))
TEXT_FILE_PATH = os.path.join(".", YEAR, FILENAME.split(".")[0] + ".txt")
DATA = parse_to_list(TEXT_FILE_PATH)


class Computer:
    def __init__(self, name) -> None:
        self.name = name
        self.connections = set()

    def __hash__(self) -> int:
        return hash(self.name)

    def add_connection(self, other):
        self.connections.add(other)

    def connections_sorted(self):
        return sorted(self.connections)

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.name > other.name

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other):
        return not self.__gt__(other)

    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)

    def __str__(self) -> str:
        return f"{self.name}: {', '.join(c.name for c in self.connections_sorted())}"

    def __repr__(self) -> str:
        return self.__str__()


def connected(a, b, c, graph):
    return (
        a in graph[b]
        and a in graph[c]
        and b in graph[a]
        and b in graph[c]
        and c in graph[a]
        and c in graph[b]
    )


def get_groups_of_three_with_t(graph):
    paths = []

    for k, connections in graph.items():
        # for c in connections:
        visited_nodes = set()
        cur = k
        path = []
        while cur not in visited_nodes:
            visited_nodes.add(cur)
            path.append(cur)
            # graph[cur] is a set
            # how to get next node?
            # first node not in visited
            for next in graph[cur]:
                if next not in visited_nodes:
                    cur = next
                    break

        paths.append(path)

    # print(paths)
    threes = set()
    for p in paths:
        print(p, len(p) == len(set(p)))
        continue
        combs = combinations(p, 3)
        for comb in combs:
            a, b, c = comb
            if connected(a, b, c, graph):
                sorted_comb = tuple(sorted(comb))
                threes.add(sorted_comb)

    # print(f"groups of three ({len(threes)}):")
    # for t in threes:
    #     print(t)

    threes_with_t = []
    for t in threes:
        a, b, c = t
        if a.startswith("t") or b.startswith("t") or c.startswith("t"):
            threes_with_t.append(t)

    # print(f"groups of three with t ({len(threes_with_t)}):")
    # for t in threes_with_t:
    #     print(t)

    return len(threes_with_t)


def get_groups_of_three_with_t_2(graph):
    threes = set()
    for a, connections in graph.items():
        for b in connections:
            for c in graph[b]:
                sorted_comb = tuple(sorted([a, b, c]))
                if connected(a, b, c, graph):
                    threes.add(sorted_comb)

    threes_with_t = []
    for t in threes:
        a, b, c = t
        if a.startswith("t") or b.startswith("t") or c.startswith("t"):
            threes_with_t.append(t)

    return len(threes_with_t)


def all_connected(computers, graph):
    for a in computers:
        for b in computers:
            if a == b:
                continue
            if not (a in graph[b] and b in graph[a]):
                return False

    return True


def find_largest_group(graph):
    found = {}

    start_length = 2

    for k, v in graph.items():
        group = set([k]) | v

        min_length = (max(found.keys() or [0]) or start_length) + 1

        for length in range(min_length, len(group)):
            # print(f"searching length: {length}")

            combs = combinations(group, length)

            for comb in combs:
                if all_connected(comb, graph):
                    if length in found:
                        found[length].append(comb)
                    else:
                        found[length] = [comb]

    passwords = found[max(found.keys())]

    if len(passwords) == 1:
        return ",".join(sorted(passwords[0]))

    for p in passwords:
        print(",".join(sorted(p)))
    # print(found)


def part1():
    # print(DATA)

    connections = {}

    for con in DATA:
        a, b = con.split("-")

        if a not in connections:
            connections[a] = set()
        if b not in connections:
            connections[b] = set()

        connections[a].add(b)
        connections[b].add(a)

    # for k, v in connections.items():
    #     print(k, v)

    # 1112 too low
    return get_groups_of_three_with_t_2(connections)
    # name_to_computer = {}


def part2():
    connections = {}

    for con in DATA:
        a, b = con.split("-")

        if a not in connections:
            connections[a] = set()
        if b not in connections:
            connections[b] = set()

        connections[a].add(b)
        connections[b].add(a)

    # for k, v in connections.items():
    #     print(k, v)

    # print(connections.keys())

    return find_largest_group(connections)

    # 1112 too low
    # return get_groups_of_three_with_t(connections)


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
