import numpy as np
from enum import Enum
import re
import time


#  each column is '[X] ', or at end '[X]\n', so length = 4*columns

stacks = None
PATTERN = "move (\d+) from (\d+) to (\d+)"

def part1Move(stacks, count, moveFrom, moveTo):
    for i in range(count):
        stacks[moveTo].append(stacks[moveFrom].pop())

def part2Move(stacks, count, moveFrom, moveTo):
    moved = stacks[moveFrom][-count:]
    stacks[moveFrom] = stacks[moveFrom][:-count]
    stacks[moveTo] += moved
    
with open("day5.txt") as f:
    line = f.readline()
    while len(line.strip()) != 0:
        if stacks is None:
            stacks = [[] for _ in range(len(line)//4)]
        for i in range(1, len(line), 4):
            c = line[i]
            if c.isalpha():
                stacks[i//4].insert(0, c)
        line = f.readline()

    line = f.readline()
    while len(line.strip()) != 0:
        m = re.match(PATTERN, line.strip())
        count = int(m.group(1))
        moveFrom = int(m.group(2))-1
        moveTo = int(m.group(3))-1
        part2Move(stacks, count, moveFrom, moveTo)
        line = f.readline()

print("".join(stack[-1] for stack in stacks))
