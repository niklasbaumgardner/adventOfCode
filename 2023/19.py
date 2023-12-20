from pathlib import Path
from loadFile import read_file
from copy import deepcopy

PATH = Path(__file__)
DATA = read_file(f"./2023/{PATH.name.split('.')[0]}.txt")

POSSIBLES = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}


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

    toCheck = []
    toCheck.append(("in", deepcopy(POSSIBLES)))
    while toCheck:
        ruleName, possibles = toCheck.pop(0)

        ruleSet = ruleSets[ruleName]

        newPossiblesList = []
        for i in range(len(ruleSet.rules) + 1):
            newPossiblesList.append(deepcopy(possibles))
        # print(
        #     newPossiblesList, len(newPossiblesList), ruleSet.rules, len(ruleSet.rules)
        # )
        for i, rule in enumerate(ruleSet.rules):
            newPossibles = newPossiblesList[i]
            if rule.func == greaterThan:
                newPossibles[rule.var][0] = rule.val + 1
            else:
                newPossibles[rule.var][1] = rule.val - 1
            for j in range(i + 1, len(newPossiblesList)):
                if rule.func == lessThan:
                    newPossiblesList[j][rule.var][0] = rule.val
                else:
                    newPossiblesList[j][rule.var][1] = rule.val

            if rule.next == "A":
                rulesThatAccept.append(newPossiblesList[i])
            elif rule.next != "R":
                toCheck.append((rule.next, newPossiblesList[i]))

        if ruleSet.default == "A":
            rulesThatAccept.append(newPossiblesList[-1])
        elif ruleSet.default != "R":
            toCheck.append((ruleSet.default, newPossiblesList[-1]))

    for r in rulesThatAccept:
        print(r)

    total = 0
    for i in range(len(rulesThatAccept)):
        temp = 1
        temp *= 1 + rulesThatAccept[i]["x"][1] - rulesThatAccept[i]["x"][0]
        temp *= 1 + rulesThatAccept[i]["m"][1] - rulesThatAccept[i]["m"][0]
        temp *= 1 + rulesThatAccept[i]["a"][1] - rulesThatAccept[i]["a"][0]
        temp *= 1 + rulesThatAccept[i]["s"][1] - rulesThatAccept[i]["s"][0]

        total += temp

    print(total)
    print(167409079868000)
    print(total - 167409079868000)

    print()
    return total


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

    total = findAcceptedRuleSets(ruleSets)

    # distinctCombinations = distinctCombinationsBrute(ruleSets)

    print(f"The number of distinct combinations is {total}")


def main():
    part1()
    part2()


main()
