from loadFile import read_file
import re

MAP_TEXT = read_file("./2023/dec5File.txt")


class Map:
    def __init__(self, rulesStrings):
        self.parse(rulesStrings)

    def parse(self, strings):
        self.ruleSets = []
        for line in strings:
            dest, source, length = line.split(" ")
            dest = int(dest)
            source = int(source)
            length = int(length)
            self.ruleSets.append((source, dest, length))

        self.ruleSets.sort(key=lambda x: x[0])

    def getDestForSource(self, s):
        if s < self.ruleSets[0][0] or s > self.ruleSets[-1][0] + self.ruleSets[-1][2]:
            return s

        for source, dest, length in self.ruleSets:
            if source <= s < source + length:
                offset = s - source
                return dest + offset

        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return s

    def __str__(self):
        return "(" + ", ".join([f"{d} {s} {l}" for s, d, l in self.ruleSets]) + ")"

    def __repr__(self):
        return self.__str__()


def createMaps():
    seeds, *maps = MAP_TEXT.split("\n\n")
    seeds = [int(s) for s in seeds.split(" ") if s.isdigit()]
    # print(seeds)

    ruleMaps = []

    for map in maps:
        title, *rules = map.split("\n")
        ruleMaps.append(Map(rules))
    # print()
    # print(ruleMaps)
    return seeds, ruleMaps


def createMaps2():
    seeds, *maps = MAP_TEXT.split("\n\n")

    ruleMaps = []
    for map in maps:
        title, *rules = map.split("\n")
        ruleMaps.append(Map(rules))
    # seeds = [int(s) for s in seeds.split(" ") if s.isdigit()]
    # seeds = re.findall(r"(d+ d+)", seeds)
    # seeds = re.findall(r"(?!(d+) (d+))+", seeds)
    # seeds = re.findall(r"(d+\sd+)", seeds)
    # seeds = re.findall(r"(?!(\d+\s{1}\d+))", seeds)
    print("before finding seeds")
    seeds = re.findall(r"(\d+\s\d+)", seeds)
    realSeeds = set()
    minLoc = 9999999999999999999999999999
    for idx, p in enumerate(seeds):
        s, l = p.split(" ")
        s = int(s)
        l = int(l)
        print(f"{idx} out of {len(seeds)}. adding range", s, s + l)
        for i in range(s, s + l):
            # realSeeds.add(i)
            curr = i
            # locs = []
            for map in ruleMaps:
                next = map.getDestForSource(curr)
                # print(f"{curr} -> {next}")
                curr = next
            # locs.append(curr)
            minLoc = min([curr, minLoc])
        print("current min location is", minLoc)
        print()

    print("found seeds")

    seeds = list(realSeeds)
    print(seeds)

    # print()
    # print(ruleMaps)
    return seeds, ruleMaps


def part1():
    seeds, ruleMaps = createMaps()

    # for s in [79, 14, 55, 13]:
    #     v = ruleMaps[0].getDestForSource(s)
    #     print(f"{s} -> {v}")
    locs = []
    for s in seeds:
        curr = s
        for map in ruleMaps:
            next = map.getDestForSource(curr)
            print(f"{curr} -> {next}")
            curr = next
        locs.append(curr)
        print()

    # print(locs)
    print(f"Lowest location is {min(locs)}")


# def part2():
#     print()
#     print("Part 2")
#     seeds, ruleMaps = createMaps2()

#     print("starting")

#     locs = []
#     for s in seeds:
#         curr = s
#         for map in ruleMaps:
#             next = map.getDestForSource(curr)
#             print(f"{curr} -> {next}")
#             curr = next
#         locs.append(curr)
#         print()

#     # print(locs)
#     print(f"Lowest location is {min(locs)}")


def main():
    part1()

    # part2()
    createMaps2()


main()
