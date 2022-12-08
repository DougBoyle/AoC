import numpy as np
from enum import Enum
import re
import time

# Representing an infinite hex grid centered around (0,0)
#
#     (0, 1)  (1, 1)
#
#  (-1, 0) (0, 0) (1, 0)
#
#     (-1, -1) (0, -1)
#
# NE = (1, 1), E = (1, 0), SE = (0, -1)
# SW = (-1, -1), W = (-1, 0), NW = (0, 1) 
#
# N/S is +/- 1 to y coordinate, then use NW/SE direction as x axis
#

# (x, y) -> 0 = white, 1 = black
grid = {}

class Direction(Enum):
    NE = (1, 1)
    E = (1, 0)
    SE = (0, -1)
    SW = (-1, -1)
    W = (-1, 0)
    NW = (0, 1)

def step(coords, direction):
    return coords[0] + direction.value[0], coords[1] + direction.value[1]

with open("day24.txt") as f:
    for line in f.readlines():
        line = line.strip()
        x, y = 0, 0
        i = 0
        while i < len(line):
            match line[i]:
                case 'e':
                    direction = Direction.E
                case 'w':
                    direction = Direction.W
                case 's':
                    i += 1
                    if line[i] == 'e':
                        direction = Direction.SE
                    else:
                        direction = Direction.SW
                case 'n':
                    i += 1
                    if line[i] == 'e':
                        direction = Direction.NE
                    else:
                        direction = Direction.NW
            x, y = step((x, y), direction)
            i += 1
        if (x, y) not in grid:
            grid[(x, y)] = 0
        grid[(x, y)] = 1 - grid[(x, y)]

print(sum(grid.values()))

# ensure a border of white tiles around all black tiles at any point
def fillNeighbours(x, y):
    if grid[(x, y)] == 0: # avoid expanding unnecessarily for white tiles
        return
    for direction in Direction:
        neighbour = step((x, y), direction)
        if neighbour not in grid:
            grid[neighbour] = 0

def nextState(x, y):
    tot = 0
    for direction in Direction:
        neighbour = step((x, y), direction)
        if neighbour in grid:
            tot += grid[neighbour]
    if grid[(x, y)] == 1:
        return 0 if tot == 0 or tot > 2 else 1
    else:
        return 1 if tot == 2 else 0

start = time.time()

for i in range(100):
    for (x, y) in list(grid.keys()):
        fillNeighbours(x, y)
    newGrid = {}
    for (x, y) in grid:
        newGrid[(x, y)] = nextState(x, y)
    grid = newGrid

# By not expanding white tiles further: 3.2s
# If always expanding: 7.6s for only 80 out of 100 iterations
# removing white tiles with no neighbouring black tiles: Still 3.2s
print("----- took %fs ------" % (time.time() - start))

print(sum(grid.values())) # 3876

