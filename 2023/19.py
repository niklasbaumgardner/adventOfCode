from pathlib import Path
from loadFile import read_file

PATH = Path(__file__)
DATA = read_file(f"./2023/{PATH.name.split('.')[0]}.txt")


def lessThan(a, b):
    return a < b


def greaterThan(a, b):
    return a > b


class Rule:
    def __init__(self, var, func, val, next):
        self.var = var
        self.func = func
        if type(val) == str:
            val = int(val)
        self.val = val
        self.next = next

    def __str__(self):
        return f"[{self.var} {'>' if self.func == greaterThan else '<'} {self.val}. next: {self.next}]"

    def __repr__(self):
        return self.__str__()


class RuleSet:
    def __init__(self, string):
        self.string = string
        self.parse()

    def parse(self):
        name, rules = self.string.strip("}").split("{")
        self.name = name
        self.rules = []
        # self.order = []

        for rule in rules.split(","):
            temp = rule.split(":")
            if len(temp) > 1:
                compare, goto = temp
                if ">" in compare:
                    var, val = compare.split(">")
                    rule = Rule(var, greaterThan, val, goto)
                    # self.rules[var] = {
                    #     "func": greaterThan,
                    #     "val": int(val),
                    #     "goto": goto,
                    # }
                    self.rules.append(rule)
                elif "<" in compare:
                    var, val = compare.split("<")
                    # if var in self.rules:
                    #     continue
                    # self.rules[var] = {"func": lessThan, "val": int(val), "goto": goto}
                    rule = Rule(var, lessThan, val, goto)
                    self.rules.append(rule)

            else:
                self.default = rule

    def __contains__(self, item):
        return item in self.rules

    def __getitem__(self, key):
        return self.rules[key]

    def __str__(self):
        return f"{self.name}: {self.rules}. default: {self.default}"

    def __repr__(self):
        return self.__str__()


def parse():
    rules, parts = DATA.split("\n\n")

    ruleSets = {}
    for line in rules.split("\n"):
        rule = RuleSet(line)
        ruleSets[rule.name] = rule

    partList = []
    for line in parts.split("\n"):
        part = {}
        for string in line.strip("{}").split(","):
            val, rating = string.split("=")
            part[val] = int(rating)

        partList.append(part)

    return ruleSets, partList


def evalParts(ruleSets, partsList):
    accepted = []
    rejected = []

    for part in partsList:
        ruleName = "in"
        while ruleName not in "AR":
            # print(f"{ruleName} -> ", end="")
            ruleSet = ruleSets[ruleName]

            ruleName = ruleSet.default
            for rule in ruleSet.rules:
                rating = part[rule.var]

                a = rating
                b = rule.val
                if rule.func(a, b):
                    ruleName = rule.next
                    break

        # print(ruleName)
        # print()
        if ruleName == "A":
            accepted.append(part)
        else:
            rejected.append(part)

    return accepted, rejected


def addAccepted(accepted):
    total = 0
    for part in accepted:
        for k, v in part.items():
            total += v
    return total


def distinctCombinationsBrute(ruleSets):
    partsList = []
    for x in range(1, 4001):
        for m in range(1, 4001):
            for a in range(1, 4001):
                for s in range(1, 4001):
                    part = {"x": x, "m": m, "a": a, "s": s}
                    partsList.append(part)
        print(x)
    accepted, rejected = evalParts(ruleSets)

    return len(accepted)


def findAcceptedRuleSets(ruleSets):
    rulesThatAccept = []
    for ruleName, ruleSet in ruleSets.items():
        if ruleSet.default == "A":
            rulesThatAccept.append(ruleSet)
            continue

        for rule in ruleSet.rules:
            if rule.next == "A":
                rulesThatAccept.append(ruleSet)
                continue

    for rs in rulesThatAccept:
        if rs.default == "A":
            # go backwards to "in" excluding rules
            pass

        for r in rs.rules:
            if r.next == "A":
                # go backwards to "in"
                print(f"{r.var}: (1, 4000)", end="")
            elif r.next == "A":
                if r.func == greaterThan:
                    print(f"{r.var}: ({r.val}, 4000)", end="")
                else:
                    print(f"{r.var}: (1, {r.val})", end="")
            elif rs.default == "A":
                for i in "xmas":
                    if i != r.var:
                        print(f"{i}: (1, 4000)", end="")
        print()
        print()
        # print(rs)


def part1():
    print("Part 1")
    ruleSets, parts = parse()

    accepted, rejected = evalParts(ruleSets, parts)

    print(accepted)
    # print(rejected)

    totalAccepted = addAccepted(accepted)

    print(f"Total accepted ratings is {totalAccepted}")
    # with break:            275390
    # without break:         377859 too low
    # with break and order:  398985 too low


def part2():
    print()
    print("Part 2")

    ruleSets, parts = parse()

    findAcceptedRuleSets(ruleSets)

    # distinctCombinations = distinctCombinationsBrute(ruleSets)

    print(f"The number of distinct combinations is {0}")


def main():
    part1()
    part2()


main()
