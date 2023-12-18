from helpers.loadFile import read_file
import math

INSTRUCTIONS = read_file("./2023/8Instructions.txt")
MAP = read_file("./2023/8Map.txt")


def create_map(map):
    map_dict = {}
    map = map.split("\n")
    for entry in map:
        if not entry:
            continue
        key, value = entry.split(" = ")
        l, r = value.split(", ")
        l = l[1:]
        r = r[:-1]
        # print(key, l, r)

        map_dict[key] = {"L": l, "R": r}
    # print(map_dict)

    return map_dict


# # PART2_INSTRUCTIONS = "LR"
# PART2_INSTRUCTIONS = INSTRUCTIONS
# PART2_MAP = """11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)"""

# # part2_map = create_map(map=PART2_MAP)
# part2_map = map_dict


def get_starting_nodes(map):
    starting_nodes = []

    for k in map.keys():
        if k[-1] == "A":
            starting_nodes.append(k)

    return starting_nodes


def get_all_next_nodes(current_list, map, instruction):
    next_nodes = []
    for current in current_list:
        next = map[current][instruction]
        next_nodes.append(next)

    return next_nodes


def all_nodes_end_with_Z(nodes):
    lst = []
    for node in nodes:
        # print(node, node[-1])
        if node[-1] == "Z":
            lst.append(1)
        else:
            lst.append(0)
    return lst


def part1():
    current = "AAA"
    END = "ZZZ"

    map_dict = create_map(map=MAP)

    step = 0
    while True:
        instruction = INSTRUCTIONS[step % len(INSTRUCTIONS)]
        step += 1

        next = map_dict[current][instruction]
        # print(next)

        if next == END:
            break

        current = next

    print(f"It took {step} steps to reach ZZZ")


def part2():
    part2_map = create_map(map=MAP)
    current_list = get_starting_nodes(part2_map)

    # print(current_list)

    # step = 0
    # while True:
    #     instruction = INSTRUCTIONS[step % len(INSTRUCTIONS)]
    #     step += 1

    #     next_nodes = get_all_next_nodes(
    #         current_list=current_list, map=part2_map, instruction=instruction
    #     )
    #     # print(next_nodes, instruction)
    #     # print(instruction, next_nodes)
    #     # if step % 10000000 == 0:
    #     #     print(next_nodes, step)

    #     nodes_end_with_Z = all_nodes_end_with_Z(next_nodes)
    #     # print(nodes_end_with_Z)
    #     sum_nodes = sum(nodes_end_with_Z)
    #     if sum_nodes > 3 or step % 100000000 == 0:
    #         print(sum_nodes, next_nodes, step)

    #     if sum_nodes == len(nodes_end_with_Z):
    #         break

    #     current_list = next_nodes

    #     # if step > 10:
    #     #     break

    stepsList = []
    for node in current_list:
        step = 0
        currentNode = node

        while True:
            instruction = INSTRUCTIONS[step % len(INSTRUCTIONS)]
            step += 1

            nextNode = part2_map[currentNode][instruction]

            if nextNode.endswith("Z"):
                stepsList.append(step)
                break

            currentNode = nextNode

    lcm = math.lcm(*stepsList)

    print(stepsList)
    print(f"It took {lcm} steps to for all starting nodes to reach Z")


def main():
    part1()

    part2()


main()
