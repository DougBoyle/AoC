import numpy as np
from enum import Enum
import re
import time

observedSubject = 7

def loop(n, subject):
    return (n * subject) % 20201227

cardCount = None
doorCount = None

cardObservedKey = 17773298
doorObservedKey = 15530095

# example
##cardObservedKey = 5764801
##doorObservedKey = 17807724

i = 0
n = 1
# only need to find the count for 1 of them
while cardCount is None and doorCount is None:
    i += 1
    n = loop(n, observedSubject)
    if n == cardObservedKey:
        cardCount = i
    if n == doorObservedKey:
        doorCount = i
print("Iterations: ", i)

# Everything taken modulo 20201227
# key 1 = 7^count1
# key 2 = 7^count2
# key = (key 2)^count1 = (key 1)^count2 = 7^(count1*count2)

def determineKey(cardKey, cardCount, doorKey, doorCount):
    if cardCount != None:
        key = doorKey
        count = cardCount
    else:
        key = cardKey
        count = doorCount
    n = 1
    for i in range(count):
        n = loop(n, key)
    return n

# pt 1.  Takes 4347326 to get card's count
# compared to 14611728 if we try to find both counts

print(cardCount, doorCount)
print(determineKey(cardObservedKey, cardCount, doorObservedKey, doorCount))

# No pt 2. to solve.





