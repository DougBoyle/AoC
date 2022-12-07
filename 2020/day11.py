from enum import Enum
import numpy as np

class Space(Enum):
    EMPTY = 1
    OCCUPIED = 2
    FLOOR = 3

    @staticmethod
    def parse(s):
        match s:
            case "#":
                return Space.OCCUPIED
            case "L":
                return Space.EMPTY
            case ".":
                return Space.FLOOR
            case _:
                raise "Space " + s + " not recognised"

with open("day11.txt", "r") as f:
    data = np.array(
        [[Space.parse(s) for s in line.strip()] for line in f.readlines()]
    )

def occupied(seats, i, j):
    if i < 0 or j < 0 or i >= seats.shape[0] or j >= seats.shape[1]:
        return False
    else:
        return seats[i,j] == Space.OCCUPIED

def getOccupiedNeighbours(seats, i, j):
    tot = 0
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            if (i != x or j != y) and occupied(seats, x, y):
                tot += 1
    return tot

def getNextSeat(seats, i, j):
    match seats[i, j]:
        case Space.EMPTY:
            if getOccupiedNeighbours(seats, i, j) == 0:
                return Space.OCCUPIED
        case Space.OCCUPIED:
            if getOccupiedNeighbours(seats, i, j) >= 4:
                return Space.EMPTY
    return seats[i, j]

#### Part 2 #####

def isFloor(seats, i, j):
    if i < 0 or j < 0 or i >= seats.shape[0] or j >= seats.shape[1]:
        return False
    else:
        return seats[i,j] == Space.FLOOR

def getBeanOccupiedNeighbours(seats, i, j):
    tot = 0
    for xDir in range(-1, 2):
        for yDir in range(-1, 2):
            if xDir == 0 and yDir == 0:
                continue
            x = i + xDir
            y = j + yDir
            while isFloor(seats, x, y):
                x += xDir
                y += yDir
            if occupied(seats, x, y):
                tot += 1
    return tot

def getNextSeat2(seats, i, j):
    match seats[i, j]:
        case Space.EMPTY:
            if getBeanOccupiedNeighbours(seats, i, j) == 0:
                return Space.OCCUPIED
        case Space.OCCUPIED:
            if getBeanOccupiedNeighbours(seats, i, j) >= 5:
                return Space.EMPTY
    return seats[i, j]

seats = data
changing = True
while changing:
    changing = False
    newSeats = seats.copy()
    for i in range(len(newSeats)):
        for j in range(len(newSeats[i])):
            # newSeat = getNextSeat(seats, i, j)
            newSeat = getNextSeat2(seats, i, j)
            if newSeat != seats[i, j]:
                changing = True
                newSeats[i, j] = newSeat
    seats = newSeats

print((seats == Space.OCCUPIED).sum())




                        




