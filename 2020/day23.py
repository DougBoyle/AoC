import numpy as np
from enum import Enum
import re
import time

from collections import deque

# Static 'mapping', to avoid boilerplate wrapper List class around Nodes.
# Without a wrapper class, also can't nicely represent Empty
class HashedLinkedList():
    mapping = {}
    def __init__(self, value, after):
        self.value = value
        self.after = after
        HashedLinkedList.mapping[value] = self
    @staticmethod
    def insertAfter(position, value):
        node = HashedLinkedList.mapping[position]
        new = HashedLinkedList(value, node.after)
        node.after = new
        return value
    @staticmethod
    def removeAfter(position):
        node = HashedLinkedList.mapping[position]
        after = node.after
        node.after = after.after
        return after.value
    @staticmethod
    def singleton(value):
        node = HashedLinkedList(value, None)
        node.after = node
        return node
    @staticmethod
    def next(value):
        return HashedLinkedList.mapping[value].after.value
    @staticmethod
    def printFrom(value):
        start = value
        after = HashedLinkedList.next(value)
        print(value, after)
        while after != start:
            value = after
            after = HashedLinkedList.next(value)
            print(value, after)
        print()

#inputString = "389125467"
inputString = "872495136"

#moves = 4
moves = 10_000_000
#moves = 10000000


#cups = deque([int(s) for s in inputString])
cups = None # actually done entirely statically by HashedLinkedList.mapping
lastValue = None
currentValue = None
minimum = 10000000
maximum = -1000000
for s in inputString:
    value = int(s)
    if cups is None:
        cups = HashedLinkedList.singleton(value)
        currentValue = value
    else:
        HashedLinkedList.insertAfter(lastValue, value)
    lastValue = value
    minimum = min(value, minimum)
    maximum = max(value, maximum)

##minimum = min(cups)
##maximum = max(cups)

    
actualMax = 1000000
for i in range(maximum, actualMax):
    lastValue = HashedLinkedList.insertAfter(lastValue, i+1)
#    cups.append(i)

#maximum = max(cups)
maximum = actualMax


print(minimum, maximum)

currentIdx = 0

start = time.time()

removed = [0, 0, 0]

# Now that list has 1M entries, need a more efficient way to manipulate
# Could try deque(), which is a linked list implementation
for i in range(moves):
    # puts current element at end, ready to pop off following 3 values
    #cups.rotate(-(currentIdx+1))
    for n in range(3):
        removed[n] = HashedLinkedList.removeAfter(currentValue)
        #removed[n] = cups.popleft()

  #  cups.rotate(1)
  #  target = cups[0] - 1
    target = currentValue - 1
##    if target < minimum:
##        target = maximum
    while target in removed or target < minimum:
        target -= 1
        if target < minimum:
            target = maximum
   # targetIdx = cups.index(target) # Always linear complexity inner loop if lookup?
    # Put target cup at end of list
 #   cups.rotate(-(targetIdx+1))
 #   cups.append(removed[0])
 #   cups.append(removed[1])
 #   cups.append(removed[2])
    for i in range(3):
        target = HashedLinkedList.insertAfter(target, removed[i])
    # Rotate back to current cup at start
  #  cups.rotate(targetIdx+1+3)
  #  currentIdx = 1
    currentValue = HashedLinkedList.next(currentValue)
#    HashedLinkedList.printFrom(3)


print("--- %s seconds ---" % (time.time() - start)) 

#oneIndex = cups.index(1)
#cups.rotate(-oneIndex)
print("Done!")

x = HashedLinkedList.next(1)
y = HashedLinkedList.next(x)
#print(cups[1] * cups[2]) # for 300 iterations, answer is 27
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






