import re
from pathlib import Path
from helpers import read_file


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class FileSystem:
    def __init__(self, data):
        self.system = []
        self.ids_seen = set()
        self.parse(data)

    def parse(self, data):
        sizes = list(map(int, data.strip()))
        # print(sizes)
        self.ids = []

        id = 0
        for i, num in enumerate(sizes):
            # print(id, num)
            if i % 2 == 0:
                self.ids.append([id, num])
                self.system += [id] * num
                id += 1
            else:
                self.system += ["."] * num

        self.ids = sorted(self.ids, key=lambda x: x[0], reverse=True)

    def find_last_non_free_space(self):
        index = -1
        for i, num in enumerate(self.system):
            if num != ".":
                index = i

        return index

    def remove_freespace(self):
        first = self.system.index(".")
        last = self.find_last_non_free_space()

        # print(first, last)

        while last - first > 1:
            self.system[first], self.system[last] = (
                self.system[last],
                self.system[first],
            )
            first = self.system.index(".")
            last = self.find_last_non_free_space()

            # print(self.system)

    def checksum(self):
        total = 0
        for i, num in enumerate(self.system):
            if type(num) == int:
                total += i * num

        return total

    def first_chunk_of_freespace(self):
        chunk = []
        for i, val in enumerate(self.system):
            if val == ".":
                chunk.append(i)
            elif len(chunk) > 0:
                return chunk

        return chunk

    def get_first_chunk_before(self, length, index):
        chunk = []
        for i, val in enumerate(self.system[:index]):
            if val == ".":
                chunk.append(i)
                if len(chunk) >= length:
                    return chunk

            elif val != ".":
                if len(chunk) >= length:
                    return chunk
                else:
                    chunk = []

        return []

    def index_all(self, id):
        return [i for i, val in enumerate(self.system) if val == id]

    def remove_freespace_by_chunk(self):

        for id, length in self.ids:
            id_indexes = self.index_all(id)
            if len(id_indexes) != length:
                print(len(id_indexes), length)

            chunk = self.get_first_chunk_before(length, id_indexes[0])
            if len(chunk) == 0:
                continue

            # print(id, id_indexes, chunk)

            for i, system_i in enumerate(id_indexes):
                self.system[system_i], self.system[chunk[i]] = (
                    self.system[chunk[i]],
                    self.system[system_i],
                )

            # print(self.system)
            # print()


def part1():
    # print(DATA)
    fs = FileSystem(DATA)
    # print(fs.system)
    fs.remove_freespace()
    return fs.checksum()


def part2():
    fs = FileSystem(DATA)
    # print(fs.system)
    # print(fs.ids)
    # print(fs.first_chunk_of_freespace())
    fs.remove_freespace_by_chunk()
    # print(fs.system)

    # 6460170597310 too high
    # 6460170597310
    # 6570501590468 too high
    # 6460170593016

    return fs.checksum()


def main():
    # print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
