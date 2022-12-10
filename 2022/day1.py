import numpy as np
from enum import Enum
import re
import time

elfs = []

with open("day1.txt") as f:
    elf = []
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            elfs.append(elf)
            elf = []
        else:
            elf.append(int(line))
    if len(elf) > 0:
        elfs.append(elf)

totals = (sum(elf) for elf in elfs)
orderedTotals = sorted(totals)

print(orderedTotals[-3:])
print(sum(orderedTotals[-3:]))

