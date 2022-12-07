import numpy as np
from enum import Enum
import re

player = 1
player1Deck = []
player2Deck = []

allCards = set()
isUnique = True

# 0 = ., 1 = #
with open("day22.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if line == "Player 2:":
            player = 2
        elif line.isnumeric():
            value = int(line)
            if value in allCards:
                isUnique = False
            else:
                allCards.add(value)
            if player == 1:
                player1Deck.append(value)
            else:
                player2Deck.append(value)

print("Distinct values: ", isUnique)
print("0 card exists: ", 0 in allCards)
print(player1Deck)
print(player2Deck)

def winnerPt1(p1, p2):
    return 1 if p1 > p2 else 2

##while len(player1Deck) > 0 and len(player2Deck) > 0:
##    p1 = player1Deck.pop(0)
##    p2 = player2Deck.pop(0)
##    if winnerPt1(p1, p2) == 1:
##        player1Deck += [p1, p2]
##    else:
##        player2Deck += [p2, p1]
##
##print(player1Deck)
##print(player2Deck)
##
##winningDeck = player1Deck if len(player1Deck) > 0 else player2Deck

def score(deck):
    result = 0
    for i in range(len(deck)):
        result += (1 + i)*deck[len(deck) - 1 - i]
    return result

## print(score(winningDeck)) # 32272

# strings of "a,b,c,d-e,f,g" for p1/p2

def getConfigString(deck1, deck2):
    return ",".join(str(x) for x in deck1) + "-" + ",".join(str(x) for x in deck2)

class WinnerException(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value

def roundWinner(deck1, deck2):
    configurations = set()
    while len(deck1) > 0 and len(deck2) > 0:        
        config = getConfigString(deck1, deck2)
        if config in configurations:
            return 1
        configurations.add(config)

        card1 = deck1.pop(0)
        card2 = deck2.pop(0)

        if card1 > len(deck1) or card2 > len(deck2):
            winner = winnerPt1(card1, card2)
        else:
            copy1 = deck1[:card1]
            copy2 = deck2[:card2]
            winner = roundWinner(copy1, copy2)
        if winner == 1:
            deck1 += [card1, card2]
        else:
            deck2 += [card2, card1]
    return 1 if len(deck1) > 0 else 2

def play(deck1, deck2):
    configurations = set()
    while len(deck1) > 0 and len(deck2) > 0:
        config = getConfigString(deck1, deck2)
        if config in configurations:
            return score(deck1)
        configurations.add(config)

        card1 = deck1.pop(0)
        card2 = deck2.pop(0)

        if card1 > len(deck1) or card2 > len(deck2):
            winner = winnerPt1(card1, card2)
        else:
            copy1 = deck1[:card1]
            copy2 = deck2[:card2]
            winner = roundWinner(copy1, copy2)
        if winner == 1:
            deck1 += [card1, card2]
        else:
            deck2 += [card2, card1]
    return score(deck1) if len(deck1) > 0 else score(deck2)


print(play(player1Deck, player2Deck)) # 33206






