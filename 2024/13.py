import re
from pathlib import Path
from helpers import read_file
from sympy import symbols, Eq, solve, Integer


PATH = Path(__file__)
YEAR = str(PATH).split("\\")[-2]
DATA = read_file(f"./{YEAR}/{PATH.name.split('.')[0]}.txt")


class Equation:
    def __init__(self, eq1, eq2):
        self.a, self.b = symbols("a b")

        self.eq1 = Eq(eq1[0] * self.a + eq1[1] * self.b, eq1[2])
        self.eq2 = Eq(eq2[0] * self.a + eq2[1] * self.b, eq2[2])

        # print(self.eq1)
        # print(self.eq2)

    def solve(self):
        return solve((self.eq1, self.eq2), (self.a, self.b))

    def cost(self):
        answer = self.solve()
        a_button = answer[self.a]
        b_button = answer[self.b]

        if isinstance(a_button, Integer) and isinstance(b_button, Integer):
            return 3 * a_button + b_button

        return 0


class Equation2(Equation):
    def __init__(self, eq1, eq2):
        eq1[2] += 10000000000000
        eq2[2] += 10000000000000
        super().__init__(eq1, eq2)


def parse_group(group, class_constuctor):
    l1, l2, l3 = group.split("\n")
    eq1a, eq2a = re.findall("\d+", l1)
    eq1b, eq2b = re.findall("\d+", l2)
    eq1c, eq2c = re.findall("\d+", l3)

    # print(eq1a, eq1b, eq1c)
    # print(eq2a, eq2b, eq2c)

    eq = class_constuctor(
        list(map(int, [eq1a, eq1b, eq1c])), list(map(int, [eq2a, eq2b, eq2c]))
    )

    return eq


def part1():
    groups = []
    for group in DATA.strip().split("\n\n"):
        # print(group)
        groups.append(parse_group(group, Equation))

    total_cost = 0
    for g in groups:
        total_cost += g.cost()

    return total_cost


def part2():
    groups = []
    for group in DATA.strip().split("\n\n"):
        # print(group)
        groups.append(parse_group(group, Equation2))

    total_cost = 0
    for g in groups:
        total_cost += g.cost()

    return total_cost


def main():
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")


main()
