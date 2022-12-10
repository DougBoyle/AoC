import numpy as np
from enum import Enum
import re
import time

def getRPS(s):
    match s:
        case "A":
            return "R"
        case "X":
            return "R"
        case "B":
            return "P"
        case "Y":
            return "P"
        case "C":
            return "S"
        case "Z":
            return "S"

def getMyRPS(theirs, mine):
    if mine == "Y":
        return theirs
    elif mine == "X":
        match theirs:
            case "R":
                return "S"
            case "P":
                return "R"
            case "S":
                return "P"
    else:
        match theirs:
            case "R":
                return "P"
            case "P":
                return "S"
            case "S":
                return "R"

def score(mine, theirs):
    total = 0
    if mine == theirs:
        total += 3
    match mine:
        case "R":
            total += 1
            if theirs == "S":
                total += 6
        case "P":
            total += 2
            if theirs == "R":
                total += 6
        case "S":
            total += 3
            if theirs == "P":
                total += 6
    return total

def scoreLine(line):
    split = line.split(" ")
    # Part 2
    theirs = getRPS(split[0])
    mine = getMyRPS(theirs, split[1])
    return score(mine, theirs)
# part 1.
#    return score(getRPS(split[1]), getRPS(split[0]))

total = 0
with open("day2.txt") as f:
    for line in f.readlines():
        total += scoreLine(line.strip())

print(total)

