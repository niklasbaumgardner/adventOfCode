from loadFile import read_file
import re
import math

GAME_TEXT = read_file("./2023/2.txt")
# print(GAME_TEXT)

MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14


def gameTextToDict():
    gameMap = {}
    for line in GAME_TEXT.split("\n"):
        game, gameSets = line.split(": ")

        gameNum = re.search(r"Game (\d+)", game).group(1)

        gamePulls = gameSets.split("; ")

        gameSetsListMap = []
        for pull in gamePulls:
            numRedMatch = re.search(r"(\d+) red", pull)
            numGreenMatch = re.search(r"(\d+) green", pull)
            numBlueMatch = re.search(r"(\d+) blue", pull)

            gameSetsListMap.append(
                [
                    int(numRedMatch.group(1)) if numRedMatch else 0,
                    int(numGreenMatch.group(1)) if numGreenMatch else 0,
                    int(numBlueMatch.group(1)) if numBlueMatch else 0,
                ]
            )

        gameMap[int(gameNum)] = gameSetsListMap

    return gameMap


GAME_MAP = gameTextToDict()
# for k, v in GAME_MAP.items():
#     print(k, v)


def part1():
    total = 0
    for gameNum, gamePullList in GAME_MAP.items():
        gamePossible = True
        for pull in gamePullList:
            r, g, b = pull

            if r > MAX_RED or g > MAX_GREEN or b > MAX_BLUE:
                gamePossible = False
                print(f"game {gameNum} is impossible. {pull}")
                break

        if gamePossible:
            total += gameNum

    print(f"total of game numbers possible is {total}")


def part2():
    total = 0

    for _, gamePullList in GAME_MAP.items():
        minRed = 0
        minGreen = 0
        minBlue = 0

        for pull in gamePullList:
            r, g, b = pull

            minRed = max(minRed, r)
            minGreen = max(minGreen, g)
            minBlue = max(minBlue, b)

        power = minRed * minGreen * minBlue
        print(
            f"minRed: ${minRed}, minGreen: {minGreen}, minBlue: {minBlue}, power: {power}"
        )
        total += power

    print(f"the sum of powers from each game is {total}")


def main():
    part1()
    part2()


main()
