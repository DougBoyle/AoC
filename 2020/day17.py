import numpy as np
from enum import Enum

class State(Enum):
    DEAD = 0
    ALIVE = 1

def parseState(s):
    if s == ".":
        return State.DEAD
    elif s == "#":
        return State.ALIVE
    else:
        raise Exception("Unknown state " + s)


with open("day17.txt", "r") as f:
    data = np.array(
        [[parseState(s) for s in line.strip()] for line in f.readlines()]
    )

cycles = 6

paddedData = np.empty((data.shape[0] + 2*cycles,
                       data.shape[1] + 2*cycles,
                       1 + 2*cycles,
                       1 + 2*cycles), dtype=object)
paddedData.fill(State.DEAD)

paddedData[cycles:cycles + data.shape[0],
           cycles:cycles + data.shape[1],
           cycles,
           cycles] = data


def getNeighbours(x, y, z, w):
    for i in range(max(0, x-1), min(paddedData.shape[0], x+2)):
        for j in range(max(0, y-1), min(paddedData.shape[1], y+2)):
            for k in range(max(0, z-1), min(paddedData.shape[2], z+2)):
                for l in range(max(0, w-1), min(paddedData.shape[3], w+2)):
                    if i != x or j != y or k != z or l != w:
                        yield paddedData[i, j, k, l]

def countAliveNeighbours(x, y, z, w):
    aliveNeighbours = 0
    for neighbour in getNeighbours(x, y, z, w):
        if neighbour == State.ALIVE:
            aliveNeighbours += 1
    return aliveNeighbours

for _ in range(cycles):
    newData = np.copy(paddedData)
    for x in range(paddedData.shape[0]):
        for y in range(paddedData.shape[1]):
            for z in range(paddedData.shape[2]):
                for w in range(paddedData.shape[3]):
                    aliveNeighbours = countAliveNeighbours(x, y, z, w)
                    match paddedData[x, y, z, w]:
                        case State.ALIVE:
                            if aliveNeighbours < 2 or aliveNeighbours > 3:
                                newData[x, y, z, w] = State.DEAD
                        case State.DEAD:
                            if aliveNeighbours == 3:
                                newData[x, y, z, w] = State.ALIVE
    paddedData = newData
    print("iteration")

print(np.sum(paddedData == State.ALIVE))
                



