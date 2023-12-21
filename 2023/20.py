from pathlib import Path
from loadFile import read_file
import math

PATH = Path(__file__)
DATA = read_file(f"./2023/{PATH.name.split('.')[0]}.txt")


class Module:
    def __init__(self, prefix, name):
        self.prefix = prefix
        self.name = name
        self.receiverModules = []
        self.parentModules = []

    def addReceiverModule(self, module):
        self.receiverModules.append(module)
        module.addParentModule(self)

    def addParentModule(self, module):
        self.parentModules.append(module)

    def receivePulse(self, callerModule, pulseType):
        # do nothing
        # print(f"{callerModule.name} -{pulseType}-> {self.name}")
        return []

    def graphVizStr(self):
        return f"{self.name} -> {', '.join([m.name for m in self.receiverModules])}\n"

    def __str__(self):
        return f"{self.prefix}{self.name} -> {', '.join([m.prefix + m.name for m in self.receiverModules])}"

    def __repr__(self):
        return self.__str__()


class FlipFlopModule(Module):
    def __init__(self, prefix, name):
        super().__init__(prefix, name)
        self.isOn = False

    def receivePulse(self, callerModule, pulseType):
        # print(f"{callerModule.name} -{pulseType}-> {self.name}")
        if pulseType == "high":
            return []

        if pulseType == "low":
            if not self.isOn:
                self.isOn = not self.isOn
                return [(m, self, "high") for m in self.receiverModules]
            else:
                self.isOn = not self.isOn
                return [(m, self, "low") for m in self.receiverModules]

    # def graphVizStr(self):
    #     return f"[label=\"{self.prefix}{self.name}\"]{self.name} -> {', '.join([m.prefix + m.name for m in self.receiverModules])}\n"


class ConjunctionModule(Module):
    def __init__(self, prefix, name):
        super().__init__(prefix, name)
        self.lastPulses = {}

    def initInitialPulses(self):
        for m in self.parentModules:
            self.lastPulses[m.name] = "low"

    def lastPulsesAllHigh(self):
        for _, v in self.lastPulses.items():
            if v == "low":
                return False
        return True

    def receivePulse(self, callerModule, pulseType):
        # print(f"{callerModule.name} -{pulseType}-> {self.name}")
        # if self.name == "zh" and pulseType == "high":
        #     print(f"{callerModule.name} -{pulseType}-> {self.name}")

        self.lastPulses[callerModule.name] = pulseType

        if self.lastPulsesAllHigh():  # TODO: This will need to be fixed I think
            return [(m, self, "low") for m in self.receiverModules]
        else:
            return [(m, self, "high") for m in self.receiverModules]


class BroadcasterModule(Module):
    def __init__(self, name):
        super().__init__("", name)
        self.queue = []
        self.findPulse = None

    def receivePulse(self, callerModule, pulseType, pulsesSent, bc=None):
        # string = f"{callerModule.name} -{pulseType}-> {self.name}\n"
        # print(f"{callerModule.name} -{pulseType}-> {self.name}")
        for mod in self.receiverModules:
            self.queue.append((mod, self, pulseType))

        lstOfLcms = []

        while self.queue:
            mod, caller, pt = self.queue.pop(0)
            # string += f"{caller.name} -{pulseType}-> {mod.name}\n"
            # if (pt, mod.name) == self.findPulse:
            #     return True
            if bc is not None and pt == "high" and mod.name == "zh":
                print(mod, bc)
                lstOfLcms.append(bc)
            self.queue += mod.receivePulse(caller, pt)
            if pt == "low":
                pulsesSent[0] += 1
            elif pt == "high":
                pulsesSent[1] += 1
        # return string
        return lstOfLcms


class ButtonModule:
    def __init__(self, broadcastModule):
        self.name = "button"
        self.broadcastModule = broadcastModule

    def clickButton(self, bc=None):
        pulsesSent = [1, 0]
        string = self.broadcastModule.receivePulse(self, "low", pulsesSent, bc)
        return pulsesSent, string


def parse():
    allModules = {}
    childModulesList = []
    for line in DATA.split("\n"):
        mod, rMods = line.split(" -> ")
        rModsLst = rMods.split(", ")
        if mod == "broadcaster":
            newMod = BroadcasterModule(mod)
        else:
            prefix, name = mod[0], mod[1:]
            if prefix == "%":
                newMod = FlipFlopModule(prefix, name)
            else:
                newMod = ConjunctionModule(prefix, name)
        allModules[newMod.name] = newMod

        childModulesList.append((newMod, rModsLst))

    for mod, rModNamesLst in childModulesList:
        for mName in rModNamesLst:
            if mName not in allModules:
                baseModule = Module("", mName)
                allModules[baseModule.name] = baseModule
            mod.addReceiverModule(allModules[mName])

        # print(mod)
    for _, mod in allModules.items():
        if type(mod) == ConjunctionModule:
            mod.initInitialPulses()

    return allModules


def generateGraphText(allModules):
    f = open(f"./2023/{PATH.name.split('.')[0]}.dot", "w")
    # f.write() here
    f.write("digraph {\n")

    for k, v in allModules.items():
        if v.receiverModules:
            f.write(v.graphVizStr())

    f.write("}")
    f.close()


def part1():
    print("Part 1")
    allModules = parse()

    broadcaster = allModules["broadcaster"]
    button = ButtonModule(broadcaster)

    lowPulses, highPulses = 0, 0
    s = set()
    d = dict()
    for _ in range(1000):
        pulsesSent, _ = button.clickButton()
        tup = tuple(pulsesSent)
        if tup in d:
            d[tup] += 1
        else:
            d[tup] = 1
        s.add(tup)
        # print(pulsesSent)
        # print()
        lowPulses += pulsesSent[0]
        highPulses += pulsesSent[1]
    print(
        f"{lowPulses} low pulses and {highPulses} high pulses were sent. Multiplying them together gives {lowPulses*highPulses}"
    )
    print(s)
    print(d)


def part2():
    print()
    print("Part 2")

    allModules = parse()

    broadcaster = allModules["broadcaster"]
    broadcaster.findPulse = ("low", "rx")
    button = ButtonModule(broadcaster)

    # generateGraphText(allModules)

    # found = False
    # count = 0
    # while not found:
    #     pulsesSent, string = button.clickButton()
    #     count += 1

    # d = {}
    lst = []
    for bc in range(1, 5001):
        pulsesSent, l = button.clickButton(bc)
        if l:
            lst += l

    print(lst)

    print(math.lcm(*lst))

    # for k, v in findCycles.items():
    #     v.append(allModules[k].lastPulsesAllHigh())

    # print(findCycles)
    # for k, v in findCycles.items():
    #     # print(k, v)
    #     # try:
    #     first = v.index(True)
    #     last = v.index(True, first + 1)

    #     # except:
    #     #     continue

    #     print(k, first, last)

    # tup = tuple(pulsesSent)
    # if string in d:
    #     d[string] += 1
    # else:
    #     d[string] = 1

    # print(len(d))

    # print(f"Got low pulse to rx after {count} button clicks")


def main():
    part1()
    part2()


main()
