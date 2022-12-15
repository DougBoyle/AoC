import numpy as np
from enum import Enum
import re
import time

trees = []

with open("day8.txt") as f:
    trees = np.array([[int(n) for n in line.strip()]
             for line in f.readlines()])

width = len(trees[0])
height = len(trees)
assert(width == height)


# i = 1 to max, j = 0 to max -> x, y coordinates
def getFromTop(i, j):
    return j, i
def getFromBottom(i, j):
    return j, height - i - 1
def getFromLeft(i, j):
    return i, j
def getFromRight(i, j):
    return width - i - 1, j

class Direction(Enum):
    N = (0, -1) # inverted, smaller index is 'higher'
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)
    
    def move(self, x, y):
        return x + self.value[0], y + self.value[1]

    def moveYX(self, y, x):
        return y + self.value[1], x + self.value[0]

    def movesYX(self, y, x, n):
        return y + self.value[1]*n, x + self.value[0]*n
    
    def index(self):
        if self == Direction.N:
            return 0
        elif self == Direction.S:
            return 1
        elif self == Direction.W:
            return 2
        elif self == Direction.E:
            return 3

    def sweepAway(self, i, j):
        if self == Direction.N:
            return getFromTop(i, j)
        elif self == Direction.S:
            return getFromBottom(i, j)
        elif self == Direction.W:
            return getFromLeft(i, j)
        elif self == Direction.E:
            return getFromRight(i, j)

    def atEndYX(self, coords):
        y, x = coords
        if self == Direction.N:
            return y == 0
        elif self == Direction.S:
            return y == height - 1
        elif self == Direction.W:
            return x == 0
        elif self == Direction.E:
            return x == width - 1

    def getLeadingEdge(self, i):
        return self.sweepAway(0, i)
        


visible = np.array([[False for _ in row] for row in trees])
# tallest tree going up/down/left/right of each position,
# actual height at edges (going in any direction)
# 0 = y-1, 1 = y+1, 2 = x-1, 3 = x+1
greatest = np.array([[[None for _ in row] for row in trees] for _ in Direction])

for i in range(width): # No trees outside border, fill in with -1 height
    for direction in Direction:
        x, y = direction.getLeadingEdge(i)
        greatest[direction.index(),y,x] = -1

for i in range(1, height):
    for j in range(width):
        for direction in Direction:
            x, y = direction.sweepAway(i, j)
            greatest[direction.index()][y][x] = max(
                    trees[direction.moveYX(y, x)],
                    greatest[direction.index()][direction.moveYX(y, x)]
                )

visible = np.min(greatest, axis=0) < trees

print(sum(sum(r) for r in visible))  # 1708


# Part 2. viewing distance for each tree in each direction
# i.e. number of trees up to and including first one same or greater height
# 1) Build working inwards from each direction, want to avoid full scan each time
# 2) From height of fist tree, result either 1,
#    or can skip ahead by viewing distance of that shorter tree.
# 3) In case where all same height e.g. 211111111111...
#    Also track firstHigherTree[dir][x][y] = distance to first tree higher than this (0 at borders)
#    = 1 if shorter than neighbour, else recursively get by following growing chain of neighbours.
#      Still recursive, but guaranteed to take max 10 hops. Only slightly different to 'greatest' above.
#
#
# 3b) Alternative would be to track last tree seen of each height.
#     Trade of speed (1 lookup) vs memory (10 entries).
#     Both poor if number of different heights very large,
#     could then e.g. store 2D binary tree of regions, with largest tree in each region, and binary search.
#

# count number of steps to the first tree higher than this one, or trees from here to edge if none
firstHigherTree = np.array([[[None for _ in row] for row in trees] for _ in Direction])
visibility = np.array([[[None for _ in row] for row in trees] for _ in Direction])

for i in range(width):
    for direction in Direction:
        x, y = direction.getLeadingEdge(i)
        firstHigherTree[direction.index(),y,x] = 0
        visibility[direction.index(),y,x] = 0


for i in range(1,height):
    for j in range(0,width):
        for direction in [Direction.N, Direction.W, Direction.S, Direction.E]:
            x,y = direction.sweepAway(i, j)
            offset = 1
            pos = direction.movesYX(y, x, offset)
            treeHeight = trees[y][x]
            nextHeight = trees[pos]

            while not direction.atEndYX(pos) and trees[pos] < treeHeight: # not at last tree yet
                offset += firstHigherTree[direction.index()][pos]
                pos = direction.movesYX(y, x, offset)

            visibility[direction.index()][y][x] = offset
            if trees[pos] == treeHeight:
                firstHigherTree[direction.index()][y][x] = offset + firstHigherTree[direction.index()][pos]
            else:
                firstHigherTree[direction.index()][y][x] = offset

visProducts = np.prod(visibility, axis=0)
print(np.max(visProducts)) # 504000







