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

    def get_biggest_id_not_seen(self):
        for id, length in self.ids:
            if id not in self.ids_seen:
                return id

        return None

    def index_all(self, id):
        return [i for i, val in enumerate(self.system) if val == id]

    def remove_freespace_by_chunk(self):
        ids_swapped = set()

        chunk = self.first_chunk_of_freespace()
        first_chunk_index = chunk[0]

        id = self.get_biggest_id_not_seen()
        id_indexes = self.index_all(id)
        first_id_index = id_indexes[0]

        # print(chunk, id, id_indexes)
        while first_chunk_index < first_id_index:
            self.ids_seen.add(id)
            print(id)

            if len(id_indexes) <= len(chunk):
                for i, system_i in enumerate(id_indexes):
                    self.system[system_i], self.system[chunk[i]] = (
                        self.system[chunk[i]],
                        self.system[system_i],
                    )

                ids_swapped.add(id)

                print(self.ids_seen)
                self.ids_seen = set(
                    [id for id, length in self.ids if id in ids_swapped]
                )
                print(self.ids_seen)
            else:
                if len(self.ids_seen) == len(self.ids):
                    self.ids_seen = set(
                        [id for id, length in self.ids if id in ids_swapped]
                    )
                    # print(self.ids_seen)
                id = self.get_biggest_id_not_seen()
                id_indexes = self.index_all(id)
                first_id_index = id_indexes[0]
                continue

            chunk = self.first_chunk_of_freespace()
            first_chunk_index = chunk[0]

            id = self.get_biggest_id_not_seen()
            id_indexes = self.index_all(id)
            first_id_index = id_indexes[0]

            print(id, first_chunk_index, first_id_index)

        #     pass


def part1():
    # print(DATA)
    fs = FileSystem(DATA)
    # print(fs.system)
    fs.remove_freespace()
    return fs.checksum()


def part2():
    fs = FileSystem(DATA)
    print(fs.system)
    # print(fs.ids)
    # print(fs.first_chunk_of_freespace())
    fs.remove_freespace_by_chunk()
    print(fs.system)
    return fs.checksum()


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
