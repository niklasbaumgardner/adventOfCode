from loadFile import read_file
from functools import cmp_to_key

CARD_RANKS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}

CRAZY_CARD_RANKS = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 1,
    "Q": 12,
    "K": 13,
    "A": 14,
}

HANDS_STRING = read_file("./2023/7.txt")


class Card:
    def __init__(self, cardVal):
        self.card = cardVal
        self.rank = CARD_RANKS[self.card]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.rank == other.rank
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.rank > other.rank

    def __lt__(self, other):
        return not self.__gt__(other)

    def __str__(self):
        return self.card

    def __repr__(self):
        return str(self)


class CrazyCard(Card):
    def __init__(self, cardVal):
        self.card = cardVal
        self.rank = CRAZY_CARD_RANKS[self.card]


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.createHand()
        self.bid = bid

    def __eq__(self, other):
        return self.cards == other.cards

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if self == other:
            return False

        # print(self, other)
        # print(self.getHandValue(), other.getHandValue())

        if self.getHandValue() > other.getHandValue():
            return True

        if self.getHandValue() < other.getHandValue():
            return False

        for i in range(len(self.cards)):
            if self.cards[i] == other.cards[i]:
                continue
            # print(self.cards[i] > other.cards[i], self.cards[i], other.cards[i])
            if self.cards[i] > other.cards[i]:
                return True
            if self.cards[i] < other.cards[i]:
                return False

    def __lt__(self, other):
        return not self.__gt__(other)

    def __sub__(self, other):
        if self == other:
            return 0
        elif self.__gt__(other):
            return 1

        return -1

    def __str__(self):
        return f"Cards: {self.cards} Bid: {self.bid}"

    def __repr__(self):
        return str(self)

    def createHand(self):
        self.handMap = {}
        for c in self.cards:
            if c.card in self.handMap:
                self.handMap[c.card] += 1
            else:
                self.handMap[c.card] = 1

        self.hand = []
        for k, v in self.handMap.items():
            self.hand.append([k, v])
        self.hand.sort(reverse=True, key=lambda x: x[1])

    def getHandValue(self):
        if len(self.hand) == 1:  # five of a kind
            return 6
        elif len(self.hand) == 2 and self.hand[0][1] == 4:  # four of a kind
            return 5
        elif len(self.hand) == 2 and self.hand[0][1] == 3:  # full house
            return 4
        elif len(self.hand) == 3 and self.hand[0][1] == 3:  # three of a kind
            return 3
        elif len(self.hand) == 3 and self.hand[0][1] == 2:  # two pair
            return 2
        elif len(self.hand) == 4 and self.hand[0][1] == 2:  # one pair
            return 1
        return 0  # high card


class CrazyHand(Hand):
    def getHandValue(self):
        if "J" not in self.handMap:
            return super().getHandValue()

        bestHand = self.makeBestHand()
        # print(f"hand: {self}. current {super().getHandValue()}. best {bestHand}")
        return bestHand

    def makeBestHand(self):
        # string = "".join([c.card for c in self.cards])
        currentHandVal = super().getHandValue()

        if len(self.hand) <= 2:
            return 6

        if len(self.hand) == 3:
            if currentHandVal == 3:  # three of a kind
                return 5
            if currentHandVal == 2:  # two pair
                print(self, self.handMap["J"])
                if self.handMap["J"] == 2:
                    return 5
                return 4

        if len(self.hand) == 4:
            return 3

        return 1


def createHands(string):
    hands = []
    for line in string.split("\n"):
        s, bid = line.split()
        cards = [Card(ch) for ch in s]
        bid = int(bid)
        hand = Hand(cards, bid)
        hands.append(hand)
    return hands


def createCrazyHandFromString(s):
    hand, bid = s.split()
    cards = [CrazyCard(ch) for ch in hand]
    bid = int(bid)
    hand = CrazyHand(cards, bid)
    return hand


def createCrazyHands(string):
    hands = []
    for line in string.split("\n"):
        hand = createCrazyHandFromString(line)
        hands.append(hand)
    return hands


def part1():
    hands = createHands(HANDS_STRING)
    # for hand in hands:
    #     print(hand)
    # print()
    hands.sort(key=cmp_to_key(lambda a, b: a - b))
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1) * hand.bid
        # print(hand)
    print(f"Total winnings are {total}")


def part2():
    hands = createCrazyHands(HANDS_STRING)
    # for hand in hands:
    #     print(hand)
    # print()
    hands.sort(key=cmp_to_key(lambda a, b: a - b))
    total = 0
    for i, hand in enumerate(hands):
        total += (i + 1) * hand.bid
        # print(hand)
    print(f"Total winnings are {total}")
    # 245576185


def main():
    part1()

    part2()


main()
