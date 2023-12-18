from loadFile import read_file

HASH_TEXT = read_file("./2023/15.txt")


class Lens:
    def __init__(self, string):
        self.string = string
        self.parse()

    def parse(self):
        if "=" in self.string:
            self.label, self.focalLen = self.string.split("=")
            self.operator = "="
        elif "-" in self.string:
            self.label, self.focalLen = self.string.split("-")
            self.operator = "-"
        if self.focalLen:
            self.focalLen = int(self.focalLen)
        self.hash_ = hashString(self.label)

    def __str__(self):
        return f"{self.label} {self.focalLen}"

    def __repr__(self):
        return self.__str__()


class HASHMAP:
    def __init__(self):
        self.boxes = dict()

    def getBox(self, hash_):
        return self.boxes.get(hash_)

    def __setBox(self, hash_, newBox):
        self.boxes[hash_] = newBox

    def findLens(self, hash_, label):
        for i, l in enumerate(self.boxes[hash_]):
            if l.label == label:
                return i
        return -1

    def removeLabelsForLens(self, lens):
        box = self.getBox(lens.hash_)
        if box:
            labelsRemovedBox = [l for l in box if l.label != lens.label]
            self.__setBox(lens.hash_, labelsRemovedBox)

    def addNewLens(self, lens):
        box = self.getBox(lens.hash_)
        if not box:
            self.__setBox(lens.hash_, [lens])
            return

        index = self.findLens(lens.hash_, lens.label)
        if index >= 0:
            self.boxes[lens.hash_][index] = lens
            return

        self.boxes[lens.hash_].append(lens)

    def operate(self, lens):
        if lens.operator == "-":
            self.removeLabelsForLens(lens)

        elif lens.operator == "=":
            self.addNewLens(lens)

    def calculateFocusingPower(self):
        power = 0
        for k, v in self.boxes.items():
            if not v:
                continue
            for i, l in enumerate(v):
                temp = (k + 1) * (i + 1) * l.focalLen
                power += temp
                # print(f"Power for {l} is {temp}")
        return power

    def __str__(self):
        string = ""
        for k, v in self.boxes.items():
            string += f"Box {k}: {v}\n" if v else ""

        return string.strip()

    def __repr__(self):
        return self.__str__()


def hash(char, curr=0):
    asciiVal = ord(char)

    curr += asciiVal
    curr *= 17

    return curr % 256


def hashString(string):
    # hsh = sum([hash(ch) for ch in string])
    hsh = 0
    for ch in string:
        hsh = hash(ch, hsh)

    return hsh


def parse():
    lst = HASH_TEXT.split(",")
    return lst


def part1():
    print("Part 1")
    lst = parse()

    hashSum = 0

    for string in lst:
        hsh = hashString(string)
        hashSum += hsh
        print(f"{string} -> {hsh}")

    print(f"Total hash sum is {hashSum}")


def part2():
    print()
    print("Part 2")

    lst = parse()
    hashMap = HASHMAP()

    for string in lst:
        lens = Lens(string)
        # print(f"{lens.label} -> {lens.hash_}")
        # print(f"After {lens.string}:")
        hashMap.operate(lens)
        # print(hashMap)
        # print()

    power = hashMap.calculateFocusingPower()

    print(f"Power of resulting lens config is {power}")


def main():
    part1()

    part2()


main()
