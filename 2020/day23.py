import numpy as np
from enum import Enum
import re
import time

from collections import deque

def singleton(value):
    return {value: value}

def graphInsertAfter(graph, position, value):
    graph[value] = graph[position]
    graph[position] = value
    return value

def graphRemoveAfter(graph, position):
    value = graph[position]
    graph[position] = graph[value]
    del graph[value]
    return value

def graphNext(graph, position):
    return graph[position]

inputString = "872495136"

moves = 10_000_000

cups = None
lastValue = None
currentValue = None
minimum = 10000000
maximum = -1000000
for s in inputString:
    value = int(s)
    if cups is None:
        cups = singleton(value)
        currentValue = value
    else:
        graphInsertAfter(cups, lastValue, value)
    lastValue = value
    minimum = min(value, minimum)
    maximum = max(value, maximum)
    
actualMax = 1000000
for i in range(maximum, actualMax):
    lastValue = graphInsertAfter(cups, lastValue, i+1)

maximum = actualMax


print(minimum, maximum)

currentIdx = 0

start = time.time()

removed = [0, 0, 0]

for i in range(moves):
    for n in range(3):
        removed[n] = graphRemoveAfter(cups, currentValue)
    target = currentValue - 1
    while target in removed or target < minimum:
        target -= 1
        if target < minimum:
            target = maximum
    for i in range(3):
        target = graphInsertAfter(cups, target, removed[i])
    currentValue = graphNext(cups, currentValue)


print("--- %s seconds ---" % (time.time() - start)) 

x = graphNext(cups, 1)
y = graphNext(cups, x)
print(x*y)

# Speeding up operation:
# Naive: 300 iterations = 10.2s
# Checking if target was removed vs not in remaining:9.2s
# Naively replacing with deque (i.e. linked list): 1.86s  i.e. 5x faster
# Increase to 1000 iterations = 6.2s - answer still 27
# Avoiding multiple inserts in middle by rotating: Still 6.2
# Pre-allocated 'removed' array: Still 6.2
# i.e. about 60k seconds or nearly a whole day for full solution

# Fastest approach is just to track dictionary of {cup -> followingCup}
# Due to type of updates happening, always have sufficient information for this.
# (Effectively a cyclic LinkedList with an additional HashMap of cupNumber -> node)

# ^ should be possible to construct that actual structure?

# Using a map of value -> linked list node (really just a cycle encoded in a map)
# 1k iterations now only 0.002s i.e. about 1k times faster
# 10k iterations = 0.03s, 100k iterations = 0.23s, 1M iterations = 2.3s, 10M = 33.5s
# Answer = 170836011000
# Refining to just use a single map directly (no object creation): 20s






