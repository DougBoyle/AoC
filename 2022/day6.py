import numpy as np
from enum import Enum
import re
import time

# Looking for first sequence of 4 different characters
# Can do in linear time (for potentially much larger length)
# by using a sliding window and lookup table.
# Table lastPosition: character -> last occurence
# Window start -> end.
# Consider c = charAt(end+1), end++
# If lastPosition[c] >= start, start = lastPosition[c]+1 (to avoid duplicate)
# lastPosition[c] = end

lastPosition = { chr(c) : -1 for c in range(ord('a'), ord('z') + 1) }

with open("day6.txt") as f:
    line = f.readline().strip()

start = 0
end = -1

target = 14

while end - start < target - 1: # ends are inclusive
    end += 1
    c = line[end]
    if lastPosition[c] >= start:
        start = lastPosition[c] + 1
    lastPosition[c] = end
    
print(end + 1) # offset for 1-indexing
